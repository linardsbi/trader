import unittest
import sys
import asyncio

from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import util
# from discord_listen import make_client



# async def start_and_get_chats(client, auth_token):
#     await client.start(auth_token, bot=False)
#     chan = client.get_all_channels()
#     await client.close()
#     return chan

# class TestConfig(unittest.TestCase):
#     # TODO: figure out how to test events
#     @unittest.skip("not implemented")
#     def test_connect(self):
#         client, auth_token = make_client()
#         self.assertIsNotNone(auth_token)
#         loop = asyncio.get_event_loop()
#         result = loop.run_until_complete(start_and_get_chats(client, auth_token))
#         loop.close()
#         self.assertTrue(result)
        
# if __name__ == '__main__':
#     unittest.main()