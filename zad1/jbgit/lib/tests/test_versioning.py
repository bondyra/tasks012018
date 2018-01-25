import unittest

from mock import MagicMock

from lib.core import config
from lib.core import file_utils
from lib.core import versioning


# main command logic unit tests

class VersioningTestCase(unittest.TestCase):
    def setUp(self):
        fileUtils = file_utils.FileUtils()
        fileUtils.walk = MagicMock(return_value=[("","","")])
        fileUtils.trim_path = MagicMock(return_value="")
        self.versioning = versioning.Versioning(fileUtils)


class TraversalTestCase(VersioningTestCase):
    def test_traversal(self):
        self.versioning.fileUtils.construct_paths = MagicMock(return_value=
                                            ["dir/a", "dir/b", "dir/" + config.jbgit_info_name])
        self.versioning.fileUtils.get_timestamp = MagicMock(return_value=1)
        repo_info = {}
        self.versioning.traverse_directory(repo_info, "")
        self.assertTrue(repo_info)
        self.assertEqual(2, len(repo_info.keys()))
        self.assertTrue("dir/a" in repo_info.keys())
        self.assertTrue("dir/b" in repo_info.keys())
        self.assertEqual([(1, "N"), (1, "N")], repo_info.values())

    def test_traversal_after_add(self):
        self.versioning.fileUtils.construct_paths = MagicMock(return_value=
                                ["dir/x", "dir/a", "dir/b", "dir/c", "dir/" + config.jbgit_info_name])
        self.versioning.fileUtils.get_timestamp = MagicMock(return_value=1)
        repo_info = {"dir/a":(1,"N"),"dir/b":(1,"N"),"dir/c":(1,"N")}
        self.versioning.traverse_directory(repo_info,"")
        self.assertTrue(repo_info)
        self.assertEqual(4,len(repo_info.keys()))
        self.assertTrue("dir/x" in repo_info.keys())
        self.assertEqual([(1,"N"),(1,"N"),(1,"N"),(1,"N")],repo_info.values())

    def test_traversal_after_delete(self):
        self.versioning.fileUtils.construct_paths = MagicMock(return_value=
                                ["dir/b", "dir/" + config.jbgit_info_name])
        self.versioning.fileUtils.get_timestamp = MagicMock(return_value=1)
        repo_info = {"dir/a": (1, 'N'), "dir/b": (1, "N")}
        self.versioning.traverse_directory(repo_info, "")
        self.assertTrue(repo_info)
        self.assertEqual(1,len(repo_info.keys()))
        self.assertTrue("dir/b" in repo_info.keys())
        self.assertEqual((1, "N"), repo_info["dir/b"])

    def test_traversal_modification(self):
        self.versioning.fileUtils.construct_paths = MagicMock(return_value=
                                ["dir/a", "dir/b", "dir/" + config.jbgit_info_name])
        self.versioning.fileUtils.get_timestamp = MagicMock(return_value=2)
        repo_info = {"dir/a": (1, 'N'), "dir/b": (1, "A")}
        self.versioning.traverse_directory(repo_info, "")
        self.assertTrue(2, len(repo_info.keys()))

        self.assertTrue("dir/a" in repo_info.keys())
        self.assertEqual(2, repo_info["dir/a"][0])
        self.assertEqual("N", repo_info["dir/a"][1])

        self.assertTrue("dir/b" in repo_info.keys())
        self.assertEqual(2, repo_info["dir/b"][0])
        self.assertEqual("M", repo_info["dir/b"][1])


class StatusTestCase(VersioningTestCase):
    def test_status(self):
        repo_info = {"a":(1,"A"),"b":(1,"A"),"c":(1,"N"),"d":(1,"M"),"e":(1,"M"),"f":(1,"M"),"g":(1,"C")}
        repo_info_old = repo_info.copy()
        status = self.versioning.get_status(repo_info) # returns (added,new,modified)
        self.assertEqual(repo_info_old,repo_info)
        self.assertEqual(2,len(status[0]))
        self.assertEqual(1,len(status[1]))
        self.assertEqual(3,len(status[2]))
        self.assertEqual({"a", "b"}, set(status[0]))
        self.assertEqual({"c"}, set(status[1]))
        self.assertEqual({"d", "e", "f"}, set(status[2]))


class AddTestCase(VersioningTestCase):
    def test_not_traversed(self):
        self.versioning.fileUtils.construct_paths = MagicMock(return_value=
                                ["dir/a", "dir/b"])
        self.versioning.fileUtils.get_timestamp = MagicMock(return_value=1)
        repo_info = {"dir/a":(1,'N')}
        self.assertRaises(Exception, self.versioning.add_files, repo_info,"","")

    def test_add(self):
        self.versioning.fileUtils.get_timestamp = MagicMock(return_value=1)
        repo_info = {"dir/a": (1, 'N'), "dir/b": (1, "M"), "dir/c": (1, "C"), "dir/d": (1, "A")}
        self.versioning.add_files(repo_info, ["dir/a", "dir/b", "dir/c", "dir/d"])
        self.assertTrue(4, len(repo_info.keys()))
        self.assertEqual("A", repo_info["dir/a"][1])
        self.assertEqual("A", repo_info["dir/b"][1])
        self.assertEqual("C", repo_info["dir/c"][1])
        self.assertEqual("A", repo_info["dir/d"][1])


class CommitTestCase(VersioningTestCase):
    def test_commit(self):
        self.versioning.fileUtils.construct_paths = MagicMock(return_value=
                                ["dir/a", "dir/b"])
        self.versioning.fileUtils.get_timestamp = MagicMock(return_value=1)
        repo_info = {"dir/a": (1, 'N'), "dir/b": (1, "M"), "dir/c": (1, "C"), "dir/d": (1, "A")}
        self.versioning.commit_changes(repo_info)
        self.assertTrue(4,len(repo_info.keys()))
        self.assertEqual("N", repo_info["dir/a"][1])
        self.assertEqual("M", repo_info["dir/b"][1])
        self.assertEqual("C", repo_info["dir/c"][1])
        self.assertEqual("C", repo_info["dir/d"][1])


if __name__ == '__main__':
    unittest.main()
