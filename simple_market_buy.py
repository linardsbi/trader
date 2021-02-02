import binance_util, threading, time

funds = 0.0
client = binance_util.make_client()

def refresh_funds(name):
    global funds
    funds = binance_util.get_remaining_amount_sync(client, name)
    time.sleep(15)


if __name__ == "__main__":
    to_coin = "BTC"
    th = threading.Thread(target=refresh_funds, args=(to_coin,), daemon=True)
    th.start()

    coin_name = input("Enter coin name: ").upper()
    if len(coin_name) >= 3:
        symbol = f"{coin_name}{to_coin}"
        try:
            binance_util.make_market_buy(client, funds, symbol)
        except:
            print(f"Invalid coin name {coin_name}")
            exit()
    else:
        print(f"Invalid coin name {coin_name}")
        exit()

    import webbrowser
    webbrowser.open_new_tab(f"https://www.binance.com/en/trade/{coin_name}_{to_coin}")


