import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
import pandas as pd
import json

with open("stock_info/alpaca_credentials.json", "r") as file:
    creds = json.load(file)

APCA_API_KEY_ID = creds['CLIENT_ID']
APCA_API_SECRET_KEY = creds['CLIENT_SECRET']

APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
APCA_API_DATA_URL = "https://data.alpaca.markets"
APCA_RETRY_MAX = 3
APCA_RETRY_WAIT = 3
APCA_RETRY_CODES = 429504

api = tradeapi.REST(APCA_API_KEY_ID, APCA_API_SECRET_KEY, APCA_API_BASE_URL, api_version='v2')


account = api.get_account()
# print(account)




def get_stock_info(ticker_symbol, start_date, end_date):
    STOCK_DATA = api.get_bars(ticker_symbol, tradeapi.TimeFrame.Day, start_date, end_date, adjustment='raw').df
    print(STOCK_DATA.head())
    STOCK_DATA.to_csv(f'stock_info/{ticker_symbol}data.csv')

get_stock_info('TSLA', "2021-09-01", "2022-03-01")

