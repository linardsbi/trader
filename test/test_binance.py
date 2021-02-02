import unittest, sys, time
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException


from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import binance_util

credentials_passed = False

class TestBinanceAPI(unittest.TestCase):
    client = binance_util.make_client()
    def test_credentials(self):
        global credentials_passed
        try:
            
            with self.assertRaises(BinanceAPIException):
                order = self.client.create_test_order(
                    symbol="BTCUSDT",
                    side=SIDE_SELL,
                    type=ORDER_TYPE_TAKE_PROFIT,
                    stopPrice=200)

            order = self.client.create_test_order(
                symbol="BTCUSDT",
                side=SIDE_BUY,
                type=ORDER_TYPE_MARKET,
                quoteOrderQty=200)

            self.assertFalse(order, "Order error")
            
            credentials_passed = True
        except BinanceAPIException as e:
            self.assertFalse(e.message, "Invalid Binance credentials!")
        
    #@unittest.skipUnless(credentials_passed, "Skipping because connection to Binance cannot be established")
    def test_system_time_delay(self):
        max_iters = 5
        diffs = []
        
        print(f"testing system time delay; will take about {max_iters}sec")
        for _ in range(max_iters):
            server_time = self.client.get_server_time()
            diffs.append(int(time.time() * 1000) - server_time['serverTime'])
            time.sleep(1)
        
        avg = sum(diffs) // max_iters
        self.assertTrue(avg > -700 and avg <= 700, f"Either the system clock is out of sync or connecting to binance takes a long time, value: {avg}")

if __name__ == '__main__':
    unittest.main()