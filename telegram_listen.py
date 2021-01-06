
import re
import asyncio
import pytesseract
import binance_util, util
import time
from io import BytesIO
from PIL import Image
from binance.client import Client
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
PeerChannel
)

class Account:
    def __init__(self):
        self.input_channel = 'https://t.me/bigpumpsignal'
        self.funds = 0.0
        self.start_time = time.time() # this should be set as the time at which the trading starts
        self.telegram_client, self.binance_client = create_client()

        self.telegram_client.run_until_disconnected()

    async def get_remaining_amount(self, symbol):
        if (bal := self.binance_client.get_asset_balance(asset=symbol)):
            self.funds = float(bal["free"])

    # plan is to buy available amount of BTC in {name}
    # first got to get the available amount -> this must be done just before starting to watch for coin name
    # then send a market quoteOrderQty of the amount into {name}
    # set a sell limit at whatever multiplier for whatever amount
    # open browser
    # that's it!
    # TODO: error handling
    def on_recieve_coin_name(self, name):
        import webbrowser
        max_timelimit = 10000000000 # this should be set to a "safe" period for buying; for now no limits
        if (time.time() - self.start_time < max_timelimit):
            binance_util.make_market_buy(self.binance_client, self.funds, name)

            #ideally "amount" should be set to a precentage of available funds
            amount = 0.001 # somehow need to check if order went through.. probably with get_remaining_amount
            binance_util.make_multiplier_sell(self.binance_client, name, amount, 10)

        webbrowser.open_new_tab(f"https://www.binance.com/en/trade/{name}_BTC")


async def handle_telegram_image(img, onImageHasCoinName = None, onImageEmpty = None):
    text = util.ocr_image(Image.open(BytesIO(await img)))
    if (name := util.get_coin_name(text)) is not None:
        if callable(onImageHasCoinName): onImageHasCoinName(name)
    else:
        if callable(onImageEmpty): onImageEmpty()

def create_client():
    # Create the client and connect
    config = util.get_config()
    client = TelegramClient(config["Telegram"]["username"],
                            config["Telegram"]["api_id"],
                            config["Telegram"]["api_hash"])
    client.start()
    print("Client Created")
    # Ensure you're authorized
    if not client.is_user_authorized():
        client.send_code_request(config['Telegram']['phone'])
        try:
            client.sign_in(config['Telegram']['phone'], input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

    return client, Client(config["Binance"]["api_key"], config["Binance"]["api_secret"])

if __name__ == "__main__":
    account = Account()

@account.telegram_client.on(events.NewMessage(chats=account.input_channel))
async def onNewMessage(event):
    print("recieved message")
    message = event.message.message
    
    if message.media is not None:
        # refresh amount in parallel to checking the image
        # TODO the order of execution matters, because the amount might not be refreshed and the program might try
        # to make an order, which is going to fail
        # refreshing must somehow be called prior the handle function calling it's success callback
        # This parallel thing might actually slow things down!
        account.telegram_client.loop.run_until_complete(asyncio.gather(
            handle_telegram_image(account.telegram_client.download_media(message=message, file=bytes), account.on_recieve_coin_name),
            account.get_remaining_amount("BTC")
        ))
        

