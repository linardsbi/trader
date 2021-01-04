import find_coin_name_in_messages
from telegram_listen import create_client

client = create_client()

async def main():
    input_channel = 'https://t.me/bigpumpsignal'
    await find_coin_name_in_messages.get_messages(client, input_channel)

with client:
    client.loop.run_until_complete(main())