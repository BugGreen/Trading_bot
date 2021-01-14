import requests
import json
# Desde acá se puede obtener infromación pública: Spreads, volumen, ordenes, etc...


class Currencies:

    parameters = {}
    payload = {}
    headers = {}

    def __init__(self, base_currency, quote_currency):
        self.base_currency = base_currency.lower()
        self.quote_currency = quote_currency.lower()
        self.url = f'https://www.buda.com/api/v2/{{}}/{self.base_currency}-{self.quote_currency}/{{}}'
        self.url_private = f'https://www.buda.com/api/v2/'

    def url_generator(self, format_2, format_1='markets') -> str:
        print(self.url.format(format_1, format_2))
        return str(self.url.format(format_1, format_2))

    @staticmethod
    def link_json_get(self, link, auth=None, params={}):
        return requests.get(link, auth=auth, params=params).json()

    @staticmethod
    def link_json_post(self, link, dictionary):
        return requests.post(link, json=dictionary).json()

    @staticmethod
    def jprint(self, obj):
        text = json.dumps(obj, indent=2)
        print(text)

    def ticker(self):
        url = self.url_generator('ticker')
        response = self.link_json_get(url)
        self.jprint(response)

    def order_book(self):
        url = self.url_generator('order_book')
        response = self.link_json_get(url)
        self.jprint(response)

    def trades_time(self):
        url = self.url_generator('trades')
        response = self.link_json_get(url)
        self.jprint(response)

    def quotation_simulation(self, amount, action):
        # Con este método se pueden generar ordenes de compra y venta de prueba
        dictionary = {
            'type': '',
            'amount': amount
        }
        url = self.url_generator('quotations')
        if action == 'buy':
            dictionary['type'] = 'bid_given_value'
        elif action == 'sell':
            dictionary['type'] = 'ask_given_value'
        else:
            print('Ingrese acción: sell o buy')
        response = self.link_json_post(url, dictionary)
        self.jprint(response)


