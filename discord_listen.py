import discord
import asyncio
import util
import binance_util
from binance.client import Client

def make_client():
    config = util.get_config()
    TOKEN_AUTH = config["Discord"]["auth_token"] # Retrieved from browser local storage

    return discord.Client(), TOKEN_AUTH

client, auth_token = make_client()
binance_client = binance_util.make_client()

@client.event
async def on_ready():
    print("ready")
    # for channel in client.get_all_channels():
    #     print(channel)
def print_for_web_only(price):
    import pyperclip
    print("Make a limit sell at:")
    print("for 10x: %f" % (price * 10))
    print("for  8x: %f" % (price * 8))
    print("for  4x: %f" % (price * 4))
    print("for  2x: %f" % (price * 2))
    pyperclip.copy(format(price * 4, "f"))

@client.event
async def on_message(message):
    if "pump-signal" in str(message.channel) and len(message.attachments) > 0:
        text = util.ocr_image(util.get_image(message.attachments[0].url))
        if (name := util.get_coin_name(text)) is not None:
            if name == "xxx" or name == "XXX": 
                print("test name")
                return
            symbol = f"{name}BTC"
            funds = await binance_util.get_remaining_amount(binance_client, "BTC")
            binance_util.make_market_buy(binance_client, funds, symbol)
            buy = binance_util.get_most_recent_buy_for(binance_client, symbol)
            print_for_web_only(float(buy["price"]))

            import webbrowser
            webbrowser.open_new_tab(f"https://www.binance.com/en/trade/{name}_BTC")

client.run(auth_token, bot=False)