import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

import time
import datetime
import pandas as pd
import win32com.client
from pandas import DataFrame, Series
import sqlite3
import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

class Kiwoom(QAxWidget):

    def __init__(self):   #초기화
        super().__init__()
        #self.day_money = 10000000  # 1일 최대 투자금액 1000만원
        self.getcondition_ = False
        self._creat_kiwoom_instance()
        self._set_signal_slots()   #OnReceive계열을 실행시킴
        self.condi_num = 17  # 18번째 조건식

    def codeNname_load(self, kospi_kosdaq):

        file = openpyxl.load_workbook("c:/users/백/DS_codedata.xlsx")

        sheet = file.get_sheet_by_name(kospi_kosdaq)  # 인자 받는 부분 나중에 수정할 것, 앞으로 지원하지 않는 기능임
        code_list = []
        name_list = []
        index_list = []

        for r in sheet.rows:
            index_list.append(r[0].value)
            code_list.append(r[1].value)
            name_list.append(r[2].value)

        codeNname = {"index": index_list, "code": code_list, "name": name_list}

        df = DataFrame(codeNname)
        return df


        #self.OnReceiveChejanData.connect(self._receive_chejan_data) # 여기 맞겠지?

    def _creat_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)
        self.OnReceiveConditionVer.connect(self._receive_conditionver)
        self.OnReceiveTrCondition.connect(self._receivetrcondition)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString,QString)", trcode, rqname)
        return ret

    #로그인 정보 얻기
    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def get_connect_state(self):   #접속상태를 알려주는 함수, 서버연결시 1을 토해낸다.
        ret = self.dynamicCall("GetConnectState()")
        return ret


    #주문하기
    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString,QString,QString, int, QString, int, int, QString, QString)", [rqname,
                        screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    #주문 체결결과 가져오기
    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    #체결되었을때 주문결과 가져오기
    def _receive_chejan_data(self,gubun, item_cnt, fid_list):
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString,QString,int,QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()


    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == "2":
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":      #일봉 조회
            self._opt10081(rqname, trcode)

        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)

        elif rqname == "opw00018_req":
            self._opw00018(rqname, trcode)

        elif rqname == "opt10075_req":    #실시간 미체결 요청
            self._opt10075(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def get_code_list_by_market(self, market):           #코드리스트 정보요청
        code_list = self.dynamicCall("GetCodeListByMarket(QSting)", market)
        code_list = code_list.split(";")
        return code_list[:-1]

    def get_master_code_name(self, code):      #코드를 입력했을 때 종목명을 뱉는다.
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def code_and_name(self):    #코드와 종목명 갱신
        code_and_name = {"soonbun":[],"code":[],"name":[]}

        #코스피
        for i, code in enumerate(self.get_code_list_by_market(["0"])):
            code_name = self.get_master_code_name(code)
            code_and_name["soonbun"].append(i)
            code_and_name["code"].append(code)
            code_and_name["name"].append(code_name)

        df = pd.DataFrame(code_and_name, columns=["code","name"], index=code_and_name["soonbun"])
        con = sqlite3.connect("c:/users/백/KW_code_and_name.db")      #데이터베이스에 저장
        df.to_sql("코스피", con, if_exists="replace")
        print("코스피 완료")

        code_and_name = {"soonbun":[],"code":[],"name":[]}

        #코스닥
        for i, code in enumerate(self.get_code_list_by_market(["10"])):
            code_name = self.get_master_code_name(code)
            code_and_name["soonbun"].append(i)
            code_and_name["code"].append(code)
            code_and_name["name"].append(code_name)

        df = pd.DataFrame(code_and_name, columns=["code","name"], index=code_and_name["soonbun"])
        con = sqlite3.connect("c:/users/백/KW_code_and_name.db")
        df.to_sql("코스닥", con, if_exists="replace")
        print("코스닥 완료")

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString,QString)", id, value)


    def get_ohlcv(self, code, start):   #일봉정보 얻기
        self.ohlcv = {"date":[],"open":[],"high":[],"low":[],"close":[],"volume":[]}
        self.set_input_value("종목코드", code)
        self.set_input_value("기준일자", start)
        self.set_input_value("수정주가구분", 1)
        self.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(0.6)

    def save_ohlcv(self, code, start):
        self.get_ohlcv(code, start)

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString,QString,QString,int,QString)", code, real_type, field_name, index,
                               item_name)
        return ret.strip()   #strip() == 공백제거

    def _opt10075(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            time_ = self._comm_get_data(trcode, "", rqname, i, "시간")
            name = self._comm_get_data(trcode, "", rqname, i, "종목명")
            sell_buy = self._comm_get_data(trcode, "", rqname, i, "매매구분")
            michegyul_ = self._comm_get_data(trcode, "", rqname, i, "미체결수량")
            won_jumun = self._comm_get_data(trcode, "", rqname, i, "원주문번호")
            quantity_ = self._comm_get_data(trcode, "", rqname, i, "주문수량")
            gagyuk = self._comm_get_data(trcode, "", rqname, i, "주문가격")

            self.michegyul["시간"].append(time_)
            self.michegyul["종목명"].append(name)
            self.michegyul["매매구분"].append(sell_buy)
            self.michegyul["미체결수량"].append(michegyul_)
            self.michegyul["원주문번호"].append(won_jumun)
            self.michegyul["주문수량"].append(quantity_)
            self.michegyul["주문가격"].append(gagyuk)

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self.ohlcv["date"].append(date)
            self.ohlcv["open"].append(int(open))
            self.ohlcv["high"].append(int(high))
            self.ohlcv["low"].append(int(low))
            self.ohlcv["close"].append(int(close))
            self.ohlcv["volume"].append(int(volume))


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


    def update_buy_qt(self, one_day_money):     #살수량 업데이트
        today = datetime.datetime.today().strftime("%Y%m%d")
        today_str = str(today)
        f = open("buy_list.txt", "rt")
        buy_list = f.readlines()
        f.close()
        buy_qt_list = []
        one_stock_money = int(one_day_money / len(buy_list))
        print("종목수:", len(buy_list))
        print("1종목 투자금액: ", one_stock_money)

        # buy list
        for row_data in buy_list:
            split_row_data = row_data.split(";")
            code = split_row_data[2]
            df = self.stock_1_ohlcv(code, today_str)            #종목 OHLCV불러오기

            df_close = list(df["close"])                        #종가 리스트
            today_df_close = df_close[0]                        #종가
            buy_qt = round(int(one_stock_money/today_df_close))        #종목 매수 수량 : 한종목 투자금액 / 종가

            buy_qt_list.append(buy_qt)
        print(buy_qt_list)


        #주문수량 입력
        for i, row_data in enumerate(buy_list):

            buy_qt2 = str(buy_qt_list[i])
            buy_list[i]=buy_list[i].replace("계산전", buy_qt2)          #계산전을 매수수량으로 교체한다.

        print(buy_list)

        #파일 업데이트
        f = open("buy_list.txt", "wt")
        for row_data in buy_list:
            f.write(row_data)
        f.close()

    def update_buy_list(self, buy_code_list):  # 대신증권 살종목 텍스트 파일 업데이트

        one_day_money = int(self.lineEdit_2.text())
        one_stock_money = int(one_day_money / len(buy_list))

        print("1일 투자금액: ", one_stock_money)

        f = open("buy_list.txt", "wt")
        for i, code in enumerate(buy_code_list):
            name = buy_name_list[i]
            close = self.buy_close_list[i]  # 살종목의 오늘 종가

            if len(code) > 6:  ##대신증권 코드에서 키움증권코드로 고치기(맨앞에 A를 제거)
                code = code[1:7]
            buy_quantity = int(one_stock_money / close)  # 매수 수량
            f.writelines("%s;매수;%s;시장가;%s;0;매수전\n" % (name, code, buy_quantity))
        f.close()

    def opt10081(self, code, date):

        self.ohlcv = {"date": [], "open": [], "high": [], "low": [], "close": [], "volume": []}
        self.set_input_value("종목코드", code)
        self.set_input_value("기준일자", date)
        self.set_input_value("수정주가구분", 1)

        self.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(0.5)

        df = pd.DataFrame(self.ohlcv, columns=["open", "high", "low", "close", "volume"],
                       index=self.ohlcv["date"])

        return df

    def opt10075(self, account , whole, sell_buy, code, chegyul):   #체결정보 조회

        self.chegyul = {"date": [], "open": [], "high": [], "low": [], "close": [], "volume": []}
        self.set_input_value("계좌번호", account)
        self.set_input_value("전체종목구분", whole)  #0:전체, 1:종목
        self.set_input_value("매매구분", sell_buy)   #0전체, 1 매도, 2 매수
        self.set_input_value("종목코드", code)     #
        self.set_input_value("체결구분", chegyul)  #0:전체, 2:체결, 1:미체결

        self.comm_rq_data("opt10075_req", "opt10075", 0, "0341")
        time.sleep(0.5)

        df = pd.DataFrame(self.michegyul, columns=["종목명", "매매구분", "미체결수량", "원주문번호", "주문수량","주문가격"],
                          index=self.ohlcv["시간"])

        return df

    def chegyul_infomation(self, acc):
        data = self.opt10075("20200319", )


    def kospi_save_ohlcv(self):
        con = sqlite3.connect("c:/users/백/KW_code_and_name.db")
        df = pd.read_sql("SELECT * FROM 코스피", con, index_col="index")
        today = datetime.datetime.today().strftime("%Y%m%d")
        todaystr = str(today)
        code_list = df["code"]

        #code_list2 = code_list[998:]
        for i, code in enumerate(code_list):
        #for i, code in enumerate(code_list2):
            down_data = self.opt10081(code, today)
            codename = self.get_master_code_name(code)
            con = sqlite3.connect("c:/users/백/stock_kospi1_" + todaystr + ".db")
            down_data.to_sql(codename, con, if_exists="replace")
            print(i, "/", len(df["code"]), "요청완료")


    def kospi_save_ohlcv2(self):
        con = sqlite3.connect("c:/users/백/KW_code_and_name.db")
        df = pd.read_sql("SELECT * FROM 코스피", con, index_col="index")
        today = datetime.datetime.today().strftime("%Y%m%d")
        todaystr = str(today)
        code_list = df["code"]

        code_list2 = code_list[998:]

        for i, code in enumerate(code_list2):
            down_data = self.opt10081(code, today)
            codename = self.get_master_code_name(code)
            con = sqlite3.connect("c:/users/백/stock_kospi1_" + todaystr + ".db")
            down_data.to_sql(codename, con, if_exists="replace")
            print(i, "/", len(df["code"]), "요청완료")

    def kosdaq_save_ohlcv(self):
        con = sqlite3.connect("c:/users/백/KW_code_and_name.db")
        df = pd.read_sql("SELECT * FROM 코스닥", con, index_col="index")
        today = datetime.datetime.today().strftime("%Y%m%d")
        todaystr = str(today)
        code_list = df["code"]
        code_list2 = code_list[998:]
        for i, code in enumerate(code_list):
        #for i, code in enumerate(code_list2):
            down_data = self.opt10081(code, today)
            codename = self.get_master_code_name(code)
            con = sqlite3.connect("c:/users/백/stock_kosdaq1_" + todaystr + ".db")
            down_data.to_sql(codename, con, if_exists="replace")
            print(i, "/", len(df["code"]), "요청완료")

    def kosdaq_save_ohlcv2(self):
        con = sqlite3.connect("c:/users/백/KW_code_and_name.db")
        df = pd.read_sql("SELECT * FROM 코스닥", con, index_col="index")
        today = datetime.datetime.today().strftime("%Y%m%d")
        todaystr = str(today)
        code_list = df["code"]
        code_list2 = code_list[998:]

        for i, code in enumerate(code_list2):
            down_data = self.opt10081(code, today)
            codename = self.get_master_code_name(code)
            con = sqlite3.connect("c:/users/백/stock_kosdaq1_" + todaystr + ".db")
            down_data.to_sql(codename, con, if_exists="replace")
            print(i, "/", len(df["code"]), "요청완료")

    def stock_1_ohlcv(self, code, day):

        down_data = self.opt10081(code, day)
        codename = self.get_master_code_name(code)
        print(code, codename, "ohlcv 다운로드 완료")

        return down_data


    def load_jongmok_data(self, codename):

        #종목 정보 불러오기
        con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")  #키움증권 다운로드 종목 데이터 베이스
        #con = sqlite3.connect("c:/users/백/DS_kosdaq_20190318.db")  #대신증권 종목 데이터 베이스

        jum = "'"
        inputstr = "SELECT * FROM " + jum + codename + jum

        self.ohlcv_kosdaq = pd.read_sql(inputstr, con, index_col="index")  #여기서 데이터형식은 DataFrame 객체다.

        #ohlcv_kosdaq = pd.read_sql("SELECT * FROM code", con, index_col="index")
        #ohlcv_kospi = pd.read_sql("SELECT * FROM 코스피", con, index_col="index")

        return self.ohlcv_kosdaq


    #코스닥 코드 엑셀파일로부터 읽기
    #def kosdaq_code_load(self):
     #   df = self.codeNname_load("kosdaq")
      #  code_list = list(df["code"])
       # name_list = list(df["name"])
        #code_name_dic = {}
        #for i, key in enumerate(code_list):
         #   code_name_dic[key] = name_list[i]
        #return code_name_dic

    #코스피 코드 엑셀파일로부터 읽기
    #def kospi_code_load(self):
     #   df = self.codeNname_load("kospi")

      #  code_list = list(df["code"])
       # name_list = list(df["name"])
        #code_name_dic = {}
        #for i, key in enumerate(code_list):
         #   code_name_dic[key] = name_list[i]
        #return code_name_dic

    #def kospi_and_kosdaq_code_load(self):
     #   T_code = self.kospi_code_load()
      #  T_code2 = self.kosdaq_code_load()
       # T_code.update(T_code2)

        #return T_code


    def kosdaq_code_load(self):
        con = sqlite3.connect("c:/users/백/KW_code_and_name.db")
        code_data = pd.read_sql("SELECT * FROM 코스닥", con, index_col="index")

        code_list = list(code_data["code"])
        name_list = list(code_data["name"])
        code_name_dic = {}
        for i, key in enumerate(code_list):
            code_name_dic[key] = name_list[i]
        return code_name_dic


    def kospi_code_load(self):
        con = sqlite3.connect("c:/users/백/KW_code_and_name.db")
        code_data = pd.read_sql("SELECT * FROM 코스피", con, index_col="index")

        code_list = list(code_data["code"])
        name_list = list(code_data["name"])
        code_name_dic = {}
        for i, key in enumerate(code_list):
            code_name_dic[key] = name_list[i]
        return code_name_dic

    def kospi_and_kosdaq_code_load(self):
        T_code = self.kospi_code_load()
        T_code2 = self.kosdaq_code_load()
        T_code.update(T_code2)

        return T_code

    def run(self):
        self.comm_connect()
        kiwoom.all_jong_bbangbbangE()
        #kiwoom.check_speedy_rising_vol(codename)
        #kiwoom.calc_ma()
        #kiwoom.load_jongmok_data(codename)
        #kiwoom.calc_ma()
        #kiwoom.save_ohlcv()
        #kiwoom.code_and_name()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.run()
    #kiwoom.save_ohlcv()

    #account_number = kiwoom.get_login_info("ACCNO")
    #account_number = account_number.split(";")[0]
    #kiwoom.set_input_value("계좌번호", account_number)
    #kiwoom.set_input_value("비밀번호", "0000")
    #kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")