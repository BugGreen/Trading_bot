import requests
import json
import time
from playsound import playsound

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
        if format_1 == 'orders':
            url = f'https://www.buda.com/api/v2/{{}}/{{}}'
        return str(url.format(format_1, format_2)) #Devuelve la URL donde llamar para realizar la operación deseadada

    # Vueleve un get requests en un objeto json
    @staticmethod
    def link_json_get(url, params=None, auth=None): #Para cargar información de la API 'Ticker' o de la orden del mercado a cancelar, si esta completa o incompleta
        try:
            data=requests.get(url, auth=auth, params=params).json()# Se trae la info del mercado o de la orden generada
            flg1 = 'ticker' in data.keys() #Key para info del mercado
            flg2 = 'order' in data.keys()#Key para info de la orden
        except:
            flg1 = False #Si no están en el diccionario de retorno quiere decir que hay un error por lo que entra en el ciclo para seguir intentando traer la info
            flg2 = False
        # print(data.keys())
        while not (flg1 or flg2):#Mientras que no encuentre tiker o order en el diccionario de retorno, sigue tratando de conectarse para traer la info         :#not 'ticker' in data.keys() or not 'order' in data.keys() :   
            try:
                data=requests.get(url,auth=auth,params=params).json() # Intenta reconectar
                flg1 = 'ticker' in data.keys()#Si logra conectar actualiza los valores de las variables flg1 y flg2
                flg2 = 'order' in data.keys()
                
            except: # Si no logra reconectar se queda intentando y no actualiza las flags
                print('_________________¡¡¡¡Intentando reconectar!!!!_________________',end="\r")
                try:
                    playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Ring07.wav")
                except:
                    print("No se encuentra ruta de archivo de audio..")
                    time.sleep(2)
                    pass
               
        return data

    # Vueleve un post requests en un objeto json
    @staticmethod

    def link_json_post(url, params, auth=None): #Para crear la orden de venta o compra, devuelve diccionario Json
        try:
            data = requests.post(url, auth=auth, json=params).json() #SE LLAMA A LA URL con la autenticación y los parámetros de la orden
            flg=data.keys() #Este flag se usa para determinar si se recibio una respuesta de error o no
            
        except:
            flg=list()
            print(flg,'2')
        while not 'order' in flg: #Si no está "order " en flg significa que no se aceptó la orden, se procede a evaluar el error
            try: #Primero se intenta enviar de nuevo la orden, 
                
                time.sleep(4)
                print('¡¡¡¡Intentando enviar orden a Buda!!!!')#,end="\r")
                data=requests.post(url,auth=auth,params=params).json() #Si funciona no entra en el except
                flg=data.keys()#Si funciona la linea anterior se actualiza flg si no... pasa de una vez al Except sin actualizar flg
                print(flg,'3')
                
            except:#Si definitivamente no hay respuesta positiva... Ahora si se evalua el error
                time.sleep(5)
                if 'errors' in flg: # Se determina si hay error en las keys del diccionario json que retornó
                    print('ERROR:')
                    print(data['message'],'  :  ',data['errors'][0]['message']) #Se imprime el error obtenido
                    
                    if data['errors'][0]['message']== 'insolvent': #Si es por fata de recursos se procede a bajar de a pocos el amount para ver si se logra generar la orden
                        print('Parámetros iniciales:  ', params['amount'],' y la cantidad de dinero: ',params['amount']*params['limit'])
                        for times in range(5): #Lo hacemos 3 veces.. Se podría cambiar para bajar mas veces pero creo que con 3 está bien
                            time.sleep(1)
                            params['amount']=params['amount']*0.995 #Se reduce unicamente el parámetro "amount"
                            print('Se baja la cantidad de monedas a: ',params['amount'],' y la cantidad de dinero a: ',params['amount']*params['limit']) #Imprimimos info del nuevo amount y nuevo dinero a invertir o recibir
                            data= requests.post(url, auth=auth, json=params).json()# Volvemos a llamar con el nuevo parámetro y esperamos llamada a ver si es positiva o de error
                            flg=data.keys()
                            if 'order' in flg:
                                return data

                    if 'errors' in flg:
                        print('Imposible solucionar el error...')
                        print(data['message'],'  :  ',data['errors'][0]['message'],'\n')
                        time.sleep(2)
                        break
                                    
                try:
                    playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Ring07.wav")
                except:
                    print("No se encuentra ruta de archivo de audio..")
                    time.sleep(2)
                    pass

        return data
 



    
    # Vuelve un put requests en un objeto json
    @staticmethod
    def link_json_put(url, params, auth): # Para cancelar 
        counter=0
        try:
            data=requests.put(url, auth=auth, json=params).json()
            flg= data.keys()
        except:
            flg=list()
        while not 'order' in flg and counter<1:
            try:
                data=requests.put(url,auth=auth,params=params).json()
                flg=data.keys()
            except:
                print('¡¡¡¡Intentando cancelar orden en Buda!!!!',end="\r")
                counter=counter+1
                try:
                    playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Ring07.wav")
                except:
                    print("No se encuentra ruta de archivo de audio..")
                    time.sleep(2)
                    pass
        return data
##_____Modificación para volver a conectar a la URL
    
    
    def task(self, action, format_2, params=None, auth=None, format_1='markets'):
        url = self.url_generator(format_2, format_1) # Se genera la URL para realizar la acción deseada 


##EN ESTE BLOQUE SE EVALUA A QUE OPERACIÓN CORRESPONDE LA ACCIÓN DESEADA
##--------------------------------------------------------GETTING------------------------------------------------------
        if action == 'get':
            try:
                json_info = self.link_json_get(url, params, auth) #________________________________________________________________________________
                return json_info
                
            except:
                
                print('Error al traer información de la API, espero 2 segundos y vuelvo a intentar...:' ,end="\r")
                time.sleep(2)
                json_info=self.link_json_get(url, params, auth)
                
                return json_info
##------------------------------------------------------------POSTING-------------------------------------------
        elif action == 'post':
            try:
                return self.link_json_post(url, params, auth)#____________________________________________________________________________________
            except:
                print('Error al enviar la orden, espero 2 segundos y vuelvo a intentar...:',end="\r" )
                try:
                    playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Ring07.wav")
                except:
                    print("No se encuentra ruta de archivo de audio..")
                    pass
                #time.sleep(2)
                return self.link_json_post(url, params, auth)
##--------------------------------------------------------------PUTTING-------------------------------------------
        elif action == 'put':
            try:
                return self.link_json_put(url, params, auth) #______________________________________________________________________________________
            except:
                print('Error al cancelar la orden, espero 2 segundos y vuelvo a intentar...:',end="\r" )
                try:
                    playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Ring07.wav")
                except:
                    print("No se encuentra ruta de archivo de audio..")
                    pass
                #time.sleep(2)
                return self.link_json_put(url, params, auth)
        else:
            
            print('action required: get or post')

##____________________________________________________________________________________________________________________________

    def ticker(self):
        return self.task('get', 'ticker')

    def order_book(self):
        return self.task('get', 'order_book')

    def trades_time(self):
        return self.task('get', 'trades')

    

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
    print(json.dumps(obj, sort_keys=True, indent=2))
