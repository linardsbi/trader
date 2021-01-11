import binance_util, util
from binance.client import Client
import util, asyncio

watch_interval = 3 # seconds
threshold = 5 # percent

def make_price_dict(client):
    return {item["symbol"]:item["price"] for item in client.get_all_tickers() if "BTC" in item["symbol"]}

loop = asyncio.get_event_loop()
client = binance_util.make_client()
prices = make_price_dict(client)

async def get_changed_coins(current_prices):
    percent_diff = lambda old_price, new_price: ((new_price - old_price) / old_price) * 100
    changed = []

    for item in current_prices:
        if "BTC" in item["symbol"] and (diff := percent_diff(float(prices[item["symbol"]]), float(item["price"]))) >= threshold:
            item["change"] = diff
            changed.append(item)

    return changed

async def check_and_print_changes(prev_prices):
    current_prices = client.get_all_tickers()
    
    pumping = await get_changed_coins(current_prices)

    for item in pumping:
        if not (item in prev_prices):
            print("Pair {} pumped by around {:.2f}%".format(item["symbol"], item["change"]))

    return pumping

async def main():
    prev_changes = []
    while True:
        prev_changes = await check_and_print_changes(prev_changes)
        await asyncio.sleep(watch_interval)

loop.run_until_complete(main())