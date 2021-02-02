
 # save all symbol prices
from binance.client import Client
from binance.enums import *
from time import time

def make_client() -> Client:
    import util
    config = util.get_config()
    return Client(config["Binance"]["api_key"], config["Binance"]["api_secret"])

def save_prices(client):
    import pickle
    try:
        prices = client.get_all_tickers()
        prices.insert(0, time())
    except Exception as e:
        print(f"failed. reason: {e}")
        return

    pickle.dump(prices, open("prices.p", "wb"))

    print("success")

def get_prices():
    import pickle
    try:
        return pickle.load(open("prices.p", "wb"))
    except Exception as e:
        print(f"failed. reason: {e}")
        return

async def get_remaining_amount(client: Client, symbol: str) -> float:
    """
    :param Client client: Binance client
    :param str symbol: coin symbol e.g. "BTC" or "USDT"
    """
    if (bal := client.get_asset_balance(asset=symbol)):
        return float(bal["free"])
    return 0.0
    
def get_remaining_amount_sync(client: Client, symbol: str) -> float:
    """
    :param Client client: Binance client
    :param str symbol: coin symbol e.g. "BTC" or "USDT"
    """
    if (bal := client.get_asset_balance(asset=symbol)):
        return float(bal["free"])
    return 0.0

def make_market_buy(client: Client, qty: float, symbol: str):
    print(f"market trading {qty} of {symbol[-3:]} for available {symbol}")
    # order = client.order_market_buy(
    #         symbol=symbol,
    #         quoteOrderQty=qty)

    # order = client.create_test_order(
    #     symbol=symbol,
    #     side=SIDE_BUY,
    #     type=ORDER_TYPE_MARKET,
    #     quoteOrderQty=qty)

    #return order

def make_multiplier_sell(client: Client, symbol: str, amount: float, multiplier: float):
    print(f"selling {symbol} at {amount} * {multiplier}")
    order = client.create_order(
        symbol=symbol,
        side=SIDE_SELL,
        type=ORDER_TYPE_TAKE_PROFIT,
        stopPrice=amount * multiplier)
    # order = client.create_test_order(
    #     symbol=symbol,
    #     side=SIDE_SELL,
    #     type=ORDER_TYPE_TAKE_PROFIT,
    #     stopPrice=amount * multiplier)

    return order

def get_trades_for(client: Client, symbol: str):
    return client.get_my_trades(symbol=symbol)

def get_most_recent_trade_for(client: Client, symbol: str):
    return get_trades_for(client, symbol)[-1]

def get_most_recent_buy_for(client: Client, symbol: str):
    for trade in reversed(get_trades_for(client, symbol)):
        if trade["isBuyer"]: return trade
    return None

def get_current_price_for(client: Client, symbol: str) -> float:
    return float(client.get_symbol_ticker(symbol=symbol)["price"])