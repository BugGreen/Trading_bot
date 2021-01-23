from public_calls import Currencies
from private_calls import BudaHMACAuth
import time
import requests
from playsound import playsound
import re
import os
import datetime

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
                if Sound:
                        try:
                            playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\windows_error.mp3")
                        except:
                            print("No se encuentra ruta de archivo de audio..")
                            pass
                        else:
                            time.sleep(1)
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
        auth = self.authentication() #Se llama a la función de autenticación
        return self.task(action, format_2, params, auth, format_1) #Retorna la respuesta de la llamada 

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
        if amount > 1: #Si amount es menor a 1 quiere decir que se esta dando en base_currency y no en quote_currency
            amount = (amount / price) * 1.004 # Se tiene en cuenta la comisión
        params = {# Es un diccionario
            'type': order_type,
            'price_type': price_type,
            'limit': price,
            'amount': amount,
        } #Parámetros iniciales que se le dará a la función de llamada, dependiendo de la respuesta la funcion de llamada los puede cambiar para evitar errores
        return self.private_task('post', 'orders', params) #Se llama a la función madre

    def order_cancellation(self, order_id):
        params = {
            'state': 'canceling',
        }
        order_data_state=self.private_task('put', order_id, params, 'orders')


        return order_data_state

    def spread(self):
        ticker = self.ticker() #Trae la info del mercado
        
        min_ask = float(ticker['ticker']['min_ask'][0])
        max_bid = float(ticker['ticker']['max_bid'][0])
        percentage = (min_ask - max_bid) / max_bid * 100
        return min_ask, max_bid, percentage #Retorna info actual del mercado 

