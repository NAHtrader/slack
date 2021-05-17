import time
import pyupbit
import datetime
import requests
import pandas as pd

def bolinger_low(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute15", count=20)
    bolinger = df['close'].rolling(20).mean().iloc[-1]
    std=df['close'].rolling(20).std().iloc[-1]
    bolinger_low=bolinger-2*std
    return bolinger_low

def call_coin():
    #coin 종류 가져오기
    databox=[]
    url = 'https://api.upbit.com/v1/market/all'
    response = requests.get(url)
    datas = response.json()
    # 데이터 프레임으로 변경
    df = pd.DataFrame(datas)
    # market 기준 한화로 변경
    coins_krw = df[df['market'].str.startswith('KRW')].reset_index(drop=True)
    num_index = len(coins_krw.index)
    for i in range(0, num_index):
        empty = [coins_krw.iloc[i,0],coins_krw.iloc[i,2]]
        databox.append(empty)
    return databox

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

coin_names=pyupbit.get_tickers(fiat="KRW")

for coin in coin_names:
    bolinger=bolinger_low(coin)
    current_price = get_current_price(coin)
    if bolinger > current_price:
        print(coin+" "+str(bolinger))
    time.sleep(0.06)
