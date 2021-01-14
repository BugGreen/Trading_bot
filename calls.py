from currencies import Currencies
from private_calls import BudaHMACAuth
# Este módulo permite hacer obtener información privada de la cuenta asociada
# a la llave y API secret: balance, historial de ordenes, generar ordenes, etc..


class PrivateCalls(Currencies):
    def __init__(self, base_currency, quote_currency, api_key, api_secret):
        super().__init__(base_currency, quote_currency)
        self.api_key = api_key
        self.api_secret = api_secret

    def authentication(self):
        return BudaHMACAuth(self.api_key, self.api_secret)

    def my_orders(self, per, page, state='traded'):
        params = {
            'state': state,
            'per': per,
            'page': page
        }
        auth = self.authentication()
        url = self.url_generator('orders')
        response = self.link_json_get(url, auth, params)
        self.jprint(response)

    def order_status(self, identification):
        url = self.url_generator(identification, 'orders')

