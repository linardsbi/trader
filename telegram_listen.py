
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

WEB_ONLY = True

class Account:
    def __init__(self, input_channel: str, binance_client=None):
        self.input_channel = input_channel
        self.funds = 0.0
        self.start_time = time.time() # this should be set as the time at which the trading starts
        self.max_buy_timelimit = 60 # this should be set to a "safe" period for buying; for now 1 min
        self.telegram_client = make_client()

        if not binance_client:
            self.binance_client = binance_util.make_client()
        else:
            self.binance_client = binance_client

        @self.telegram_client.on(events.NewMessage(chats=self.input_channel))
        async def onNewMessage(event):
            print("recieved message")
            message = event.message.message
            
            if message.media is not None:
                await account.set_remaining_amount("BTC")
                await handle_telegram_image(self.telegram_client.download_media(message=message, file=bytes), self.on_recieve_coin_name),
            elif (name := util.get_coin_name(event.stringify())):
                self.on_recieve_coin_name(name)


    async def set_remaining_amount(self, symbol):
        if (bal := self.binance_client.get_asset_balance(asset=symbol)):
            self.funds = float(bal["free"])

    # plan is to buy available amount of BTC in {name}
    # first got to get the available amount -> this must be done just before starting to watch for coin name
    # then send a market quoteOrderQty of the amount into {name}
    # set a sell limit at whatever multiplier for whatever amount
    # open browser
    # that's it!
    # TODO: error handling
    # TODO this should be abstracted out of this class so it could be called from discord_listen
    def on_recieve_coin_name(self, name):
        import datetime
        print(f"got {name} at {datetime.datetime.now()}")
        import webbrowser
        
        webbrowser.open_new_tab(f"https://www.binance.com/en/trade/{name}_BTC")
        symbol = f"{name}BTC"
        
        if WEB_ONLY:
            if (time.time() - self.start_time < self.max_buy_timelimit and self.funds != 0):
                binance_util.make_market_buy(self.binance_client, self.funds, symbol)
                buy = binance_util.get_most_recent_buy_for(self.binance_client, symbol)
                util.print_for_web_only(float(buy["price"]))
            else:
                print(f"time passed: {time.time() - self.start_time}\ncurrent BTC: {self.funds}")
        else:
            # while loop in case the orders don't go through
            # should add a delay though not to overwhelm the api
            # TODO this still needs a lot of work because it does not work
            while (time.time() - self.start_time < self.max_buy_timelimit and self.funds):
                binance_util.make_market_buy(self.binance_client, self.funds, symbol)

                #ideally, "amount" should be set to a precentage of available funds
                amount = float(binance_util.get_most_recent_buy_for(self.binance_client, symbol)["price"]) # somehow need to check if order went through..
                
                if not amount: 
                    self.set_remaining_amount("BTC") # refresh the amount of BTC on the account
                    continue # try again

                binance_util.make_multiplier_sell(self.binance_client, name, amount, 3)


async def handle_telegram_image(img, onImageHasCoinName = None, onImageEmpty = None):
    text = util.ocr_image(Image.open(BytesIO(await img)))
    if (name := util.get_coin_name(text)) is not None:
        if callable(onImageHasCoinName): onImageHasCoinName(name)
    else:
        if callable(onImageEmpty): onImageEmpty()

def make_client():
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

    return client

if __name__ == "__main__":
    account = Account(input_channel='https://t.me/bigpumpsignal')
    print(binance_util.get_most_recent_buy_for(account.binance_client, "BTCEUR"))
    account.telegram_client.run_until_disconnected()

    
        

