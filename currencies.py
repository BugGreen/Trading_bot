import requests
import json


class Currencies:

    parameters = {}
    payload = {}
    headers = {}

    def __init__(self, base_currency, quote_currency):
        self.base_currency = base_currency.lower()
        self.quote_currency = quote_currency.lower()
        self.url = f'https://www.buda.com/api/v2/markets/{self.base_currency}-{self.quote_currency}/{{}}'

    def link_json_get(self, link):
        return requests.get(link, params=self.parameters).json()

    def link_json_post(self, link, dictionary):
        return requests.post(link, json=dictionary).json()

    def jprint(self, obj):
        text = json.dumps(obj, indent=2)
        print(text)

    def ticker(self):
        url = self.url.format('ticker')
        response = self.link_json_get(url)
        self.jprint(response)

    def order_book(self):
        url = self.url.format('order_book')
        response = self.link_json_get(url)
        self.jprint(response)

    def trades_time(self):
        url = self.url.format('trades')
        response = self.link_json_get(url)
        self.jprint(response)

    def quotation_simulation(self, amount, action):
        # Con este método se pueden generar ordenes de compra y venta de prueba
        dictionary = {
            'type': '',
            'amount': amount
        }
        url = self.url.format('quotations')
        if action == 'buy':
            dictionary['type'] = 'bid_given_value'
        elif action == 'sell':
            dictionary['type'] = 'ask_given_value'
        else:
            print('Ingrese acción: sell o buy')
        response = self.link_json_post(url, dictionary)
        self.jprint(response)
