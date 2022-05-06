from uniswap import Uniswap
import requests
from requests import Request, Session

metamaskvar = '0xE82cC7e4505a076EE6a582F947bC3237B6C5146c'
privatekeyvar = '09ecdeabd3df6f0dc7cf2e5d2dba7d6c4e636a04991b91c28485c8794bf7faa8'
infura_url = 'https://mainnet.infura.io/v3/757b2b9233fa40578c2b0ddeda1038c3'

uniswap_wrapper = Uniswap(metamaskvar, privatekeyvar, infura_url, version=2)

# coinmarketcap coin quotes call
coinbase_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
coinbase_params = {
    'symbol': 'ETH',
    'convert': 'USD'
}
coinbase_headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'd87bdff3-1750-457f-8056-8e83f70f7c28'
}

session = Session()
session.headers.update(coinbase_headers)

try:
    response = session.get(coinbase_url, params=coinbase_params).json()
    data = response['data']
    ethdata = data['ETH']
    pricedata = ethdata['quote']
    usdprice = pricedata['USD']
    ethprice = int(usdprice['price'])
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

gaspriceurl = 'https://owlracle.info/eth/gas'

gaslimit = 250000
TO_GWEI = 10**10


gas = int(requests.get(gaspriceurl).json()['speeds'][3]['gasPrice'])
print(gas)
print('gas in gwei = {}'.format(str(int(gas) /10)))

# print(type(TO_GWEI))
# print(type(ethprice))
# print(type(gas))
# print(type(gaslimit))


print('The price of Ethereum is {} USD'.format(ethprice))
gasprice = (int(gas) / (TO_GWEI)) * ethprice * gaslimit
print('Estimated max gas price (USD) = {}'.format(str(gasprice)))


"""Trading part"""
bat = "0x0D8775F648430679A709E98d2b0Cb6250d2887EF"
eth = "0x0000000000000000000000000000000000000000"

"""To query the ethereum balance of the user that wants to make the swap, and also the bat balance.
How many BAT one ETH will purchase on uniswap"""

ONE_ETH = 1 * 10 ** 18
AMOUNTETH = 1

print("ETH balance in metamask = {}".format(uniswap_wrapper.get_eth_balance()/ONE_ETH))
print("BAT balance in metamask = {}".format(uniswap_wrapper.get_token_balance(bat)))
# print('How many BAT will 1 ETH purchase on uniswap = {}'.format(uniswap_wrapper.get_token_eth_output_price(bat, AMOUNTETH)))

print('How many BAT will 1 ETH purchase on uniswap = {} BAT tokens'.format(uniswap_wrapper.get_price_output(eth, bat, ONE_ETH)))

print('Price of purchase (USD) = {}'.format(str(AMOUNTETH*ethprice)))

"""Make a trade"""
# tx = uniswap_wrapper.make_trade_output(eth,bat, AMOUNTETH)
# print(tx)
