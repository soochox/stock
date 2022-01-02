import sys
from PyQt5.QtWidgets import *
import Kiwoom
import get_code_list
import time
import pandas as pd
from pandas import DataFrame, Series
import sqlite3
import datetime

class PyMon:
    def __init__(self):
        self.kiwoom = Kiwoom.Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()


    def get_code_list(self):   #키움증권 온라인 전용
        self.kospi_codes = self.kiwoom.get_code_list_by_market(["0"])
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(["10"])

    def get_ohlcv(self, code, start):  #키움증권 온라인 전용
        self.kiwoom.ohlcv = {"date":[],"open":[],"high":[],"low":[],"close":[],"volume":[]}
        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(0.2)

        df = DataFrame(self.kiwoom.ohlcv, columns=["open", "high", "low", "close", "volume"], index=self.kiwoom.ohlcv["date"])
        return df



    def off_get_ohlcv(self, codename):   #파일로 부터 ohlcv가져와서 DataFrame형식을 반환, 한종목만

        con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")  # 종목 데이터 베이스

        jum = "'"
        inputstr = "SELECT * FROM " + jum + codename + jum
        df = pd.read_sql(inputstr, con, index_col="index")  # 여기서 데이터형식은 DataFrame 객체다.

        return df


    def check_speedy_rising_volume(self,name, today):
        df = self.off_get_ohlcv(name)
        vol_list = df["volume"]
        today_vol = vol_list[today]

        today_vol_MA10 = df["vol_MA10"][today]

        self.today_close = df["close"][today] #오늘의 종가

        if len(vol_list) < 10:
            return False

        if today_vol_MA10 * 4.8 > today_vol > today_vol_MA10 * 3.8:
            return True

    def getconditionload(self):   #조건식 로딩 요청
        self.dynamicCall("GetConditionLoad()")
        print("조건식 로딩 요청")

    def _receive_conditionver(self):
        print("_receive_condition")
        data = self.dynamicCall("GetConditionNameList()")   #조건식을 data에 저장
        data_list = data.split(";")                         #조건식을 ; 기준으로 쪼개서 리스트로 저장
        del data_list[-1]                                   #조건식 리스트에 마지막 빈 데이터를 제거함
        count_data = len(data_list)                         #조건식의 개수를 파악
        print(count_data, "개의 조건식이 검색되었습니다.")

        condi_dic = {}                                      #빈딕셔너리 선언

        for i in data_list:
            key, value = i.split("^")                       #조건식 번호와 이름을 ^ 기준으로 쪼개서 딕셔너리의 키와 값으로 저장
            condi_dic[int(key)] = value

        condi_name_list = list(condi_dic.values())          #조건식 이름을 따로 저장
        condi_index_list = list(condi_dic.keys())            #조건식 번호를 따로 저장

        print(condi_name_list)
        print(condi_index_list)

        #condi_num_list = [17, 18,19,20]                                      #19~21번째 조건식
        #for condi_num in condi_num_list:

        str_condi_name = str(condi_name_list[self.condi_num])    #18번째 조건식 이름
        int_condi_index = int(condi_index_list[self.condi_num])  #18번째 조건식 번호
        print(str_condi_name)
        self.sendcondition("0150", str_condi_name, int_condi_index, 0)   #조건식에 해당하는 종목을 불러오라고 요청

            #ret_send = self.dynamicCall("SendCondition(QString, QString, int, int", "0150", str_condi_name, int_condi_index,0)
            #print(ret_send)



    def sendcondition(self, strScrNo, strConditionName, nIndex, nSearch):  #조건식에 해당하는 종목을 불러오라고 요청
        ret_send = self.dynamicCall("SendCondition(QString, QString, int, int", strScrNo, strConditionName, nIndex, nSearch)
        print(ret_send)   #1이면 정상

    def _receivetrcondition(self, strScrNo, strCodeList, strConditionName, nIndex, nNext):
        print("조건식 번호", self.condi_num)

        if self.condi_num == 17:   #처음이면
            self.final_code_list = []

        if strCodeList == "":
            print("조건식에 부합하는 종목이 없습니다.")

        else:
            codelist = strCodeList.split(";")
            del codelist[-1]

            if len(self.final_code_list) == 0:  #첫번째 쓰는 거면
                self.final_code_list = codelist
            else:
                self.final_code_list = self.final_code_list+codelist

            print(codelist)
            print("종목개수: ", len(codelist))

        if self.condi_num == 20: #마지막 조건식이면 쓴다.
            self.final_code_list = set(self.final_code_list)  #중복제거
            self.final_code_list = list(self.final_code_list)  #중복제거
            all_code = self.kospi_and_kosdaq_code_load()   #코드와 종목명 불러오기
            final_namelist = []
            for code in self.final_code_list:
                final_namelist.append(all_code[code])   #거래 종목의 종목명 구하기
            print(final_namelist)
            buy_quantity = "계산전"

            f = open("buy_list.txt", "wt")
            for i, code in enumerate(self.final_code_list):
                name = final_namelist[i]
                f.writelines("%s;매수;%s;시장가;%s;0;매수전\n" % (name, code, buy_quantity))
            f.close()
            self.condi_num = 17  # 초기화
        else:
            #self.getcondition_ = True  #이거 삭제할지 확인필요
            self.condi_num = self.condi_num+1      #다음조건식으로
            self.getconditionload()

    def update_buy_list(self, buy_code_list, buy_name_list):
        day_money = 10000000 #1일 최대 투자금액 1000만원
        one_stock_money = int(day_money / self.buy_list_len)
        print(one_stock_money)

        f = open("buy_list.txt", "wt")
        for i, code in enumerate(buy_code_list):
            name = buy_name_list[i]
            close = self.buy_close_list[i]  #살종목의 오늘 종가

            if len(code) > 6:   ##대신증권 코드에서 키움증권코드로 고치기(맨앞에 A를 제거)
                code = code[1:7]
            buy_quantity = int(one_stock_money / close)   #매수 수량
            f.writelines("%s;매수;%s;시장가;%s;0;매수전\n" %(name, code, buy_quantity))
        f.close()

    # --------------아래부터 대신증권 전용-----------------------------------
    def DS_offline_code_load1(self):  #코스닥 코드 정보 로딩
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 종목 데이터 베이스
        jum = "'"
        inputstr = "SELECT * FROM " + jum + "kosdaq" + jum
        df = pd.read_sql(inputstr, con, index_col="index")  # 여기서 데이터형식은 DataFrame 객체다.

        return df


    def off_code_to_name(self, code):
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 코드 데이터 베이스
        codedata = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")
        codelist = codedata["code"]
        namelist = codedata["name"]
        for i, codee in codelist:
            if codee == code:
                serch_name = namelist[i]
                break
        return serch_name

    #------------------------------------------------
    def Today_buy_list(self):
        code_data = self.DS_offline_code_load1()
        name_list = code_data["name"]
        code_list = code_data["code"]
        #today = datetime.datetime.today().strftime("%Y%m%d")
        today = 20190315
        buy_list = []
        buy_name_list = []

        self.buy_close_list = []  #살종목의 종가

        for i, name in enumerate(name_list):
            print(i, "/", len(name_list), name)
            if self.check_speedy_rising_volume(name, today):
                code = code_list[i]
                buy_name_list.append(name)
                buy_list.append(code)

                self.buy_close_list.append(self.today_close)  # 오늘종가 기록

        print(buy_name_list)
        self.buy_list_len = len(buy_list)    #살 종목 수
        self.update_buy_list(buy_list, buy_name_list)


    def run(self):
        print(self.kospi_codes[0:4])
        print(self.kosdaq_codes[0:4])



if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    pymon.run()
