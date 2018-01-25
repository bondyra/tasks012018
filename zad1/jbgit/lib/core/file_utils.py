# Files and paths processing functions

import os
import re

from lib.core import config


class FileUtils:
    def __init__(self):
        pass

    # removes obsolete ./ from multiple file paths (to keep file paths unique)
    def trim_paths(self, file_paths):
        # single element case
        if not isinstance(file_paths, list):
            file_paths = [file_paths]

        return map((lambda f: re.sub("\./", "", f)), file_paths)

    # combines root path and multiple file paths
    def construct_paths(self, root_path, file_paths):
        # single element case
        if not isinstance(file_paths, list):
            file_paths = [file_paths]

        return map((lambda fp: root_path + "/" + fp), file_paths)

    # all file paths exist on disk?
    # file_paths must be iterable
    def all_files_exist(self, file_paths):
        return all(map((lambda file_path: os.path.exists(file_path)), file_paths))

    def check_if_in_repository(self, dir_path):
        return os.path.exists(self.construct_paths(dir_path, config.jbgit_info_name)[0])

    def walk(self, dir_path):
        return os.walk(dir_path)

    def check_if_file_is_repo(self, file_path):
        return re.match(".*\\" + config.jbgit_info_name + "$", file_path) is not None

    def get_timestamp(self, file_path):
        return os.path.getmtime(file_path)
