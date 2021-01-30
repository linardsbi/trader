import unittest
import sys

from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import util

class TestConfig(unittest.TestCase):
    def test_has_config_file(self):
        self.assertTrue(path.exists("./config.ini"), "You need to rename config.ini.example to config.ini")

    def test_config_has_keys(self):
        config_keys = util.get_config().keys()
        self.assertIn("Binance", config_keys)
        self.assertIn("Telegram", config_keys)
        self.assertIn("Discord", config_keys)


if __name__ == '__main__':
    unittest.main()