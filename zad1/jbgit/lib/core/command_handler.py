# Command handlers

from lib.core import config


class CommandHandler:
    def __init__(self, _fileUtils, _messageBuilder, _versioning):
        self.fileUtils = _fileUtils
        self.messageBuilder = _messageBuilder
        self.versioning = _versioning

    # File path validation
    def validate_args(self, repo_path, args):
        # special "*" arg handling
        if '*' in args:
            return ['*']

        # combine args with current working directory
        file_paths = self.fileUtils.construct_paths(repo_path, args)

        # remove all occurrences of "./" in file paths
        trimmed_paths = self.fileUtils.trim_paths(file_paths)

        # arguments validation
        if not self.fileUtils.all_files_exist(trimmed_paths):
            raise Exception(config.files_dont_exist_err)

        return trimmed_paths


    # Status command handler.
    # Returns tuple (repository object, output control message)
    def handle_status(self, repo_info, repo_path):
        # update repository statistics
        self.versioning.traverse_directory(repo_info, repo_path)
        # get repo statistics
        (added, new, modified) = self.versioning.get_status(repo_info)
        # construct output control message
        return (repo_info, self.messageBuilder.build_status(config.default_status_msg, added, new, modified))


    # Commit command handler.
    # Returns tuple (repository object, output control message)
    def handle_commit(self, repo_info, repo_path):
        # update repository statistics
        self.versioning.traverse_directory(repo_info, repo_path)
        count = self.versioning.commit_changes(repo_info)
        # construct output control message
        return (repo_info, self.messageBuilder.build_xmessage(config.default_commit_msg, count))


    # Add command handler.
    # Returns tuple (repository object, output control message)
    def handle_add(self, repo_info, repo_path, args):
        # proper file params validation
        file_paths = self.validate_args(repo_path, args)
        # update repository statistics
        self.versioning.traverse_directory(repo_info, repo_path)
        # perform add operation
        count = self.versioning.add_files(repo_info, file_paths)
        # construct output control message
        return (repo_info, self.messageBuilder.build_xmessage(config.default_add_msg, count))


    # Init command handler.
    # Returns tuple (repository object, output control message)
    def handle_init(self, repo_path):
        # no prior assumptions, just return empty dict
        return ({}, self.messageBuilder.build_init_message(config.default_init_msg, repo_path))