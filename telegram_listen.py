
import re
import asyncio
import pytesseract

from io import BytesIO
from PIL import Image
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
PeerChannel
)


def ocr_image(image):
    print("- Doing OCR -")
    return str(((pytesseract.image_to_string(image)))) 

def create_client():
    import util
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

input_channel = 'https://t.me/bigpumpsignal'

client = create_client()

def get_coin_name(text):
    if len(name := re.findall(r"[\$S]([A-Z]{3,4})", text)) > 0:
        return name[0]
    return None

@client.on(events.NewMessage(chats=input_channel))
async def onNewMessage(event):
    message = event.message.message
    if message.media is not None:
            img =  await client.download_media(message=message, file=bytes)
            text = ocr_image(Image.open(BytesIO(img)))
            if (name := get_coin_name(text)) is not None:
                print(name)

async def get_messages():
    channel = await client.get_entity(input_channel)

    history = await client(GetHistoryRequest(
        peer=channel,
        offset_id=0,
        offset_date=None,
        add_offset=0,
        limit=10,
        max_id=0,
        min_id=0,
        hash=0
    ))

    if not history.messages:
        print("no messages")
        return None

    import webbrowser
    for message in history.messages:
        if message.media is not None:
            img = await client.download_media(message=message, file=bytes)
            
            text = ocr_image(Image.open(BytesIO(img)))
            if (name := get_coin_name(text)) is not None:
                webbrowser.open(f"https://www.binance.com/en/trade/{name}_BTC")

        
async def main():
    await get_messages()

with client:
    client.loop.run_until_complete(main())