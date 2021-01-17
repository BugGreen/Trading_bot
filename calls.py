from public_calls import Currencies
from private_calls import BudaHMACAuth
import time
import requests
# Este módulo permite hacer obtener información privada de la cuenta asociada
# a la llave y API secret: balance, historial de ordenes, generar ordenes, etc..


class PrivateCalls(Currencies):
    def __init__(self, base_currency, quote_currency, api_key, api_secret):
        super().__init__(base_currency, quote_currency)
        self.api_key = api_key
        self.api_secret = api_secret

    def authentication(self):
        return BudaHMACAuth(self.api_key, self.api_secret)

    def private_task(self, action, format_2, params=None, format_1='markets'):
        auth = self.authentication()
        return self.task(action, format_2, params, auth, format_1)

    def my_orders(self, per, page, state='traded'):
        params = {
            'state': state,
            'per': per,
            'page': page
        }
        return self.private_task('get', 'orders', params)

    def order_status(self, identification):
        return self.private_task('get', identification, None, 'orders')

    def order_creation(self, order_type, price, amount, price_type='limit'):
        if amount > 1:
            amount = (amount / price) * 1.004
        params = {
            'type': order_type,
            'price_type': price_type,
            'limit': price,
            'amount': amount,
        }
        return self.private_task('post', 'orders', params)

    def order_cancellation(self, order_id):
        params = {
            'state': 'canceling',
        }
        return self.private_task('put', order_id, params, 'orders')

    def spread(self):
        ticker = self.ticker()
        min_ask = float(ticker['ticker']['min_ask'][0])
        max_bid = float(ticker['ticker']['max_bid'][0])
        percentage = (min_ask - max_bid) / max_bid * 100
        return min_ask, max_bid, percentage

    def order_choice(self, order_type, amount, gain=0):
        feed = 0.4
        values = self.spread()

        if order_type == 'Ask':
            price = values[0] - 1
        elif order_type == 'Bid':
            price = values[1] + 1
        else:
            print('Ingresar una operación valida')
            return None

        if values[2] >= (gain + feed):
            response = self.order_creation(order_type, price, amount)
            return price, response['order']['id']
        else:
            print('El spread no es suficiente')
            return 'El spread no es suficiente'

    def filled(self, identification):
        amounts = self.order_status(identification)
        original, traded = amounts['order']['original_amount'][0], amounts['order']['traded_amount'][0]
        diff = float(original) - float(traded)
        if diff == 0:
            return 'Traded', diff
        else:
            if diff == original:
                return 'Received', diff
            else:
                return 'Incomplete', diff

    @staticmethod
    def change_type(order_type):
        if order_type == 'Ask':
            return 'Bid'
        elif order_type == 'Bid':
            return 'Ask'
        else:
            return None

    def order_cycle(self, order_type, amount):

        order_data = self.order_choice(order_type, amount)
        '''
        if order_data == 'El spread no es suficiente':
            price = float(self.order_book()['order_book']['bids'][1][0]+1)'''


        try:
            price, identification = order_data[0], order_data[1]
        except TypeError:
            print('Nos jodimos')
            return None

        print(price)
        time.sleep(5)
        count = 1
        while 1 > 0:
            print(count)
            references = self.spread()
            if order_type == 'Ask':
                reference = references[0] # Min Ask
            elif order_type == 'Bid':
                reference = references[1] # Max Bid
            if price != reference:
                status_info = self.filled(identification)
                status, diff = status_info[0], status_info[1]
                if status == 'Traded':
                    order_type = self.change_type(order_type)
                elif status == 'Incomplete':
                    amount = diff
                print(reference, order_type, '\nProcedo a cancelar amos')
                # print(self.order_book()['order_book']['bids'][1])
                self.order_cancellation(identification)
                time.sleep(4)
                order_data = self.order_choice(order_type, amount)
                price, identification = order_data[0], order_data[1]
                # time.sleep(4)
            # if count % 50 == 0:
            # time.sleep(5)
            count += 1
            time.sleep(1)
