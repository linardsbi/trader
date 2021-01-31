
 # save all symbol prices
from binance.client import Client
from binance.enums import *
from time import time

def make_client():
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

async def get_remaining_amount(client, symbol):
    if (bal := client.get_asset_balance(asset=symbol)):
        return float(bal["free"])
    return 0.0

def make_market_buy(client, qty, symbol):
    print(f"market trading {qty} of bitcoin for available {symbol}")
    order = client.order_market_buy(
            symbol=symbol,
            quoteOrderQty=qty)

    # order = client.create_test_order(
    #     symbol=symbol,
    #     side=SIDE_BUY,
    #     type=ORDER_TYPE_MARKET,
    #     quoteOrderQty=qty)

    return order

def make_multiplier_sell(client, symbol, amount, multiplier):
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

def get_trades_for(client, symbol):
    return client.get_my_trades(symbol=symbol)

def get_most_recent_trade_for(client, symbol):
    return get_trades_for(client, symbol)[-1]

def get_most_recent_buy_for(client, symbol):
    for trade in reversed(get_trades_for(client, symbol)):
        if trade["isBuyer"]: return trade
    return None

def get_current_price_for(client, symbol):
    return float(client.get_symbol_ticker(symbol=symbol)["price"])