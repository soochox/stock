import pandas as pd

Damage = pd.DataFrame({
    'name': ['히드라', '저글링', '질럿', '커세어', '마린', '벌처'],
    'race': ['Zerg', 'Zerg', 'protoss', 'protoss', 'terran', 'terran'],
    'damage': [10, 5, 16, 5, 6, 20]
})
print(data)


# import pandas_datareader as pdr
#
# code = '002800'
# ticker = code + '.KQ'       # 코스닥 KQ, 코스피 KS
# df = pdr.get_data_yahoo(ticker)
# df['change'] = df['Adj Close'].diff()
# df['close2'] = df['Adj Close'].shift()
# df['change_R'] = df['change'] / df['close2']
# df['change_R2'] = df['Adj Close'].pct_change()
#
# print(df[['change', 'Adj Close', 'close2', 'change_R', 'change_R2']])
#


# # import telepot
# import telegram
#
# TOKEN = '1968085479:AAEck4QaWFrY9Bl7tNKRaqF3lNe0dIrr3Kg'
# mc = '1956916092'
# bot = telegram.Bot(TOKEN)
# bot.sendMessage(mc, "으르렁")

# import pandas_datareader as pdr
# df = pdr.get_data_yahoo('^KS11', start='20180101')   # ^KS11 코스피 지수
# # df = pdr.naver.NaverDailyReader('005930', start='20200101', end='20201231').read()
# print(df)


# import pyupbit as ub
# import sqlite3
# import pandas as pd
# import numpy as np
#
#
#
# def save_ticker():
#     tickers = ub.get_tickers()
#     df = pd.DataFrame(tickers)
#     df.rename(columns={0: 'ticker'}, inplace=True)
#
#     con = sqlite3.connect("c:/users/백/tickers.db")
#     df.to_sql("tickers", con, if_exists="replace")
#     con.close()
#
# def load_ticker():
#     con = sqlite3.connect("c:/users/백/tickers.db")
#     data = pd.read_sql("SELECT * FROM 'tickers'", con, index_col='index')
#     con.close()
#     ticker_list = data['ticker']
#     ticker_list = list(ticker_list)
#     return ticker_list
#
#
# def download_ohlc():
#     ticker_list = load_ticker()
#
#     con = sqlite3.connect("c:/users/백/coin_data.db")
#     for i, ticker in enumerate(ticker_list):
#         ticker_krw = ticker[:3]
#
#         if ticker_krw == 'KRW':
#             df = ub.get_ohlcv(ticker)
#             df.to_sql(ticker[4:], con, if_exists="replace")
#     con.close()
#
#
# def merge_data():  # 모든 데이터 한테이블 통합
#
#     ticker_list = load_ticker()
#     coin_name_list = []
#
#     for full_ticker in ticker_list:
#         krw_btc_ticker = full_ticker[:3]
#         if krw_btc_ticker == 'KRW':
#             coin_name_list.append(full_ticker[4:])
#
#     file = "c:/users/백/coin_data.db"
#
#     con = sqlite3.connect(file)  # 키움증권 다운로드 종목 데이터 베이스
#     # c = con.cursor()
#
#     # df = pd.read_sql("SELECT * FROM 'ADA'", con)
#     # df['name'] = "ADA"
#     # df_result = df.head(0)
#     # df_result.to_sql("통합", con, if_exists="replace")
#
#     date_name_list = []
#     df_result = pd.DataFrame()
#
#     for i, coin_name in enumerate(coin_name_list):      # 뺑뺑이 돌리기
#
#         print("%d / %d %s 진입" % (i, len(coin_name_list), coin_name))
#         df_coin = pd.read_sql("SELECT * FROM " + "'" + coin_name + "'", con, index_col=None)
#         df_coin['date'] = df_coin['index']
#         df_coin.drop("index", axis=1, inplace=True)  # axis=1 은 열을 의미한다.
#         for k, date in enumerate(list(df_coin['date'])):
#
#             date = date[:11]
#             date_name = date + coin_name
#             date_name_list.append(date_name)
#         print(len(df_coin['open']))
#         print(len(date_name_list))
#         df_coin['date_name'] = date_name_list
#         date_name_list = []
#
#
#         if i == 0:
#             df_result = df_coin
#
#         else:
#             df_result = df_result.append(df_coin)
#
#     # df_result.set_index('date_name', inplace=True)
#     print(df_result)
#     df_result.to_sql("통합", con, if_exists="replace")
#
#     con.close()
#
#
# merge_data()







## pandas 공부
# https://blog.naver.com/suwonleee/222429079610

# import pandas as pd
#
# df = pd.read_csv('C:/Users/백/무한도전.csv', encoding='cp949', index_col=0)
# print(df)

# 특정 셀의 데이터 수정

# # 1. a.loc 이용: 원하는 행,열의 이름을 직접 입력해주는 경우
# b = df.loc['하하', '별명']
# print(b)

# # 2. a.iloc 이용: 데이터프레임의 인덱스 번호를 입력해주는 경우
# df.iloc[1, 4] = "마포구 보안관"
# b = df.loc['하하', '별명']
# print(b)


# # 열 전체를 수정
# df['출생년월'] = ['1972년', '1979년','1979년','1970년','1971년','1978년','1980년','1978년',]

# # 행전체를 수정
# df.loc['노홍철'] = ['1979년', '5개', 'Yes', '180', '노찌롱']
# print(df)
#
# # 새로운 행데이터 추가
# hkh_df = [1988, '4개', 'Yes', 175, '종이인형']
# df.loc[len(df)] = hkh_df            # 최하단에 새로운 행추가
# print(df)                           # 인덱스 값이 없으므로 인덱스는 8로 출력된다.
# df.rename(index={8: '황광희'}, inplace=True)       # 행이름 변경(index)
# print(df)
#
# df.rename(columns={'별명': '별명(A.K.A)'}, inplace=True)
# print(df)

# 프로퍼티 사용하기
# https://dojang.io/mod/page/view.php?id=2476

# 1. 아랫 부분을 @property를 사용하여 똑같이 구현할 수 있다.(getter/setter)
# class Person:
#     def __init__(self):
#         self.__age = 0
#
#     def get_age(self):            # getter
#         return self.__age
#
#     def set_age(self, value):     # setter
#         self.__age = value
#
# james = Person()
# james.set_age(20)
#
# print(james.get_age())

# @property 사용하여 구현
# class Person:
#     def __init__(self):
#         self.__age = 0
#
#     @property
#     def age(self):              # 여기가 getter 부분
#         return self.__age
#
#     @age.setter
#     def age(self, value):       # 여기가 setter 부분
#         self.__age = value
#
# james = Person()
# james.age = 20          # 인스턴스.속성 형식으로 접근하여 값 저장
# print(james.age)        # 인스턴스.속성 형식으로 값을 가져옴

# # 한줄 if문 - 작성형식: 결과 = A if 조건 else B
# cat = 'cat'
# dog = 'dog'
# ret = None
#
# animal = 'cat'
#
# if animal is dog:
#     ret = dog
# else:
#     ret = cat
# print("첫번째", ret)
#
# ret = dog if animal is dog else cat
# print("두번재", ret)


# 열거형: 변수가 가질수 있는 값들을 미리 열거 해놓은 자료형
# 예를 들어 일주일은 월화수목금토일 만 있으면 되고 1년은 1월부터 12월까지만 있으면 된다.


