from calls import PrivateCalls
from public_calls import jprint

api_key = '04296e6396ee7bf618adb9f3ea0bb171'

# 'c7d404858e32e7b511d3382bd94b93ec'
# 'f9ed00f004950c465f25f063602d4b12'
api_secret = 'kUm9a+lyeCSnr/7JaHtH+n3VGNHyD5zJ9T8xLtzF'

# 'p/xY2gk6bqg+FZ01U8AGxmC7rzzNTI0oor9OJmyl'
# 'OXMU46wu6EX4Nbv/0kEJyNTGMlW36zTMknvFd64L'

btc_cop = PrivateCalls('btc', 'clp', api_key, api_secret)
btc_clp = PrivateCalls('btc', 'clp', api_key, api_secret)

# print(btc_cop.order_book()['order_book']['asks'][1])
jprint(btc_cop.my_orders(1, 1, 'traded'))
try:
    btc_cop.order_cycle('Bid', 595)
except:
    print('Tuvimos un error, procederé a volverlo a intentar')
    btc_clp.order_cycle('Bid', 595)

