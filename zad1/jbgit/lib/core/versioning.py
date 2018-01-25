# Logic for versioning


class Versioning:
    def __init__(self, _fileUtils):
        self.fileUtils = _fileUtils

    # traverse repository and update files info
    def traverse_directory(self, repo_info, path):
        all_file_paths = []
        for (root_path, dir, file_paths) in self.fileUtils.walk(path):
            # normalize root path
            root_path = self.fileUtils.trim_paths(root_path)[0]

            # map to full file path
            file_paths = self.fileUtils.construct_paths(root_path, file_paths)
            all_file_paths += file_paths

        for file_path in all_file_paths:
            # explicit gitignore
            if self.fileUtils.check_if_file_is_repo(file_path):
                continue

            timestamp = self.fileUtils.get_timestamp(file_path)

            # add new files or update old ones
            if file_path not in repo_info:
                repo_info[file_path] = (timestamp, "N")
            else:
                file_info = repo_info[file_path]
                if file_info[0] < timestamp:
                    current_mark = file_info[1]
                    # mark added or commited files as modified, else keep mark
                    new_mark = "M" if current_mark in ["A", "C"] else current_mark
                    repo_info[file_path] = (timestamp, new_mark)

        # check if files were deleted. if so, simply remove them from repo_info
        for el in (set(repo_info)-set(all_file_paths)):
            repo_info.pop(el, None)

    # for all staged ("A") files update status to commited ("C")
    def commit_changes(self, repo_info):
        keys = [k for k, v in repo_info.items() if v[1] == "A"]
        # affected files count for output messages
        count = len(keys)
        for key in keys:
            repo_info[key] = (repo_info[key][0], "C")

        return count

    # add all specified files
    def add_files(self, repo_info, file_paths):
        # affected files count for output messages
        count = 0

        # special "*" handling
        if '*' in file_paths:
            for key in repo_info:
                if repo_info[key][1] in ["N", "M"]:
                    repo_info[key] = (repo_info[key][0], "A")
                    count += 1
        else:
            if any(map((lambda x: self.fileUtils.check_if_file_is_repo(x)), file_paths)):
                    raise Exception("Cannot add repository file.")

            invalid = [i for i in file_paths if i not in repo_info]
            if len(invalid) > 0:
                raise Exception("Files not traversed in add function: " + str(invalid))
            for file_path in file_paths:
                if repo_info[file_path][1] in ["N", "M"]:
                    repo_info[file_path] = (repo_info[file_path][0], "A")
                    count += 1

        return count

    # gets repository info statistics (added files, new files, modified files)
    def get_status(self, repo_info):
        added_files = [k for k, v in repo_info.items() if v[1] == "A"]
        new_files = [k for k, v in repo_info.items() if v[1] == "N"]
        modified_files = [k for k, v in repo_info.items() if v[1] == "M"]
        return (added_files, new_files, modified_files)