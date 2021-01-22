from calls import PrivateCalls
from public_calls import jprint
import time

api_key = '19d2817443f81b67b22bc47977b99765'

# 'c7d404858e32e7b511d3382bd94b93ec'
# 'f9ed00f004950c465f25f063602d4b12'
api_secret = 'lDAqkFjfDnOcUt0TjFA321td3DfQKPTxdEVKWJ3c'

# 'p/xY2gk6bqg+FZ01U8AGxmC7rzzNTI0oor9OJmyl'
# 'OXMU46wu6EX4Nbv/0kEJyNTGMlW36zTMknvFd64L'

btc_cop = PrivateCalls('btc', 'cop', api_key, api_secret)
btc_clp = PrivateCalls('btc', 'clp', api_key, api_secret)

# print(btc_cop.order_book()['order_book']['asks'][1])

btc_cop.permanent_order('Ask', 20000)
