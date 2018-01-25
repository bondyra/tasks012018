# Top layer command processor

from lib.core import config


class Runner:
    def __init__(self, _path, _args, _storage, _fileUtils, _commandHandler):
        self.path = _path
        self.args = _args
        self.storage = _storage
        self.storage.set_path(self.path)
        self.fileUtils = _fileUtils
        self.commandHandler = _commandHandler

    @staticmethod
    def usage(pre_error):
        return (pre_error + config.usage_msg)

    # Run command processing
    def run(self):

        # in case of invalid command print usage
        if len(self.args) < 2:
            return self.usage(config.no_cmd_err)

        cmd = self.args[1]

        if cmd not in config.jbgit_valid_cmds:
            return self.usage(config.invalid_cmd_err + " \"" + self.args[1] + "\".")

        # main processing
        in_repository = self.fileUtils.check_if_in_repository(self.path)

        if cmd == 'init':
            if in_repository:
                raise Exception(config.repo_initialized_err)

            (repo_info, message) = self.commandHandler.handle_init(self.path)
        else:
            if not in_repository:
                raise Exception(config.not_in_repository_err)

            # read repository information
            repo_info = self.storage.read_repository()

            if cmd == 'status':
                if len(self.args) > 2:
                    raise Exception(config.should_be_zero_param_err)

                (repo_info, message) = self.commandHandler.handle_status(repo_info, self.path)

            elif cmd == 'commit':

                if len(self.args) > 2:
                    raise Exception(config.should_be_zero_param_err)

                (repo_info, message) = self.commandHandler.handle_commit(repo_info, self.path)

            elif cmd == 'add':
                # for add at least one param must be provided
                if len(self.args) == 2:
                    raise Exception(config.should_be_params_err)

                (repo_info, message) = self.commandHandler.handle_add(repo_info, self.path, self.args[2:])

            else:
                raise Exception(config.bad_configuration_err)

        self.storage.save_repository(repo_info)

        return message
