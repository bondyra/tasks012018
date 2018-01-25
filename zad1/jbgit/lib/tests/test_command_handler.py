import unittest

from mock import MagicMock

from lib.core import command_handler
from lib.core import file_utils
from lib.core import message_builder
from lib.core import versioning


# unit tests for arguments validation + init handler ( other command logic unit tests are in test_versioning.py)

class InitHandlerTestCase(unittest.TestCase):
    def setUp(self):
        fileUtils = file_utils.FileUtils()
        messageBuilder = message_builder.MessageBuilder()
        messageBuilder.build_init_message = MagicMock(return_value="msg")
        v = versioning.Versioning(fileUtils)

        self.cmdHandler = command_handler.CommandHandler(fileUtils, messageBuilder, v)

    def test_init_handler(self):
        result = self.cmdHandler.handle_init("")
        self.assertTrue(not result[0])
        self.assertTrue(isinstance(result[0], dict))
        self.assertEqual("msg", result[1])
        self.assertTrue(isinstance(result[1], str))
        self.assertEqual(2, len(result))


if __name__ == '__main__':
    unittest.main()

