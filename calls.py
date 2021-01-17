from public_calls import Currencies, jprint
from private_calls import BudaHMACAuth
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
        self.private_task('get', identification, {}, 'orders')

    def order_creation(self, order_type, price, amount, price_type='limit'):
        amount = (amount / price) * 1.004
        '''if order_type == 'Ask':
            amount = (amount / price) * 1.004
        elif order_type == 'Bid':
            amount = (price / )
        print(order_type)'''
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