## REVISAR ESTA FUNCIÓN NO ESTÁ CATALOGANDO BIEN,TOCA PONERLE UN MARGEN DIFF NO ES IGUAL A CERO NI AL ORIGINAL RESPECTIVAMENTE,HAY DECIMALES DE POR MEDIO
    def filled(self, identification):
        amounts = self.order_status(identification)
        original, traded = amounts['order']['original_amount'][0], amounts['order']['traded_amount'][0]
        diff = float(original) - float(traded)
        base_money=re.findall('([A-Z]*)-',amounts['order']['market_id'])[0]
        if base_money == 'LTC':
            min=0.0031
        elif base_money == 'BTC':
            min=0.000021
        elif base_money == 'ETH':
            min= 0.0011
        elif base_money == 'BCH':
            min= 0.0011
        else:
            print('MERCADO NO RECONOCIDO')

        if diff < min: #REVISAR ESTO... PARECE QUE NO SIEMPRE ES 0 CUANDO SE REALIZA LA OPERACIÓN
            print('La orden se completó')
            return 'Traded', diff
        else:
            if diff > float(original)*0.98:
                print('La orden está en espera')
                return 'Received', diff
            else:
                print('Se ejecutó de forma incompleta')
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
        values = self.spread() # Info actual del mercado- Min ask - Max bid - spread
        
        if order_type == 'Ask':
            price = values[0] - 0.1
        elif order_type == 'Bid':
            price = values[1] + 0.1
        #Se determinó el precio de venta o compra dependiendo de la operación

        if values[2] >= (gain + feed): #Se decide si se hace la orden dependiendo del spread
            try: #Intente crear la orden 
                response = self.order_creation(order_type, price, amount) #Si se crea la orden se recoge información de la misma, es un diccionario json
                # ACA SI existe error en la orden puedo encontrar en respons 'code'---',message entre otras'
                originalamount=float(response['order']['original_amount'][0])*float(response['order']['limit'][0]) #Se asigna el valor de la orden creada al original amount
                # Retorna: Precio de apertura---id de orden---Spread en porcentaje---id de mercado---Fecha de creación-----Valor en pesos a comprar o vender,retorna tambien toda la respuesta
                return price, response['order']['id'] , values[2],response['order']['market_id'] , response['order']['created_at'],originalamount,response
            except:
                print('No es posible crear la orden, verifique si realiza la operación con una cantidad al monto mínimo o si tiene los recursos suficientes...')
                time.sleep(3)
                
                


            
        else:
            
            return None, None, None

    def order_cycle(self, order_type, amount,gain,Sound):
        changes_types=list()
        changes_dates=list()
        amount_list=list()
        price_list=list()
        diference=list()
        diferences=list()
        originalamount=amount
        try:
            print('Intentando crear orden...')
            order_data = self.order_choice(order_type, amount,gain) ###------- Se intenta crear la orden dependiendo del spreed , si no no se actualiza la fecha de iniciación 
            # original_amount=
            try:
                starts_at=order_data[4] #Se actualiza la fecha de creación de la orden
            except:
                starts_at='No se ha ejecutado la primera orden'
        except:
            return 
        try: #Intenta adquirir información de la orden inicial creada si no lo logra le asigna a price y a identification "None"
            price, identification, original_amount = order_data[0], order_data[1], order_data[5]
            print(originalamount, original_amount)
            # if Sound: #Esto es solo para adornar y notificar la creación de la orden inicialñ con un sonido
            #     try:
            #         playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\Alarm09.wav")
            #     except:
            #         print("No se encuentra ruta de archivo de audio..")
            #         pass
            # else:
            time.sleep(1)
        except: #Asignación de None si no pudo recuperar información de la orden inicial
            price= None
            identification= None

        if order_data == (None,None,None): # Si no pudo crear la orden quiere decir que order choice determino que el spread no era adecuado, por lo que no hay información de la orden inicial
            while order_data== (None,None,None): # Se queda esperando hasta un spread adecuado
                order_data = self.order_choice(order_type,amount,gain)
                
                time.sleep(2)
                print('Esperando un Spread adecuado el actual es de:',round( self.spread()[2],3),'% Diferencia del: ',round( self.spread()[2],3)-gain,'%',end="\r")
                try:
                    price, identification, original_amount = order_data[0], order_data[1], order_data[5]
                except:
                    continue
                cancelling=False #Se le asigna a la variable cancelling false por que no hay ninguna orden que cancelar pues no se ha creado

            
        else:
            cancelling=True # Si se creo la orden inicial si exite orden cancelable por lo que se le asigna True
        amount_0=original_amount
        amount=amount_0
        opera= str() #Esta variable se usa para traducir que tipo de operación es Ask=Vender Bid= Comprar
        sells = 0 #Entero para almacenar el numero de operaciones exitosas de ventas
        buys = 0#Entero para almacenar el numero de operaciones exitosas de compras
        print('Precio de apertura: ',price) # Se imprime el precio de apertura de la orden inicial, o bueno... Del mercado en ese momento
        time.sleep(0) #Este tiempo se puede modificar para darle una espera mientras aceptan la orden para que no cree 2 ordenes iniciales, pues puede que no alcance a detectar que aceptaron la orden anterior... Es enredado
        count = 1 #Antes de comenzar el ciclo de lógica se crea la variable count para contar las iteraciones
        while 1 > 0: #Ciclo infinito
            # amount=original_amount
            #print('El spread actual es de : ',round(order_data[2],3),'%')
            references = self.spread() #Actualizamos la información del mercado para comparar el precio de nuestra orden con el del mercado actual y así tomar desición, Retorna max-
            if order_type=='Ask':
                opera = 'Vender'
            elif order_type =='Bid':
                opera = 'Comprar'
                #SE TRADUCEN LAS ORDENES A ESPAÑOL
            try:
                print('El spread actual es de : ',round(references[2],3),'% Diferencia del ',round(references[2]-gain,3),'% ----Se está intentando',opera, amount/price, ' criptos en :',round(amount,2), 'A un precio de: ',round(price,2))#round(order_data[2],3),'%')
            except:
                print('No hay orden creada')
                pass
            if not order_data[2]==None and cancelling==True: # Si se creó la orden inicial y hay orden para cancelar entra en el if
                if order_type == 'Ask':
                    reference = references[0] # Min Ask
                elif order_type == 'Bid':
                    reference = references[1] # Max Bid
                    # Se determina la refencia de precio dependiendo del tipo de orden que se está ejecutando... y se le asigna a reference, references viene del método spread
                
                
                if round(price,2) != reference : #Si el precio al cual se creó la orden es diferente de al del mercado
                    print(price,reference)
                    status_info = self.filled(identification) # Se determina el estado de la orden COMLETA A MEDIAS O PENDIENTE
                    status, diff = status_info[0], status_info[1] #SE le asigna a status el estado de la orden y a diff la cantidad faltante por ejecutar
                                        
                    if status == 'Traded': # Si se completa la orden
                        if amount<1:
                            amount_list.append(amount) 
                        elif amount>1:
                            amount_list.append(amount/order_data[0])
                         #EN LOS CONDICIONALES ANTERIOR SOLO SE GUARDAN EN UN VECTOR EL AMOYUNT DE LA ORDEN COMPLETADA
                        if order_type =='Ask':
                            sells=sells+1
                            changes_types.append('Venta')
                        if order_type =='Bid':
                            buys=buys+1
                            changes_types.append('Compra')
                        # Y ACA SE GUARDAN LOS TIPOS DE ORDENES REALIZADAS IGUAL, EN UN VECTOR

                        now = datetime.datetime.now()
                        day=str(now.day)
                        month=str(now.month)
                        year=str(now.year)
                        hour=str(now.hour)
                        minute=str(now.minute)
                        price_list.append(order_data[0])

                        date= day+'/'+month+'/'+year+'  '+hour+':'+minute
                        changes_dates.append(date)
                        order_type = self.change_type(order_type) # SE CAMBIA EL TIPO DE ORDEN VENTA O COMPRA
                        ## EN EL BLOQUE DE INSTRUCCIONES PREVIAS SE GUARDAN LAS HORAS Y FECHAS DE LAS OPERACIONES COMPLETADAS
                        amount=amount_0*0.9960159 ## REVISAR°°________________________________________________°°°°
                        print("Se ejecutó la orden en la iteración: ",count)
                        cancelling=False

                        if Sound:
                            try:
                                playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\sound87.wav")
                            except:
                                print("No se encuentra ruta de archivo de audio..")
                                pass
                        else:
                            time.sleep(1)
                    #ACA SUENA CUANDO SE COMPLETA UNA ORDEN---------- ES OPCIONAL CON EL BOLEANO Sound

                    if status == 'Incomplete': # Si la orden se ejecuto a medias... 
                        if amount<1:
                            amount_list.append(amount-diff) 
                        elif amount>1:
                            amount_list.append((amount-diff)/order_data[0])
                         #EN LOS CONDICIONALES ANTERIOR SOLO SE GUARDAN EN UN VECTOR EL AMOYUNT DE LA ORDEN COMPLETADA
                        if order_type =='Ask':
                            sells=sells+1
                            changes_types.append('Venta Incompleta')
                        if order_type =='Bid':
                            buys=buys+1
                            changes_types.append('Compra Incompleta')
                        # Y ACA SE GUARDAN LOS TIPOS DE ORDENES REALIZADAS IGUAL, EN UN VECTOR

                        now = datetime.datetime.now()
                        day=str(now.day)
                        month=str(now.month)
                        year=str(now.year)
                        hour=str(now.hour)
                        minute=str(now.minute)
                        price_list.append(order_data[0])

                        date= day+'/'+month+'/'+year+'  '+hour+':'+minute
                        changes_dates.append(date)

                        print('Se ejecutó a medias la orden')
                        if Sound:
                            try:
                                playsound(r"C:\Users\dagma\Desktop\Trading_Bot_Git\Trading_bot\sound82.wav")
                            except:
                                print("No se encuentra ruta de archivo de audio..")
                                pass
                        else:
                            pass

                        amount = diff*price*0.9960159 #Acá se le asignará a la nueva orden el restante de lo que
                  #  if status ==  'Received':
                       # amount=amount_0*0.9960159


                    #SE EVALUA SI HAY ORDEN POR CANCELAR
                    if cancelling==True:
                        print('\n....CANCELANDO ORDEN....')                    
                        try:
                            data_order_cancelation=self.order_cancellation(identification)
                            if not data_order_cancelation['order']['state']=='canceled':
                                cancelOK=False
                                Error=False
                            else:
                                cancelOK=True
                            while cancelOK==False:
                                data_order_cancelation=self.order_cancellation(identification)
                                if data_order_cancelation['order']['state']=='traded':
                                    cancelOK=True



                                order_state=data_order_cancelation#self.order_status(identification)
                                
                                # print('Cancelación: ',data_order_cancelation['order']['state'],end='\r')
                                if order_state['order']['state']=='canceled':
                                    print('\n No hay error en la cancelación')
                                    Error=False
                                    cancelOK=True
                                
                                else:
                                    cancelOK=False
                                    Error=True
                                    print('...Intentando cancelar orden...',end='\r')
                                
                        except:
                            break
                            # Error=True
                            # # Trys=1
                            # time.sleep(2)
                            # while Error== True:
                            #     print('No se logró cancelar la orden... intento de nuevo')
                            #     try:    
                            #         data_order_cancelation=self.order_cancellation(identification)
                            #         if 'order' in data_order_cancelation:
                            #             Error=False
                            #     except:
                            #         pass

                            
                    
                    # # print(self.order_book()['order_book']['bids'][1])
                    # try:#Intenta cancelar orden
                    #     self.order_cancellation(identification)
                    #     time.sleep(1)
                    # except:
                    #     print('No pude cancelar orden... Volveré a intentar')
                    #     time.sleep(1)
                    #     try:
                    #         self.order_cancellation(identification)
                    #         time.sleep(1)
                    #     except:
                    #         print('Defeinitivamente no pude cancelar la orden... salgo del loop')
                    #         break

                    # SE TERMINA DE CANCELAR LA ORDEN

                    if Error==False:
                        # time.sleep(0.5)
                        try: #ACÁ SE INTENTA CREAR LA NUEVA ORDEN DEL TIPO CONTRARIO
                            # print('1')
                            order_data = self.order_choice(order_type, amount,gain) ## Se crea la nueva orden
                            # print('2')
                            order_data_creation=order_data[6]
                            # print('3')
                            order_data_creation=self.order_status(order_data[1])
                            # print('4')
                            print(order_data_creation['order']['state'])
                            while not order_data_creation['order']['state']=='pending':
                                print('Esperando recepción',end='\r')
                                order_data_creation=self.order_status(order_data[1])

                            print('\n Se creó la orden...')

                            if order_data ==(None,None,None):
                                cancelling=False # SI NO SE CREA LA ORDEN NO HABRÄ ORDEN POR CANCELAR POR LO QUE CANCELLING = FAlse
                            elif order_data_creation['order']['state']=='pending' :
                                print('Orden enviada y aceptada')
                                cancelling=True # SI SE LOGRA CREAR ENTONCES SI HABRÁ POR LO QUE CANCELLING =True 

                        except:
                            cancelling=False
                            pass
                    else:
                        print('No se crea orden...')

                        continue



                    price, identification= order_data[0], order_data[1] 
                    # time.sleep(4)
                # if count % 50 == 0:
                # time.sleep(5)
                count += 1
                if count%10==0:
                    os.system('cls')
                    try:
                        print('Se llevan: ',count,' iteraciones.  Se está intentando: ',opera)
                        print('Se llevan: ', buys,' compras y ',sells,' ventas----> ',order_data[3] )
                        date=re.findall('(.*)T',starts_at)[0]
                        hour=int(str((re.findall('([0-9]*):',(re.findall('T(.*):',starts_at)[0].split()[0])))[0]))-5
                        if hour <0:
                            hour=hour+24
                        
                        minute=int(re.findall(':(.*):',starts_at)[0])
                        print('La primera orden se hizo: ', date,' ',hour,':',minute)
                        print('\n')
                        if not changes_dates==[]:
                            print('Tipo de acción---Cantidad---Total Ej---Precio---Fecha')
                            for idx in range(len(changes_dates)):
                                
                                print(changes_types[idx],' ',amount_list[idx],' ',amount_list[idx]* price_list[idx],' ',price_list[idx],' ',changes_dates[idx])
                                # if changes_types[idx]=='Compra':
                                #     diference[idx]=(amount_list[idx])
                                #     diferences[idx]=(-amount_list[idx]* price_list[idx])
                                # elif changes_types[idx]=='Venta':
                                #     diference[idx]=(-amount_list[idx])
                                #     diferences[idx]=(amount_list[idx]* price_list[idx])
                            
                            #print('Balance de operaciones: ',sum(diference), ' ||||| ' ,sum(diferences))
                            print('_____________________________________________________________________\n')

                    except:
                        print('No hay información relacionada')
                time.sleep(0.2)

            elif cancelling == False:
                cancel=0


                while order_data== (None,None,None): # EN ESTE CICLO SE CREARÁ LA ORDEN CUANDO EL SPREAD SEA ADECUADO 
                    if cancel==0: #SOLO INTENTA CANCELAR UNA VEZ
                        try:
                            self.order_cancellation(identification) #INTENTA CANCELAR LA ORDEN SI EXISTE UNA PREVIA ANTES DE QUE EL SPREAD CAIGA
                            print(reference, order_type, '\n....CANCELANDO ORDEN....')
                        except:
                            pass

                    order_data = self.order_choice(order_type,amount,gain)
                    try:
                        price, identification, original_amount = order_data[0], order_data[1], order_data[5]
                    except:
                        pass
                    print('Esperando un Spread adecuado... Actual de: ',round(self.spread()[2],3),'% Diferencia del: ',round(self.spread()[2],3)-gain,'%')
                    cancelling=False
                    cancel=cancel+1
                    time.sleep(1)
                #CUANDO SALE DEL CICLO ES  POR QUE LOGRO CREAR UNA ORDEN POR LO QUE CANCELLING SE VUELVE VERDAD YA HAY UNA ORDEN, Y COMIENZA EL CICLO DE NUEVO
                amount_0=original_amount
                cancelling=True
                print("Spread vuelve a ser adecuado")
                time.sleep(2)
                #order_data=self.order_choice(order_type,amount)

            
