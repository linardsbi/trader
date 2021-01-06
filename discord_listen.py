import discord
import asyncio
import util

TOKEN_AUTH = util.get_config()["Discord"]["auth_token"] # Retrieved from browser local storage

client = discord.Client()

@client.event
async def on_ready():
    print("ready")
    # for channel in client.get_all_channels():
    #     print(channel)

@client.event
async def on_message(message):
    if "pump-signal" in str(message.channel) and len(message.attachments) > 0:
        text = util.ocr_image(util.get_image(message.attachments[0].url))
        print(text)
        if (name := util.get_coin_name(text)) is not None:
            import webbrowser
            webbrowser.open_new_tab(f"https://www.binance.com/en/trade/{name}_BTC")

client.run(TOKEN_AUTH, bot=False)