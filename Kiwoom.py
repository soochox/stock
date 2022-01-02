import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import datetime
from pandas import DataFrame
import sqlite3

TR_REQ_TIME_INTERVAL = 0.2


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._creat_kiwoom_instance()
        self._set_signal_slots()
        self.OnReceiveChejanData.connect(self._receive_chejan_data) # 여기 맞겠지?
        self.condi_num = 12  # 13번째 조건식

    def _creat_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)  # 여기 맞겠지?
        self.OnReceiveConditionVer.connect(self._receive_conditionver)
        self.OnReceiveMsg.connect(self._receive_msg)
        # self.OnReceiveTrCondition.connect(self._handler_tr_condition)

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
        #print("로그인 루프 나감")

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QSting)", market)   #코스피/코스닥
        code_list = code_list.split(";")
        return code_list[:-1]

    def get_master_code_name(self, code):    #코드를 종목명으로
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString,QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString,QString,int,QString)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString,QString,QString,int,QString)", code, real_type, field_name, index,
                               item_name)
        # ret = self.dynamicCall("GetCommData(QString,QString,QString,int,QString)", code, real_type, field_name, index,
        #                         item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString,QString)", trcode, rqname)
        return ret


    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        ## 고쳐야함
        if next == "2":
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)

        elif rqname == "opw00018_req":
            self._opw00018(rqname, trcode)

        elif rqname == "opt10001_req":  #기본 종목 정보 조회
            self.receive_check_stock_basic_info(rqname, trcode)

        elif rqname == "opw00007_req":  #주문정보 조회 요청
            self._opw00007(rqname, trcode, next)
        elif rqname == "opw00007_req_can":  #주문취소 요청
            self._opw00007_cancell(rqname, trcode, next)
        elif rqname == "opt20001_req":
            self._opt20001(rqname, trcode, next)   #지수정보 요청
        elif rqname == "rq_account_evaluate":     #일자별 실현 손익요청
            self._opt10074(rqname, trcode, next)

        # elif rqname == "send_order_req":  # 주문정보 수신
        #     print("주문정보 수신완료")
        #     self._send_order(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass

    def now__(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    def _receive_msg(self, scrnum, rqname, trcode, msg):
        print('receive_msg')
        print(msg)
        return


    def base_info_request(self, code): #주식 기본정보 요청
        self.set_input_value("종목코드", code)
        self.comm_rq_data("opt10001_req","opt10001",0, "0101")

    def order_info_req(self, next, cancell):   #주문정보 현황 요청/주문취소  1:주문취소, 그외 주문조회

        if next == 0:
            self.order_info = []  # 주문 번호
            self.final_none_contranct_order_num = []  # 취소 주문번호
            self.final_none_cont_stock_num_list = []  # 취소 종목코드
            self.final_none_cont_remain_num = []  # 취소 주문잔량

        today = datetime.datetime.now()
        todaystring = today.strftime('%Y%m%d')   #오늘 날짜 yymmdd 형식으로
        self.set_input_value("주문일자", todaystring)
        self.set_input_value("계좌번호", "5514437210")
        self.set_input_value("비밀번호입력매체구분", "00")
        self.set_input_value("조회구분", 3)    #1: 주문순, 2역순, 3미체결, 4체결내역만
        self.set_input_value("주식채권구분", "1")
        self.set_input_value("매도수구분", "0")    #전체

        if cancell == 1:   #주문취소
            req_name = "opw00007_req_can"
            self.comm_rq_data(req_name, "opw00007", next, "1008")    #2는 연속조회(30건이상)
            print(self.now__(), "  주문취소 요청완료")
            print("===========================================================")
        else:    #주문정보 출력
            print(self.now__(), "  주문정보 현황 조회")
            req_name = "opw00007_req"
            self.comm_rq_data(req_name,"opw00007", next, "1009")
            print("===========================================================")

    def rq_jisu(self, market, code):
        self.set_input_value("시장구분", market)
        self.set_input_value("업종코드", code)
        self.comm_rq_data("opt20001_req", "opt20001", 0, "0201")

    def rq_account_evaluate(self, acc):    #금일 실현손익 조회 요청
        print("들어옴")
        today = datetime.datetime.today().strftime("%Y%m%d")
        self.set_input_value("계좌번호", acc)
        self.set_input_value("시작일자", today)
        self.set_input_value("종료일자", today)
        print("셋인풋밸류 완료")
        self.comm_rq_data("rq_account_evaluate", "opt10074"	,  "0"	,  "5201")
        print("계좌 평가현황 요청 완료")
        print("===========================================================")

    def _opt10074(self, rqname, trcode, next):   #금일 실현손익 조회 요청
        self.day_profit = self._comm_get_data(trcode, "", rqname, 0, "실현손익")
        print("계좌평가현황 완료")
        print("===========================================================")

    def receive_check_stock_basic_info(self, rqname, trcode):   #종목 기본정보요청 수신
        name = self._comm_get_data(trcode, "", rqname, 0, "종목명")
        open = self._comm_get_data(trcode, "", rqname, 0, "시가")
        high = self._comm_get_data(trcode, "", rqname, 0, "고가")
        low = self._comm_get_data(trcode, "", rqname, 0, "저가")
        cl = self._comm_get_data(trcode, "", rqname, 0, "현재가")
        self.base_stock_info = [name, open, high, low, cl]

    def _opt20001(self, rqname, trcode, next):  # 지수정보 요청
        print('지수정보 수신')
        open = self._comm_get_data(trcode, "", rqname, 0, "시가")
        high = self._comm_get_data(trcode, "", rqname, 0, "고가")
        low = self._comm_get_data(trcode, "", rqname, 0, "저가")
        now_price = self._comm_get_data(trcode, "", rqname, 0, "현재가")
        kosdaq_change = self._comm_get_data(trcode, "", rqname, 0, "전일대비")
        kosdaq_change_ratio = self._comm_get_data(trcode, "", rqname, 0, "등락률")
        print('지수정보 수신2')
        self.today_jisu_data = [open, high, low, now_price, kosdaq_change, kosdaq_change_ratio]
        print('지수정보 수신3')


    def _opt10081(self, rqname, trcode):   #계좌의 보유 종목 정보 출력
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

    def _opw00007(self, rqname, trcode, next):
        print(self.now__(), "  주문현황 요청 서버 답신 받음")
        data_cnt = self._get_repeat_cnt(trcode, rqname)   #주문한 건수
        check_order_info = []

        for i in range(data_cnt):
            odrnum = self._comm_get_data(trcode, "", rqname, i, "주문번호")
            stockname = self._comm_get_data(trcode, "", rqname, i, "종목명")
            contract_num = int(self._comm_get_data(trcode, "", rqname, i, "체결수량"))
            jubsoo = self._comm_get_data(trcode, "", rqname, i, "접수구분")
            joomoon = self._comm_get_data(trcode, "", rqname, i, "주문구분")
            check_order_info.append(odrnum+";"+stockname+";"+str(contract_num)+ ";"+jubsoo+";" +joomoon)

        self.order_info = self.order_info + check_order_info
        if next != "2":
            print("총 주문건수 : %s, 조회결과 : %s" % (len(self.order_info), self.order_info))


    def _opw00007_cancell(self, rqname, trcode, next):   #주문취소 요청 답신
        print("주문취소 요청 서버 답신 받음")
        print("next: %s" % next)
        account_number = "5514437210"
        data_cnt = self._get_repeat_cnt(trcode, rqname)  # 주문한 건수
        none_cont_remain_num = []  #주문잔량 수
        none_contranct_order_num = []
        none_contranct_order_stock = []
        none_cont_stock_num_list = []

        if data_cnt-1 == 0:    #데이터가 1이면 주문 내역이 없다?? 확인 필요함
            print("금일 주문 내역이 없습니다.")
            return

        for i in range(data_cnt):
            contract_remain = int(self._comm_get_data(trcode, "", rqname, i, "주문잔량"))
            odrnum = self._comm_get_data(trcode, "", rqname, i, "주문번호")
            stockname = self._comm_get_data(trcode, "", rqname, i, "종목명")
            stocknum = self._comm_get_data(trcode, "", rqname, i, "종목번호")

            if contract_remain > 0:    #주문잔량이 0보다 크면
                none_contranct_order_num.append(odrnum)      #주문번호
                none_contranct_order_stock.append(stockname)    #종목명
                none_cont_stock_num_list.append(stocknum)      #종목코드
                none_cont_remain_num.append(contract_remain)    #주문잔량

        if len(none_cont_remain_num) == 0:
            print("미체결 주문이 없습니다.")
        else:
            print("미체결 주문번호", none_contranct_order_num)    #주문번호
            print("미체결 주문 종목", none_cont_stock_num_list)   #종목코드

        self.final_none_contranct_order_num = self.final_none_contranct_order_num + none_contranct_order_num  #주문번호
        self.final_none_cont_stock_num_list = self.final_none_cont_stock_num_list + none_cont_stock_num_list   #종목코드
        self.final_none_cont_remain_num = self.final_none_cont_remain_num + none_cont_remain_num  #주문잔량

        if next != 2:
            if len(self.final_none_contranct_order_num) > 0:
                print("미체결 주문번호 : %s" % self.final_none_contranct_order_num)
                for i, order_num in enumerate(self.final_none_contranct_order_num):
                    none_cont_stock_num = self.final_none_cont_stock_num_list[i][1:]  #첫번째 글자 "A" 제거
                    none_cont_remain = self.final_none_cont_remain_num[i]   #주문잔량
                    self.send_order("order_cancell_req", "0109", account_number, 3, none_cont_stock_num, none_cont_remain, "", "", order_num)
                    time.sleep(0.4)
                print(self.now__(), "  주문취소 요청 완료")
                print("===========================================================")

    def send_order(self,rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString,QString,QString, int,QString, int, int, QString,QString)",[rqname, screen_no,
        acc_no, order_type, code, quantity, price, hoga, order_no])

    def get_chejan_data(self,fid):
        ret = self.dynamicCall("GetChejanData(int)",fid)
        return ret

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print("주문번호 : %s" % self.get_chejan_data(9203))
        # print("주문수량 : %s" % self.get_chejan_data(900))
        # print("주문단가 : %s" % self.get_chejan_data(901))
        print(self.now__(), "   %s %s주 %s원으로 주문 접수완료" % (self.get_chejan_data(302).rstrip(), self.get_chejan_data(900), self.get_chejan_data(901)))
        print("===========================================================")

    def get_login_info(self,tag):
        ret = self.dynamicCall("GetLoginInfo(QString)",tag)
        return ret


    def _opw00001(self, rqname, trcode):
        d2_deposit = self._comm_get_data(trcode, "", rqname, 0, "d+2추정예수금")
        self.d2_deposit = Kiwoom.change_format(d2_deposit)
        print("추정예수금: %s" % d2_deposit)

    def reset_opw00018_output(self):
        self.opw00018_output = {"single":[], "multi":[]}

    def _opw00018(self, rqname, trcode):   #계좌조회
        #single data
        total_purchase_price = self._comm_get_data(trcode, "", rqname, 0, "총매입금액")
        total_eval_price = self._comm_get_data(trcode, "", rqname, 0, "총평가금액")
        total_eval_profit_lose_price = self._comm_get_data(trcode, "", rqname, 0, "총평가손익금액")
        total_earning_rate = self._comm_get_data(trcode, "", rqname, 0, "총수익률(%)")
        estimated_deposit = self._comm_get_data(trcode, "", rqname, 0, "추정예탁자산")

        total_earning_rate = Kiwoom.change_format(total_earning_rate)
        total_earning_rate = float(total_earning_rate)/100
        total_earning_rate = round(total_earning_rate, 2)
        total_earning_rate = str(total_earning_rate)

        # if self.get_server_gubun():
        #     total_earning_rate = float(total_earning_rate)/100
        #     total_earning_rate = str(total_earning_rate)

        self.opw00018_output["single"].append(Kiwoom.change_format(total_purchase_price))
        self.opw00018_output["single"].append(Kiwoom.change_format(total_eval_price))
        self.opw00018_output["single"].append(Kiwoom.change_format(total_eval_profit_lose_price))
        self.opw00018_output["single"].append(total_earning_rate)
        self.opw00018_output["single"].append(Kiwoom.change_format(estimated_deposit))

        # multidata
        rows = self._get_repeat_cnt(trcode, rqname)   #보유종목 수량

        for i in range(rows):
            code = self._comm_get_data(trcode, "", rqname, i, "종목번호")
            name = self._comm_get_data(trcode, "", rqname, i, "종목명")
            quantity = self._comm_get_data(trcode, "", rqname, i, "보유수량")
            purchase_price = self._comm_get_data(trcode, "", rqname, i, "매입가")
            current_price = self._comm_get_data(trcode, "", rqname, i, "현재가")
            eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, i, "평가손익")
            earning_rate = self._comm_get_data(trcode, "", rqname, i, "수익률(%)")
            eval_price = str(int(quantity) * int(current_price))  #평가금액

            quantity = Kiwoom.change_format(quantity)
            purchase_price = Kiwoom.change_format(purchase_price)
            current_price = Kiwoom.change_format(current_price)
            eval_profit_loss_price = Kiwoom.change_format(eval_profit_loss_price)
            eval_price = Kiwoom.change_format(eval_price)
            earning_rate = Kiwoom.change_format2(earning_rate)
            self.opw00018_output['multi'].append([code, name, quantity, purchase_price, current_price, eval_price, eval_profit_loss_price, earning_rate])   #디스플레이용

    def get_server_gubun(self):
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "") #서버 구분 요청 1이면 모의??
        return ret

    def getconditionload(self):   #조건식 로딩 요청
        self.dynamicCall("GetConditionLoad()")
        print(self.now__(), "  전체 조건식 로딩 요청")
        print("===========================================================")

    def _receive_conditionver(self):
        print(self.now__(), "  조건식 로딩 요청 결과를 받았습니다.")
        data = self.dynamicCall("GetConditionNameList()")   #조건식 이름 을 data에 저장
        data_list = data.split(";")                         #조건식을 ; 기준으로 쪼개서 리스트로 저장
        del data_list[-1]                                   #조건식 리스트에 마지막 빈 데이터를 제거함
        count_data = len(data_list)                         #조건식의 개수를 파악

        condi_dic = {}                                      #빈딕셔너리 선언
        for i in data_list:
            key, value = i.split("^")                       #조건식 번호와 이름을 ^ 기준으로 쪼개서 딕셔너리의 키와 값으로 저장
            condi_dic[int(key)] = value

        print(condi_dic)  #모든 조건식 출력
        # condi_name_list = list(condi_dic.values())          #조건식 이름을 따로 저장
        # condi_index_list = list(condi_dic.keys())            #조건식 번호를 따로 저장
        print(self.now__(), "  조건식 전체 로딩 완료")
        print("==========================================================")


    def sendcondition(self, strScrNo, strConditionName, nIndex, nSearch, condi_num):  #조건식에 해당하는 종목을 불러오라고 요청, condi_num = 조건식 순번(내가 임의로 넣음거임)
        self.dynamicCall('KOA_Functions("SetConditionSearchFlag", "AddPrice")')
        ret_send = self.dynamicCall("SendCondition(QString, QString, int, int)", strScrNo, strConditionName, nIndex, nSearch)  #nSearch 실시간 조건검색
        if ret_send == 1:  #1이면 정상
            print(self.now__(), "  조건식 %s 로딩 정상 요청" % condi_num)

    def write_buy_list(self, buy_code_list):  # 대신증권 살종목 텍스트 파일 업데이트

        # one_day_money = int(self.lineEdit_2.text())
        # one_stock_money = int(one_day_money / len(buy_list))
        #
        # print("1일 투자금액: ", one_stock_money)

        f = open("buy_list.txt", "wt")
        for i, code in enumerate(buy_code_list):
            data = self.base_info_request(code)
            name = data.split(";")[0]
            close = data.split(";")[1]
            buy_quantity = int(one_stock_money / close)  # 매수 수량
            print(name)
            #f.writelines("%s;매수;%s;시장가;%s;0;매수전\n" % (name, code, buy_quantity))
        f.close()

    def kosdaq_save_ohlcv(self, code_list):  #현재가, 코드리스트를 받아서 그종목의 정보를 출력한다.

        today = datetime.datetime.today().strftime("%Y%m%d")
        todaystr = str(today)

        for i, code in enumerate(code_list):

            down_data = self.opt10081(code, today)
            codename = self.get_master_code_name(code)
            con = sqlite3.connect("c:/users/백/stock_kospi1_" + todaystr + ".db")
            down_data.to_sql(codename, con, if_exists="replace")
            print(i, "/", len(df["code"]), "요청완료")


    @staticmethod
    def change_format(data):
        strip_data = data.lstrip("-0")

        if strip_data == "" or strip_data == ".00":
            strip_data = "0"

        a = float(strip_data)
        format_data = format(int(a), ',d')

        if data.startswith("-"):
            format_data = "-" + format_data

        return format_data

    @staticmethod
    def change_format2(data):    #수익률에 대한 포맷변경, str 형식만 가능하다.
        strip_data = data.lstrip("-0")

        if strip_data == "":
            strip_data = 0

        if strip_data.startswith("."):
            strip_data = "0"+strip_data

        if data.startswith("-"):
            strip_data = "-"+strip_data
            
        a_data = int(strip_data)*0.01
        final_data = str(round(a_data, 2))
        # return strip_data
        return final_data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    # account_number = kiwoom.get_login_info("ACCNO")
    # account_number = account_number.split(";")[0]
    # kiwoom.set_input_value("계좌번호", account_number)
    # kiwoom.set_input_value("비밀번호", "0000")
    # kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")