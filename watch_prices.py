import requests
import binance_util
from binance.client import Client
import asyncio
import time


class Watcher:
    is_allowed_symbol = lambda self, symbol: any([x in symbol for x in self.symbols]) and not any([x in symbol for x in self.not_symbols])
    
    def __init__(self, symbols=("BTC",), not_symbols=()) -> None:
        """
        param tuple symbols: Symbols to watch
        param tuple not_symbols: Symbols to exclude
        """
        self.reset_prices(symbols, not_symbols)

    def reset_prices(self, symbols=("BTC"), not_symbols=()):
        """
        param tuple symbols: Symbols to watch
        param tuple not_symbols: Symbols to exclude
        """
        self.symbols = symbols
        self.not_symbols = not_symbols
        self.client = binance_util.make_client()
        self.prices = self.make_price_dict()
        self.last_price_time = time.time()
        

    def make_price_dict(self):
        return {item["symbol"]:item["price"] 
                for item in self.client.get_all_tickers() 
                if self.is_allowed_symbol(item["symbol"])}

    async def get_changed_coins(self, change_threshold=5.0):
        """
        :returns list: List of Coin dicts {"symbol": str, "price": float}
        """
        try:
            current_prices = self.client.get_all_tickers()
        except requests.exceptions.ConnectionError:
            print("Connection aborted, reconnecting")
            self.client = binance_util.make_client()
            return []

        percent_diff = lambda old_price, new_price: ((new_price - old_price) / old_price) * 100
        changed = []

        for item in current_prices:
            if self.is_allowed_symbol(item["symbol"]) and (diff := percent_diff(float(self.prices[item["symbol"]]), float(item["price"]))) >= change_threshold:
                item["change"] = diff
                item["changed_at"] = time.time()
                changed.append(item)

        return changed

async def check_and_print_changes(prev_prices, w, change_threshold):
    pumping = await w.get_changed_coins(change_threshold)

    for item in pumping:
        if not (item in prev_prices):
            print("Pair {} pumped by around {:.2f}%".format(item["symbol"], item["change"]))

    return pumping

async def main():
    watch_interval = 3 # seconds
    threshold = 5 # percent
    w = Watcher()
    prev_changes = []
    print(f"Watching for changes greater than or equal to {threshold}%")
    print(w.prices)
    while True:
        prev_changes = await check_and_print_changes(prev_changes, w, threshold)
        await asyncio.sleep(watch_interval)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())