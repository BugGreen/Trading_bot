from calls import PrivateCalls
from playsound import playsound
import requests
import re
from tqdm.auto import tqdm


def print_market_info(market_info):
    count = 0
    print('\n \n \n')
    print('______________________________________________________________________________________________________')

    for info in market_info:
        print('__________________________________________________________________________________________________')
        if info == 'btc-clp':
            print('Market---Spread-----Volume----Last-Price-----Min-ask-------max-bi----------24h Var---7d var')
        information = market_info[info]
        unsorted_keys = information.keys()
        keys = sorted(unsorted_keys)
        print(count, info, ' : ', round(float(information[keys[6]][2]), 3), ' | ', round(float(information[keys[7]][0]),
                                                                                         1),
              ' | ', (information[keys[0]][0]), ' | ', (information[keys[3]][0]), ' | ', (information[keys[2]][0]),
              ' | ', round(float(information[keys[4]])*100, 1), ' | ', round(float(information[keys[5]])*100, 1))
        count = count+1


# Función para adquirir información de todos los mercados
def get_market_info(api_key: str, api_secret: str, printer=True):
    info = dict()
    market_id = ['btc-clp', 'eth-clp', 'bch-clp', 'ltc-clp', 'btc-cop', 'eth-cop', 'bch-cop', 'ltc-cop', 'btc-pen',
                 'eth-pen', 'bch-pen', 'ltc-pen']

    for identification in tqdm(market_id, desc='Recopilando info...'):
        base_currency = re.findall('([a-z]*)-', identification)[0]
        quote_currency = re.findall('-([a-z]*)', identification)[0]

        market = PrivateCalls(base_currency, quote_currency, api_key, api_secret)

        info[identification] = (market.ticker()['ticker'])
        min_ask, max_bid = float(info[identification]['min_ask'][0]), float(info[identification]['max_bid'][0])
        info[identification]['spread'] = market.spread(min_ask, max_bid)

    if printer:
        print_market_info(info)

    return info
