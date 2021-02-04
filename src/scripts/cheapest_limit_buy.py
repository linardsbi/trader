import binance_util, threading, time

funds = None
client = binance_util.make_client()

def refresh_funds(name):
    global funds
    while True:
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
            price = binance_util.get_current_price_for(client, symbol)
            lowest_pr = binance_util.get_smallest_ask_price_at_amount(client, symbol, float(funds))
            if lowest_pr:
                qty = format(float(funds) / float(price), "f")

                order = client.order_limit_buy(symbol=symbol, 
                quantity=qty, 
                price=lowest_pr)

                print(f"limit buying {qty} of {coin_name} at {lowest_pr}")

        except Exception as e:
            print(f"{e}\n with: {coin_name}")
            exit()
    else:
        print(f"Invalid coin name {coin_name}")
        exit()

    import webbrowser
    webbrowser.open_new_tab(f"https://www.binance.com/en/trade/{coin_name}_{to_coin}")
