
def get_prices():
    from binance.client import Client
    import secrets
    import pickle
    import util

    config = util.get_config()
    client = Client(config["Binance"]["api_key"], config["Binance"]["api_secret"])

   # get all symbol prices
    try:
        prices = client.get_all_tickers()
    except Exception as e:
        print(f"failed. reason: {e}")
        return

    pickle.dump(prices, open("prices.p", "wb"))

    print("success")
