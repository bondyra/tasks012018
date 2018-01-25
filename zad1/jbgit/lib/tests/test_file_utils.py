import unittest

from lib.core import file_utils


# path handling unit tests


class FileUtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.fileUtils = file_utils.FileUtils()

    def test_trim_path(self):
        actual_s = "some/path/to/dir"
        s = "./some/path/to/dir"
        s2 = self.fileUtils.trim_paths(s)
        self.assertEqual([actual_s], s2)

    def test_trim_path2(self):
        actual_s = "some/path/to/dir"
        s = "././some/path/to/dir"
        s2 = self.fileUtils.trim_paths(s)
        self.assertEqual([actual_s], s2)

    def test_trim_paths(self):
        s = ["./abc", "abc", "././abc", "./././abc/abc"]
        s2 = self.fileUtils.trim_paths(s)
        self.assertEqual(len(s), len(s2))
        self.assertEqual({"abc", "abc", "abc", "abc/abc"},set(s2))

    def test_construct_path(self):
        s = "c"
        root = "a/b"
        self.assertEqual(["a/b/c"], self.fileUtils.construct_paths(root, s))

    def test_construct_paths(self):
        root = "a/b"
        s = ["a", "b", "c"]
        s2 = self.fileUtils.construct_paths(root, s)
        self.assertEqual(len(s), len(s2))
        self.assertEqual({"a/b/a", "a/b/b", "a/b/c"}, set(s2))


if __name__ == '__main__':
    unittest.main()
