import time
import pyupbit
import datetime
import requests
import pandas as pd

access = "access key"
secret = "secret key"
myToken = "Token"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def bolinger_low(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute15", count=20)
    bolinger = df['close'].rolling(20).mean().iloc[-1]
    std=df['close'].rolling(20).std().iloc[-1]
    bolinger_low=bolinger-2*std
    return bolinger_low

def price_gap(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute15", count=20)
    std = df['close'].rolling(20).std().iloc[-1]
    return std


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

coin_names=pyupbit.get_tickers(fiat="KRW")
# 로그인
upbit = pyupbit.Upbit(access, secret)
print("Alarm start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#bolinger", "Alarm start")

while True:
    try:
        min = datetime.datetime.now().minute
        sec = datetime.datetime.now().second
        # post_message(myToken, "#bolinger", "Checking")
        if min%15==0 and sec==2:
            post_message(myToken, "#bolinger", "Checking")
            for coin in coin_names:
                bolinger= bolinger_low(coin)
                current_price=get_current_price(coin)
                if bolinger>current_price:
                    gap=price_gap(coin)
                    percent_test=(current_price-bolinger)/gap
                    percent=round(percent_test,2)
                    post_message(myToken, "#bolinger", coin+" [gap : " +str(percent)+"% ] ")
                time.sleep(0.1)

    except Exception as e:
        print(e)
        post_message(myToken,"#bolinger", e)
        time.sleep(1)