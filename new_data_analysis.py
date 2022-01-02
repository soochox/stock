import sys
import numpy as np
import FinanceDataReader as fdr
from pandas import DataFrame
from talib import abstract
from talib.abstract import *
import pandas as pd
import talib as ta


class baek_data_analysis():

    def data_download_(self, name, start_x):   #주가정보 가져오기
        # 현대차(005380) 2018년도부터 현재까지 주가 정보를 가져온다.
        df = fdr.DataReader(name, start_x)
        df_dataframe = DataFrame(df)
        cl = df["Close"].values

        return cl

    def moving_avrg(self):
        df = self.data_download_("005380", "2018")

        pd_MA = ta.MA(df['Close'], timeperiod=5)

        print(pd_MA.head())

    def bband_(self):
        cl = self.data_download_("005380", "2018")
        bbands10 = pd.Series(ta.BBANDS(cl, timeperiod=20, nbdevup=2, nbdevdn=2))  # 밴드는 또 Series를 만들었다가
        df['bbands10_up'] = bbands10[0]  # 하나씩 일일이 인덱싱해줘야 함.
        df['bbands10_mov'] = bbands10[1]
        df['bbands10_down'] = bbands10[2]
        print(df['bbans10_down'])

if __name__ == "__main__":

    baek_data_ = baek_data_analysis()
    name = "005380"
    start_x = "20161020"

    #baek_data_.data_download_(name, start_x)
    baek_data_.bband_()
