from calls import PrivateCalls
from public_calls import jprint
import time

api_key = '04296e6396ee7bf618adb9f3ea0bb171'

# 'c7d404858e32e7b511d3382bd94b93ec'
# 'f9ed00f004950c465f25f063602d4b12'
api_secret = 'kUm9a+lyeCSnr/7JaHtH+n3VGNHyD5zJ9T8xLtzF'

# 'p/xY2gk6bqg+FZ01U8AGxmC7rzzNTI0oor9OJmyl'
# 'OXMU46wu6EX4Nbv/0kEJyNTGMlW36zTMknvFd64L'

btc_cop = PrivateCalls('btc', 'cop', api_key, api_secret)
btc_clp = PrivateCalls('btc', 'clp', api_key, api_secret)

# print(btc_cop.order_book()['order_book']['asks'][1])

'''
def avoid_errors(obj, order_type, amount):
    try:
        obj.order_cycle(order_type, amount)
    except (KeyError, ):
        time.sleep(2.5)
        current_order = obj.my_orders(1, 1, 'canceled')['orders'][0]['type']
        print(current_order)
        return current_order


def permanent_order(obj, order_type, amount):
    while 1 > 0:
        order_type = avoid_errors(obj, order_type, amount)


# permanent_order(btc_clp, 'Bid', 600)
btc_clp.order_cycle('Bid', 600)

'''
'''
try:
    order_type = 'Bid'
    btc_clp.order_cycle(order_type, 600)
except:
    try:
        time.sleep(2.5)
        current_order = btc_clp.my_orders(1, 1, 'canceled')['orders'][0]['type']
        print(current_order)
        order_type = current_order
    except:
        print('KeyError')
        pass
    print('Tuvimos un error, procederé a volverlo a intentar')
    btc_clp.order_cycle(order_type, 600)

'''

btc_clp.permanent_order('Bid', 600)
