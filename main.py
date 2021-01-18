from calls import PrivateCalls
from public_calls import jprint
from calls import get_market_info
import re
api_key = 'f9ed00f004950c465f25f063602d4b12'

# 'c7d404858e32e7b511d3382bd94b93ec'
# 'f9ed00f004950c465f25f063602d4b12'
api_secret = 'OXMU46wu6EX4Nbv/0kEJyNTGMlW36zTMknvFd64L' # PUESTA LLAVE Y SECRETO DE DAGO

# 'p/xY2gk6bqg+FZ01U8AGxmC7rzzNTI0oor9OJmyl'
# 'OXMU46wu6EX4Nbv/0kEJyNTGMlW36zTMknvFd64L'

def createmarket(marketss,api_key,api_secret):
    create_market=True
    create_order=False

    while create_order==False and create_market==True :
        print("\n \n EJEMPLO------------------>(1,Bid,5000)-------------->Sin paréntesis")
        print("Recuerde que se debe realizar en la moneda del mercado correspondiente el monto a tranzar")
        Selection=input('Seleccione el mercado que desea operar, operación a realizar y monto, separados por espacio: ')
        print("\n \n")
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
                market.order_cycle(operation, ammount)
                print('Se creo la orden satisfactoriamente...')
                create_order=False
                create_market=False
            except:
                print('No fue posible crear la orden, intente de nuevo...')
                create_order=False
                create_market=True
                continue





# btc_cop = PrivateCalls('btc', 'cop', api_key, api_secret)
# btc_clp = PrivateCalls('btc', 'clp', api_key, api_secret)

# eth_cop = PrivateCalls('eth', 'cop', api_key, api_secret)
# bch_cop = PrivateCalls('bch', 'cop', api_key, api_secret)

# print(btc_cop.order_book()['order_book']['asks'][1])
# btc_cop.order_cycle('Bid', 5000)
#_______________________________________________________________________
market_info= get_market_info(api_key,api_secret)


markets=(market_info.keys())
# selection=input('Seleccione el mercado que desea operar, operación a realizar y monto, separados por espacio: ')
createmarket(markets, api_key, api_secret)



# print(market_info['ltc-btc']['message'])


# for info in market_info:
#     print(info ,':',type(info),'\n \n')



# try:
#     btc_cop.order_cycle('Bid', 595)
# except:
#     print('Tuvimos un error, procederé a volverlo a intentar')
#     btc_clp.order_cycle('Bid', 595)

