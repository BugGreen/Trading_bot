from public_calls import Currencies
from private_calls import BudaHMACAuth
import time
import re

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
        order_type = order_type.title()
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

    def spread(self, min_ask=False, max_bid=False):  # min_ask y max_bid se pasan como parámetros en get_market_info
        if min_ask and max_bid:
            pass
        else:
            ticker = self.ticker()
            min_ask = float(ticker['ticker']['min_ask'][0])
            max_bid = float(ticker['ticker']['max_bid'][0])
        percentage = (min_ask - max_bid) / max_bid * 100
        return min_ask, max_bid, percentage

    def order_choice(self, order_type, amount, gain=0, min_ask=False, max_bid=False):
        feed = 0.8
        values = self.spread(min_ask, max_bid)

        if order_type == 'Ask':
            price = values[0] - 0.1
        elif order_type == 'Bid':
            price = values[1] + 0.1
        else:
            print('Ingresar una operación valida')
            return None

        if values[2] >= (gain + feed):
            response = self.order_creation(order_type, price, amount)
            return price, response['order']['id']
        else:
            return 'El spread no es suficiente'

    def filled(self, identification, min_order):
        amounts = self.order_status(identification)
        original, traded = float(amounts['order']['original_amount'][0]), float(amounts['order']['traded_amount'][0])
        diff = original - traded

        if diff <= min_order:
            return 'Traded', diff
        else:
            if diff >= original * 0.98:
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

    def correct_order_creations(self):
        pending_orders = self.my_orders(3, 1, 'pending')['orders']
        print(len(pending_orders))
        for order_num in range(1, len(pending_orders)):
            self.order_cancellation(float(pending_orders[order_num]['id']))

    @staticmethod
    def set_min_max(order_book, order_in_book, order_type):
        if order_type == 'Ask':
            min_ask, max_bid = order_book['asks'][order_in_book][0], order_book['bids'][0][0]
        elif order_type == 'Bid':
            min_ask, max_bid = order_book['asks'][0][0], order_book['bids'][order_in_book][0]
        return min_ask, max_bid

    # Esto hace que cuando el spread no sea suficiente, genere una orden en un lugar donde el spread si lo sea.
    def spread_regulator(self, order_type, amount, order_book):
        # Primero se verifica que el error de spread no sea por la contrapartida del mercado:
        order_in_book = 1
        if order_type == 'Ask':
            min_ask, max_bid = order_book['asks'][0][0], order_book['bids'][1][0]
        elif order_type == 'Bid':
            min_ask, max_bid = order_book['asks'][1][0], order_book['bids'][0][0]
        order_data = self.order_choice(order_type, amount, min_ask=float(min_ask), max_bid=float(max_bid))
        # En caso de que no sea lo anterior, se busca que la orden que cumpla con los requisitos de spread:
        while order_data == 'El spread no es suficiente':
            boundary_values = self.set_min_max(order_book, order_in_book, order_type)
            min_ask, max_bid = boundary_values[0], boundary_values[1]
            order_in_book += 1
            order_data = self.order_choice(order_type, amount, min_ask=float(min_ask), max_bid=float(max_bid))
        print('Generando una orden en la posición {} del libro de ordenes del mercado {}'.format(order_in_book,
                                                                                                 order_type))
        return order_data, order_in_book

    def order_cycle(self, order_type, amount, min_order):

        order_type = order_type.title()
        order_data = self.order_choice(order_type, amount, min_ask=False, max_bid=False)
        order_in_book = False
        print(order_data)

        if order_data == 'El spread no es suficiente':
            order_book = self.order_book()['order_book']
            spread_regulator_data = self.spread_regulator(order_type, amount, order_book)
            order_data, order_in_book = spread_regulator_data[0], spread_regulator_data[1]

        try:
            price, identification = order_data[0], order_data[1]
        except TypeError:
            print('Debe haber algún error de escritura')
            return None

        print(price)
        time.sleep(5)
        count = 1

        original_amount = amount

        while 1 > 0:

            references = self.spread()
            if order_type == 'Ask':
                reference = references[0]  # Min Ask
            elif order_type == 'Bid':
                reference = references[1]  # Max Bid
            if price != reference:
                status_info = self.filled(identification, min_order)
                status, diff = status_info[0], status_info[1]

                if status == 'Traded':

                    print('La orden {}, fue completada satisfactoriamente en la iteración {}. -'.format(order_type,
                                                                                                        count),
                          time.asctime(time.localtime()))
                    order_type = self.change_type(order_type)
                    amount = original_amount
                    print('Procedo a generar una orden {} -'.format(order_type), time.asctime(time.localtime()))
                    time.sleep(3.5)

                elif status == 'Incomplete':

                    amount = diff
                    print('La orden fue completada parcialmente, continúo con una orden {}, '
                          'con una cantidad de {}.'.format(order_type, amount), diff)

                elif order_in_book:
                    # time.sleep(10)
                    boundary_values = self.set_min_max(order_book, order_in_book - 1, order_type)
                    min_ask, max_bid = boundary_values[0], boundary_values[1]
                    order_data = self.order_choice(order_type, amount, min_ask=float(min_ask), max_bid=float(max_bid))
                    if order_data == 'El spread no es suficiente':
                        continue

                print('Cancelar orden -', time.asctime(time.localtime()))
                self.correct_order_creations()
                self.order_cancellation(identification)
                order_data = self.order_choice(order_type, amount)
                price, identification = order_data[0], order_data[1]

            count += 1
            time.sleep(2)

    def set_min_order(self):
        base_currency = self.base_currency.upper()

        if base_currency == 'LTC':
            min_order = 0.0031
        elif base_currency == 'BTC':
            min_order = 0.000021
        elif base_currency == 'ETH':
            min_order = 0.0011
        elif base_currency == 'BCH':
            min_order = 0.0011
        else:
            print('MERCADO NO RECONOCIDO')
            return None
        return min_order

    def avoid_errors(self, order_type, amount, min_order):
        try:
            self.order_cycle(order_type, amount, min_order)
        except:
            time.sleep(1)
            current_order = self.my_orders(1, 1, 'canceled')['orders'][0]['type']
            print(current_order)
            return current_order

    def permanent_order(self, order_type, amount):
        min_order = self.set_min_order()
        while 1 > 0:
            order_type = self.avoid_errors(order_type, amount, min_order)
