from public_calls import Currencies
from private_calls import BudaHMACAuth
import time
import requests
from playsound import playsound
import re
import os

from tqdm.auto import tqdm
# Este módulo permite hacer obtener información privada de la cuenta asociada
# a la llave y API secret: balance, historial de ordenes, generar ordenes, etc..


## Función para adquirir información de todos los mercados
def get_market_info(api_key: str, api_secret: str, printter=True):
    Info=dict()
    #market_id=['btc-clp','eth-clp','bch-clp','ltc-clp','btc-cop','eth-cop','bch-cop','ltc-cop','btc-pen','eth-pen','bch-pen','ltc-pen','btc-ars','eth-ars','bch-ars','ltc-ars','eth-btc','bch-btc','ltc-btc']
    market_id=['btc-clp','eth-clp','bch-clp','ltc-clp','btc-cop','eth-cop','bch-cop','ltc-cop','btc-pen','eth-pen','bch-pen','ltc-pen']
   
    for id in tqdm(market_id, desc='Recopilando info...'):
        base_currency= re.findall('([a-z]*)-',id)[0]
        quote_currency= re.findall('-([a-z]*)',id)[0]
        # print (base_currency)
        # print (quote_currency)
        market = PrivateCalls(base_currency, quote_currency, api_key, api_secret)

        #Info[id]= market.ticker()
        #print (id,':',(market.ticker().keys()))
        Info[id] = (market.ticker()['ticker'])
        #print(type(Info[id]))
        #print(type(Info[id]))
        Info[id]['spread'] = market.spread()
        #print (Info.keys())

    if printter:
        printmarktinfo(Info)

    return Info


def printmarktinfo (market_info):
    count=0
    print('\n \n \n')
    print('______________________________________________________________________________________________________')

    for info in market_info:
        print('__________________________________________________________________________________________________')
        if info=='btc-clp':
            print('Market---Spread-----Volume----Last-Price-----Min-ask-------max-bi----------24h Var---7d var')
        information = market_info[info]
        unsortedkeys = information.keys()
        keys = sorted(unsortedkeys)
        # print(keys)
        # print (info,':',market_info[info].items())
        ##-----Market--------------------Spread----------------------------------------Volume---------------------------------Last_price----------------------min_ask-------------------------------max_bid----------------------variation24h------------------------------------variation7d
        print (count,info,' : ',round(float(information[keys[6]][2]),3),' | ',round(float(information[keys[7]][0]),1),' | ',(information[keys[0]][0]),' | ',(information[keys[3]][0]),' | ',(information[keys[2]][0]),' | ',round(float(information[keys[4]])*100,1),' | ',round(float(information[keys[5]])*100,1))
        count= count+1
    #____________________________________________________________________________



