User Story
====
- As a support team member looking for streamlining the process of tenant's Sense config creation
- I would like to have an executable script that will create a Sense config for a tenant and commits it to the repo
- So that I could have time saved and avoid manual errors

Solution
====
Python script that:
- creates a config file for a specified tenant 
  - `create_config_file()`
- reads the directory with checked out _SenseConfigurations/SenseConfigurations/Configurations/30.199999_ repository
- confirms no existing configuration files are present
  - `confirm_file_does_not_exist()`
- checks out and pulls production branch 
  - `checkout_and_pull_production_git_branch()`
- creates new git branch for a specified ICM number
  - `create_git_branch_for_icm()`
- copies new config file to a new git branch 
  - `copy_config_file_to_git_branch()`
- stages changes, commits, and pushes to git
  - `stage_commit_and_push_changes_to_git()`
  - `publish_branch()`

Instructions
====

## Prerequisites and Sense repository
1. Install python and git
2. Clone SenseConfigurations repository
3. Change directory to cloned repository
4. Specify git email and name `git config user.email "you@example.com"` and `git config user.name "Your Name"`
5. Change directory to any folder that is not in cloned SenseConfigurations directory


## Git setup and Python script
1. Run `python -m venv script-creator` to create virtual environment where `script-creator` is the name for virtual environment. See [Creating a virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)
2. Change directory: `cd .\config-creator\`
3. Then [activate virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)
4. Run `git init` to initialize new git repository
5. Run `git pull https://github.com/NeverTheSame/Dakota.git` to download all required files
6. Edit secret.json file with
   -  `"SENSE_CONFIGURATIONS": "sense_path"`, where `sense_path` is the path to SenseConfigurations repository (see Prerequisites and Sense repository - step 2)
   - `"alias": "you_alias"`, where `you_alias` is your alias 
   - `"owner": "your_name"`, where `your_name` is your name
   - leave `"LINUX_SENSE_CONFIGURATIONS_PATH": ""` empty
7. Run script: `python main.py org_id case_number` where:
   - org_id is the orgID of the tenant
   - case_number is case ID
  

## Pull request
_To be automated per demand._
1. Go to Pull Requests for SenseConfigurations repository section
2. Click on Create pull Request 
3. Choose `production` branch to merge into 
4. Confirm there is only one changed file and the path is correct 
5. In Overview tab, choose reviewers and work items to link
6. Click Create
7. Set auto-complete to remove branch after merge 