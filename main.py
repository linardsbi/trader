from binance.client import Client
import secrets
import pickle
from binance.enums import *
import time

# 1. get coin name
# 2. check if have assets
# 3. create buy orders at various limits (splitting 25% or 50%)
# 4. if buy order succeeds, 
# 5. if buy order fails, 
# 6. for each successful buy, create sell order (splitting 50% of order at 10x and 50% at 5x)
# 7. if sell succeeds and initial investment != 10x, goto 2.
# 8. if sell fails, cancel and goto 6., setting lower multiplier

# max orders per second = 10 
# that makes 50-50 initial split + each split in 4 = 8
import util
if __name__ == "__main__":
    config = util.get_config()
    client = Client(config["Binance"]["api_key"], config["Binance"]["api_secret"])
    
    order = client.create_test_order(
            symbol='BNBBTC',
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=100)
    print(order)
#     print(client.get_account())
