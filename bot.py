from urllib import response
from setter import ONE_ETH
from uniswap import Uniswap
import requests
from requests import Request, Session

infura_url = 'https://mainnet.infura.io/v3/757b2b9233fa40578c2b0ddeda1038c3'
def get_url(address, privatekey):
    uniswap_wrapper = Uniswap(address, privatekey, infura_url, version=2)
    return uniswap_wrapper

def get_price_of_currency(symbol):
    sym = symbol.upper()
    coinbase_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    coinbase_params = {
        'symbol': sym,
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
        currdata = data[symbol]
        pricedata = currdata['quote']
        usdprice = pricedata['USD']
        currprice = int(usdprice['price'])
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return currprice

def gas_price(symbol):
    sym = symbol.lower()
    gaspriceurl = f'https://owlracle.info/{sym}/gas'
    gaslimit = 250000
    TO_GWEI = 10**10
    gas = int(requests.get(gaspriceurl).json()['speeds'][3]['gasPrice'])
    print('The price of {} is {} USD'.format(symbol, currprice))
    gasprice = (int(gas) / (TO_GWEI)) * currprice * gaslimit
    print('Estimated max gas price (USD) = {}'.format(str(gasprice)))


def main():
    metamask_address = input("Enter your wallet Address : ")
    private_key = input("Enter your private key : ")
    get_url(metamask_address, private_key)

    token = input("Enter the base token you want to track : (Enter its short form)")
    currprice = get_price_of_currency(token)
    gas_price(token)

    traded_token, traded_token_name = input("Enter the token address you want to trade and its name separated by a comma").split()) 

    AMOUNT_CURR = 1
    ONE_UNIT_CURR = 1 * 10 ** 18
    


