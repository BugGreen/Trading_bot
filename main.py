from calls import PrivateCalls

api_key = 'f9ed00f004950c465f25f063602d4b12'
# '04296e6396ee7bf618adb9f3ea0bb171'
api_secret = 'OXMU46wu6EX4Nbv/0kEJyNTGMlW36zTMknvFd64L'
# 'kUm9a+lyeCSnr/7JaHtH+n3VGNHyD5zJ9T8xLtzF'

btc_cop = PrivateCalls('btc', 'cop', api_key, api_secret)
btc_clp = PrivateCalls('btc', 'clp', api_key, api_secret)

btc_cop.order_cycle('Bid', 3000)
