from calls import PrivateCalls
from public_calls import jprint
from calls import get_market_info, createmarket
import re
api_key = 'f9ed00f004950c465f25f063602d4b12'

# 'c7d404858e32e7b511d3382bd94b93ec'
# 'f9ed00f004950c465f25f063602d4b12'
api_secret = 'OXMU46wu6EX4Nbv/0kEJyNTGMlW36zTMknvFd64L' # PUESTA LLAVE Y SECRETO DE DAGO

# 'p/xY2gk6bqg+FZ01U8AGxmC7rzzNTI0oor9OJmyl'
# 'OXMU46wu6EX4Nbv/0kEJyNTGMlW36zTMknvFd64L'
#_______________________________________________________________________
market_info= get_market_info(api_key,api_secret)



markets=(market_info.keys())
gain=float(input('Digite la ganancia tentativa en %: '))
createmarket(markets, api_key, api_secret,gain=gain,Sound=True)

#btc_cop=PrivateCalls('btc', 'cop', api_key, api_secret)