from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
PeerChannel
)
import sys, unittest
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import util, binance_util

from telegram_listen import Account, make_client

class TestTelegram(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        #self.binance_client = binance_util.make_client()

    def test_credentials(self):
        client = make_client()
        self.assertIsInstance(client, TelegramClient)
        client.disconnect()

        

if __name__ == '__main__':
    unittest.main()