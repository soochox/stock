import sys
import lib as lib
# import kiwoom as ki

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *

# import pandas as pd
from pprint import pprint
import re
import requests
from threading import Timer, Thread, Event

import json
from collections import OrderedDict

import webbrowser
from functools import partial

# 미수거래 넣어야 됨

class perpetualTimer():
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()
        self.thread.cancel()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("뉴스매매(Makeby 욱)")
        self.setGeometry(300, 300, 1200, 700)
        self.setTable()

        # self.t = perpetualTimer(1, self.startNews)
        # self.t.start()

        # timer = QTimer()
        # timer.timeout.connect(self.startNews)
        # timer.start(1000)
        self.current_timer = ""
        # self.start_timer() # 로그인후 실행하도록 변경

        self.apiUrl = "내 API 주소는 비밀"

        self.thread_cnt = 0
        self.last_title = ""

        # 키움개인정보
        # self.user_id = "dev84" # 테스트
        self.user_id = ""
        self.account_number = ""  # 키움계좌

        # print(sys.version)

        # 키움증권
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        # 키움 이벤트 등록(시그널과 슬롯을 연결)
        self.kiwoom.OnEventConnect.connect(self.event_connect) # 개인정보 호출됨
        self.kiwoom.OnReceiveChejanData.connect(self.receive_chejan_data) # 매수체결후 호출됨
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        self.kiwoom.OnReceiveMsg.connect(self.receive_msg) # 매수시도후 에러발생시

        # print("매수테스트 시작")
        # 8102230011
        # 8102-2300
        '''
        로그인 후 테스트 해야함
        returnCode = self.kiwoom.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)", ["auto_buy", "4989", "8102-2300", 10, "034220", 3, "", "03", ""])
        if returnCode != 0:
            # print("매수결과 = " + str(returnCode))
            KiwoomProcessingError("sendOrder() : " + ReturnCode.CAUSE[returnCode])
        else:
            print("매수성공 끼야호!")
        '''

        self.textLabel = QLabel("정보 : ", self)
        self.textLabel.setGeometry(510, 20, 500, 20)

        self.btn_test = QPushButton("매수테스트", self)
        self.btn_test.move(900, 20)
        # btn_test.clicked.connect(ki_instance.btn1_clicked)
        self.btn_test.clicked.connect(self.test_buy)

        self.btn1 = QPushButton("로그인", self)
        self.btn1.move(1000, 20)
        # btn1.clicked.connect(ki_instance.btn1_clicked)
        self.btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton("상태체크", self)
        btn2.move(1100, 20)
        # btn2.clicked.connect(ki_instance.btn2_clicked)
        btn2.clicked.connect(self.btn2_clicked)

        '''
        self.ed = QLineEdit()
        self.ed.move(700, 50)
        self.ed.setText("홍길동")  #  텍스트 쓰기
        text = self.ed.text()  #  텍스트 읽기
        self.ed.setPlaceholderText("이름을 입력하시오") #  Watermark로 텍스트 표시
        self.ed.selectAll() #  텍스트 모두 선택
        # ed.setReadOnly(True)#  에디트는 읽기 전용으로
        # e.setEchoMode(QLineEdit.Password)#  Password 스타일 에디트
        '''
        keywordLabel = QLabel("종목&키워드 매칭(종목코드:키워드1,키워드2,키워드3...)", self)
        keywordLabel.setGeometry(510, 50, 500, 50)

        self.keywordbtn = QPushButton("매칭 저장", self)
        self.keywordbtn.move(1100, 60)
        self.keywordbtn.clicked.connect(self.keywordbtn_clicked)

        self.textEdit = QTextEdit(self)
        self.textEdit.resize(670, 250)
        self.textEdit.move(510, 100)

        logLabel = QLabel("로그", self)
        logLabel.setGeometry(510, 370, 500, 50)

        self.textEdit2 = QTextEdit(self)
        self.textEdit2.resize(670, 250)
        self.textEdit2.move(510, 420)
        # self.textEdit2.setReadOnly(True)

        """""
        btn1 = QPushButton("Click me", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)
        """

    def start_timer(self):
        if self.current_timer:
            self.current_timer.stop()
            self.current_timer.deleteLater()

        self.current_timer = QTimer()
        self.current_timer.timeout.connect(self.startNews)
        self.current_timer.setSingleShot(True)
        self.current_timer.start(1000)

    def keywordbtn_clicked(self):
        # print("저장")
        content = self.textEdit.toPlainText()
        # print(content)
        # print(self.user_id)

        post_data = {"type": "keyword_save", "stock_id": self.user_id, "content": content}
        r = requests.post(self.apiUrl, data=post_data)
        result_json = r.text  # {"result":"OK"}
        # print(result_json)

        #  JSON 디코딩
        dict = json.loads(result_json)
        # print("result = " + dict['result']) # OK
        if dict['result'] == "OK":
            w = QWidget()  # The QWidget widget is the base class
            w.setWindowTitle('키워드저장버튼')
            w.resize(400, 200)
            result = QMessageBox.information(w, "Information", "저장완료")

            # if result == QMessageBox.Ok:
            #    myTextbox.setText("Clicked OK on Information.")

    def btn1_clicked(self):
        # print("로그인 버튼 클릭")
        ret = self.kiwoom.dynamicCall("CommConnect()")
        if ret == 0:
            self.statusBar().showMessage("로그인 창 열기 성공")
            # self.btn1.setText('로그인 정보보기')
            # self.getLoginInfo()
        else:
            self.statusBar().showMessage("로그인 창 열기 실패")
        # print(ret)

    def btn1_clicked_logined(self):
        print("ok")

    # 로그인 상태 확인
    def btn2_clicked(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")

    # 로그인 유저 정보 호출
    def getLoginInfo(self, type):
        # print("getLoginInfo")
        info = self.kiwoom.dynamicCall("GetLoginInfo(QString)", type)
        # print(info)
        return info

    def get_stock_info(self, code):
        # print("get_stock_info Code = " + code)

        #  SetInputValue
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)

        #  CommRqData
        #  구분자 : opt10001
        #  스프릿 : opt10001_req
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "opt10001_req__WOOK__" + code, "opt10001", 0, "0101")

    def test_buy(self):
        returnCode = self.kiwoom.dynamicCall(
            "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
            ["auto_buy", "4989", "8102230011", 1, "034220", 10, "", "03", ""])
        if returnCode != 0:
            # print("매수결과 = " + str(returnCode))
            KiwoomProcessingError("sendOrder : " + ReturnCode.CAUSE[returnCode])
        else:
            print("매수성공 끼야호!")

    def receive_trdata(self, screen_no, rqname, trcode, recordname, prev_next, data_len, err_code, msg1, msg2):

        rqname_split = re.split('__WOOK__', rqname)
        rqname = rqname_split[0]
        code = rqname_split[1]

        print("====================================")
        print("receive_trdata 호출됨 , rqname = " + rqname)

        if rqname == "opt10001_req":
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "거래량")
            now_price = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", trcode, "", rqname, 0, "현재가")

            '''
            strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("종목코드"));   strData.Trim();
            strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("거래량"));   strData.Trim();
            strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("시가"));   strData.Trim();
            strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("고가"));   strData.Trim();
            strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("저가"));   strData.Trim();
            strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("현재가"));   strData.Trim();            
            '''
            print("====================================")
            print("종목코드 : " + code)
            print("종목명 : " + name.strip())
            print("거래량 : " + volume.strip())
            print("현재가 : " + now_price.strip())

            #  여기서 매수하자
            n_price = abs(int(now_price.strip()))

            # self.account_number = self.account_number.replace(';', '')
            temp = re.split(';', self.account_number)
            buy_account_number = temp[0]

            print("buy_account_number = " + buy_account_number)
            print("n_price = " + str(n_price))

            returnCode = self.kiwoom.dynamicCall(
                "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                ["auto_buy", "4989", buy_account_number, 1, code, 1, "", "03", ""])
            if returnCode != 0:
                # print("매수결과 = " + str(returnCode))
                KiwoomProcessingError("sendOrder : " + ReturnCode.CAUSE[returnCode])
            else:
                msg = "매수성공, 종목코드 = " + code + ", 계좌번호 = " + buy_account_number
                print(msg)

                content = self.textEdit2.toPlainText()
                self.textEdit2.setText(msg + "\n" + content)

            '''
            [SendOrder() 함수]

            SendOrder(
            BSTR sRQName, // 사용자 구분명
            BSTR sScreenNo, // 화면번호
            BSTR sAccNo,  // 계좌번호 10자리
            LONG nOrderType,  // 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
            BSTR sCode, // 종목코드
            LONG nQty,  // 주문수량
            LONG nPrice, // 주문가격
            BSTR sHogaGb,   // 거래구분(혹은 호가구분)은 아래 참고
            BSTR sOrgOrderNo  // 원주문번호입니다. 신규주문에는 공백, 정정(취소)주문할 원주문번호를 입력합니다.
            )

            9개 인자값을 가진 국내 주식주문 함수이며 리턴값이 0이면 성공이며 나머지는 에러입니다.
            1초에 5회만 주문가능하며 그 이상 주문요청하면 에러 -308을 리턴합니다.

            [거래구분]
            모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

            00 : 지정가
            03 : 시장가
            05 : 조건부지정가
            06 : 최유리지정가
            07 : 최우선지정가
            10 : 지정가IOC
            13 : 시장가IOC
            16 : 최유리IOC
            20 : 지정가FOK
            23 : 시장가FOK
            26 : 최유리FOK
            61 : 장전시간외종가
            62 : 시간외단일가매매
            81 : 장후시간외종가            
            '''


    # 로그인 후 실행되는 함수
    # 로그인성공
    def event_connect(self, code):
        if code == 0:
            self.statusBar().showMessage("로그인 성공")
            self.user_id = self.getLoginInfo("USER_ID")
            self.account_number = self.getLoginInfo("ACCNO")
            #  print(self.account_number)

            self.textLabel.setText("●계좌번호 : " + self.account_number)
            self.btn1.setText(self.user_id + "님")
            # 버튼 이벤트 해제해야 하는데 일단 스킵

            # 종목코드:키워드 정보 가져오기
            post_data = {"type": "get_keyword", "stock_id": self.user_id}
            r = requests.post(self.apiUrl, data=post_data)
            result_json = r.text  # {"result":"OK"}

            #  JSON 디코딩
            dict = json.loads(result_json)
            data = dict['data']
            # print("종목키워드 데이터\n=================\n" + data + "\n=================\n")
            self.textEdit.setText(data)

            # 매수테스트
            '''
            종목코드 : 003550
            종목명 : LG
            거래량 : 42202
            현재가 : 86000
            account_number = 8102230011
            8739688531
            n_price = 86000            
            '''

            '''
            print("로그인 후 매수테스트")
            returnCode = self.kiwoom.dynamicCall(
                "SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                ["auto_buy", "4989", "8102230011", 1, "034220", 10, "", "03", ""])
            if returnCode != 0:
                # print("매수결과 = " + str(returnCode))
                KiwoomProcessingError("sendOrder : " + ReturnCode.CAUSE[returnCode])
            else:
                print("매수성공 끼야호!")
            '''

            self.start_timer()
        else:
            self.statusBar().showMessage("로그인 실패")

        # print("event_connect 호출됨")
        # self.event_connect_loop.exit()

    # SendOrder(주문) 성공후 호출
    '''
      BSTR sGubun, // 체결구분 접수와 체결시 '0'값, 국내주식 잔고전달은 '1'값, 파생잔고 전달은 '4'
      LONG nItemCnt,
      BSTR sFIdList    
    '''
    # 매수성공
    def receive_chejan_data(self, gubun, item_cnt, field_list):
        # print("매수성공함")
        print("receive_chejan_data 호출, 매수성공, gubun = " + gubun + " , item_cnt = " + item_cnt + " , field_list = " + field_list)
        # print(self.get_chejan_data(9203))
        # print(self.get_chejan_data(302))
        # print(self.get_chejan_data(900))
        # print(self.get_chejan_data(901))

    # 매수성공(일단 사용안함)
    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    # 매수에러
    def receive_msg(self, scr_no, rq_name, tr_code, msg):
        print("receive_msg 호출됨, 매수에러 발생, rq_name = " + rq_name + ", tr_code = " + tr_code + ", msg = " + msg)

    def setTable(self):
        # self.setGeometry(5,5,200,200)

        newsLabel = QLabel("실시간 뉴스", self)
        newsLabel.setGeometry(5, 5, 500, 50)

        self.tableWidget = QTableWidget(self)

        # self.tableWidget.resize(500, 500)
        self.tableWidget.setGeometry(5, 50, 500, 500)

        self.tableWidget.setRowCount(20)
        self.tableWidget.setColumnCount(3)

        # self.tableWidget.setVerticalHeaderLabels(['1','2'])
        self.tableWidget.setHorizontalHeaderLabels(['제목', '시간', '상세보기'])

        # 데이터 넣기
        # self.setTableWidgetData()
        # self.startNews()

    def startNews(self):
        self.thread_cnt = self.thread_cnt + 1
        print("뉴스 쓰레드 가동(" + str(self.thread_cnt) + ")")

        # 뉴스 쓰레드 가동(283) 에서
        # Process finished with exit code -1073740940 (0xC0000374) 에러발생
        # Process finished with exit code -1073741819 (0xC0000005)
        # Process finished with exit code -1073741819 (0xC0000005)

        # 뉴스 저장하기
        # self.setNews2()

        # 뉴스 가져오기
        # self.get_news()

        # 뉴스 쓰레드 가동(281) 에서
        # Process finished with exit code -1073740940 (0xC0000374)
        self.get_set_news()

        # self.t = perpetualTimer(1, self.startNews)
        # self.t.start()

        # timer = QTimer()
        # timer.timeout.connect(self.startNews)
        # timer.start(1000)

        self.start_timer()

    '''
    def setTableWidgetData(self):
        self.tableWidget.setItem(0, 0, QTableWidgetItem("(0,0)"))
        self.tableWidget.setItem(0, 1, QTableWidgetItem("(0,1)"))
        self.tableWidget.setItem(1, 0, QTableWidgetItem("(1,0)"))
        self.tableWidget.setItem(1, 1, QTableWidgetItem("(1,1)"))
    '''

    """
    def btn1_clicked(self):
        QMessageBox.about(self, "message", "clicked")
    """

    # API 서버에서 뉴스크롤링 실행시키고, 바로 가져오기
    def get_set_news(self):
        post_data = {"type": "getset", "stock_id": self.user_id}
        r = requests.post(self.apiUrl, data=post_data)
        result_json = r.text  # {"result":"OK"}

        #  JSON 디코딩
        dict = json.loads(result_json)
        # print("get_set_news = " + dict['result'])

        # 매칭된 키워드가 있으면 로그로 보여주기
        '''
        뉴스 쓰레드 가동(135)
        {'111': ['(주)', '결과']}
        '''
        if dict['log_text']:
            content = self.textEdit2.toPlainText()
            self.textEdit2.setText(dict['log_text'] + content)

        #  print(dict['list'])
        #  print(dict['buy_code'])
        #  for i in dict['buy_code']:
        #     print("구매종목코드 : " + i)
        '''
        003550 : LG
        034220 : LG디스플레이
        001120 : LG상사
        '''
        buy_code = re.split(',', dict['buy_code'])
        for row in buy_code:
            if row:
                # print("구매종목코드 : " + row)
                self.get_stock_info(row)

        # print(dict['list'])
        cnt = 0
        # self.tableWidget.setRowCount(20)

        for row in dict['list']:
            if cnt == 0:
                if self.last_title == row['title']:
                    break
                else:
                    #  print(row['title'] + " " + row['time'])
                    self.last_title = row['title']
                    #  for i in range(0, 20):
                    #  self.tableWidget.setItem(i, 0, QTableWidgetItem("1"))
                    #  self.tableWidget.setItem(i, 1, QTableWidgetItem("1"))

            title = row['title'][0:30]
            self.tableWidget.setItem(cnt, 0, QTableWidgetItem(title))
            self.tableWidget.setItem(cnt, 1, QTableWidgetItem(row['time']))

            detailbtn = QPushButton("보기")
            # detailbtn.clicked.connect(lambda:self.detailbtn_clicked(row['idx']))
            detailbtn.clicked.connect(partial(self.detailbtn_clicked, row['idx']))
            self.tableWidget.setCellWidget(cnt, 2, detailbtn)
            # print(row['idx'])

            #  데이터 갱신을 위해 포커스를 주자
            self.tableWidget.setCurrentCell(cnt, 0)
            self.tableWidget.setCurrentCell(cnt, 1)
            self.tableWidget.setCurrentCell(cnt, 2)
            cnt = cnt + 1

        # 각 열크기 맞춤
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

    # 기사 상세보기 띄우기
    def detailbtn_clicked(self, idx):
        # print(idx)
        url = self.apiUrl + "?type=news_detail&idx=" + idx + "&stock_id=" + self.user_id
        webbrowser.open(url)

    # API 서버에서 뉴스크롤링 실행시키기
    def setNews2(self):
        post_data = {"type": "set", "stock_id": self.user_id}
        r = requests.post(self.apiUrl, data=post_data)
        result_json = r.text  # {"result":"OK"}

        #  JSON 디코딩
        dict = json.loads(result_json)
        print("setNews2 = " + dict['result'])

    # 파이썬 자체에서 크롤링
    def setNews(self):
        # 공시정보 가져오기
        # lib.get_financial_statements('http://dart.fss.or.kr/api/search.json?auth=5d7fe977e575fb2ec15661d0a1556f40793237f6')
        outhtml = lib.get_financial_statements('크롤링 주소는 비밀')
        # print(outhtml)
        # output = re.match(r'(?s).*<!-- List BBS Block Start -->(.*)<!-- //List BBS Block End -->.*', outhtml, re.M|re.I)
        # print(output.group(1))
        # output = re.match(r'(?s).*<div class="newListArea">(.*)</div>(.*)</div>.*', output.group(1), re.M|re.I)
        output = re.match(r'(?s).*<!-- %%LIST data%% -->(.*)<!-- %%ENDLIST data%% -->.*', outhtml, re.M | re.I)
        output_data = ''
        if output is not None:
            output_data = output.group(1)
            # print(output)
        else:
            print("젠장... 비었음...")

        # print(output_data)
        outlist = re.split('</tr>', output_data)
        # pprint(outlist)

        cnt = 0
        all_json = OrderedDict()
        for row in outlist:
            # date = lib.get_between_string(row, '<div id="date_0">', '</div>')
            # print(row)
            row_list = re.split('<td', row)
            # pprint(row_list)
            # print(row_list[2])
            # print(lib.strip_tags(row_list[3]))
            # print(row_list[3])
            try:
                row_json = OrderedDict()
                tmp = re.match(r'(?s).*<div id="date_.*">(.*)</div></td>.*', row_list[1])
                date = tmp.group(1)

                tmp = re.match(r'(?s).*<div id="time_.*">(.*)</div></td>.*', row_list[2])
                time = tmp.group(1)

                tmp = re.match(r'(?s).*<div id=\'title_.*\'>(.*)</div></a>.*', row_list[3])
                title = tmp.group(1)
                title = title.replace('&nbsp; ', '')

                row_json['date'] = date
                row_json['time'] = time
                row_json['title'] = title

                all_json[str(cnt)] = row_json
            except:
                '''
                print("끝줄에러")
                '''

            '''
            test = ""
            test += "date = " + date + " || "
            test += "time = " + time + " || "
            test += "title = " + title + " || "
            print(str(cnt) + " = " + test)
            '''
            cnt = cnt + 1

        # pprint(all_json)
        jsonString = json.dumps(all_json)
        post_data = {'data': jsonString, "type": "news_toss", "stock_id": self.user_id}
        # print(jsonString)
        # pprint(post_data)

        # 디비에 저장
        r = requests.post(self.apiUrl, data=post_data)
        result_json = r.text  # {"result":"OK"}

    def get_news(self):
        post_data = {"type": "get", "stock_id": self.user_id}
        r = requests.post(self.apiUrl, data=post_data)
        result_json = r.text  # {"result":"OK"}
        # print("result_json = " + result_json)

        #  JSON 디코딩
        dict = json.loads(result_json)

        #  Dictionary 데이타 체크
        print("get_news = " + dict['result'])

        # print(dict['list'])
        cnt = 0
        # self.tableWidget.setRowCount(20)

        for row in dict['list']:
            if cnt == 0:
                if self.last_title == row['title']:
                    break
                else:
                    # print(row['title'] + " " + row['time'])
                    self.last_title = row['title']
                    # for i in range(0, 20):
                    # self.tableWidget.setItem(i, 0, QTableWidgetItem("1"))
                    # self.tableWidget.setItem(i, 1, QTableWidgetItem("1"))

            title = row['title'][0:40]
            self.tableWidget.setItem(cnt, 0, QTableWidgetItem(title))
            self.tableWidget.setItem(cnt, 1, QTableWidgetItem(row['time']))

            # 데이터 갱신을 위해 포커스를 주자
            self.tableWidget.setCurrentCell(cnt, 0)
            self.tableWidget.setCurrentCell(cnt, 1)
            cnt = cnt + 1

        # 각 열크기 맞춤
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()


class KiwoomProcessingError(Exception):
    """ 키움에서 처리실패에 관련된 리턴코드를 받았을 경우 발생하는 예외 """

    def __init__(self, msg="처리 실패"):
        # self.msg = msg
        print(msg)

    def __str__(self):
        return self.msg

    def __repr__(self):
        return self.msg

class ReturnCode(object):
    """ 키움 OpenApi+ 함수들이 반환하는 값 """

    OP_ERR_NONE = 0 # 정상처리
    OP_ERR_FAIL = -10   # 실패
    OP_ERR_LOGIN = -100 # 사용자정보교환실패
    OP_ERR_CONNECT = -101   # 서버접속실패
    OP_ERR_VERSION = -102   # 버전처리실패
    OP_ERR_FIREWALL = -103  # 개인방화벽실패
    OP_ERR_MEMORY = -104    # 메모리보호실패
    OP_ERR_INPUT = -105 # 함수입력값오류
    OP_ERR_SOCKET_CLOSED = -106 # 통신연결종료
    OP_ERR_SISE_OVERFLOW = -200 # 시세조회과부하
    OP_ERR_RQ_STRUCT_FAIL = -201    # 전문작성초기화실패
    OP_ERR_RQ_STRING_FAIL = -202    # 전문작성입력값오류
    OP_ERR_NO_DATA = -203   # 데이터없음
    OP_ERR_OVER_MAX_DATA = -204 # 조회가능한종목수초과
    OP_ERR_DATA_RCV_FAIL = -205 # 데이터수신실패
    OP_ERR_OVER_MAX_FID = -206  # 조회가능한FID수초과
    OP_ERR_REAL_CANCEL = -207   # 실시간해제오류
    OP_ERR_ORD_WRONG_INPUT = -300   # 입력값오류
    OP_ERR_ORD_WRONG_ACCTNO = -301  # 계좌비밀번호없음
    OP_ERR_OTHER_ACC_USE = -302 # 타인계좌사용오류
    OP_ERR_MIS_2BILL_EXC = -303 # 주문가격이20억원을초과
    OP_ERR_MIS_5BILL_EXC = -304 # 주문가격이50억원을초과
    OP_ERR_MIS_1PER_EXC = -305  # 주문수량이총발행주수의1%초과오류
    OP_ERR_MIS_3PER_EXC = -306  # 주문수량이총발행주수의3%초과오류
    OP_ERR_SEND_FAIL = -307 # 주문전송실패
    OP_ERR_ORD_OVERFLOW = -308  # 주문전송과부하
    OP_ERR_MIS_300CNT_EXC = -309    # 주문수량300계약초과
    OP_ERR_MIS_500CNT_EXC = -310    # 주문수량500계약초과
    OP_ERR_ORD_WRONG_ACCTINFO = -340    # 계좌정보없음
    OP_ERR_ORD_SYMCODE_EMPTY = -500 # 종목코드없음

    CAUSE = {
        0: '정상처리',
        -10: '실패',
        -100: '사용자정보교환실패',
        -102: '버전처리실패',
        -103: '개인방화벽실패',
        -104: '메모리보호실패',
        -105: '함수입력값오류',
        -106: '통신연결종료',
        -200: '시세조회과부하',
        -201: '전문작성초기화실패',
        -202: '전문작성입력값오류',
        -203: '데이터없음',
        -204: '조회가능한종목수초과',
        -205: '데이터수신실패',
        -206: '조회가능한FID수초과',
        -207: '실시간해제오류',
        -300: '입력값오류',
        -301: '계좌비밀번호없음',
        -302: '타인계좌사용오류',
        -303: '주문가격이20억원을초과',
        -304: '주문가격이50억원을초과',
        -305: '주문수량이총발행주수의1%초과오류',
        -306: '주문수량이총발행주수의3%초과오류',
        -307: '주문전송실패',
        -308: '주문전송과부하',
        -309: '주문수량300계약초과',
        -310: '주문수량500계약초과',
        -340: '계좌정보없음',
        -500: '종목코드없음'
    }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()