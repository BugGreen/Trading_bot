from calls import PrivateCalls
from functions import get_market_info
from public_calls import jprint

api_key = '5712449297d2fb1f9913d4f696e27a67'
api_secret = 'BjOstWaN0gv5TzF8JNY9MDgGrnoCrLzBrWhYAteV'

btc_cop = PrivateCalls('btc', 'cop', api_key, api_secret)
btc_clp = PrivateCalls('btc', 'clp', api_key, api_secret)
btc_pen = PrivateCalls('btc', 'pen', api_key, api_secret)

btc_cop.permanent_order('Bid', 3000)
# btc_clp.permanent_order('Bid', 595)
# btc_pen.permanent_order('bid', 18.7)

# print(btc_cop.order_book()['order_book']['asks'][1])
# get_market_info(api_key, api_secret)

