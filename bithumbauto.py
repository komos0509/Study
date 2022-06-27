import pybithumb
import datetime
import time

with open('bithumb.txt') as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)


def get_target_price(ticker):
    df = pybithumb.get_candlestick(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = pybithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw/float(sell_price)
    bithumb.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)
   
def get_yesterday_ma5(ticker):
    df = pybithumb.get_candlestick(ticker)
    close = df['close']
    ma5 = close.rolling(window=5).mean()
    return ma5[-2]
    
now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_ma5('BCH')
target_price = get_target_price('BCH')

while True:
    while True:
        current_price = pybithumb.get_current_price('BCH')
        print(current_price)
        time.sleep(60)
        if pybithumb.get_current_price('BCH') >= current_price:
            print(pybithumb.get_current_price('BCH'))
            buy_crypto_currency('BCH')
        else:
            sell_crypto_currency('BCH')
            print(pybithumb.get_current_price('BCH'))
            break   
