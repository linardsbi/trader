from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
PeerChannel
)
import webbrowser

async def get_messages(client, input_channel):
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
            handle_telegram_image(await client.download_media(message=message, file=bytes), 
                              lambda name: webbrowser.open_new_tab(f"https://www.binance.com/en/trade/{name}_BTC"))