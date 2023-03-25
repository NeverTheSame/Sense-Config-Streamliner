import os
import subprocess
import shutil
import json_worker
import sys


def return_alias():
    alias = json_worker.return_key_value_from_json("alias")
    if alias == "":
        print("alias is not set in secret.json. Please set it and try again.")
        sys.exit(1)
    return alias


def checkout_and_pull_production_git_branch(senseconfigurations_path):
    os.chdir(senseconfigurations_path)
    subprocess.run(["git", "checkout", "-q", "production"])
    subprocess.run(["git", "pull", "origin", "production"])


def create_git_branch_for_icm(icm_number):
    """Create a git branch for the ICM"""
    alias = return_alias()
    subprocess.run(["git", "checkout", "-b", f"user/{alias}/mitigate-ICM-" + icm_number])


def copy_config_file_to_git_branch(new_config, linux_senseconfigurations_path):
    """Copy config file to the git branch"""
    path_to_git_actions_script = os.path.dirname(os.path.realpath(__file__))
    os.chdir(path_to_git_actions_script)
    shutil.copyfile(new_config, linux_senseconfigurations_path + "/" + new_config)


def stage_changes_and_commit(file_to_commit, icm_number, linux_senseconfigurations_path):
    os.chdir(linux_senseconfigurations_path)
    subprocess.run(["git", "add", file_to_commit])
    subprocess.run(["git", "commit", "-m", "ICM mitigation for " + icm_number])


def publish_branch(icm_number):
    alias = return_alias()
    subprocess.run(["git", "push", "origin", f"user/{alias}/mitigate-ICM-" + icm_number])
