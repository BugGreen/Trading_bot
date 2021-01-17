from public_calls import Currencies, jprint
from calls import PrivateCalls
import time
'''
btc_cop = Currencies('btc', 'Cop')
btc_cop.quotation_simulation(100000, 'buy')
btc_cop.quotation_simulation(100000, 'sell')
'''


api_key = 'f9ed00f004950c465f25f063602d4b12'
# '04296e6396ee7bf618adb9f3ea0bb171'
api_secret = 'OXMU46wu6EX4Nbv/0kEJyNTGMlW36zTMknvFd64L'
# 'kUm9a+lyeCSnr/7JaHtH+n3VGNHyD5zJ9T8xLtzF'

btc_cop = PrivateCalls('btc', 'cop', api_key, api_secret)

'''
parameters = list()
values = list()
for i in range(3):
    #print(btc_cop.ticker()['ticker'].keys())
    lista = [parm for parm in btc_cop.ticker()['ticker']]
    for parm in btc_cop.ticker()['ticker']:
        parameters.append(parm)
        if type(btc_cop.ticker()['ticker'][parm])==str:
            values.append(btc_cop.ticker()['ticker'][parm])
        else:
            values.append(btc_cop.ticker()['ticker'][parm][0])
    print (parameters)
    print (values)
    parameters=list()
    values=list()
'''


def spread(obj):
    ticker = obj.ticker()
    min_ask = float(ticker['ticker']['min_ask'][0])
    max_bid = float(ticker['ticker']['max_bid'][0])
    percentage = (min_ask - max_bid) / max_bid * 100
    return min_ask, max_bid, percentage


def order_choice(obj, order_type, amount, gain=0):
    feed = 0.4
    values = spread(obj)
    if order_type == 'Ask':
        price = values[0] - 1
    elif order_type == 'Bid':
        price = values[1] + 1
    else:
        print('Ingresar una operación valida')
        return None

    if values[2] >= (gain + feed):
        response = obj.order_creation(order_type, price, amount)

        # print(response)
        return price, response['order']['id']
    else:
        print('El spread no es suficiente')


def order_cycle(obj, order_type, amount):
    order_data = order_choice(obj, order_type, amount)
    price, identification = order_data[0], order_data[1]
    print(price)
    time.sleep(5)
    count = 1
    while 1 > 0:
        print(count)
        references = spread(obj)
        if order_type == 'Ask':
            reference = references[0]
        elif order_type == 'Bid':
            reference = references[1]
        if price != reference:
            print(reference)
            print(obj.order_cancellation(identification))

            order_data = order_choice(obj, order_type, amount)
            price, identification = order_data[0], order_data[1]
            print(price - spread(obj)[1])
            time.sleep(5)
        count += 1


order_cycle(btc_cop, 'Ask', 3000)



'''
btc_cop_ticker = btc_cop.ticker()
eth_cop_ticker = eth_cop.ticker()
print(spread(btc_cop_ticker))
print(spread(eth_cop_ticker))
jprint(btc_cop.order_book()['order_book']['asks'])
'''