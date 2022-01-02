import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
import win32com.client
import talib as ta
from talib import abstract
from PyQt5.QtCore import *
import numpy as np
import matplotlib.pyplot as plt
import FinanceDataReader as fdr

import time
import datetime
import pandas as pd
from pandas import DataFrame, Series
import sqlite3


from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

class AI_test2(QAxWidget):
    def __init__(self):
        super().__init__()

    def load_stock_data(self, name, kos):
        con = sqlite3.connect("c:/users/백/" + kos + "_data.db")
        df = pd.read_sql("SELECT * FROM " + "'" + name + "' ", con, index_col=None)

        con.close()
        return df

    def disp_moving_av(self, name, day, kos)
        df = self.load_stock_data(name, kos)
        df.sort_index(inplace=True, ascending=False)  # 인덱스 기준으로 역으로 정렬

        result=[]

        if len(df['open']) > 0:  #값이 없는것을 제외시킨다

            cl = df['close'] * 0.1 * 10
            dfma = ta.SMA(cl, day)

            result = cl/dfma

        return result

    def bband_(self, name, day, pp):
        df = self.load_stock_data(name, kos)
        df.sort_index(inplace=True, ascending=False)  # 인덱스 기준으로 역으로 정렬
        result = []

        if len(df['open']) > 0:  # 값이 없는것을 제외시킨다
            cl = df['close'] * 0.1 * 10
            bbands = pd.Series(ta.BBANDS(cl, day, pp, pp))  # 밴드는 또 Series를 만들었다가

            bbands_upR = cl / bbands[0]  # 하나씩 일일이 인덱싱해줘야 함.
            bbands30_downR = cl / bbands[2]
            bbands_width = (bbands[0] - bbands[2]) / cl

            df2 = {
                "bbands_upR" + day : bbands_upR, "bbands_downR" + day : bbands30_downR,
                "bbands_width" + day : bbands_width
            }
            result = DataFrame(df2)

        return result

    def D_N_ohlc(self, name):  # 1일~5일 ohlc확인

        self.kospi_kosdaq = self.comboBox_2.currentText()
        con = sqlite3.connect("c:/users/백/" + self.kospi_kosdaq + "_data.db")  # 기술적지표 추가된거에 추가
        # con = sqlite3.connect("c:/users/백/trace_" + self.kospi_kosdaq + ".db")   #원본에 추가(나중에 join으로 합치기)

        df = pd.read_sql("SELECT * FROM " + "'" + name + "' ", con, index_col=None)

        if len(df['open']) > 0:  # 값이 없는것을 제외시킨다

            date = df['index']
            op = df['open'] * 0.1 * 10
            cl = df['close'] * 0.1 * 10
            hi = df['high'] * 0.1 * 10
            lo = df['low'] * 0.1 * 10
            ch = df['change_ratio'] * 0.1 * 10

            D1_open_list = []
            D1_close_list = []
            D1_high_list = []
            D1_low_list = []
            D1_change_R_list = []

            D1_v10maR_list = []

            D2_open_list = []
            D2_close_list = []
            D2_high_list = []
            D2_low_list = []
            D2_change_R_list = []

            D3_open_list = []
            D3_close_list = []
            D3_high_list = []
            D3_low_list = []
            D3_change_R_list = []

            D4_open_list = []
            D4_close_list = []
            D4_high_list = []
            D4_low_list = []
            D4_change_R_list = []

            D5_open_list = []
            D5_close_list = []
            D5_high_list = []
            D5_low_list = []
            D5_change_R_list = []

            v10mar = df['vma10_R']
            for i in range(len(op)):

                if i > len(op) - 1 - 1:  # 가장 최근 데이터는 익일 정보가 없으므로 0추가 (과거 → 현재), 0부터 1을 더뺀다
                    D1_open_list.append(0)
                    D1_close_list.append(0)
                    D1_high_list.append(0)
                    D1_low_list.append(0)
                    D1_change_R_list.append(0)

                    D1_v10maR_list.append(0)

                    D2_open_list.append(0)
                    D2_close_list.append(0)
                    D2_high_list.append(0)
                    D2_low_list.append(0)
                    D2_change_R_list.append(0)

                    D3_open_list.append(0)
                    D3_close_list.append(0)
                    D3_high_list.append(0)
                    D3_low_list.append(0)
                    D3_change_R_list.append(0)
                    D4_open_list.append(0)
                    D4_close_list.append(0)
                    D4_high_list.append(0)
                    D4_low_list.append(0)
                    D4_change_R_list.append(0)
                    D5_open_list.append(0)
                    D5_close_list.append(0)
                    D5_high_list.append(0)
                    D5_low_list.append(0)
                    D5_change_R_list.append(0)

                elif i > len(op) - 2 - 1:

                    D1_open_list.append(op[i + 1])
                    D1_close_list.append(cl[i + 1])
                    D1_high_list.append(hi[i + 1])
                    D1_low_list.append(lo[i + 1])
                    D1_change_R_list.append(ch[i + 1])
                    D1_v10maR_list.append(v10mar[i + 1])

                    D2_open_list.append(0)
                    D2_close_list.append(0)
                    D2_high_list.append(0)
                    D2_low_list.append(0)
                    D2_change_R_list.append(0)

                    D3_open_list.append(0)
                    D3_close_list.append(0)
                    D3_high_list.append(0)
                    D3_low_list.append(0)
                    D3_change_R_list.append(0)
                    D4_open_list.append(0)
                    D4_close_list.append(0)
                    D4_high_list.append(0)
                    D4_low_list.append(0)
                    D4_change_R_list.append(0)
                    D5_open_list.append(0)
                    D5_close_list.append(0)
                    D5_high_list.append(0)
                    D5_low_list.append(0)
                    D5_change_R_list.append(0)

                elif i > len(op) - 3 - 1:

                    D1_open_list.append(op[i + 1])
                    D1_close_list.append(cl[i + 1])
                    D1_high_list.append(hi[i + 1])
                    D1_low_list.append(lo[i + 1])
                    D1_change_R_list.append(ch[i + 1])

                    D1_v10maR_list.append(v10mar[i + 1])

                    D2_open_list.append(op[i + 2])
                    D2_close_list.append(cl[i + 2])
                    D2_high_list.append(hi[i + 2])
                    D2_low_list.append(lo[i + 2])
                    D2_change_R_list.append(ch[i + 2])

                    D3_open_list.append(0)
                    D3_close_list.append(0)
                    D3_high_list.append(0)
                    D3_low_list.append(0)
                    D3_change_R_list.append(0)
                    D4_open_list.append(0)
                    D4_close_list.append(0)
                    D4_high_list.append(0)
                    D4_low_list.append(0)
                    D4_change_R_list.append(0)
                    D5_open_list.append(0)
                    D5_close_list.append(0)
                    D5_high_list.append(0)
                    D5_low_list.append(0)
                    D5_change_R_list.append(0)

                elif i > len(op) - 4 - 1:

                    D1_open_list.append(op[i + 1])
                    D1_close_list.append(cl[i + 1])
                    D1_high_list.append(hi[i + 1])
                    D1_low_list.append(lo[i + 1])
                    D1_change_R_list.append(ch[i + 1])
                    D1_v10maR_list.append(v10mar[i + 1])

                    D2_open_list.append(op[i + 2])
                    D2_close_list.append(cl[i + 2])
                    D2_high_list.append(hi[i + 2])
                    D2_low_list.append(lo[i + 2])
                    D2_change_R_list.append(ch[i + 2])

                    D3_open_list.append(op[i + 3])
                    D3_close_list.append(cl[i + 3])
                    D3_high_list.append(hi[i + 3])
                    D3_low_list.append(lo[i + 3])
                    D3_change_R_list.append(ch[i + 3])

                    D4_open_list.append(0)
                    D4_close_list.append(0)
                    D4_high_list.append(0)
                    D4_low_list.append(0)
                    D4_change_R_list.append(0)
                    D5_open_list.append(0)
                    D5_close_list.append(0)
                    D5_high_list.append(0)
                    D5_low_list.append(0)
                    D5_change_R_list.append(0)

                elif i > len(op) - 5 - 1:

                    D1_open_list.append(op[i + 1])
                    D1_close_list.append(cl[i + 1])
                    D1_high_list.append(hi[i + 1])
                    D1_low_list.append(lo[i + 1])
                    D1_change_R_list.append(ch[i + 1])

                    D1_v10maR_list.append(v10mar[i + 1])

                    D2_open_list.append(op[i + 2])
                    D2_close_list.append(cl[i + 2])
                    D2_high_list.append(hi[i + 2])
                    D2_low_list.append(lo[i + 2])
                    D2_change_R_list.append(ch[i + 2])

                    D3_open_list.append(op[i + 3])
                    D3_close_list.append(cl[i + 3])
                    D3_high_list.append(hi[i + 3])
                    D3_low_list.append(lo[i + 3])
                    D3_change_R_list.append(ch[i + 3])

                    D4_open_list.append(op[i + 4])
                    D4_close_list.append(cl[i + 4])
                    D4_high_list.append(hi[i + 4])
                    D4_low_list.append(lo[i + 4])
                    D4_change_R_list.append(ch[i + 4])

                    D5_open_list.append(0)
                    D5_close_list.append(0)
                    D5_high_list.append(0)
                    D5_low_list.append(0)
                    D5_change_R_list.append(0)


                else:

                    D1_open_list.append(op[i + 1])
                    D1_close_list.append(cl[i + 1])
                    D1_high_list.append(hi[i + 1])
                    D1_low_list.append(lo[i + 1])
                    D1_change_R_list.append(ch[i + 1])

                    D1_v10maR_list.append(v10mar[i + 1])

                    D2_open_list.append(op[i + 2])
                    D2_close_list.append(cl[i + 2])
                    D2_high_list.append(hi[i + 2])
                    D2_low_list.append(lo[i + 2])
                    D2_change_R_list.append(ch[i + 2])

                    D3_open_list.append(op[i + 3])
                    D3_close_list.append(cl[i + 3])
                    D3_high_list.append(hi[i + 3])
                    D3_low_list.append(lo[i + 3])
                    D3_change_R_list.append(ch[i + 3])

                    D4_open_list.append(op[i + 4])
                    D4_close_list.append(cl[i + 4])
                    D4_high_list.append(hi[i + 4])
                    D4_low_list.append(lo[i + 4])
                    D4_change_R_list.append(ch[i + 4])

                    D5_open_list.append(op[i + 5])
                    D5_close_list.append(cl[i + 5])
                    D5_high_list.append(hi[i + 5])
                    D5_low_list.append(lo[i + 5])
                    D5_change_R_list.append(ch[i + 5])

            df['D1_open'] = D1_open_list
            df['D1_close'] = D1_close_list
            df['D1_high'] = D1_high_list
            df['D1_low'] = D1_low_list
            df['D1_changeR'] = D1_change_R_list

            df['D1_v10maR'] = D1_v10maR_list

            df['D2_open'] = D2_open_list
            df['D2_close'] = D2_close_list
            df['D2_high'] = D2_high_list
            df['D2_low'] = D2_low_list
            df['D2_changeR'] = D2_change_R_list

            df['D3_open'] = D3_open_list
            df['D3_close'] = D3_close_list
            df['D3_high'] = D3_high_list
            df['D3_low'] = D3_low_list
            df['D3_changeR'] = D3_change_R_list

            df['D4_open'] = D4_open_list
            df['D4_close'] = D4_close_list
            df['D4_high'] = D4_high_list
            df['D4_low'] = D4_low_list
            df['D4_changeR'] = D4_change_R_list

            df['D5_open'] = D5_open_list
            df['D5_close'] = D5_close_list
            df['D5_high'] = D5_high_list
            df['D5_low'] = D5_low_list
            df['D5_changeR'] = D5_change_R_list
        con.close()

        return df

    def add_high_low(self, day):

        i = 0
        day_high_list = high[i:i + day]
        day_high_list.sort(reverse=True)
        print(day_high_list[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    baek_data_= baek_data_analysis2()
    baek_data_.show()
    app.exec_()

