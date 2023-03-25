import sys
import os
import shutil
from pathlib import Path
import git_actions
import json_worker
import tkinter as tk
from tkinter import filedialog

TEMPLATE_FILE_PREFIX = "ServerConfigurations.Linux.30.199999."
TEMPLATE_FILE_POSTFIX = ".IgnoreOpenFileEvents.js"
ORIGINAL_TEMPLATE_FILE = TEMPLATE_FILE_PREFIX + "orgID" + TEMPLATE_FILE_POSTFIX


def create_config_file(org_id, icm_number):
    """Copy config file to the current directory and return its name"""
    new_config_file_name = TEMPLATE_FILE_PREFIX + org_id + TEMPLATE_FILE_POSTFIX
    shutil.copyfile(ORIGINAL_TEMPLATE_FILE, new_config_file_name)
    with open(new_config_file_name, "r") as file:
        lines = file.readlines()
        with open(new_config_file_name, "w") as file:
            for line in lines:
                if "orgID" in line:
                    line = line.replace("orgID", org_id)
                if "icmID" in line:
                    line = line.replace("icmID", icm_number)
                if "owner_full_name" in line:
                    line = line.replace("owner_full_name", json_worker.return_key_value_from_json("owner"))
                file.write(line)
    return new_config_file_name


def confirm_file_does_not_exist(file_name):
    """Check if file exists in production and if it does, exit the script"""
    linux_senseconfigurations_path = json_worker.return_key_value_from_json("LINUX_SENSE_CONFIGURATIONS_PATH")
    my_file = Path(os.path.join(f"{linux_senseconfigurations_path}", file_name))
    if os.path.exists(my_file):
        print(f"File {file_name} already exists. Exiting.")
        sys.exit(1)
    print(f"File {file_name} does not exist. Continuing.")


def use_UI():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory()
    return directory


def confirm_sense_config_path_in_secret_file():
    """Check if SENSE_CONFIGURATIONS path is already in secret.json"""
    current_sense_path = json_worker.return_key_value_from_json("SENSE_CONFIGURATIONS")
    if current_sense_path == "":
        print("SENSE_CONFIGURATIONS path is not set in secret.json. Please set it and try again.")
        sys.exit(1)
    if current_sense_path != "":
        print("SENSE_CONFIGURATIONS path is set in secret.json. Continuing.")
        linux_senseconfigurations_path = os.path.join(f"{current_sense_path}", "Configurations", "30.199999")
        json_worker.write_key_value_to_json("LINUX_SENSE_CONFIGURATIONS_PATH", linux_senseconfigurations_path)
        return current_sense_path, linux_senseconfigurations_path


def confirm_parameters():
    if len(sys.argv) != 3:
        print("Please pass org_ID and ICM number as parameters")
        sys.exit(1)
    if len(sys.argv) == 3:
        org_id = sys.argv[1]
        icm_number = sys.argv[2]
        return org_id, icm_number


def main():
    """Pass org_ID as a first parameter for copy_config_file function.
    Pass ICM number as a second parameter for create_git_branch_for_icm function."""
    senseconfigurations_path, linux_senseconfigurations_path = confirm_sense_config_path_in_secret_file()
    org_id, icm_number = confirm_parameters()
    new_config = create_config_file(org_id, icm_number)
    confirm_file_does_not_exist(new_config)
    git_actions.checkout_and_pull_production_git_branch(senseconfigurations_path)
    git_actions.create_git_branch_for_icm(icm_number)
    git_actions.copy_config_file_to_git_branch(new_config, linux_senseconfigurations_path)
    git_actions.stage_changes_and_commit(new_config, icm_number, linux_senseconfigurations_path)
    git_actions.publish_branch(icm_number)


if "__main__" == __name__:
    main()
