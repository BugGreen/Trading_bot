from currencies import Currencies, jprint
from calls import PrivateCalls
'''
btc_cop = Currencies('btc', 'Cop')
btc_cop.quotation_simulation(100000, 'buy')
btc_cop.quotation_simulation(100000, 'sell')
'''


api_key = '04296e6396ee7bf618adb9f3ea0bb171'
api_secret = 'kUm9a+lyeCSnr/7JaHtH+n3VGNHyD5zJ9T8xLtzF'

bt_cop = PrivateCalls('btc', 'cop', api_key, api_secret)
orders = bt_cop.order_creation('Ask', 150000000, 0.00075 / 2)
print(type(orders))
ident = orders['order']['id']
print(ident)
jprint(orders)
