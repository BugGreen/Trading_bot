import requests
import json
# Desde acá se puede obtener infromación pública: Spreads, volumen, ordenes, etc...


class Currencies:

    def __init__(self, base_currency, quote_currency):
        self.base_currency = base_currency.lower()
        self.quote_currency = quote_currency.lower()
        self.url = f'https://www.buda.com/api/v2/{{}}/{self.base_currency}-{self.quote_currency}/{{}}'
        self.url_private = f'https://www.buda.com/api/v2/'

    # Este método genera el link que se necesita en cada caso
    def url_generator(self, format_2, format_1='markets') -> str:
        url = self.url
        return str(url.format(format_1, format_2))

    # Vueleve un get requests en un objeto json
    @staticmethod
    def link_json_get(self, url, params=None, auth=None):
        return requests.get(url, auth=auth, params=params).json()

    # Vueleve un post requests en un objeto json
    @staticmethod
    def link_json_post(self, url, params, auth=None):
        return requests.post(url, auth=auth, json=params).json()

    def task(self, action, format_2, params=None, auth=None, format_1='markets'):
        url = self.url_generator(format_2, format_1)
        if action == 'get':
            return self.link_json_get(self, url, params, auth)
        elif action == 'post':
            return self.link_json_post(self, url, params, auth)
        else:
            print('action required: get or post')

    def ticker(self):
        self.task('get', 'ticker')

    def order_book(self):
        self.task('get', 'order_book')

    def trades_time(self):
        self.task('get', 'trades')

    # Con este método se pueden generar ordenes de compra y venta de prueba
    def quotation_simulation(self, amount, action):

        dictionary = {
            'type': '',
            'amount': amount
        }
        if action == 'buy':
            dictionary['type'] = 'bid_given_value'
        elif action == 'sell':
            dictionary['type'] = 'ask_given_value'
        else:
            print('Ingrese acción: sell o buy')
        self.task('post', 'quotations', dictionary)


# Imprime el objeto json de una manera más legible
def jprint(obj):
    print(json.dumps(obj, indent=2))
