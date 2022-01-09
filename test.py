import sys

import pandas as pd
import pandas_datareader as pdr
import numpy as np
from pandas import Series, DataFrame

import sqlite3
import talib as ta
import openpyxl
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows


# 삼성전자 - 005930

def download_basic_data(code):
    start_date = '20110102'
    # data = pdr.get_data_yahoo(code + '.KS', start='20190101')
    data = pdr.naver.NaverDailyReader(code, start=start_date).read()
    date_list = []
    date_index = data.index
    for date in date_index:
        date = str(date)
        date = date[:4] + date[5:7] + date[8:10]
        date = int(date)
        date_list.append(date)

    df = pd.DataFrame(data)
    df['index'] = date_list
    df['Open'] = pd.to_numeric(df['Open'])
    df['Close'] = pd.to_numeric(df['Close'])
    df['High'] = pd.to_numeric(df['High'])
    df['Low'] = pd.to_numeric(df['Low'])
    df['Change'] = df['Close'].diff()
    df['change_ratio'] = df['Close'].pct_change()  # 변화량을 퍼센테이지로 구한다.
    df['change_ratio'] = df['change_ratio'].round(5)
    df['Volume'] = pd.to_numeric(df['Volume'])

    df.to_csv("test_005930.csv")
    return df

def download_jisu(code):
    start_date = '20110102'
    # data = pdr.get_data_yahoo(code + '.KS', start='20190101')
    data = pdr.get_data_yahoo(code, start=start_date)

    # date_list = []
    # date_index = data.index
    # for date in date_index:
    #     date = str(date)
    #     date = date[:4] + date[5:7] + date[8:10]
    #     date = int(date)
    #     date_list.append(date)

    df = pd.DataFrame(data)
    df['Change'] = df['Adj Close'].diff()
    df['change_ratio'] = df['Adj Close'].pct_change()  # 변화량을 퍼센테이지로 구한다.
    df['change_ratio'] = df['change_ratio'].round(5)

    df.to_csv("test_jisu.csv")
    return df


def add_tech(df):    #한종목의 기술적 지표 계산
    op = df['Open']
    cl = df['Close']
    shift_close = cl.shift()  # 전일 종가
    hi = df['High']
    lo = df['Low']
    vo = df['Volume']
    df['Open_R'] = (op - shift_close) / shift_close
    df['High_R'] = (hi - shift_close) / shift_close
    df['Low_R'] = (lo - shift_close) / shift_close
    df['Vol_R'] = vo.pct_change()
    df['Vol_R'] = df['Vol_R'].round(5)      # 전일 대비 거래량


    max_10_list = df['Close'].rolling(window=10).max()
    min_10_list = df['Close'].rolling(window=10).min()
    max_20_list = df['Close'].rolling(window=20).max()
    min_20_list = df['Close'].rolling(window=20).min()
    max_55_list = df['Close'].rolling(window=55).max()
    min_55_list = df['Close'].rolling(window=55).min()
    max_60_list = df['Close'].rolling(window=60).max()
    min_60_list = df['Close'].rolling(window=60).min()

    max_10_R_list = (df['Close'] - max_10_list) / max_10_list   # 10일 최고가대비 얼마나 하락했는가
    min_10_R_list = (df['Close'] - min_10_list) / min_10_list  # 10일 최저가대비 얼마나 상승했는가

    max_20_R_list = (df['Close'] - max_20_list) / max_20_list
    min_20_R_list = (df['Close'] - min_20_list) / min_20_list

    max_55_R_list = (df['Close'] - max_55_list) / max_55_list
    min_55_R_list = (df['Close'] - min_55_list) / min_55_list

    max_60_R_list = (df['Close'] - max_60_list) / max_60_list
    min_60_R_list = (df['Close'] - min_60_list) / min_60_list


    df['max_10_R'] = max_10_R_list
    df['max_10_R'] = df['max_10_R'].round(5)
    df['min_10_R'] = min_10_R_list
    df['min_10_R'] = df['min_10_R'].round(5)
    df['max_20_R'] = max_20_R_list
    df['max_20_R'] = df['max_20_R'].round(5)
    df['min_20_R'] = min_20_R_list
    df['min_20_R'] = df['min_20_R'].round(5)
    df['max_55_R'] = max_55_R_list
    df['max_55_R'] = df['max_55_R'].round(5)
    df['min_55_R'] = min_55_R_list
    df['min_55_R'] = df['min_55_R'].round(5)
    df['max_60_R'] = max_60_R_list
    df['max_60_R'] = df['max_60_R'].round(5)
    df['min_60_R'] = min_60_R_list
    df['min_60_R'] = df['min_60_R'].round(5)
    #
    # # 열순서 정렬
    # df = df[['name', 'Open', 'High', 'Low', 'Close', 'Volume', 'Change', 'change_ratio', 'Open_R',
    #          'High_R', 'Low_R', 'Vol_R', 'atr20(N)', 'vma20_R', 'dp_ma3', 'dp_ma5', 'dp_ma10', 'dp_ma20',
    #          'dp_ma60', 'bbands_width', 'bong', 'N20_R', 'd1_open', 'd1_high', 'd1_low', 'd1_close',
    #          'd1_open_R', 'd1_high_R', 'd1_low_R', 'd1_close_R',
    #          'd2_open', 'd2_high', 'd2_low', 'd2_close', 'd2_open_R', 'd2_high_R', 'd2_low_R', 'd2_close_R',
    #          'max_10_R', 'min_10_R', 'max_20_R', 'min_20_R', 'max_55_R', 'min_55_R', 'max_60_R', 'min_60_R']]

    return df

