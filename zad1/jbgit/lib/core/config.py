# global package configurations

# main settings
jbgit_info_name = '.jbgit'
jbgit_encoding = "utf-8"
jbgit_valid_cmds = ['status', 'commit', 'add', 'init']

# exception messages section
repo_initialized_err = "Error - repository already initialized."
not_in_repository_err = "Error - currently not in repository."
invalid_cmd_err = "Invalid command specified."
no_cmd_err = "No command specified."
repo_invalid_initialization_name_err = "Invalid repository name."
should_be_zero_param_err = "Command requires zero arguments."
should_be_params_err = "Please provide at least one file name."
bad_configuration_err = "Bad configuration of jbgit. Check if jbgit.lib.configuration is valid."
files_dont_exist_err = "Error - files don't exist on disk."
invalid_file_paths_err = "Error - invalid file paths."

# control messages section
default_init_msg = "Repository succesfully initialized"
default_add_msg = "Succesfully added X files."
default_commit_msg = "Succesfully commited X files."
no_commit_msg = "Nothing staged for commit."
default_status_msg = "Current repository status:"
usage_msg = \
    "\nUsage: jbgit <command> [<args>]\nCommand could be one of init, add, commit, status\n\n" + \
    "init command - initailizes empty jbgit repository in current working directory\n" + \
    "add command - adds files specified via args to staging phase\n" + \
    "commit command - commits currently staged files\n" + \
    "status command - shows repository status"
