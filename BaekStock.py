import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from get_code_list import *
from pandas import Series, DataFrame
import sqlite3


form_class = uic.loadUiType("BaekStock.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom = Kiwoom()
        self.today_trade_ready = False  # 주문 안함
        self.condi_load = False #조건식 로드 안함
        self.trade_stocks_done = False #주문 안함

        self.timer = QTimer(self)   #1초마다 시간을 띄우도록
        self.timer.start(1000)     #1초에 한 번 timeout 시그널이 발생함
        self.timer.timeout.connect(self.timeout)  #timeout시그널 발생시 timeout 함수로 이동

        self.pushButton.clicked.connect(self.connect_kiwoom)  #접속버튼 클릭시
        self.code_name_btn.clicked.connect(self.code_name_gaengsin)  # 코드네임갱신 버튼 클릭시
        self.kospi_down_btn.clicked.connect(self.kospi_down)  # 코스피다운 버튼 클릭시
        self.kospi_down2_btn.clicked.connect(self.kospi_down2)  # 코스피다운2 버튼 클릭시
        self.kosdaq_down_btn.clicked.connect(self.kosdaq_down)  # 코스닥다운 버튼 클릭시
        self.kosdaq_down2_btn.clicked.connect(self.kosdaq_down2)  # 코스닥다운2 버튼 클릭시

        self.pushButton_7.clicked.connect(self.auto_buy)
        self.pushButton_8.clicked.connect(self.auto_sell)

        self.pushButton_2.clicked.connect(self.getconditionload_button)  # 조건식 저장

        self.pushButton_11.clicked.connect(self.update_buy_qt_button)  # 살종목 텍스트 파일 수량 업데이트(키움)
        self.pushButton_9.clicked.connect(self.stock_1_ohlcv_button)   #한종목만 검색

        self.pushButton_10.clicked.connect(self.TestTest)    #테스트 버튼

    def connect_kiwoom(self):
        self.kiwoom.comm_connect()
        # 계좌번호 얻기
        accouns_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        accounts_list = accounts.split(";")[0:accouns_num]
        self.comboBox.addItems(accounts_list)


    #코드리스트 갱신하여 저장하기
    def code_name_gaengsin(self):
        self.kiwoom.code_and_name()

    def kospi_down(self):
        self.kiwoom.kospi_save_ohlcv()

    def kospi_down2(self):
        self.kiwoom.kospi_save_ohlcv2()

    def kosdaq_down(self):
        self.kiwoom.kosdaq_save_ohlcv()

    def kosdaq_down2(self):
        self.kiwoom.kosdaq_save_ohlcv2()

    def getconditionload_button(self):
        self.kiwoom.getconditionload()
        print("조건식 불러오기 완료")

    def chegyul_info_button(self):
        self.kiwoom.opt10075()

    def update_buy_qt_button(self):
        one_day_money = int(self.lineEdit_2.text())
        self.kiwoom.update_buy_qt(one_day_money)


    def DS_ohlcv_down(self):

        start_date = self.spinBox_2.value()

        end_date = self.spinBox_3.value()

        self.kiwoom.ds_save_ohlc(start_date, end_date)


    def auto_buy(self):
        hoga_lookup = {"지정가": "00", "시장가": "03"}

        f = open("buy_list.txt", "rt")
        buy_list = f.readlines()
        f.close()

        #계좌번호
        account = self.comboBox.currentText()

        # buy list
        for row_data in buy_list:
            split_row_data = row_data.split(";")
            hoga = split_row_data[3]  #지정가 or 시장가
            code = split_row_data[2]
            num = split_row_data[4]
            price = split_row_data[5]


            if split_row_data[-1].rstrip() == "매수전":
                self.kiwoom.send_order("send_order_req", "0101", account, 1, code, num, price, hoga_lookup[hoga],"")
                print(split_row_data[0], ": 매수 주문완료")
                time.sleep(1)

        #매도후 텍스트파일 처리

        #buy_list

        for i, row_data in enumerate(buy_list):
            buy_list[i]=buy_list[i].replace("매수전", "주문완료")

        #file update

        f = open("buy_list.txt","wt")
        for row_data in buy_list:
            f.write(row_data)
        f.close()
        print("자동 매수주문 완료")

    def auto_sell(self):
        hoga_lookup = {"지정가": "00", "시장가": "03"}

        f = open("sell_list.txt", "rt")
        sell_list = f.readlines()
        f.close()

        # 계좌번호
        account = self.comboBox.currentText()


        # sell list
        for row_data in sell_list:
            split_row_data = row_data.split(";")
            hoga = split_row_data[3]  # 지정가 or 시장가
            code = split_row_data[2]
            num = split_row_data[4]
            price = split_row_data[5]
            name = split_row_data[0]

            if split_row_data[-1].rstrip() == "매도전":
                self.kiwoom.send_order("send_order_req", "0101", account, 2, code, num, price, hoga_lookup[hoga],"")
                print(name, ": 매도 주문완료")
                time.sleep(1)

        # 매도후 텍스트파일 처리
        # sell_list
        for i, row_data in enumerate(sell_list):
            sell_list[i] = sell_list[i].replace("매도전", "주문완료")
        # file update
        f = open("sell_list.txt", "wt")
        for row_data in sell_list:
            f.write(row_data)
        f.close()
        print("자동 매도주문 완료")


    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: "+text_time

        kstate = self.kiwoom.get_connect_state()

        if kstate == 1:
            state_msg1 = "키움 서버 연결중"
        else:
            state_msg1 = "키움 서버 미연결"

        trade_time = QTime(15, 22, 0)
        auto_login_time = QTime(15, 20, 0)
        #trade_time = QTime(15, 00, 0)
        #auto_login_time = QTime(14, 59, 0)

        if kstate == 0 and current_time > auto_login_time and self.today_trade_ready is False and self.checkBox.isChecked():  #자동매매 체크시 자동 로그인 되도록
            self.connect_kiwoom()  #자동로그인
            time.sleep(10)
            print("자동로그인 완료")

        if kstate == 1 and current_time > auto_login_time and self.condi_load is False and self.checkBox.isChecked():  # 자동매매 체크시 자동 로그인 되도록
            self.kiwoom.getconditionload()
            self.today_conditoinload = True
            self.condi_load = True
            print("getconditioinload 완료")

        if kstate == 1 and current_time > auto_login_time and self.today_trade_ready is False and self.kiwoom.getcondition_ is True and self.checkBox.isChecked():
                                       # 매매할 종목 적기
            self.kiwoom.update_buy_qt()
            print("update_buy_qt 완료")
            time.sleep(10)
            self.today_trade_ready = True

        if kstate == 1 and current_time > trade_time and self.today_trade_ready is True and self.trade_stocks_done is False and self.checkBox.isChecked():
            time.sleep(10)
            self.auto_trade()

        self.statusbar.showMessage(state_msg1 + " | " + time_msg)


    def auto_trade(self):    ##자동 주문 설정
        self.auto_buy()
        time.sleep(5)
        self.auto_sell()

        self.trade_stocks_done = True

    def update_buy_list(self, buy_code_list):  # 대신증권 살종목 텍스트 파일 업데이트
        day_money = 5000000  # 1일 최대 투자금액 500만원
        one_stock_money = int(day_money / self.buy_list_len)
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

    def sichoga_sell(self):  #시초가에 지정한 가격에 매도
        print("AA")

    def stock_1_ohlcv_button(self):
        codedata = self.kiwoom.kospi_and_kosdaq_code_load()
        name = self.lineEdit.text()
        codelist = list(codedata.keys())

        for code in codelist:                       #딕셔너리에서 value값으로 key값을 찾는 과정이다.
            if codedata[code] == name:
                break
                ###없는키 입력시 출력할 메시지 작성 필요

        today = datetime.datetime.today().strftime("%Y%m%d")
        todaystr = str(today)

        self.kiwoom.stock_1_ohlcv(code, todaystr)

        print(code)
        print(name)


    def TestTest(self):

        print("dd")
        a = self.kiwoom.kospi_and_kosdaq_code_load()
        print(a)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
