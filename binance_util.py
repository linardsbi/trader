
 # save all symbol prices
from binance.client import Client
from binance.enums import *

def save_prices(client):
    import pickle

    try:
        prices = client.get_all_tickers()
    except Exception as e:
        print(f"failed. reason: {e}")
        return

    pickle.dump(prices, open("prices.p", "wb"))

    print("success")

async def get_remaining_amount(client, symbol):
    if (bal := client.get_asset_balance(asset=symbol)):
        return float(bal["free"])
    return 0.0

def make_market_buy(client, qty, coin_name):
    print(f"market trading {qty} of bitcoin for available {coin_name}")
    # order = client.order_market_buy(
    #         symbol=f"{coin_name}BTC",
    #         quoteOrderQty=qty)

    order = client.create_test_order(
        symbol=f"{coin_name}BTC",
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quoteOrderQty=qty)

    return order

def make_multiplier_sell(client, coin_name, amount, multiplier):
    # order = client.create_order(
    #     symbol=f"{coin_name}BTC",
    #     side=SIDE_SELL,
    #     type=ORDER_TYPE_TAKE_PROFIT,
    #     stopPrice=amount * multiplier)
    order = client.create_test_order(
        symbol=f"{coin_name}BTC",
        side=SIDE_SELL,
        type=ORDER_TYPE_TAKE_PROFIT,
        stopPrice=amount * multiplier)

    return order