def createmarket(marketss,api_key,api_secret,gain=0,Sound=True):
    create_market=True
    create_order=False

    while create_order==False and create_market==True :
        print("\n \n EJEMPLO------------------>(1,Bid,5000)-------------->Sin paréntesis")
        print("Recuerde que se debe realizar en la moneda del mercado correspondiente el monto a tranzar")
        Selection=input('Seleccione el mercado que desea operar, operación a realizar y monto, separados por espacio, 000 para recargar: ')
        print("\n \n")
        if Selection=="000":
            print('Cargando información de nuevo')
            market_info= get_market_info(api_key,api_secret)
            marketss=(market_info.keys())
            createmarket(marketss,api_key, api_secret,gain=gain,Sound=Sound)

        markets=[key for key in marketss]
        
        select=Selection.split()
        
        try:
            base_currency=re.findall('([a-z]*)-',markets[int(select[0])])[0]
            quote_currency=re.findall('-([a-z]*)',markets[int(select[0])])[0]
            operation= re.findall('[A-z]*',select[1])[0]
            ammount= float(re.findall('[0-9]*',select[2])[0])
        except:
            print('Seleccione unos parámetros adecuados...')
            create_market=True
            create_order=False
            continue



        try:
            market=PrivateCalls(base_currency, quote_currency, api_key, api_secret)
            create_order=True
            create_market=False
            print('Se creo el mercado satisfactoriamente...')
            if Sound:
                try:
                    playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Alarm09.wav")
                except:
                    print("No se encuentra ruta de archivo de audio..")
                    pass
            else:
                time.sleep(2)
                
        except:
            print('Seleccione Datos adecuados..... Su selección fue: ', Selection)
            create_order=False
            create_market=True
            continue

        
        # operation= re.findall('[A-z]*',select[1])[0]
        # ammount= float(re.findall('[0-9]*',select[2])[0])

        print('Mercado: ', base_currency,'-', quote_currency, '         Acción: ',operation, '            Cantidad: ', ammount)
        
        input('Presione enter para continuar... \n')
        while create_order==True and create_market==False:
            try:
                market.order_cycle(operation, ammount,gain,Sound)
                create_order=False
                create_market=False
            except:
                print('No fue posible crear la orden, intente de nuevo...')
                create_order=False
                create_market=True
                continue







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


    def order_choice(self, order_type, amount, gain):
        feed = 0.4
        values = self.spread()

        if order_type == 'Ask':
            price = values[0] - 1
        elif order_type == 'Bid':
            price = values[1] + 1
        

        if values[2] >= (gain + feed):
            try:
                response = self.order_creation(order_type, price, amount)
                return price, response['order']['id'],values[2]
            except:
                print('No es posible crear la orden, verifique si realiza la operación con una cantidad al monto mínimo o si tiene los recursos suficientes...')
                time.sleep(3)
                os.system('cls')
                


            
        else:
            
            return None, None, None

    def order_cycle(self, order_type, amount,gain,Sound):
        
        try:
            print('Intentando crear orden...')
            order_data = self.order_choice(order_type, amount,gain) ###-------
        except:
            return 
        try:
            price, identification = order_data[0], order_data[1]
            if Sound:
                try:
                    playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Alarm09.wav")
                except:
                    print("No se encuentra ruta de archivo de audio..")
                    pass
            else:
                time.sleep(1)
        except:
            price= None
            identification= None

        if order_data == (None,None,None):
            while order_data== (None,None,None):
                order_data = self.order_choice(order_type,amount,gain)
                print('Esperando un Spread adecuado el actual es de:',round( self.spread()[2],3),'% Diferencia del: ',round( self.spread()[2],3)-gain,'%',end="\r")
                cancelling=False

            
        else:
            cancelling=True


        print('Precio de apertura: ',price)
        time.sleep(0)
        count = 1
        while 1 > 0:
            #print('El spread actual es de : ',round(order_data[2],3),'%')
            references = self.spread()
            print('El spread actual es de : ',round(references[2],3),'% Diferencia del ',round(references[2],3)-gain,'%' )#round(order_data[2],3),'%')
            if not order_data[2]==None and cancelling==True:
                if order_type == 'Ask':
                    reference = references[0] # Min Ask
                elif order_type == 'Bid':
                    reference = references[1] # Max Bid
                
                if price != reference :
                    status_info = self.filled(identification)
                    status, diff = status_info[0], status_info[1]
                    
                    if status == 'Traded':
                        order_type = self.change_type(order_type)
                        print("Se ejecutó la orden en la iteración: ",count)

                        if Sound:
                            try:
                                playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Alarm09.wav")
                            except:
                                print("No se encuentra ruta de archivo de audio..")
                                pass
                        else:
                            time.sleep(1)


                    elif status == 'Incomplete':
                        if Sound:
                            try:
                                playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Alarm08.wav")
                            except:
                                print("No se encuentra ruta de archivo de audio..")
                                pass
                        else:
                            pass

                        amount = diff
                    if cancelling==True:                    
                        self.order_cancellation(identification)
                    print(reference, order_type, '\n....CANCELANDO ORDEN....')
                    # print(self.order_book()['order_book']['bids'][1])
                    self.order_cancellation(identification)
                    time.sleep(0)

                    try:
                        order_data = self.order_choice(order_type, amount,gain) ## Se crea la nueva orden
                        if order_data ==(None,None,None):
                            cancelling=False
                        else:
                            cancelling=True
                    except:
                        cancelling=False
                        pass

                    price, identification = order_data[0], order_data[1]
                    # time.sleep(4)
                # if count % 50 == 0:
                # time.sleep(5)
                count += 1
                time.sleep(1)
            else:
                cancel=0
                while order_data== (None,None,None):
                    if cancel==0:
                        try:
                            self.order_cancellation(identification)
                            print(reference, order_type, '\n....CANCELANDO ORDEN....')
                        except:
                            pass
                    order_data = self.order_choice(order_type,amount,gain)
                    price, identification = order_data[0], order_data[1]
                    print('Esperando un Spread adecuado... Actual de: ',round(self.spread()[2],3),'% Diferencia del: ',round(self.spread()[2],3)-gain,'%')
                    cancelling=False
                    cancel=cancel+1
                    time.sleep(1)
                cancelling=True
                print("Spread vuelve a ser adecuado")
                time.sleep(2)
                #order_data=self.order_choice(order_type,amount)

            