def buy_sell(df):
    close_list = df.Close
    position = 0
    position_list = []
    order_list = []

    buy_type = 0
    buy_type_list = []
    buy_price = 0
    buy_price_list = []
    sell_price = 0
    sell_price_list = []
    open_profit = 0
    open_profit_list =[]
    close_profit = 0
    close_profit_list = []
    winnloss = 0
    winnloss_list = []

    # stop_loss_price_list = np.zeros(len(close_list))  # 나중에 추가할 것

    max_20_list = df.max_20_R
    max_55_list = df.max_55_R
    min_10_list = df.min_10_R
    min_20_list = df.min_20_R

    for i, close in enumerate(close_list):
        max_20 = max_20_list.iloc[i]
        max_55 = max_55_list.iloc[i]
        min_10 = min_10_list.iloc[i]
        min_20 = min_20_list.iloc[i]

        if max_20 == 0 and winnloss == 0 and position == 0:  # S1 신규매입 조건 : 20일 신고가, 직전거래에서 손해시(winnloss == 0)
            order = 1
            order_list.append(order)
            position = 1
            position_list.append(position)
            buy_type = "S1"
            buy_type_list.append(buy_type)

            buy_price = close
            buy_price_list.append(buy_price)
            sell_price = 0
            sell_price_list.append(sell_price)
            open_profit = 0
            open_profit_list.append(open_profit)
            close_profit = 0
            close_profit_list.append(close_profit)
            winnloss = 0
            winnloss_list.append(winnloss)

        # if max_20 == 0 and N != None and N_ratio > 0.01 and ma60 != None and ma60 > 1 and winnloss == 0 and position == 0:
        # S1 신규매입 조건 : 20일 신고가, 직전거래에서 손해시(winnloss == 0), N은 최소 2%이상 --- S1 적용, 60이평 위
        # if max_20 == 0 and N != None and N_ratio > 0.01 and winnloss == 0 and position == 0:
        #     # S1 신규매입 조건 : 20일 신고가, 직전거래에서 손해시(winnloss == 0), N은 최소 2%이상 --- S1 적용, 60이평 조건 제거

        elif max_55 == 0 and winnloss == 1 and position == 0:    # S1 신규매입 조건 : 20일 신고가, 직전거래에서 수익시(winnloss == 1)

            # elif max_55 == 0 and N != None and N_ratio > 0.01 and ma60 != None and ma60 > 1 and winnloss == 1 and position == 0:
            # S2 매수조건 진입, 60이평 위 조건 추가
            # elif max_55 == 0 and N != None and N_ratio > 0.01 and winnloss == 1 and position == 0:
            #     # S2 매수조건 진입, 60이평 위 조건 제거
            order = 1
            order_list.append(order)
            position = 1
            position_list.append(position)
            buy_type = "S2"
            buy_type_list.append(buy_type)
            buy_price = close
            buy_price_list.append(buy_price)
            sell_price = 0
            sell_price_list.append(sell_price)
            open_profit = 0
            open_profit_list.append(open_profit)
            close_profit = 0
            close_profit_list.append(close_profit)
            winnloss = 1
            winnloss_list.append(winnloss)

        # elif position == 1 and close < stoploss_price:  # 손절(종가기준)
        #     order = -1
        #     order_list.append(order)
        #     position = 0
        #     position_list.append(position)
        #
        #     close_profit = close - buy_price
        #
        #     buy_price = 0
        #     buy_price_list.append(buy_price)
        #     sell_price = close
        #     sell_price_list.append(sell_price)
        #     open_profit = 0
        #     open_profit_list.append(open_profit)
        #
        #     close_profit_list.append(close_profit)
        #     if close_profit > 0:
        #         winnloss = 1
        #     else:
        #         winnloss = 0
        #     winnloss_list.append(winnloss)

        elif min_10 == 0 and buy_type == "S1" and position == 1:  # S1 청산 조건 : 종가기준 10일 최저가 하향 돌파
            order = -1
            order_list.append(order)
            position = 0
            position_list.append(position)

            buy_type_list.append(buy_type)
            buy_type = 0

            close_profit = close - buy_price

            buy_price = 0
            buy_price_list.append(buy_price)
            sell_price = close
            sell_price_list.append(sell_price)
            open_profit = 0
            open_profit_list.append(open_profit)

            close_profit_list.append(close_profit)
            if close_profit > 0:
                winnloss = 1
            else:
                winnloss = 0
            winnloss_list.append(winnloss)

        elif min_20 == 0 and buy_type == "S2" and position == 1:  # S2 청산 조건 : 종가기준 20일 최저가 하향 돌파
            order = -1
            order_list.append(order)
            position = 0
            position_list.append(position)
            buy_type_list.append(buy_type)
            buy_type = 0

            close_profit = close - buy_price

            buy_price = 0
            buy_price_list.append(buy_price)
            sell_price = close
            sell_price_list.append(sell_price)
            open_profit = 0
            open_profit_list.append(open_profit)

            close_profit_list.append(close_profit)
            if close_profit > 0:
                winnloss = 1
            else:
                winnloss = 0
            winnloss_list.append(winnloss)

        else:
            order = 0
            order_list.append(order)
            position_list.append(position)
            buy_type_list.append(buy_type)
            buy_price_list.append(buy_price)
            sell_price = 0
            sell_price_list.append(sell_price)
            if position == 1:
                open_profit = close - buy_price
                open_profit_list.append(open_profit)
            else:
                open_profit = 0
                open_profit_list.append(open_profit)
            close_profit = 0
            close_profit_list.append(close_profit)
            winnloss_list.append(winnloss)

    df['order'] = order_list
    df['position'] = position_list
    df['buy_type'] = buy_type_list
    df['buy_price'] = buy_price_list
    df['open_profit'] = open_profit_list
    df['close_profit'] = close_profit_list
    df['winnloss'] = winnloss_list
    df['cum_profit'] = df['close_profit'].cumsum() + df['open_profit']  # 누적 수익
    print(df)
    df.to_csv("test2222222222.csv")





# tickers = ['^KS11', '^KQ11']  # 코스피, 코스닥
try:
    data = pd.read_csv("test_005930.csv")
    print("File is founded, load data...")

except FileNotFoundError:
    code = '005930' # 삼성전자
    print("File is Not founded, download data...")
    data = download_basic_data(code)

try:
    data_jisu = pd.read_csv("test_jisu.csv")
    print("File is founded, load data...")

except FileNotFoundError:
    code = '^KS11'  # 코스피
    print("File is Not founded, download data...")
    data_jisu = download_jisu(code)

data2 = add_tech(data)
buy_sell(data2)
print('test')

# 데이터 합병
# data_jisu2 = pd.DataFrame()
# data_jisu2['Date'] = data_jisu['Date']
# data_jisu2['kospi close'] = data_jisu['Adj Close']
# data_jisu2['kospi change_r'] = data_jisu['change_ratio']
# print(data_jisu2)
# df_merge = pd.merge(data, data_jisu2, how='left', on='Date')
#
# print(df_merge)
# df_merge.to_csv("final_data.csv")
#
# df = add_tech(data)






