# IO operations

import json

from lib.core import config


class Storage:
    def __init__(self, _fileUtils):
        self.repo_path = ""
        self.fileUtils = _fileUtils

    def set_path(self, _path):
        self.repo_path = _path

    # loads repository info from specified path
    def read_repository(self):
        assert(self.repo_path != "")
        assert(self.fileUtils.check_if_in_repository(self.repo_path))

        repo_file = self.fileUtils.construct_paths(self.repo_path, config.jbgit_info_name)[0]

        f = open(repo_file, "r")
        repo_info = json.load(f, encoding=config.jbgit_encoding)
        return repo_info

    # dumps json representation of repository info to specific path
    def save_repository(self, repo_info):
        assert(self.repo_path != "")

        repo_file = self.fileUtils.construct_paths(self.repo_path, config.jbgit_info_name)[0]

        f = open(repo_file, "w")
        json.dump(repo_info, f, encoding=config.jbgit_encoding)
