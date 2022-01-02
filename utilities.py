import sqlite3
import time
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')


conn = sqlite3.connect('c:/users/백/tutorial.db')
c = conn.cursor()

def create_table():   #테이블 만들기
    c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(unix REAL, datestamp TEXT, keyword TEXT, value REAL)')
    c.execute('CREATE TABLE stuffToPlot2(unix REAL, datestamp TEXT, keyword TEXT, value REAL)')

def data_entry():   #테이블에 데이터 넣기
    c.execute("INSERT INTO stuffToPlot VALUES(1452455, '2016-01-01', 'Python1', 5)")
    conn.commit()
    c.close()
    conn.close()

def dynamic_data_entry():    #변수로 데이터 넣기
    for i in range(20):
        unix = time.time()
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))
        keyword = 'Python2'
        value = random.randrange(0,10)
        #c.execute("INSERT INTO stuffToPlot (unix, datestamp, keyword, value) VALUES (?,?,?,?)",
         #         (unix, date, keyword, value))
        c.execute("INSERT INTO stuffToPlot2 (unix, datestamp, keyword, value) VALUES (?,?,?,?)",
                  (unix, date, keyword, value))

        conn.commit()
    c.close()
    conn.close()

    def D_N_ohlc(self, name):  # 1일~5일 ohlc확인

        self.kospi_kosdaq = self.comboBox_2.currentText()
        con = sqlite3.connect("c:/users/백/" + self.kospi_kosdaq + "_data.db")  # 기술적지표 추가된거에 추가
        # con = sqlite3.connect("c:/users/백/trace_" + self.kospi_kosdaq + ".db")   #원본에 추가(나중에 join으로 합치기)

        df = pd.read_sql("SELECT * FROM " + "'" + name + "' ", con, index_col=None)

        # if len(df['open']) > 0:  # 값이 없는것을 제외시킨다
        date = df['index']
        op = df['open'] * 0.1 * 10
        cl = df['close'] * 0.1 * 10
        hi = df['high'] * 0.1 * 10
        lo = df['low'] * 0.1 * 10
        ch = df['change_ratio'] * 0.1 * 10
        v10mar = df['vma10_R']

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

def read_from_db():   #데이터 가져오기
    #c.execute('SELECT * FROM stuffToPlot')   #stuffToPlot 테이블을 선택
    c.execute('SELECT keyword, unix FROM stuffToPlot')   #stuffToPlot 테이블에서 불러오고 싶은 열만 선택
    #c.execute("SELECT * FROM stuffToPlot WHERE value=3 AND keyword = 'Python'")  # value가 3 이고 keyword 가 Python인 데이터만 선택
    c.execute("SELECT * FROM stuffToPlot WHERE unix > 1452618731")  # unix가 1452618731보다 큰것만 선택
    #data = c.fetchall()  #fetch - 가지고 오다.
    #print(data)
    for row in c.fetchall(): #한줄씩 출력
        #print(row)
        print(row[0])  #첫번째 데이터만 출력

def graph_data():   #데이터를 가지고 그래프 그리기
    c.execute('SELECT unix, value FROM stuffToPlot')
    dates = []
    values = []

    for row in c.fetchall():
        #print(row[0])
        #print(datetime.datetime.fromtimestamp(row[0]))
        dates.append(datetime.datetime.fromtimestamp(row[0]))
        values.append(row[1])
    plt.plot_date(dates, values, '-')
    plt.show()

def del_and_update():
    #c.execute('SELECT * FROM stuffToPlot')
    #[print(row) for row in c.fetchall()]   #for 문을 한줄에 썼다?

    #c.execute('UPDATE stuffToPlot SET value = 99 WHERE value = 8')  #value 열의 값이 8인곳을 99로 고친다.
    #conn.commit()
    #c.execute('SELECT * FROM stuffToPlot')
    #[print(row) for row in c.fetchall()]  # for 문을 한줄에 썼다?

    #c.execute('DELETE FROM stuffToPlot WHERE value = 99')   #value열의 값이 99인곳을 지운다.
    #conn.commit()
    #print(50*'#')


    c.execute('SELECT * FROM stuffToPlot WHERE value = 2')
    [print(row) for row in c.fetchall()]   #fetchall 은 한번 쓰면 끝이다. 아래줄에서 다시 셀렉트 해줘야한다.
    c.execute('SELECT * FROM stuffToPlot WHERE value = 2')
    print(len(c.fetchall()))


    def past_Day_ohlc(self, name):  #전시점 tech 넣기

        self.kospi_kosdaq = self.comboBox_2.currentText()
        con = sqlite3.connect("c:/users/백/" + self.kospi_kosdaq + "_data.db")  # 기술적지표 추가된거에 추가
        # con = sqlite3.connect("c:/users/백/trace_" + self.kospi_kosdaq + ".db")   #원본에 추가(나중에 join으로 합치기)
        df = pd.read_sql("SELECT * FROM " + "'" + name + "' ", con, index_col=None)
        print(len(df['open']))
        if len(df['open']) > 0:  # 값이 없는것을 제외시킨다
            print("진입")
            df['date'] = df['index']
            df.drop("level_0", axis=1, inplace=True)  # column을 삭제하는 가장 좋은 방법은 drop을 사용하는 것입니다.
            df.drop("index", axis=1, inplace=True)  # column을 삭제하는 가장 좋은 방법은 drop을 사용하는 것입니다.

            op = df['open'] * 0.1 * 10
            cl = df['close'] * 0.1 * 10
            hi = df['high'] * 0.1 * 10
            lo = df['low'] * 0.1 * 10
            ch = df['change_ratio'] * 0.1 * 10
            v10 = df['vma10_R']
            dp_ma3 = df['dp_ma3']
            dp_ma5 = df['dp_ma5']
            dp_ma10 = df['dp_ma10']
            dp_ma20 = df['dp_ma20']
            dp_ma30 = df['dp_ma30']
            dp_ma40 = df['dp_ma40']
            dp_ma50 = df['dp_ma50']
            dp_ma60 = df['dp_ma60']
            dp_ma80 = df['dp_ma80']
            dp_ma100 = df['dp_ma100']
            dp_ma120 = df['dp_ma120']
            dp_ma240= df['dp_ma240']
            u_tail_R = df['u_tail_R']
            l_tail_R = df['l_tail_R']
            vol_d1_R = df['vol_d1_R']
            bband20_upR = df['bbands20_upR']
            bbands20_downR = df['bbands20_downR']
            bbands_width= df['bbands_width']

            #rsi5 = df['rsi5']
            rsi10 = df['rsi10']
            rsi20 = df['rsi20']
            #rsi30 = df['rsi30']
            #rsi40 = df['rsi40']
            #rsi50 = df['rsi50']
            rsi60 = df['rsi60']
            #rsi80 = df['rsi80']
            #rsi100 = df['rsi100']
            #rsi120 = df['rsi120']

            bf1_open_list = []
            bf1_close_list = []
            bf1_high_list = []
            bf1_low_list = []
            bf1_change_R_list = []
            bf1_v10maR_list = []

            bf1_dp_ma3 = []
            bf1_dp_ma5 = []
            bf1_dp_ma10 = []
            bf1_dp_ma20 = []
            bf1_dp_ma30 = []
            bf1_dp_ma40 = []
            bf1_dp_ma50 = []
            bf1_dp_ma60 = []
            bf1_dp_ma80 = []
            bf1_dp_ma100 = []
            bf1_dp_ma120 = []
            bf1_dp_ma240 = []
            bf1_u_tail_R_list = []
            bf1_l_tail_R_list = []
            bf1_vol_d1_R = []
            bf1_bband20_upR = []
            bf1_bbands20_downR = []
            bf1_bbands_width = []
            #bf1_rsi5 = []
            bf1_rsi10 = []
            bf1_rsi20 = []
            #bf1_rsi30 = []
            #bf1_rsi40 = []
            #bf1_rsi50 = []
            bf1_rsi60 = []
            #bf1_rsi80 = []
            #bf1_rsi100 = []
            #bf1_rsi120 = []


            bf2_open_list = []
            bf2_close_list = []
            bf2_high_list = []
            bf2_low_list = []
            bf2_change_R_list = []
            bf2_v10maR_list = []
            bf2_dp_ma3 = []
            bf2_dp_ma5 = []
            bf2_dp_ma10 = []
            bf2_dp_ma20 = []
            bf2_dp_ma30 = []
            bf2_dp_ma40 = []
            bf2_dp_ma50 = []
            bf2_dp_ma60 = []
            bf2_dp_ma80 = []
            bf2_dp_ma100 = []
            bf2_dp_ma120 = []
            bf2_dp_ma240 = []
            bf2_u_tail_R_list = []
            bf2_l_tail_R_list = []
            bf2_vol_d1_R = []
            bf2_bband20_upR = []
            bf2_bbands20_downR = []
            bf2_bbands_width = []
            #bf2_rsi5 = []
            bf2_rsi10 = []
            bf2_rsi20 = []
            #bf2_rsi30 = []
            #bf2_rsi40 = []
            #bf2_rsi50 = []
            bf2_rsi60 = []
            #bf2_rsi80 = []
            #bf2_rsi100 = []
            #bf2_rsi120 = []

            #bf3_open_list = []
            #bf3_close_list = []
            #bf3_high_list = []
            #bf3_low_list = []
            #bf3_change_R_list = []
            #bf3_v10maR_list = []
            #bf3_dp_ma3 = []
            #bf3_dp_ma5 = []
            #bf3_dp_ma10 = []
            #bf3_dp_ma20 = []
            #bf3_dp_ma30 = []
            #bf3_dp_ma40 = []
            #bf3_dp_ma50 = []
            #bf3_dp_ma60 = []
            #bf3_dp_ma80 = []
            #bf3_dp_ma100 = []
            #bf3_dp_ma120 = []
            #bf3_dp_ma240 = []
            #bf3_u_tail_R_list = []
            #bf3_l_tail_R_list = []
            #bf3_vol_d1_R = []
            #bf3_bband20_upR = []
            #bf3_bbands20_downR = []
            #bf3_bbands_width = []
            #bf3_rsi5 = []
            #bf3_rsi10 = []
            #bf3_rsi20 = []
            #bf3_rsi30 = []
            #bf3_rsi40 = []
            #bf3_rsi50 = []
            #bf3_rsi60 = []
            #bf3_rsi80 = []
            #bf3_rsi100 = []
            #bf3_rsi120 = []

            for i in range(len(op)):

                if i == 0:  # 가장 과거 데이터는 전일 정보가 없으므로 0추가 (과거 → 현재), 0부터 1을 더뺀다
                    bf1_open_list.append(0)
                    bf1_close_list.append(0)
                    bf1_high_list.append(0)
                    bf1_low_list.append(0)
                    bf1_change_R_list.append(0)
                    bf1_v10maR_list.append(0)

                    bf1_dp_ma3.append(0)
                    bf1_dp_ma5.append(0)
                    bf1_dp_ma10.append(0)
                    bf1_dp_ma20.append(0)
                    bf1_dp_ma30.append(0)
                    bf1_dp_ma40.append(0)
                    bf1_dp_ma50.append(0)
                    bf1_dp_ma60.append(0)
                    bf1_dp_ma80.append(0)
                    bf1_dp_ma100.append(0)
                    bf1_dp_ma120.append(0)
                    bf1_dp_ma240.append(0)
                    bf1_u_tail_R_list.append(0)
                    bf1_l_tail_R_list.append(0)
                    bf1_vol_d1_R.append(0)
                    bf1_bband20_upR.append(0)
                    bf1_bbands20_downR.append(0)
                    bf1_bbands_width.append(0)
                    #bf1_rsi5.append(0)
                    bf1_rsi10.append(0)
                    bf1_rsi20.append(0)
                    #bf1_rsi30.append(0)
                    #bf1_rsi40.append(0)
                    #bf1_rsi50.append(0)
                    bf1_rsi60.append(0)
                    #bf1_rsi80.append(0)
                    #bf1_rsi100.append(0)
                    #bf1_rsi120.append(0)

                    bf2_open_list.append(0)
                    bf2_close_list.append(0)
                    bf2_high_list.append(0)
                    bf2_low_list.append(0)
                    bf2_change_R_list.append(0)
                    bf2_v10maR_list.append(0)
                    bf2_dp_ma3.append(0)
                    bf2_dp_ma5.append(0)
                    bf2_dp_ma10.append(0)
                    bf2_dp_ma20.append(0)
                    bf2_dp_ma30.append(0)
                    bf2_dp_ma40.append(0)
                    bf2_dp_ma50.append(0)
                    bf2_dp_ma60.append(0)
                    bf2_dp_ma80.append(0)
                    bf2_dp_ma100.append(0)
                    bf2_dp_ma120.append(0)
                    bf2_dp_ma240.append(0)
                    bf2_u_tail_R_list.append(0)
                    bf2_l_tail_R_list.append(0)
                    bf2_vol_d1_R.append(0)
                    bf2_bband20_upR.append(0)
                    bf2_bbands20_downR.append(0)
                    bf2_bbands_width.append(0)
                    #bf2_rsi5.append(0)
                    bf2_rsi10.append(0)
                    bf2_rsi20.append(0)
                    #bf2_rsi30.append(0)
                    #bf2_rsi40.append(0)
                    #bf2_rsi50.append(0)
                    bf2_rsi60.append(0)
                    #bf2_rsi80.append(0)
                    #bf2_rsi100.append(0)
                    #bf2_rsi120.append(0)

                    #bf3_open_list.append(0)
                    #bf3_close_list.append(0)
                    #bf3_high_list.append(0)
                    #bf3_low_list.append(0)
                    #bf3_change_R_list.append(0)
                    #bf3_v10maR_list.append(0)
                    #bf3_dp_ma3.append(0)
                    #bf3_dp_ma5.append(0)
                    #bf3_dp_ma10.append(0)
                    #bf3_dp_ma20.append(0)
                    #bf3_dp_ma30.append(0)
                    #bf3_dp_ma40.append(0)
                    #bf3_dp_ma50.append(0)
                    #bf3_dp_ma60.append(0)
                    #bf3_dp_ma80.append(0)
                    #bf3_dp_ma100.append(0)
                    #bf3_dp_ma120.append(0)
                    #bf3_dp_ma240.append(0)
                    #bf3_u_tail_R_list.append(0)
                    #bf3_l_tail_R_list.append(0)
                    #bf3_vol_d1_R.append(0)
                    #bf3_bband20_upR.append(0)
                    #bf3_bbands20_downR.append(0)
                    #bf3_bbands_width.append(0)
                    #bf3_rsi5.append(0)
                    #bf3_rsi10.append(0)
                    #bf3_rsi20.append(0)
                    #bf3_rsi30.append(0)
                    #bf3_rsi40.append(0)
                    #bf3_rsi50.append(0)
                    #bf3_rsi60.append(0)
                    #bf3_rsi80.append(0)
                    #bf3_rsi100.append(0)
                    #bf3_rsi120.append(0)

                elif i == 1:  #둘째날 데이터

                    bf1_open_list.append(op[i-1])
                    bf1_close_list.append(cl[i-1])
                    bf1_high_list.append(hi[i-1])
                    bf1_low_list.append(lo[i-1])
                    bf1_change_R_list.append(ch[i-1])
                    bf1_v10maR_list.append(v10[i-1])

                    bf1_dp_ma3.append(dp_ma3[i-1])
                    bf1_dp_ma5.append(dp_ma5[i-1])
                    bf1_dp_ma10.append(dp_ma10[i-1])
                    bf1_dp_ma20.append(dp_ma20[i-1])
                    bf1_dp_ma30.append(dp_ma30[i-1])
                    bf1_dp_ma40.append(dp_ma40[i-1])
                    bf1_dp_ma50.append(dp_ma50[i-1])
                    bf1_dp_ma60.append(dp_ma60[i-1])
                    bf1_dp_ma80.append(dp_ma80[i-1])
                    bf1_dp_ma100.append(dp_ma100[i-1])
                    bf1_dp_ma120.append(dp_ma120[i-1])
                    bf1_dp_ma240.append(dp_ma240[i-1])
                    bf1_u_tail_R_list.append(u_tail_R[i-1])
                    bf1_l_tail_R_list.append(l_tail_R[i-1])
                    bf1_vol_d1_R.append(vol_d1_R[i-1])
                    bf1_bband20_upR.append(bband20_upR[i-1])
                    bf1_bbands20_downR.append(bbands20_downR[i-1])
                    bf1_bbands_width.append(bbands_width[i-1])

                    #bf1_rsi5.append(rsi5[i-1])
                    bf1_rsi10.append(rsi10[i-1])
                    bf1_rsi20.append(rsi20[i-1])

                    #bf1_rsi30.append(rsi30[i-1])
                    #bf1_rsi40.append(rsi40[i-1])
                    #bf1_rsi50.append(rsi50[i-1])
                    bf1_rsi60.append(rsi60[i-1])

                    #bf1_rsi80.append(rsi80[i-1])
                    #bf1_rsi100.append(rsi100[i-1])
                    #bf1_rsi120.append(rsi120[i-1])

                    bf2_open_list.append(0)
                    bf2_close_list.append(0)
                    bf2_high_list.append(0)
                    bf2_low_list.append(0)
                    bf2_change_R_list.append(0)
                    bf2_v10maR_list.append(0)
                    bf2_dp_ma3.append(0)
                    bf2_dp_ma5.append(0)
                    bf2_dp_ma10.append(0)
                    bf2_dp_ma20.append(0)
                    bf2_dp_ma30.append(0)
                    bf2_dp_ma40.append(0)
                    bf2_dp_ma50.append(0)
                    bf2_dp_ma60.append(0)
                    bf2_dp_ma80.append(0)
                    bf2_dp_ma100.append(0)
                    bf2_dp_ma120.append(0)
                    bf2_dp_ma240.append(0)
                    bf2_u_tail_R_list.append(0)
                    bf2_l_tail_R_list.append(0)
                    bf2_vol_d1_R.append(0)
                    bf2_bband20_upR.append(0)
                    bf2_bbands20_downR.append(0)
                    bf2_bbands_width.append(0)
                    #bf2_rsi5.append(0)
                    bf2_rsi10.append(0)
                    bf2_rsi20.append(0)
                    #bf2_rsi30.append(0)
                    #bf2_rsi40.append(0)
                    #bf2_rsi50.append(0)
                    bf2_rsi60.append(0)
                    #bf2_rsi80.append(0)
                    #bf2_rsi100.append(0)
                    #bf2_rsi120.append(0)

                    #bf3_open_list.append(0)
                    #bf3_close_list.append(0)
                    #bf3_high_list.append(0)
                    #bf3_low_list.append(0)
                    #bf3_change_R_list.append(0)
                    #bf3_v10maR_list.append(0)
                    #bf3_dp_ma3.append(0)
                    #bf3_dp_ma5.append(0)
                    #bf3_dp_ma10.append(0)
                    #bf3_dp_ma20.append(0)
                    #bf3_dp_ma30.append(0)
                    #bf3_dp_ma40.append(0)
                    #bf3_dp_ma50.append(0)
                    #bf3_dp_ma60.append(0)
                    #bf3_dp_ma80.append(0)
                    #bf3_dp_ma100.append(0)
                    #bf3_dp_ma120.append(0)
                    #bf3_dp_ma240.append(0)
                    #bf3_u_tail_R_list.append(0)
                    #bf3_l_tail_R_list.append(0)
                    #bf3_vol_d1_R.append(0)
                    #bf3_bband20_upR.append(0)
                    #bf3_bbands20_downR.append(0)
                    #bf3_bbands_width.append(0)
                    #bf3_rsi5.append(0)
                    #bf3_rsi10.append(0)
                    #bf3_rsi20.append(0)
                    #bf3_rsi30.append(0)
                    #bf3_rsi40.append(0)
                    #bf3_rsi50.append(0)
                    #bf3_rsi60.append(0)
                    #bf3_rsi80.append(0)
                    #bf3_rsi100.append(0)
                    #bf3_rsi120.append(0)

                #elif i == 2:
                else:

                    bf1_open_list.append(op[i - 1])
                    bf1_close_list.append(cl[i - 1])
                    bf1_high_list.append(hi[i - 1])
                    bf1_low_list.append(lo[i - 1])
                    bf1_change_R_list.append(ch[i - 1])
                    bf1_v10maR_list.append(v10[i - 1])
                    bf1_dp_ma3.append(dp_ma3[i - 1])
                    bf1_dp_ma5.append(dp_ma5[i - 1])
                    bf1_dp_ma10.append(dp_ma10[i - 1])
                    bf1_dp_ma20.append(dp_ma20[i - 1])
                    bf1_dp_ma30.append(dp_ma30[i - 1])
                    bf1_dp_ma40.append(dp_ma40[i - 1])
                    bf1_dp_ma50.append(dp_ma50[i - 1])
                    bf1_dp_ma60.append(dp_ma60[i - 1])
                    bf1_dp_ma80.append(dp_ma80[i - 1])
                    bf1_dp_ma100.append(dp_ma100[i - 1])
                    bf1_dp_ma120.append(dp_ma120[i - 1])
                    bf1_dp_ma240.append(dp_ma240[i - 1])
                    bf1_u_tail_R_list.append(u_tail_R[i - 1])
                    bf1_l_tail_R_list.append(l_tail_R[i - 1])
                    bf1_vol_d1_R.append(vol_d1_R[i - 1])
                    bf1_bband20_upR.append(bband20_upR[i - 1])
                    bf1_bbands20_downR.append(bbands20_downR[i - 1])
                    bf1_bbands_width.append(bbands_width[i - 1])
                    # bf1_rsi5.append(rsi5[i-1])
                    bf1_rsi10.append(rsi10[i - 1])
                    bf1_rsi20.append(rsi20[i - 1])
                    # bf1_rsi30.append(rsi30[i-1])
                    # bf1_rsi40.append(rsi40[i-1])
                    # bf1_rsi50.append(rsi50[i-1])
                    bf1_rsi60.append(rsi60[i - 1])
                    # bf1_rsi80.append(rsi80[i-1])
                    # bf1_rsi100.append(rsi100[i-1])
                    # bf1_rsi120.append(rsi120[i-1])

                    bf2_open_list.append(op[i - 2])
                    bf2_close_list.append(cl[i - 2])
                    bf2_high_list.append(hi[i - 2])
                    bf2_low_list.append(lo[i - 2])
                    bf2_change_R_list.append(ch[i - 2])
                    bf2_v10maR_list.append(v10[i - 2])
                    bf2_dp_ma3.append(dp_ma3[i - 2])
                    bf2_dp_ma5.append(dp_ma5[i - 2])
                    bf2_dp_ma10.append(dp_ma10[i - 2])
                    bf2_dp_ma20.append(dp_ma20[i - 2])
                    bf2_dp_ma30.append(dp_ma30[i - 2])
                    bf2_dp_ma40.append(dp_ma40[i - 2])
                    bf2_dp_ma50.append(dp_ma50[i - 2])
                    bf2_dp_ma60.append(dp_ma60[i - 2])
                    bf2_dp_ma80.append(dp_ma80[i - 2])
                    bf2_dp_ma100.append(dp_ma100[i - 2])
                    bf2_dp_ma120.append(dp_ma120[i - 2])
                    bf2_dp_ma240.append(dp_ma240[i - 2])
                    bf2_u_tail_R_list.append(u_tail_R[i - 2])
                    bf2_l_tail_R_list.append(l_tail_R[i - 2])
                    bf2_vol_d1_R.append(vol_d1_R[i - 2])
                    bf2_bband20_upR.append(bband20_upR[i - 2])
                    bf2_bbands20_downR.append(bbands20_downR[i - 2])
                    bf2_bbands_width.append(bbands_width[i - 2])

                    #bf2_rsi5.append(rsi5[i - 2])
                    bf2_rsi10.append(rsi10[i - 2])
                    bf2_rsi20.append(rsi20[i - 2])
                    #bf2_rsi30.append(rsi30[i - 2])
                    #bf2_rsi40.append(rsi40[i - 2])
                    #bf2_rsi50.append(rsi50[i - 2])
                    bf2_rsi60.append(rsi60[i - 2])
                    #bf2_rsi80.append(rsi80[i - 2])
                    #bf2_rsi100.append(rsi100[i - 2])
                    #bf2_rsi120.append(rsi120[i - 2])


                    #bf3_open_list.append(0)
                    #bf3_close_list.append(0)
                    #bf3_high_list.append(0)
                    #bf3_low_list.append(0)
                    #bf3_change_R_list.append(0)
                    #bf3_v10maR_list.append(0)
                    #bf3_dp_ma3.append(0)
                    #bf3_dp_ma5.append(0)
                    #bf3_dp_ma10.append(0)
                    #bf3_dp_ma20.append(0)
                    #bf3_dp_ma30.append(0)
                    #bf3_dp_ma40.append(0)
                    #bf3_dp_ma50.append(0)
                    #bf3_dp_ma60.append(0)
                    #bf3_dp_ma80.append(0)
                    #bf3_dp_ma100.append(0)
                    #bf3_dp_ma120.append(0)
                    #bf3_dp_ma240.append(0)
                    #bf3_u_tail_R_list.append(0)
                    #bf3_l_tail_R_list.append(0)
                    #bf3_vol_d1_R.append(0)
                    #bf3_bband20_upR.append(0)
                    #bf3_bbands20_downR.append(0)
                    #bf3_bbands_width.append(0)
                    #bf3_rsi5.append(0)
                    #bf3_rsi10.append(0)
                    #bf3_rsi20.append(0)
                    #bf3_rsi30.append(0)
                    #bf3_rsi40.append(0)
                    #bf3_rsi50.append(0)
                    #bf3_rsi60.append(0)
                    #bf3_rsi80.append(0)
                    #bf3_rsi100.append(0)
                    #bf3_rsi120.append(0)

                #else:

                    #bf1_open_list.append(op[i - 1])
                    #bf1_close_list.append(cl[i - 1])
                    #bf1_high_list.append(hi[i - 1])
                    #bf1_low_list.append(lo[i - 1])
                    #bf1_change_R_list.append(ch[i - 1])
                    #bf1_v10maR_list.append(v10[i - 1])
                    #bf1_dp_ma3.append(dp_ma3[i - 1])
                    #bf1_dp_ma5.append(dp_ma5[i - 1])
                    #bf1_dp_ma10.append(dp_ma10[i - 1])
                    #bf1_dp_ma20.append(dp_ma20[i - 1])
                    #bf1_dp_ma30.append(dp_ma30[i - 1])
                    #bf1_dp_ma40.append(dp_ma40[i - 1])
                    #bf1_dp_ma50.append(dp_ma50[i - 1])
                    #bf1_dp_ma60.append(dp_ma60[i - 1])
                    #bf1_dp_ma80.append(dp_ma80[i - 1])
                    #bf1_dp_ma100.append(dp_ma100[i - 1])
                    #bf1_dp_ma120.append(dp_ma120[i - 1])
                    #bf1_dp_ma240.append(dp_ma240[i - 1])
                    #bf1_u_tail_R_list.append(u_tail_R[i - 1])
                    #bf1_l_tail_R_list.append(l_tail_R[i - 1])
                    #bf1_vol_d1_R.append(vol_d1_R[i - 1])
                    #bf1_bband20_upR.append(bband20_upR[i - 1])
                    #bf1_bbands20_downR.append(bbands20_downR[i - 1])
                    #bf1_bbands_width.append(bbands_width[i - 1])
                    # bf1_rsi5.append(rsi5[i-1])
                    #bf1_rsi10.append(rsi10[i - 1])
                    #bf1_rsi20.append(rsi20[i - 1])
                    # bf1_rsi30.append(rsi30[i-1])
                    # bf1_rsi40.append(rsi40[i-1])
                    # bf1_rsi50.append(rsi50[i-1])
                    #bf1_rsi60.append(rsi60[i - 1])
                    # bf1_rsi80.append(rsi80[i-1])
                    # bf1_rsi100.append(rsi100[i-1])
                    # bf1_rsi120.append(rsi120[i-1])

                    #bf2_open_list.append(op[i - 2])
                    #bf2_close_list.append(cl[i - 2])
                    #bf2_high_list.append(hi[i - 2])
                    #bf2_low_list.append(lo[i - 2])
                    #bf2_change_R_list.append(ch[i - 2])
                    #bf2_v10maR_list.append(v10[i - 2])

                    #bf2_dp_ma3.append(dp_ma3[i - 2])
                    #bf2_dp_ma5.append(dp_ma5[i - 2])
                    #bf2_dp_ma10.append(dp_ma10[i - 2])
                    #bf2_dp_ma20.append(dp_ma20[i - 2])
                    #bf2_dp_ma30.append(dp_ma30[i - 2])
                    #bf2_dp_ma40.append(dp_ma40[i - 2])
                    #bf2_dp_ma50.append(dp_ma50[i - 2])
                    #bf2_dp_ma60.append(dp_ma60[i - 2])
                    #bf2_dp_ma80.append(dp_ma80[i - 2])
                    #bf2_dp_ma100.append(dp_ma100[i - 2])
                    #bf2_dp_ma120.append(dp_ma120[i - 2])
                    #bf2_dp_ma240.append(dp_ma240[i - 2])
                    #bf2_u_tail_R_list.append(u_tail_R[i - 2])
                    #bf2_l_tail_R_list.append(l_tail_R[i - 2])
                    #bf2_vol_d1_R.append(vol_d1_R[i - 2])
                    #bf2_bband20_upR.append(bband20_upR[i - 2])
                    #bf2_bbands20_downR.append(bbands20_downR[i - 2])
                    #bf2_bbands_width.append(bbands_width[i - 2])
                    #bf2_rsi5.append(rsi5[i - 2])
                    #bf2_rsi10.append(rsi10[i - 2])
                    #bf2_rsi20.append(rsi20[i - 2])
                    #bf2_rsi30.append(rsi30[i - 2])
                    #bf2_rsi40.append(rsi40[i - 2])
                    #bf2_rsi50.append(rsi50[i - 2])
                    #bf2_rsi60.append(rsi60[i - 2])
                    #bf2_rsi80.append(rsi80[i - 2])
                    #bf2_rsi100.append(rsi100[i - 2])
                    #bf2_rsi120.append(rsi120[i - 2])

                    #bf3_open_list.append(op[i - 3])
                    #bf3_close_list.append(cl[i - 3])
                    #bf3_high_list.append(hi[i - 3])
                    #bf3_low_list.append(lo[i - 3])
                    #bf3_change_R_list.append(ch[i - 3])
                    #bf3_v10maR_list.append(v10[i - 3])

                    #bf3_dp_ma3.append(dp_ma3[i - 3])
                    #bf3_dp_ma5.append(dp_ma5[i - 3])
                    #bf3_dp_ma10.append(dp_ma10[i - 3])
                    #bf3_dp_ma20.append(dp_ma20[i - 3])
                    #bf3_dp_ma30.append(dp_ma30[i - 3])
                    #bf3_dp_ma40.append(dp_ma40[i - 3])
                    #bf3_dp_ma50.append(dp_ma50[i - 3])
                    #bf3_dp_ma60.append(dp_ma60[i - 3])
                    #bf3_dp_ma80.append(dp_ma80[i - 3])
                    #bf3_dp_ma100.append(dp_ma100[i - 3])
                    #bf3_dp_ma120.append(dp_ma120[i - 3])
                    #bf3_dp_ma240.append(dp_ma240[i - 3])
                    #bf3_u_tail_R_list.append(u_tail_R[i - 3])
                    #bf3_l_tail_R_list.append(l_tail_R[i - 3])
                    #bf3_vol_d1_R.append(vol_d1_R[i - 3])
                    #bf3_bband20_upR.append(bband20_upR[i - 3])
                    #bf3_bbands20_downR.append(bbands20_downR[i - 3])
                    #bf3_bbands_width.append(bbands_width[i - 3])
                    #bf3_rsi5.append(rsi5[i - 3])
                    #bf3_rsi10.append(rsi10[i - 3])
                    #bf3_rsi20.append(rsi20[i - 3])
                    #bf3_rsi30.append(rsi30[i - 3])
                    #bf3_rsi40.append(rsi40[i - 3])
                    #bf3_rsi50.append(rsi50[i - 3])
                    #bf3_rsi60.append(rsi60[i - 3])
                    #bf3_rsi80.append(rsi80[i - 3])
                    #bf3_rsi100.append(rsi100[i - 3])
                    #bf3_rsi120.append(rsi120[i - 3])


            df['bf1_open_list'] = bf1_open_list
            df['bf1_close_list'] = bf1_close_list
            df['bf1_high_list'] = bf1_high_list
            df['bf1_low_list'] = bf1_low_list
            df['bf1_change_R_list'] =bf1_change_R_list
            df['bf1_v10maR_list'] =bf1_v10maR_list
            df['bf1_dp_ma3'] = bf1_dp_ma3
            df['bf1_dp_ma5'] = bf1_dp_ma5
            df['bf1_dp_ma10'] = bf1_dp_ma10
            df['bf1_dp_ma20'] =bf1_dp_ma20
            df['bf1_dp_ma30'] =bf1_dp_ma30
            df['bf1_dp_ma40'] =bf1_dp_ma40
            df['bf1_dp_ma50'] =bf1_dp_ma50
            df['bf1_dp_ma60'] =bf1_dp_ma60
            df['bf1_dp_ma80'] =bf1_dp_ma80
            df['bf1_dp_ma100'] =bf1_dp_ma100
            df['bf1_dp_ma120'] =bf1_dp_ma120
            df['bf1_dp_ma240'] =bf1_dp_ma240
            df['bf1_u_tail_R_list'] =bf1_u_tail_R_list
            df['bf1_l_tail_R_list'] =bf1_l_tail_R_list
            df['bf1_vol_d1_R'] =bf1_vol_d1_R
            df['bf1_bband20_upR'] =bf1_bband20_upR
            df['bf1_bbands20_downR'] =bf1_bbands20_downR
            df['bf1_bbands_width'] =bf1_bbands_width
            #df['bf1_rsi5'] =bf1_rsi5
            df['bf1_rsi10'] =bf1_rsi10
            df['bf1_rsi20'] =bf1_rsi20
            #df['bf1_rsi30'] =bf1_rsi30
            #df['bf1_rsi40'] =bf1_rsi40
            #df['bf1_rsi50'] =bf1_rsi50
            df['bf1_rsi60'] =bf1_rsi60
            #df['bf1_rsi80'] =bf1_rsi80
            #df['bf1_rsi100'] =bf1_rsi100
            #df['bf1_rsi120'] =bf1_rsi120

            df['bf2_open_list'] = bf2_open_list
            df['bf2_close_list'] = bf2_close_list
            df['bf2_high_list'] = bf2_high_list
            df['bf2_low_list'] = bf2_low_list
            df['bf2_change_R_list'] = bf2_change_R_list
            df['bf2_v10maR_list'] = bf2_v10maR_list
            df['bf2_dp_ma3'] = bf2_dp_ma3
            df['bf2_dp_ma5'] = bf2_dp_ma5
            df['bf2_dp_ma10'] = bf2_dp_ma10
            df['bf2_dp_ma20'] = bf2_dp_ma20
            df['bf2_dp_ma30'] = bf2_dp_ma30
            df['bf2_dp_ma40'] = bf2_dp_ma40
            df['bf2_dp_ma50'] = bf2_dp_ma50
            df['bf2_dp_ma60'] = bf2_dp_ma60
            df['bf2_dp_ma80'] = bf2_dp_ma80
            df['bf2_dp_ma100'] = bf2_dp_ma100
            df['bf2_dp_ma120'] = bf2_dp_ma120
            df['bf2_dp_ma240'] = bf2_dp_ma240
            df['bf2_u_tail_R_list'] = bf2_u_tail_R_list
            df['bf2_l_tail_R_list'] = bf2_l_tail_R_list
            df['bf2_vol_d1_R'] = bf2_vol_d1_R
            df['bf2_bband20_upR'] = bf2_bband20_upR
            df['bf2_bbands20_downR'] = bf2_bbands20_downR
            df['bf2_bbands_width'] = bf2_bbands_width
            #df['bf2_rsi5'] = bf2_rsi5
            df['bf2_rsi10'] = bf2_rsi10
            df['bf2_rsi20'] = bf2_rsi20
            #df['bf2_rsi30'] = bf2_rsi30
            #df['bf2_rsi40'] = bf2_rsi40
            #df['bf2_rsi50'] = bf2_rsi50
            df['bf2_rsi60'] = bf2_rsi60
            #df['bf2_rsi80'] = bf2_rsi80
            #df['bf2_rsi100'] = bf2_rsi100
            #df['bf2_rsi120'] = bf2_rsi120

            #df['bf3_open_list'] = bf3_open_list
            #df['bf3_close_list'] = bf3_close_list
            #df['bf3_high_list'] = bf3_high_list
            #df['bf3_low_list'] = bf3_low_list
            #df['bf3_change_R_list'] = bf3_change_R_list
            #df['bf3_v10maR_list'] = bf3_v10maR_list
            #df['bf3_dp_ma3'] = bf3_dp_ma3
            #df['bf3_dp_ma5'] = bf3_dp_ma5
            #df['bf3_dp_ma10'] = bf3_dp_ma10
            #df['bf3_dp_ma20'] = bf3_dp_ma20
            #df['bf3_dp_ma30'] = bf3_dp_ma30
            #df['bf3_dp_ma40'] = bf3_dp_ma40
            #df['bf3_dp_ma50'] = bf3_dp_ma50
            #df['bf3_dp_ma60'] = bf3_dp_ma60
            #df['bf3_dp_ma80'] = bf3_dp_ma80
            #df['bf3_dp_ma100'] = bf3_dp_ma100
            #df['bf3_dp_ma120'] = bf3_dp_ma120
            #df['bf3_dp_ma240'] = bf3_dp_ma240
            #df['bf3_u_tail_R_list'] = bf3_u_tail_R_list
            #df['bf3_l_tail_R_list'] = bf3_l_tail_R_list
            #df['bf3_vol_d1_R'] = bf3_vol_d1_R
            #df['bf3_bband20_upR'] = bf3_bband20_upR
            #df['bf3_bbands20_downR'] = bf3_bbands20_downR
            #df['bf3_bbands_width'] = bf3_bbands_width
            #df['bf3_rsi5'] = bf3_rsi5
            #df['bf3_rsi10'] = bf3_rsi10
            #df['bf3_rsi20'] = bf3_rsi20
            #df['bf3_rsi30'] = bf3_rsi30
            #df['bf3_rsi40'] = bf3_rsi40
            #df['bf3_rsi50'] = bf3_rsi50
            #df['bf3_rsi60'] = bf3_rsi60
            #df['bf3_rsi80'] = bf3_rsi80
            #df['bf3_rsi100'] = bf3_rsi100
            #df['bf3_rsi120'] = bf3_rsi120
            print("완료1")
        con.close()
        print("완료2")
        return df
    def tech__(self, name):    #한종목의 기술적 지표 계산
        self.kospi_kosdaq = self.comboBox_2.currentText()

        con = sqlite3.connect("c:/users/백/stock_" + self.kospi_kosdaq + "_vol_ma.db")

        df = pd.read_sql("SELECT * FROM "+ "'"+ name +"' ", con, index_col=None) #df = pd.read_sql("SELECT * FROM CMG제약 ", con , index_col = None)
        df.sort_index(inplace= True, ascending= False)  #인덱스 기준으로 역으로 정렬


        if len(df['open']) > 0:  #값이 없는것을 제외시킨다

            op = df['open'] * 0.1 * 10
            cl = df['close'] * 0.1 * 10
            hi = df['high'] * 0.1 * 10
            lo = df['low'] * 0.1 * 10
            vo = df['volume'] * 0.1 * 10


            #df['ma3'] = ta.SMA(cl, 3)
            #df['ma5'] = ta.SMA(cl, 5)
            #df['ma10'] = ta.SMA(cl, 10)
            #df['ma20'] = ta.SMA(cl, 20)
            #df['ma60'] = ta.SMA(cl, 60)
            #df['ma120'] = ta.SMA(cl, 120)
            #df['ma240'] = ta.SMA(cl, 240)

            dfma3 = ta.SMA(cl, 3)

            dfma5 = ta.SMA(cl, 5)

            dfma10 = ta.SMA(cl, 10)
            dfma20 = ta.SMA(cl, 20)

            dfma30 = ta.SMA(cl, 30)
            dfma40 = ta.SMA(cl, 40)
            dfma50 = ta.SMA(cl, 50)

            dfma60 = ta.SMA(cl, 60)

            dfma80 = ta.SMA(cl, 80)
            dfma100 = ta.SMA(cl, 100)

            dfma120 = ta.SMA(cl, 120)
            dfma240 = ta.SMA(cl, 240)

            #df['vma10_R'] = vo / ta.SMA(vo, 10)
            #df['dp_ma3'] = cl / df['ma3']
            #df['dp_ma5'] = cl / df['ma5']
            #df['dp_ma10'] = cl / df['ma10']
            #df['dp_ma20'] = cl / df['ma20']
            #df['dp_ma60'] = cl / df['ma60']
            #df['dp_ma120'] = cl / df['ma120']
            #df['dp_ma240'] = cl / df['ma240']

            df['vma10_R'] = vo / ta.SMA(vo, 10)

            df['dp_ma3'] = cl / dfma3

            df['dp_ma5'] = cl / dfma5

            df['dp_ma10'] = cl / dfma10
            df['dp_ma20'] = cl / dfma20

            df['dp_ma30'] = cl / dfma30
            df['dp_ma40'] = cl / dfma40
            df['dp_ma50'] = cl / dfma50

            df['dp_ma60'] = cl / dfma60

            df['dp_ma80'] = cl / dfma80
            df['dp_ma100'] = cl / dfma100

            df['dp_ma120'] = cl / dfma120
            df['dp_ma240'] = cl / dfma240

            #df['dp_ma3'] = cl / df['ma3']
            #df['dp_ma5'] = cl / df['ma5']
            #df['dp_ma10'] = cl / df['ma10']
            #df['dp_ma20'] = cl / df['ma20']
            #df['dp_ma60'] = cl / df['ma60']
            #df['dp_ma120'] = cl / df['ma120']
            #df['dp_ma240'] = cl / df['ma240']


            bbands30 = pd.Series(ta.BBANDS(cl, timeperiod=30, nbdevup=1.8, nbdevdn=1.8))  # 밴드는 또 Series를 만들었다가
            df['bbands30_upR'] = cl/bbands30[0]  # 하나씩 일일이 인덱싱해줘야 함.
            #df['bbands30_mov'] = bbands30[1]
            df['bbands30_downR'] = cl/bbands30[2]
            df['bbands_width'] = (bbands30[0] - bbands30[2]) / cl

            macd = pd.Series(ta.MACD(cl, 10, 15, 7))  # 밴드는 또 Series를 만들었다가
            df['macd_line'] = macd[0]  # 하나씩 일일이 인덱싱해줘야 함.
            df['macd_sig'] = macd[1]
            df['macd_histo'] = macd[2]

            df['rsi5'] = ta.RSI(cl, 5)

            df['rsi10'] = ta.RSI(cl, 10)
            df['rsi20'] = ta.RSI(cl, 20)
            df['rsi30'] = ta.RSI(cl, 5)
            df['rsi40'] = ta.RSI(cl, 5)
            df['rsi50'] = ta.RSI(cl, 5)
            df['rsi60'] = ta.RSI(cl, 60)
            df['rsi80'] = ta.RSI(cl, 60)
            df['rsi100'] = ta.RSI(cl, 60)
            df['rsi120'] = ta.RSI(cl, 60)

        return df


    def chooga_yul(self):  #한종목의 한열만 추가
        self.kospi_kosdaq = self.comboBox_2.currentText()
        con = sqlite3.connect("c:/users/백/" + self.kospi_kosdaq + "_data.db")

        #df = pd.read_sql("SELECT * FROM " + "'" + name + "' ", con,
         #                index_col=None)
        df = pd.read_sql("SELECT * FROM CMG제약 ", con , index_col = None)

        if len(df['open']) > 0:  # 값이 없는것을 제외시킨다
            op = df['open'] * 0.1 * 10
            cl = df['close'] * 0.1 * 10
            hi = df['high'] * 0.1 * 10
            lo = df['low'] * 0.1 * 10
            vo = df['volume'] * 0.1 * 10
            change_R = df['change_ratio']
            ma5 = df['ma5'] * 0.1 * 10
            df['yesterD_cl'] = (cl / (1 + change_R)) * 0.1 * 10  #전일 종가 구하기
            yesterD_cl = df['yesterD_cl']

            bong = (cl - op) / yesterD_cl  # 전일 종가 기준 봉사이즈
            upper_tail = (hi - cl) / yesterD_cl  #윗꼬리 비율구하기
            lower_tail = (cl - lo) /yesterD_cl   #아랫꼬리 비율구하기

            macd = pd.Series(ta.MACD(cl, 10, 15, 7))  # 밴드는 또 Series를 만들었다가
            macd_line = macd[0]  # 하나씩 일일이 인덱싱해줘야 함.
            macd_sig = macd[1]
            macd_histo = macd[2]


        return bong




    def backup_add_one_col_tech(self):  #한열만 추가
        self.kospi_kosdaq = self.comboBox_2.currentText()

        con = sqlite3.connect("c:/users/백/stock_" + self.kospi_kosdaq + "data2.db")

        df = pd.read_sql("SELECT * FROM " + "'" + name + "' ", con,
                         index_col=None)  # df = pd.read_sql("SELECT * FROM CMG제약 ", con , index_col = None)

        if len(df['open']) > 0:  # 값이 없는것을 제외시킨다

            op = df['open'] * 0.1 * 10
            cl = df['close'] * 0.1 * 10
            hi = df['high'] * 0.1 * 10
            lo = df['low'] * 0.1 * 10
            vo = df['volume'] * 0.1 * 10
            change_R = df['change_ratio']
            df['yesterD_cl'] = (cl / (1+ change_R)) *0.1 *10

            vol_d1_R = []  # 전일대비 거래량 비율 구하기
            D1_profit_list = []  # 익일 종가 - 당일종가 비율
            D1_open_list = []  # 익일 시가
            D1_high_list = []  # 익일 고가
            D1_low_list = []  # 익일 저가
            D1_close_list = []  # 익일 종가


            for i in range(len(op)):

                if i == 0:  # 첫번째 데이터는 전일 정보가 없으므로 0추가
                    vol_d1_R.append(0)

                elif vo[i - 1] == 0:  # 0으로 나누는 경우 error방지
                    vol_d1_R.append(0)

                else:
                    vol_d1_Ratio = vo[i] / vo[i - 1]  # i=오늘, i-1 = 어제 i가 커질수록 과거에서 미래로 가는것임. 전일대비 거래량
                    # print(i,":", vo[i], ":", vo[i-1], ";", vol_d1_Ratio)
                    vol_d1_R.append(vol_d1_Ratio)
                    # print(vol_d1_R)

            for i in range(len(op)):
                if i == len(op) - 1:  # 가장 최근 데이터는 익일 정보가 없으므로 0추가
                    D1_profit_list.append(0)
                    D1_open_list.append(0)
                    D1_high_list.append(0)
                    D1_low_list.append(0)
                    D1_close_list.append(0)

                elif cl[i] == 0:  # 0으로 나누는 경우 error방지
                    D1_profit_list.append(0)

                else:
                    D1_profit = (cl[i + 1] - cl[i]) / cl[i]
                    D1_profit_list.append(D1_profit)
                    D1_open_list.append(op[i + 1])
                    D1_high_list.append(hi[i + 1])
                    D1_low_list.append(lo[i + 1])
                    D1_close_list.append(cl[i + 1])

            df['vol_d1_R'] = vol_d1_R
            df['D1_open'] = D1_open_list
            df['D1_high'] = D1_high_list
            df['D1_low'] = D1_low_list
            df['D1_close'] = D1_close_list
            df['D1_profit'] = D1_profit_list  # 종가거래 하루 수익
        return df


    def past_Day_ohlc(self, name):  #전시점 tech 넣기

        self.kospi_kosdaq = self.comboBox_2.currentText()
        con = sqlite3.connect("c:/users/백/" + self.kospi_kosdaq + "_data.db")  # 기술적지표 추가된거에 추가
        # con = sqlite3.connect("c:/users/백/trace_" + self.kospi_kosdaq + ".db")   #원본에 추가(나중에 join으로 합치기)
        df = pd.read_sql("SELECT * FROM " + "'" + name + "' ", con, index_col=None)
        print(len(df['open']))
        if len(df['open']) > 0:  # 값이 없는것을 제외시킨다
            print("진입")
            df['date'] = df['index']
            df.drop("level_0", axis=1, inplace=True)  # column을 삭제하는 가장 좋은 방법은 drop을 사용하는 것입니다.
            df.drop("index", axis=1, inplace=True)  # column을 삭제하는 가장 좋은 방법은 drop을 사용하는 것입니다.

            op = df['open'] * 0.1 * 10
            cl = df['close'] * 0.1 * 10
            hi = df['high'] * 0.1 * 10
            lo = df['low'] * 0.1 * 10
            ch = df['change_ratio'] * 0.1 * 10
            v10 = df['vma10_R']
            dp_ma3 = df['dp_ma3']
            dp_ma5 = df['dp_ma5']
            dp_ma10 = df['dp_ma10']
            dp_ma20 = df['dp_ma20']
            dp_ma30 = df['dp_ma30']
            dp_ma40 = df['dp_ma40']
            dp_ma50 = df['dp_ma50']
            dp_ma60 = df['dp_ma60']
            dp_ma80 = df['dp_ma80']
            dp_ma100 = df['dp_ma100']
            dp_ma120 = df['dp_ma120']
            dp_ma240= df['dp_ma240']
            u_tail_R = df['u_tail_R']
            l_tail_R = df['l_tail_R']
            vol_d1_R = df['vol_d1_R']
            bband20_upR = df['bbands20_upR']
            bbands20_downR = df['bbands20_downR']
            bbands_width= df['bbands_width']

            #rsi5 = df['rsi5']
            rsi10 = df['rsi10']
            rsi20 = df['rsi20']
            #rsi30 = df['rsi30']
            #rsi40 = df['rsi40']
            #rsi50 = df['rsi50']
            rsi60 = df['rsi60']
            #rsi80 = df['rsi80']
            #rsi100 = df['rsi100']
            #rsi120 = df['rsi120']

            bf1_open_list = []
            bf1_close_list = []
            bf1_high_list = []
            bf1_low_list = []
            bf1_change_R_list = []
            bf1_v10maR_list = []

            bf1_dp_ma3 = []
            bf1_dp_ma5 = []
            bf1_dp_ma10 = []
            bf1_dp_ma20 = []
            bf1_dp_ma30 = []
            bf1_dp_ma40 = []
            bf1_dp_ma50 = []
            bf1_dp_ma60 = []
            bf1_dp_ma80 = []
            bf1_dp_ma100 = []
            bf1_dp_ma120 = []
            bf1_dp_ma240 = []
            bf1_u_tail_R_list = []
            bf1_l_tail_R_list = []
            bf1_vol_d1_R = []
            bf1_bband20_upR = []
            bf1_bbands20_downR = []
            bf1_bbands_width = []
            #bf1_rsi5 = []
            bf1_rsi10 = []
            bf1_rsi20 = []
            #bf1_rsi30 = []
            #bf1_rsi40 = []
            #bf1_rsi50 = []
            bf1_rsi60 = []
            #bf1_rsi80 = []
            #bf1_rsi100 = []
            #bf1_rsi120 = []


            bf2_open_list = []
            bf2_close_list = []
            bf2_high_list = []
            bf2_low_list = []
            bf2_change_R_list = []
            bf2_v10maR_list = []
            bf2_dp_ma3 = []
            bf2_dp_ma5 = []
            bf2_dp_ma10 = []
            bf2_dp_ma20 = []
            bf2_dp_ma30 = []
            bf2_dp_ma40 = []
            bf2_dp_ma50 = []
            bf2_dp_ma60 = []
            bf2_dp_ma80 = []
            bf2_dp_ma100 = []
            bf2_dp_ma120 = []
            bf2_dp_ma240 = []
            bf2_u_tail_R_list = []
            bf2_l_tail_R_list = []
            bf2_vol_d1_R = []
            bf2_bband20_upR = []
            bf2_bbands20_downR = []
            bf2_bbands_width = []
            #bf2_rsi5 = []
            bf2_rsi10 = []
            bf2_rsi20 = []
            #bf2_rsi30 = []
            #bf2_rsi40 = []
            #bf2_rsi50 = []
            bf2_rsi60 = []


            for i in range(len(op)):

                if i == 0:  # 가장 과거 데이터는 전일 정보가 없으므로 0추가 (과거 → 현재), 0부터 1을 더뺀다
                    bf1_open_list.append(0)
                    bf1_close_list.append(0)
                    bf1_high_list.append(0)
                    bf1_low_list.append(0)
                    bf1_change_R_list.append(0)
                    bf1_v10maR_list.append(0)

                    bf1_dp_ma3.append(0)
                    bf1_dp_ma5.append(0)
                    bf1_dp_ma10.append(0)
                    bf1_dp_ma20.append(0)
                    bf1_dp_ma30.append(0)
                    bf1_dp_ma40.append(0)
                    bf1_dp_ma50.append(0)
                    bf1_dp_ma60.append(0)
                    bf1_dp_ma80.append(0)
                    bf1_dp_ma100.append(0)
                    bf1_dp_ma120.append(0)
                    bf1_dp_ma240.append(0)
                    bf1_u_tail_R_list.append(0)
                    bf1_l_tail_R_list.append(0)
                    bf1_vol_d1_R.append(0)
                    bf1_bband20_upR.append(0)
                    bf1_bbands20_downR.append(0)
                    bf1_bbands_width.append(0)
                    #bf1_rsi5.append(0)
                    bf1_rsi10.append(0)
                    bf1_rsi20.append(0)
                    #bf1_rsi30.append(0)
                    #bf1_rsi40.append(0)
                    #bf1_rsi50.append(0)
                    bf1_rsi60.append(0)
                    #bf1_rsi80.append(0)
                    #bf1_rsi100.append(0)
                    #bf1_rsi120.append(0)

                    bf2_open_list.append(0)
                    bf2_close_list.append(0)
                    bf2_high_list.append(0)
                    bf2_low_list.append(0)
                    bf2_change_R_list.append(0)
                    bf2_v10maR_list.append(0)
                    bf2_dp_ma3.append(0)
                    bf2_dp_ma5.append(0)
                    bf2_dp_ma10.append(0)
                    bf2_dp_ma20.append(0)
                    bf2_dp_ma30.append(0)
                    bf2_dp_ma40.append(0)
                    bf2_dp_ma50.append(0)
                    bf2_dp_ma60.append(0)
                    bf2_dp_ma80.append(0)
                    bf2_dp_ma100.append(0)
                    bf2_dp_ma120.append(0)
                    bf2_dp_ma240.append(0)
                    bf2_u_tail_R_list.append(0)
                    bf2_l_tail_R_list.append(0)
                    bf2_vol_d1_R.append(0)
                    bf2_bband20_upR.append(0)
                    bf2_bbands20_downR.append(0)
                    bf2_bbands_width.append(0)
                    #bf2_rsi5.append(0)
                    bf2_rsi10.append(0)
                    bf2_rsi20.append(0)
                    #bf2_rsi30.append(0)
                    #bf2_rsi40.append(0)
                    #bf2_rsi50.append(0)
                    bf2_rsi60.append(0)

                elif i == 1:  #둘째날 데이터

                    bf1_open_list.append(op[i-1])
                    bf1_close_list.append(cl[i-1])
                    bf1_high_list.append(hi[i-1])
                    bf1_low_list.append(lo[i-1])
                    bf1_change_R_list.append(ch[i-1])
                    bf1_v10maR_list.append(v10[i-1])

                    bf1_dp_ma3.append(dp_ma3[i-1])
                    bf1_dp_ma5.append(dp_ma5[i-1])
                    bf1_dp_ma10.append(dp_ma10[i-1])
                    bf1_dp_ma20.append(dp_ma20[i-1])
                    bf1_dp_ma30.append(dp_ma30[i-1])
                    bf1_dp_ma40.append(dp_ma40[i-1])
                    bf1_dp_ma50.append(dp_ma50[i-1])
                    bf1_dp_ma60.append(dp_ma60[i-1])
                    bf1_dp_ma80.append(dp_ma80[i-1])
                    bf1_dp_ma100.append(dp_ma100[i-1])
                    bf1_dp_ma120.append(dp_ma120[i-1])
                    bf1_dp_ma240.append(dp_ma240[i-1])
                    bf1_u_tail_R_list.append(u_tail_R[i-1])
                    bf1_l_tail_R_list.append(l_tail_R[i-1])
                    bf1_vol_d1_R.append(vol_d1_R[i-1])
                    bf1_bband20_upR.append(bband20_upR[i-1])
                    bf1_bbands20_downR.append(bbands20_downR[i-1])
                    bf1_bbands_width.append(bbands_width[i-1])

                    #bf1_rsi5.append(rsi5[i-1])
                    bf1_rsi10.append(rsi10[i-1])
                    bf1_rsi20.append(rsi20[i-1])

                    #bf1_rsi30.append(rsi30[i-1])
                    #bf1_rsi40.append(rsi40[i-1])
                    #bf1_rsi50.append(rsi50[i-1])
                    bf1_rsi60.append(rsi60[i-1])

                    #bf1_rsi80.append(rsi80[i-1])
                    #bf1_rsi100.append(rsi100[i-1])
                    #bf1_rsi120.append(rsi120[i-1])

                    bf2_open_list.append(0)
                    bf2_close_list.append(0)
                    bf2_high_list.append(0)
                    bf2_low_list.append(0)
                    bf2_change_R_list.append(0)
                    bf2_v10maR_list.append(0)
                    bf2_dp_ma3.append(0)
                    bf2_dp_ma5.append(0)
                    bf2_dp_ma10.append(0)
                    bf2_dp_ma20.append(0)
                    bf2_dp_ma30.append(0)
                    bf2_dp_ma40.append(0)
                    bf2_dp_ma50.append(0)
                    bf2_dp_ma60.append(0)
                    bf2_dp_ma80.append(0)
                    bf2_dp_ma100.append(0)
                    bf2_dp_ma120.append(0)
                    bf2_dp_ma240.append(0)
                    bf2_u_tail_R_list.append(0)
                    bf2_l_tail_R_list.append(0)
                    bf2_vol_d1_R.append(0)
                    bf2_bband20_upR.append(0)
                    bf2_bbands20_downR.append(0)
                    bf2_bbands_width.append(0)
                    #bf2_rsi5.append(0)
                    bf2_rsi10.append(0)
                    bf2_rsi20.append(0)
                    #bf2_rsi30.append(0)
                    #bf2_rsi40.append(0)
                    #bf2_rsi50.append(0)
                    bf2_rsi60.append(0)

                #elif i == 2:
                else:

                    bf1_open_list.append(op[i - 1])
                    bf1_close_list.append(cl[i - 1])
                    bf1_high_list.append(hi[i - 1])
                    bf1_low_list.append(lo[i - 1])
                    bf1_change_R_list.append(ch[i - 1])
                    bf1_v10maR_list.append(v10[i - 1])
                    bf1_dp_ma3.append(dp_ma3[i - 1])
                    bf1_dp_ma5.append(dp_ma5[i - 1])
                    bf1_dp_ma10.append(dp_ma10[i - 1])
                    bf1_dp_ma20.append(dp_ma20[i - 1])
                    bf1_dp_ma30.append(dp_ma30[i - 1])
                    bf1_dp_ma40.append(dp_ma40[i - 1])
                    bf1_dp_ma50.append(dp_ma50[i - 1])
                    bf1_dp_ma60.append(dp_ma60[i - 1])
                    bf1_dp_ma80.append(dp_ma80[i - 1])
                    bf1_dp_ma100.append(dp_ma100[i - 1])
                    bf1_dp_ma120.append(dp_ma120[i - 1])
                    bf1_dp_ma240.append(dp_ma240[i - 1])
                    bf1_u_tail_R_list.append(u_tail_R[i - 1])
                    bf1_l_tail_R_list.append(l_tail_R[i - 1])
                    bf1_vol_d1_R.append(vol_d1_R[i - 1])
                    bf1_bband20_upR.append(bband20_upR[i - 1])
                    bf1_bbands20_downR.append(bbands20_downR[i - 1])
                    bf1_bbands_width.append(bbands_width[i - 1])
                    # bf1_rsi5.append(rsi5[i-1])
                    bf1_rsi10.append(rsi10[i - 1])
                    bf1_rsi20.append(rsi20[i - 1])
                    # bf1_rsi30.append(rsi30[i-1])
                    # bf1_rsi40.append(rsi40[i-1])
                    # bf1_rsi50.append(rsi50[i-1])
                    bf1_rsi60.append(rsi60[i - 1])
                    # bf1_rsi80.append(rsi80[i-1])
                    # bf1_rsi100.append(rsi100[i-1])
                    # bf1_rsi120.append(rsi120[i-1])

                    bf2_open_list.append(op[i - 2])
                    bf2_close_list.append(cl[i - 2])
                    bf2_high_list.append(hi[i - 2])
                    bf2_low_list.append(lo[i - 2])
                    bf2_change_R_list.append(ch[i - 2])
                    bf2_v10maR_list.append(v10[i - 2])
                    bf2_dp_ma3.append(dp_ma3[i - 2])
                    bf2_dp_ma5.append(dp_ma5[i - 2])
                    bf2_dp_ma10.append(dp_ma10[i - 2])
                    bf2_dp_ma20.append(dp_ma20[i - 2])
                    bf2_dp_ma30.append(dp_ma30[i - 2])
                    bf2_dp_ma40.append(dp_ma40[i - 2])
                    bf2_dp_ma50.append(dp_ma50[i - 2])
                    bf2_dp_ma60.append(dp_ma60[i - 2])
                    bf2_dp_ma80.append(dp_ma80[i - 2])
                    bf2_dp_ma100.append(dp_ma100[i - 2])
                    bf2_dp_ma120.append(dp_ma120[i - 2])
                    bf2_dp_ma240.append(dp_ma240[i - 2])
                    bf2_u_tail_R_list.append(u_tail_R[i - 2])
                    bf2_l_tail_R_list.append(l_tail_R[i - 2])
                    bf2_vol_d1_R.append(vol_d1_R[i - 2])
                    bf2_bband20_upR.append(bband20_upR[i - 2])
                    bf2_bbands20_downR.append(bbands20_downR[i - 2])
                    bf2_bbands_width.append(bbands_width[i - 2])

                    #bf2_rsi5.append(rsi5[i - 2])
                    bf2_rsi10.append(rsi10[i - 2])
                    bf2_rsi20.append(rsi20[i - 2])
                    #bf2_rsi30.append(rsi30[i - 2])
                    #bf2_rsi40.append(rsi40[i - 2])
                    #bf2_rsi50.append(rsi50[i - 2])
                    bf2_rsi60.append(rsi60[i - 2])
                    #bf2_rsi80.append(rsi80[i - 2])
                    #bf2_rsi100.append(rsi100[i - 2])
                    #bf2_rsi120.append(rsi120[i - 2])


            df['bf1_open_list'] = bf1_open_list
            df['bf1_close_list'] = bf1_close_list
            df['bf1_high_list'] = bf1_high_list
            df['bf1_low_list'] = bf1_low_list
            df['bf1_change_R_list'] =bf1_change_R_list
            df['bf1_v10maR_list'] =bf1_v10maR_list
            df['bf1_dp_ma3'] = bf1_dp_ma3
            df['bf1_dp_ma5'] = bf1_dp_ma5
            df['bf1_dp_ma10'] = bf1_dp_ma10
            df['bf1_dp_ma20'] =bf1_dp_ma20
            df['bf1_dp_ma30'] =bf1_dp_ma30
            df['bf1_dp_ma40'] =bf1_dp_ma40
            df['bf1_dp_ma50'] =bf1_dp_ma50
            df['bf1_dp_ma60'] =bf1_dp_ma60
            df['bf1_dp_ma80'] =bf1_dp_ma80
            df['bf1_dp_ma100'] =bf1_dp_ma100
            df['bf1_dp_ma120'] =bf1_dp_ma120
            df['bf1_dp_ma240'] =bf1_dp_ma240
            df['bf1_u_tail_R_list'] =bf1_u_tail_R_list
            df['bf1_l_tail_R_list'] =bf1_l_tail_R_list
            df['bf1_vol_d1_R'] =bf1_vol_d1_R
            df['bf1_bband20_upR'] =bf1_bband20_upR
            df['bf1_bbands20_downR'] =bf1_bbands20_downR
            df['bf1_bbands_width'] =bf1_bbands_width
            #df['bf1_rsi5'] =bf1_rsi5
            df['bf1_rsi10'] =bf1_rsi10
            df['bf1_rsi20'] =bf1_rsi20
            #df['bf1_rsi30'] =bf1_rsi30
            #df['bf1_rsi40'] =bf1_rsi40
            #df['bf1_rsi50'] =bf1_rsi50
            df['bf1_rsi60'] =bf1_rsi60
            #df['bf1_rsi80'] =bf1_rsi80
            #df['bf1_rsi100'] =bf1_rsi100
            #df['bf1_rsi120'] =bf1_rsi120

            df['bf2_open_list'] = bf2_open_list
            df['bf2_close_list'] = bf2_close_list
            df['bf2_high_list'] = bf2_high_list
            df['bf2_low_list'] = bf2_low_list
            df['bf2_change_R_list'] = bf2_change_R_list
            df['bf2_v10maR_list'] = bf2_v10maR_list
            df['bf2_dp_ma3'] = bf2_dp_ma3
            df['bf2_dp_ma5'] = bf2_dp_ma5
            df['bf2_dp_ma10'] = bf2_dp_ma10
            df['bf2_dp_ma20'] = bf2_dp_ma20
            df['bf2_dp_ma30'] = bf2_dp_ma30
            df['bf2_dp_ma40'] = bf2_dp_ma40
            df['bf2_dp_ma50'] = bf2_dp_ma50
            df['bf2_dp_ma60'] = bf2_dp_ma60
            df['bf2_dp_ma80'] = bf2_dp_ma80
            df['bf2_dp_ma100'] = bf2_dp_ma100
            df['bf2_dp_ma120'] = bf2_dp_ma120
            df['bf2_dp_ma240'] = bf2_dp_ma240
            df['bf2_u_tail_R_list'] = bf2_u_tail_R_list
            df['bf2_l_tail_R_list'] = bf2_l_tail_R_list
            df['bf2_vol_d1_R'] = bf2_vol_d1_R
            df['bf2_bband20_upR'] = bf2_bband20_upR
            df['bf2_bbands20_downR'] = bf2_bbands20_downR
            df['bf2_bbands_width'] = bf2_bbands_width
            #df['bf2_rsi5'] = bf2_rsi5
            df['bf2_rsi10'] = bf2_rsi10
            df['bf2_rsi20'] = bf2_rsi20
            #df['bf2_rsi30'] = bf2_rsi30
            #df['bf2_rsi40'] = bf2_rsi40
            #df['bf2_rsi50'] = bf2_rsi50
            df['bf2_rsi60'] = bf2_rsi60
            #df['bf2_rsi80'] = bf2_rsi80
            #df['bf2_rsi100'] = bf2_rsi100
            #df['bf2_rsi120'] = bf2_rsi120


            print("완료1")
        con.close()
        print("완료2")
        return df

    #백업 200210 def tech__(self, name):    #한종목의 기술적 지표 계산
        self.kospi_kosdaq = self.comboBox_2.currentText()

        con = sqlite3.connect("c:/users/백/stock_" + self.kospi_kosdaq + "_vol_ma.db")

        df = pd.read_sql("SELECT * FROM "+ "'"+ name +"' ", con, index_col=None) #df = pd.read_sql("SELECT * FROM CMG제약 ", con , index_col = None)
        df.sort_index(inplace= True, ascending= False)  #인덱스 기준으로 역으로 정렬


        if len(df['open']) > 0:  #값이 없는것을 제외시킨다

            op = df['open'] * 0.1 * 10
            cl = df['close'] * 0.1 * 10
            hi = df['high'] * 0.1 * 10
            lo = df['low'] * 0.1 * 10
            vo = df['volume'] * 0.1 * 10


            #df['ma3'] = ta.SMA(cl, 3)
            #df['ma5'] = ta.SMA(cl, 5)
            #df['ma10'] = ta.SMA(cl, 10)
            #df['ma20'] = ta.SMA(cl, 20)
            #df['ma60'] = ta.SMA(cl, 60)
            #df['ma120'] = ta.SMA(cl, 120)
            #df['ma240'] = ta.SMA(cl, 240)

            dfma3 = ta.SMA(cl, 3)

            dfma5 = ta.SMA(cl, 5)

            dfma10 = ta.SMA(cl, 10)
            dfma20 = ta.SMA(cl, 20)

            dfma30 = ta.SMA(cl, 30)
            dfma40 = ta.SMA(cl, 40)
            dfma50 = ta.SMA(cl, 50)

            dfma60 = ta.SMA(cl, 60)

            dfma80 = ta.SMA(cl, 80)
            dfma100 = ta.SMA(cl, 100)

            dfma120 = ta.SMA(cl, 120)
            dfma240 = ta.SMA(cl, 240)

            df['vma10_R'] = vo / ta.SMA(vo, 10)
            df['dp_ma3'] = cl / dfma3
            df['dp_ma5'] = cl / dfma5
            df['dp_ma10'] = cl / dfma10
            df['dp_ma20'] = cl / dfma20
            df['dp_ma30'] = cl / dfma30
            df['dp_ma40'] = cl / dfma40
            df['dp_ma50'] = cl / dfma50
            df['dp_ma60'] = cl / dfma60
            df['dp_ma80'] = cl / dfma80
            df['dp_ma100'] = cl / dfma100
            df['dp_ma120'] = cl / dfma120
            df['dp_ma240'] = cl / dfma240

            bbands30 = pd.Series(ta.BBANDS(cl, timeperiod=30, nbdevup=1.8, nbdevdn=1.8))  # 밴드는 또 Series를 만들었다가
            df['bbands30_upR'] = cl/bbands30[0]  # 하나씩 일일이 인덱싱해줘야 함.
            #df['bbands30_mov'] = bbands30[1]
            df['bbands30_downR'] = cl/bbands30[2]
            df['bbands_width'] = (bbands30[0] - bbands30[2]) / cl

            macd = pd.Series(ta.MACD(cl, 5, 34, 7))  # 밴드는 또 Series를 만들었다가
            #df['macd_line5,34,7'] = macd[0]  # 하나씩 일일이 인덱싱해줘야 함.
            #df['macd_sig5,34,7'] = macd[1]
            #df['macd_histo5,34,7'] = macd[2]

            df['macd_line5,34,7'] = macd[0] / dfma5  # 5일 이평기준 어느정도에 있는가?
            df['macd_sig5,34,7'] = macd[1] / dfma5
            df['macd_histo5,34,7'] = macd[2] / dfma5  #히스토그램 구하는 공식은 단기이평-장기 이평임

            df['rsi5'] = ta.RSI(cl, 5)
            df['rsi10'] = ta.RSI(cl, 10)
            df['rsi20'] = ta.RSI(cl, 20)
            df['rsi30'] = ta.RSI(cl, 5)
            df['rsi40'] = ta.RSI(cl, 5)
            df['rsi50'] = ta.RSI(cl, 5)
            df['rsi60'] = ta.RSI(cl, 60)
            df['rsi80'] = ta.RSI(cl, 60)
            df['rsi100'] = ta.RSI(cl, 60)
            df['rsi120'] = ta.RSI(cl, 60)

        return df


def test():

    #c.execute("INSERT INTO stuffToPlot VALUES(SELECT * FROM stuffToPlot2)")
    #c.execute('SELECT * FROM stuffToPlot')
    #d=c.fetchall()
    #[print(row) for row in d]
    data = {}
    df = pd.DataFrame(data)

    aa = []
    bb = []
    cc = []
    dd = []
    print(type(aa))

    for i in range(10):
        aa.append(random.randrange(1, 10))
        bb.append(random.randrange(1, 10))
        cc.append(random.randrange(1, 10))
        dd.append(random.randrange(1, 10))


    df['aa'] = aa
    df['bb'] = bb
    df['cc'] = cc
    df['dd'] = dd
    #print(df)

    print(50* '#')


    c.execute('INSERT INTO stuffToPlot SELECT * FROM stuffToPlot2')
    conn.commit()
    c.close()


import sys
from pywinauto import application
import win32com.client

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

import pandas as pd
import time
from datetime import datetime, timedelta

from DS_stock_none_GUI import *
from pandas import DataFrame, Series
import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import talib as ta

form_class = uic.loadUiType("DS_stock.ui")[0]


class DS_stock(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.dsstock_none_gui = Daeshin_stock()
        self.setupUi(self)
        self.timer = QTimer(self)  # 1초마다 시간을 띄우도록
        self.timer.start(1000)  # 1초에 한 번 timeout 시그널이 발생함
        self.timer.timeout.connect(self.timeout)  # timeout시그널 발생시 timeout 함수로 이동
        self.download_ohlc_done = False  # 당일 거래량 계산 안됨
        self.lastmsg = ""

        self.pushButton.clicked.connect(self.DS_auto_login)  # 접속버튼 클릭시
        self.pushButton_2.clicked.connect(self.DS_kosdaq_code_load)
        self.pushButton_3.clicked.connect(self.DS_save_ohlc_button)
        self.pushButton_4.clicked.connect(self.DS_vol_ma_calc_button)
        self.pushButton_5.clicked.connect(self.Seek_today_buy_list_button)
        self.pushButton_6.clicked.connect(self.verify_vMA10_button)
        self.pushButton_7.clicked.connect(self.add_vol_ratio)
        self.pushButton_8.clicked.connect(self.add_tomorrow_sell_profit)
        self.pushButton_10.clicked.connect(self.add_bong_size_button)
        self.pushButton_15.clicked.connect(self.verify_BONG_size_button)
        self.pushButton_9.clicked.connect(self.verify_change_ratio_button)

        self.pushButton_17.clicked.connect(self.add_close_ma)
        self.pushButton_16.clicked.connect(self.veriyfy_gap_rising_button)
        self.pushButton_18.clicked.connect(self.add_gap_size_ratio_button)
        self.pushButton_19.clicked.connect(self.DS_kosdaq_industry)
        self.pushButton_12.clicked.connect(self.trace_d1_change_button)
        self.pushButton_14.clicked.connect(self.add_ma_converge_button)
        self.pushButton_20.clicked.connect(self.add_ma_converge_button)
        self.pushButton_21.clicked.connect(self.DS_save_today_ohlc)
        self.pushButton_22.clicked.connect(self.add_tech_today)
        self.pushButton_23.clicked.connect(self.execute_query__)
        self.pushButton_24.clicked.connect(self.DS_save_jisu)
        self.pushButton_25.clicked.connect(self.move_to_excel)
        self.pushButton_26.clicked.connect(self.DS_save_ohlc_one_tabel)
        self.pushButton_11.clicked.connect(self.test___)

    def timeout(self):
        current_time = QTime.currentTime()
        DS_login_time = QTime(15, 16, 0)
        calc_time = QTime(15, 17, 0)

        text_time = current_time.toString("hh:mm:ss")
        time_msg = "현재시간: " + text_time
        dstate = self.DS_connect_confirm()

        if dstate == 1:
            state_msg = "대신 서버 연결중"
        else:
            state_msg = "대신 서버 미연결"

        self.statusbar.showMessage(state_msg + " | " + time_msg + " | " + self.lastmsg)

        # 자동 로그인 설정
        if current_time > DS_login_time and dstate != 1 and self.checkBox_2.isChecked():
            self.DS_auto_login()
            time.sleep(60)

        # 자동 살종목 선정 설정
        if current_time > calc_time and self.download_ohlc_done is False and dstate == 1 and self.checkBox.isChecked():
            today = datetime.datetime.today()  # " 오늘"
            end_date = today.strftime("%Y%m%d")  # 오늘
            start_date = (today - datetime.timedelta(15)).strftime("%Y%m%d")

            self.DS_save_ohlc_button()
            self.statusbar.showMessage("ohlc 다운로드 완료")
            time.sleep(10)
            self.DS_vol_ma_calc_button()
            self.statusbar.showMessage("이평계산 완료")
            time.sleep(10)
            self.Seek_today_buy_list_button()
            self.statusbar.showMessage("살종목 갱신 완료")
            time.sleep(10)

            self.download_ohlc_done = True

    def DS_auto_login(self):  # 대신증권 Cybos plus 자동로그인
        app = application.Application()
        app.start("C:/DAISHIN/STARTER/ncStarter.exe /prj:cp /id:uni9ue /pwd:psyy2758 /pwdcert: /autostart")

    def DS_kosdaq_industry(self):  # 코스닥 산업별 코드리스트 저장
        instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        kosdaq_indst_codelist = instCpCodeMgr.GetKosdaqIndustry1List()
        kosdaq_indst_nameist = []

        print(kosdaq_indst_codelist)
        for code in kosdaq_indst_codelist:
            kosdaq_indst_nameist.append(instCpCodeMgr.CodeToName(code))
        kosdaq_indst = {"code": kosdaq_indst_codelist, "name": kosdaq_indst_nameist}

        df_kosdaq_indst = DataFrame(kosdaq_indst)
        print(df_kosdaq_indst)

        con = sqlite3.connect("c:/users/백/DS_JISU_codedata.db")
        df_kosdaq_indst.to_sql("kosdaq_JISU", con, if_exists="replace")

    def DS_kosdaq_code_load(self):
        instCpCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
        kospi_codelist = instCpCodeMgr.GetStockListByMarket(1)
        kospi_namelist = []
        kosdaq_codelist = instCpCodeMgr.GetStockListByMarket(2)
        kosdaq_namelist = []

        for code in kospi_codelist:
            kospi_namelist.append(instCpCodeMgr.CodeToName(code))

        kospi_codeNname = {"code": kospi_codelist, "name": kospi_namelist}

        df_kospi_codeNname = DataFrame(kospi_codeNname)

        con = sqlite3.connect("c:/users/백/DS_codedata.db")
        df_kospi_codeNname.to_sql("kospi", con, if_exists="replace")

        for code in kosdaq_codelist:
            kosdaq_namelist.append(instCpCodeMgr.CodeToName(code))

        kosdaq_codeNname = {"code": kosdaq_codelist, "name": kosdaq_namelist}

        df_kosdaq_codeNname = DataFrame(kosdaq_codeNname)
        con = sqlite3.connect("c:/users/백/DS_codedata.db")
        df_kosdaq_codeNname.to_sql("kosdaq", con, if_exists="replace")
        self.lastmsg = "대신증권 코드 갱신 완료"

    def DS_save_ohlc_button(self):

        start_date = self.spinBox.value()
        end_date = self.spinBox_2.value()

        instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

        con = sqlite3.connect("c:/users/백/DS_codedata.db")
        kospi_kosdaq = self.comboBox.currentText()
        codedata = pd.read_sql("SELECT * FROM " + kospi_kosdaq, con, index_col="index")
        con.close()

        code_list = codedata["code"]
        name_list = codedata["name"]

        bong__ = self.comboBox_2.currentText()

        if bong__ == "일봉":
            bong = "D"  # 일봉
        elif bong__ == "월봉":
            bong = "M"
        else:
            bong = "m"
            boon = self.comboBox_3.currentText()
            print(boon)

        for i, code in enumerate(code_list):
            name = name_list[i]

            str_1 = str(i + 1)
            str_2 = str(len(code_list))

            instStockChart.SetInputValue(0, code)
            if bong == "D":  # 일봉요청이면
                instStockChart.SetInputValue(1, ord("1"))  # 날짜로 요청
                instStockChart.SetInputValue(2, end_date)  # 요청기간
                instStockChart.SetInputValue(3, start_date)  # 요청기간
            else:
                instStockChart.SetInputValue(1, ord("2"))  # 개수로 요청
                instStockChart.SetInputValue(4, 1950)  # 요청개수

            if bong == "m":
                instStockChart.SetInputValue(5, (0, 1, 2, 3, 4, 5, 6, 8, 37))  # 1번은 시간
                instStockChart.SetInputValue(7, 10)  # 틱/분봉주기
            else:
                instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 6, 8, 37))  # 1번 시간 제외

            instStockChart.SetInputValue(6, ord(bong))  # 봉 구분
            instStockChart.SetInputValue(9, ord("1"))  # 수정 주가

            # BlockRequest
            instStockChart.BlockRequest()

            time.sleep(0.25)  # 1종목 요청 후 X초 쉬고난뒤 다음 종목 요청

            # GetHeaderValue
            numdata = instStockChart.GetHeaderValue(3)
            print(numdata)
            numfield = instStockChart.GetHeaderValue(1)

            # GetDataValue : 0번열 : 날짜, 1: open, 2:high, 3:low, 4: close, 5:change, 6:vol
            date_list = []
            time_list = []
            open_list = []
            high_list = []
            low_list = []
            close_list = []
            change_list = []
            volume_list = []
            change_ratio_list = []

            for j in range(numdata):
                date = instStockChart.GetDataValue(0, j)
                date_list.append(date)

            for j in range(numdata):
                open = instStockChart.GetDataValue(1, j)
                open_list.append(open)

            for j in range(numdata):
                high = instStockChart.GetDataValue(2, j)
                high_list.append(high)

            for j in range(numdata):
                low = instStockChart.GetDataValue(3, j)
                low_list.append(low)

            for j in range(numdata):
                close = instStockChart.GetDataValue(4, j)
                close_list.append(close)

            for j in range(numdata):
                change = instStockChart.GetDataValue(5, j)
                change_list.append(change)

            for j in range(numdata):
                volume = instStockChart.GetDataValue(6, j)
                volume_list.append(volume)

            for j in range(numdata):
                if j == numdata - 1:
                    change_ratio_list.append(0)

                    break
                change = change_list[j]
                close = close_list[j + 1]
                change_ratio = round(change / close, 5)

                change_ratio_list.append(change_ratio)

            ds_ohlcv = {"date": date_list, "open": open_list, "high": high_list, "low": low_list, "close": close_list,
                        "change": change_list, "volume": volume_list, "change_ratio": change_ratio_list}

            df = pd.DataFrame(ds_ohlcv, columns=["open", "high", "low", "close", "change", "volume", "change_ratio"],
                              index=ds_ohlcv["date"])

            today = datetime.datetime.today().strftime("%Y%m%d")
            # todaystr = str(today)

            con = sqlite3.connect("c:/users/백/stock_" + kospi_kosdaq + "_vol_ma.db")

            df.to_sql(name, con, if_exists="replace")

            lastmsg_here_def = str_1 + "/" + str_2 + name + " 완료"
            print(lastmsg_here_def)
            # self.statusbar.showMessage(lastmsg_here_def)

    def DS_save_ohlc_one_tabel(self):

        start_date = self.spinBox.value()
        end_date = self.spinBox_2.value()

        instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

        con = sqlite3.connect("c:/users/백/DS_codedata.db")
        kospi_kosdaq = self.comboBox.currentText()
        codedata = pd.read_sql("SELECT * FROM " + kospi_kosdaq, con, index_col="index")

        code_list = codedata["code"]
        name_list = codedata["name"]
        bong1 = "D"  # 일봉
        bong2 = "M"  # 월봉
        bong3 = "m"  # 분봉
        con.close()

        for i, code in enumerate(code_list):
            name = name_list[i]
            str_1 = str(i + 1)
            str_2 = str(len(code_list))

            instStockChart.SetInputValue(0, code)
            instStockChart.SetInputValue(1, ord("1"))
            # instStockChart.SetInputValue(1, ord("2"))  # 개수로 요청
            instStockChart.SetInputValue(2, end_date)  # 요청기간
            instStockChart.SetInputValue(3, start_date)  # 요청기간
            # instStockChart.SetInputValue(4, 1950)  # 요청개수
            # instStockChart.SetInputValue(5, (0, 1, 2, 3, 4, 5, 6, 8, 37))  # 분봉전용
            instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 6, 8, 37))
            instStockChart.SetInputValue(6, ord(bong1))  # 일봉
            # instStockChart.SetInputValue(6, ord(bong3))   #분봉
            # instStockChart.SetInputValue(7, 10)  #틱/분봉주기
            instStockChart.SetInputValue(9, ord("1"))

            # BlockRequest
            instStockChart.BlockRequest()

            time.sleep(0.25)  # 1종목 요청 후 X초 쉬고난뒤 다음 종목 요청

            # GetHeaderValue
            numdata = instStockChart.GetHeaderValue(3)
            numfield = instStockChart.GetHeaderValue(1)

            # GetDataValue : 0번열 : 날짜, 1: open, 2:high, 3:low, 4: close, 5:change, 6:vol
            date_list = []
            open_list = []
            high_list = []
            low_list = []
            close_list = []
            change_list = []
            volume_list = []
            change_ratio_list = []
            index_list = []
            name2_list = []

            for j in range(numdata):
                date = instStockChart.GetDataValue(0, j)
                date_list.append(date)
                open = instStockChart.GetDataValue(1, j)
                open_list.append(open)
                high = instStockChart.GetDataValue(2, j)
                high_list.append(high)
                low = instStockChart.GetDataValue(3, j)
                low_list.append(low)
                close = instStockChart.GetDataValue(4, j)
                close_list.append(close)
                change = instStockChart.GetDataValue(5, j)
                change_list.append(change)
                volume = instStockChart.GetDataValue(6, j)
                volume_list.append(volume)
                index_list.append(str(date) + name)
                name2_list.append(name)
                if j == numdata - 1:
                    change_ratio_list.append(0)
                    break
                change = change_list[j]
                change_ratio = round(change / (close - change), 4)
                change_ratio_list.append(change_ratio)

            ds_ohlcv = {"index": index_list, "date": date_list, "name": name2_list, "open": open_list,
                        "high": high_list, "low": low_list,
                        "close": close_list, "change": change_list, "volume": volume_list,
                        "change_ratio": change_ratio_list}

            df = pd.DataFrame(ds_ohlcv, columns=["date", "name", "open", "high", "low", "close", "change", "volume",
                                                 "change_ratio"], index=ds_ohlcv["index"])
            con1 = sqlite3.connect("c:/users/백/stock_" + kospi_kosdaq + "_vol_ma.db")

            # df.to_sql(name, con1, if_exists="replace")
            df.to_sql(kospi_kosdaq, con1, if_exists="append")
            lastmsg_here_def = str_1 + "/" + str_2 + name + " 완료"
            con1.close()
            print(lastmsg_here_def)
            # self.statusbar.showMessage(lastmsg_here_def)

    def DS_save_today_ohlc(self):

        instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

        con = sqlite3.connect("c:/users/백/DS_codedata.db")
        kospi_kosdaq = self.comboBox.currentText()
        codedata = pd.read_sql("SELECT * FROM " + kospi_kosdaq, con, index_col="index")
        con.close()

        code_list = codedata["code"]
        name_list = codedata["name"]
        bong1 = "D"  # 일봉

        for i, code in enumerate(code_list):
            name = name_list[i]

            print(name + str(i) + "/" + str(len(name_list)))

            str_1 = str(i + 1)
            str_2 = str(len(code_list))

            instStockChart.SetInputValue(0, code)
            # instStockChart.SetInputValue(1, ord("1"))
            instStockChart.SetInputValue(1, ord("2"))  # 개수로 요청
            # instStockChart.SetInputValue(2, end_date)  #요청기간
            # instStockChart.SetInputValue(3, start_date)  #요청기간
            instStockChart.SetInputValue(4, 60)  # 요청개수
            # instStockChart.SetInputValue(5, (0, 1, 2, 3, 4, 5, 6, 8, 37))  # 분봉전용
            instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 6, 8, 37))
            instStockChart.SetInputValue(6, ord(bong1))  # 일봉
            # instStockChart.SetInputValue(6, ord(bong3))   #분봉
            # instStockChart.SetInputValue(7, 10)  #틱/분봉주기
            instStockChart.SetInputValue(9, ord("1"))

            # BlockRequest
            instStockChart.BlockRequest()

            time.sleep(0.25)  # 1종목 요청 후 X초 쉬고난뒤 다음 종목 요청

            # GetHeaderValue
            numdata = instStockChart.GetHeaderValue(3)
            print(numdata)
            numfield = instStockChart.GetHeaderValue(1)

            # GetDataValue : 0번열 : 날짜, 1: open, 2:high, 3:low, 4: close, 5:change, 6:vol
            index_list = []
            name2_list = []
            date_list = []
            open_list = []
            high_list = []
            low_list = []
            close_list = []
            change_list = []
            volume_list = []
            change_ratio_list = []

            for j in range(numdata):
                date = instStockChart.GetDataValue(0, j)
                date_list.append(date)
                open = instStockChart.GetDataValue(1, j)
                open_list.append(open)
                high = instStockChart.GetDataValue(2, j)
                high_list.append(high)
                low = instStockChart.GetDataValue(3, j)
                low_list.append(low)
                close = instStockChart.GetDataValue(4, j)
                close_list.append(close)
                change = instStockChart.GetDataValue(5, j)
                change_list.append(change)
                volume = instStockChart.GetDataValue(6, j)
                volume_list.append(volume)
                index_list.append(str(date) + name)
                name2_list.append(name)
                if j == numdata - 1:
                    change_ratio_list.append(0)

                    break
                change = change_list[j]
                close = close_list[j + 1]  # 전일 종가
                change_ratio = round(change / close, 5)

                change_ratio_list.append(change_ratio)

            ds_ohlcv = {"index": index_list, "date": date_list, "name": name2_list, "open": open_list,
                        "high": high_list, "low": low_list,
                        "close": close_list, "change": change_list, "volume": volume_list,
                        "change_ratio": change_ratio_list}

            df = pd.DataFrame(ds_ohlcv, columns=["date", "name", "open", "high", "low", "close", "change", "volume",
                                                 "change_ratio"],
                              index=ds_ohlcv["index"])

            today = datetime.datetime.today().strftime("%Y%m%d")
            todaystr = str(today)
            con = sqlite3.connect("c:/users/백/" + todaystr + kospi_kosdaq + "_data.db")
            df.to_sql(kospi_kosdaq, con, if_exists='append')
            con.close()

        print("오늘OHCLV 다운완료")

    def add_tech_today(self, name):  # 기술적 지표 계산
        kospi_kosdaq = self.comboBox.currentText()
        today = datetime.datetime.today().strftime("%Y%m%d")
        todaystr = str(today)

        con = sqlite3.connect("c:/users/백/" + todaystr + kospi_kosdaq + "_data.db")

        df = pd.read_sql("SELECT * FROM " + kospi_kosdaq, con,
                         index_col=None)  # df = pd.read_sql("SELECT * FROM CMG제약 ", con , index_col = None)
        # df = pd.read_sql("SELECT * FROM " + kospi_kosdaq, con, index_col="index")
        df.sort_index(inplace=True, ascending=False)  # 인덱스 기준으로 역으로 정렬

        op = df['open'] * 0.1 * 10
        cl = df['close'] * 0.1 * 10
        hi = df['high'] * 0.1 * 10
        lo = df['low'] * 0.1 * 10
        vo = df['volume'] * 0.1 * 10

        dfma3 = ta.SMA(cl, 3)
        dfma5 = ta.SMA(cl, 5)
        dfma10 = ta.SMA(cl, 10)
        dfma20 = ta.SMA(cl, 20)
        dfma60 = ta.SMA(cl, 60)

        df['vma10_R'] = vo / ta.SMA(vo, 10)

        df['dp_ma3'] = cl / dfma3
        df['dp_ma5'] = cl / dfma5
        df['dp_ma10'] = cl / dfma10
        df['dp_ma20'] = cl / dfma20
        df['dp_ma60'] = cl / dfma60

        bbands20 = pd.Series(ta.BBANDS(cl, timeperiod=20, nbdevup=2, nbdevdn=2))  # 밴드는 또 Series를 만들었다가
        df['bbands20_upR'] = cl / bbands20[0]  # 하나씩 일일이 인덱싱해줘야 함.

        # df['bbands20_mov'] = bbands20[1]
        df['bbands20_downR'] = cl / bbands20[2]
        macd = pd.Series(ta.MACD(cl, 10, 15, 7))  # 밴드는 또 Series를 만들었다가
        df['macd_line'] = macd[0]  # 하나씩 일일이 인덱싱해줘야 함.
        df['macd_sig'] = macd[1]
        df['macd_histo'] = macd[2]

        df['rsi10'] = ta.RSI(cl, 10)
        df['rsi20'] = ta.RSI(cl, 20)
        df['rsi60'] = ta.RSI(cl, 60)
        df.to_sql(kospi_kosdaq, con, if_exists='replace')
        con.close()
        print("최종완료")

    def execute_query__(self):
        kospi_kosdaq = self.comboBox.currentText()

        # today = datetime.datetime.today().strftime("%Y%m%d")
        test = "20200129"
        today = datetime.datetime.today()
        todaystr = str(today.strftime("%Y%m%d"))

        year_ = datetime.datetime.today().year
        month_ = datetime.datetime.today().month
        day_ = datetime.datetime.today().day
        week_day = datetime.date(year_, month_, day_).weekday()  # 요일 구하기 5=토, 6=일, 0 = 월
        print(week_day)

        if week_day == 5:
            print("완료")
            today = today + timedelta(days=-1)  # 토요일이면 하루전
        elif week_day == 6:
            today = today + timedelta(days=-2)  # 일요일이면 이틀전

        modified_todaystr = str(today.strftime("%Y%m%d"))
        print(modified_todaystr)
        # query_ = "change_ratio > 0.04 AND change_ratio < 0.22 AND vma10_R <2 AND bbands20_upR > 0.38 AND bbands20_upR <0.76 AND date == " + modified_todaystr  # 쿼리 입력
        query_ = "change_ratio > 0.04 AND change_ratio < 0.22 AND vma10_R <2 AND bbands20_upR > 0.38 AND bbands20_upR <0.76 AND date == " + test  # 쿼리 입력
        con = sqlite3.connect("c:/users/백/" + todaystr + kospi_kosdaq + "_data.db")  # 키움증권 다운로드 종목 데이터 베이스

        # if self.kospi_kosdaq == "kospi":
        #   df = pd.read_sql("SELECT * FROM 동화약품 WHERE " + query_, con, index_col=None)   #코스피

        # else:
        #   df = pd.read_sql("SELECT * FROM 삼천당제약 WHERE " + query_, con, index_col=None)
        df = pd.read_sql("SELECT * FROM " + kospi_kosdaq + " WHERE " + query_, con, index_col=None)
        print("OK4")

        con.close()
        self.dsstock_none_gui.simul_data_to_excel(df)
        print("엑셀저장 완료")

    def DS_save_jisu(self):
        start_date = self.spinBox.value()
        end_date = self.spinBox_2.value()

        self.dsstock_none_gui.DS_save_jisu__(start_date, end_date)

    def DS_vol_ma_calc_button(self):
        day = self.spinBox_3.value()
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권용 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")
        codename_list = df["name"]  # 코드네임을 리스트로 저장

        for i, codename in enumerate(codename_list):  # 뺑뺑이 돌리기
            self.dsstock_none_gui.calc_ma(codename, day)
            print(i + 1, "/", len(codename_list), codename, " 완료")

    def add_close_ma(self):  # 가격 이평 추가

        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권용 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")
        codename_list = df["name"]  # 코드네임을 리스트로 저장

        for i, codename in enumerate(codename_list):  # 뺑뺑이 돌리기
            self.dsstock_none_gui.calc_close_ma3_5_10_20_60_120(codename)
            print(i + 1, "/", len(codename_list), codename, " 완료")

    def add_vol_ratio(self):
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권용 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")
        name_list = df["name"]  # 코드네임을 리스트로 저장

        for i, name in enumerate(name_list):  # 뺑뺑이 돌리기
            vol_ma10_ratio_list = self.dsstock_none_gui.calc_vol_ma10_ratio(name)

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")  # 키움증권 다운로드 종목 데이터 베이스
            jum = "'"
            inputstr = "SELECT * FROM " + jum + name + jum

            df = pd.read_sql(inputstr, con, index_col="index")  # 여기서 데이터형식은 DataFrame 객체다.
            df.insert(len(df.columns), "vol_ma10_ratio", vol_ma10_ratio_list)

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")
            df.to_sql(name, con, if_exists="replace")
            print(i + 1, "/", len(name_list), name, " 완료")

    def add_bong_size_button(self):
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권용 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")
        name_list = df["name"]  # 코드네임을 리스트로 저장

        for i, name in enumerate(name_list):  # 뺑뺑이 돌리기
            bong_size_list = self.dsstock_none_gui.add_bong_size(name)

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")  # 키움증권 다운로드 종목 데이터 베이스
            jum = "'"
            inputstr = "SELECT * FROM " + jum + name + jum

            df = pd.read_sql(inputstr, con, index_col="index")  # 여기서 데이터형식은 DataFrame 객체다.
            df.insert(len(df.columns), "bong_size", bong_size_list)

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")
            df.to_sql(name, con, if_exists="replace")
            print(i + 1, "/", len(name_list), name, " 완료")

    def add_gap_size_ratio_button(self):
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권용 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")
        name_list = df["name"]  # 코드네임을 리스트로 저장

        for i, name in enumerate(name_list):  # 뺑뺑이 돌리기
            gap_size_ratio_list = self.dsstock_none_gui.add_gap_size_ratio(name)

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")  # 키움증권 다운로드 종목 데이터 베이스
            jum = "'"
            inputstr = "SELECT * FROM " + jum + name + jum

            df = pd.read_sql(inputstr, con, index_col="index")  # 여기서 데이터형식은 DataFrame 객체다.
            df.insert(len(df.columns), "gap_size", gap_size_ratio_list)

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")
            df.to_sql(name, con, if_exists="replace")
            print(i + 1, "/", len(name_list), name, " 완료")

        print("최종완료")

    def add_ma_converge_button(self):
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권용 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")
        name_list = df["name"]  # 코드네임을 리스트로 저장

        for i, name in enumerate(name_list):  # 뺑뺑이 돌리기
            print(name + " 진입")
            diff_ma_ratio_list = self.dsstock_none_gui.add_ma_converge(name)

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")  # 키움증권 다운로드 종목 데이터 베이스
            jum = "'"
            inputstr = "SELECT * FROM " + jum + name + jum

            df = pd.read_sql(inputstr, con, index_col="index")  # 여기서 데이터형식은 DataFrame 객체다.
            df.insert(len(df.columns), "ma_converge_ratio", diff_ma_ratio_list)

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")
            df.to_sql(name, con, if_exists="replace")
            print(i + 1, "/", len(name_list), name, " 완료")
        print("최종완료")

    def add_bolband(self):
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권용 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")
        name_list = df["name"]  # 코드네임을 리스트로 저장

    def add_tomorrow_sell_profit(self):  # 익일 매도시 수익률 데이터에 추가하기
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권용 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")
        name_list = df["name"]  # 코드네임을 리스트로 저장

        for i, name in enumerate(name_list):  # 뺑뺑이 돌리기
            df1 = self.dsstock_none_gui.today_close_buy_tomorrow_close_sell(name)

            D1_profit_list = df1["profit"]
            D1_profit_ratio_list = df1["profit_ratio"]

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")  # 키움증권 다운로드 종목 데이터 베이스
            jum = "'"
            inputstr = "SELECT * FROM " + jum + name + jum

            df = pd.read_sql(inputstr, con, index_col="index")  # 여기서 데이터형식은 DataFrame 객체다.

            # df.drop("D+1_profit", axis=1, inplace=True)   #column을 삭제하는 가장 좋은 방법은 drop을 사용하는 것입니다.
            # dataframe.drop("컬럼 이름", axis=1, inplace=True)
            # 여기서 axis는 축을 의미하고 0은 row를 1은 column을 의미하게 됩니다.
            # inplace=True라고 설정을 해야지 바로 drop의 동작을 실행합니다.
            df.insert(len(df.columns), "D+1_profit", D1_profit_list)

            df.insert(len(df.columns), "D+1_profit_ratio", D1_profit_ratio_list)

            con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")
            df.to_sql(name, con, if_exists="replace")
            print(i + 1, "/", len(name_list), name, " 완료")

    def DS_connect_confirm(self):
        instCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
        return instCpCybos.IsConnect

    def Seek_today_buy_list_button(self):
        self.dsstock_none_gui.Seek_Today_buy_list()

    def verify_BONG_size_button(self):
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권 기준 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")  # 대신증권 기준 코드와 코드네임 불러오기
        all_codename_list = df["name"]  # 코드네임을 리스트로 저장

        low_X = self.doubleSpinBox_9.value()
        high_X = self.doubleSpinBox_10.value()

        final_result_date = []
        final_codename = []
        final_result_d0_close = []
        final_result_d0_change_ratio = []
        final_result_d1_close = []
        final_result_profit = []
        final_result_profit_rate = []
        final_result_BONG_size_ratio = []

        for i, name in enumerate(all_codename_list):  # 뺑뺑이 돌리기

            print(name)

            final_result = self.dsstock_none_gui.verify_BONG_size(name, low_X, high_X)

            # if i == 0:
            #   final_result_date = final_result["date"]
            #  final_codename = final_result["codename"]
            # final_result_d0_close = final_result["D+0_close"]
            # final_result_d0_change_ratio = final_result["D+0_change_ratio"]
            # final_result_d1_close = final_result["D+1_close"]
            # final_result_BONG_size_ratio = final_result["BONG_size_ratio"]
            # final_result_profit = final_result["profit"]
            # final_result_profit_rate = final_result["profit_rate"]

            final_result_date += final_result["date"]
            final_codename += final_result["codename"]
            final_result_d0_close += final_result["D+0_close"]
            final_result_d0_change_ratio += final_result["D+0_change_ratio"]
            final_result_d1_close += final_result["D+1_close"]
            final_result_BONG_size_ratio += final_result["BONG_size_ratio"]
            final_result_profit += final_result["profit"]
            final_result_profit_rate += final_result["profit_rate"]

            print(i + 1, "/", len(all_codename_list), " 완료")

        final_result2 = {"date": final_result_date, "codename": final_codename, "D+0_close": final_result_d0_close,
                         "D+0_change_ratio": final_result_d0_change_ratio,
                         "D+1_close": final_result_d1_close, "BONG_size_ratio": final_result_BONG_size_ratio,
                         "profit": final_result_profit, "profit_rate": final_result_profit_rate}

        final_result2_df = DataFrame(final_result2)
        sorted_result_df = final_result2_df.sort_values(by="date", ascending=False)

        print("OK2")

        # print(sorted_result_df)
        print(sorted_result_df["codename"])

        # sqlite3로 저장
        # con = sqlite3.connect("c:/users/백/kosdaq_result"+ low_X_str + "~" + high_X_str + ".db")
        # final_result2_df.to_sql("결과", con, if_exists="replace")

        # 엑셀로 결과 저장
        self.dsstock_none_gui.simul_data_to_excel(sorted_result_df)

    def verify_vMA10_button(self):  # 거래량 이평 급등종목 시뮬레이션

        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권 기준 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")  # 대신증권 기준 코드와 코드네임 불러오기
        codename_list = df["name"]  # 코드네임을 리스트로 저장

        low_X = self.doubleSpinBox.value()
        high_X = self.doubleSpinBox_2.value()
        low_X_str = str(low_X)
        high_X_str = str(high_X)
        final_result_date = []
        final_codename = []
        final_result_d0_open = []
        final_result_d0_high = []
        final_result_d0_low = []
        final_result_d0_close = []
        final_result_d0_change_ratio = []
        final_result_d1_high = []
        final_result_d1_low = []
        final_result_d1_close = []
        final_result_vol_ma10_ratio = []
        final_result_gap_size_ratio = []
        final_close_ma3_ratio = []
        final_close_ma5_ratio = []
        final_close_ma10_ratio = []
        final_close_ma20_ratio = []
        final_close_ma60_ratio = []
        final_close_ma120_ratio = []
        final_ma_converge_ratio = []
        final_result_profit = []
        final_result_profit_rate = []

        for i, codename in enumerate(codename_list):  # 뺑뺑이 돌리기

            print(str(codename) + "진입")

            final_result = self.dsstock_none_gui.verify_vMA10(codename, low_X, high_X)

            final_date = list(final_result["date"])
            print(len(final_date))

            if len(final_date) > 0:
                final_result_date += final_result["date"]
                final_codename += final_result["codename"]
                final_result_d0_open += final_result["D+0_open"]
                final_result_d0_high += final_result["D+0_high"]
                final_result_d0_low += final_result["D+0_low"]
                final_result_d0_close += final_result["D+0_close"]
                final_result_d0_change_ratio += final_result["D+0_change_ratio"]
                final_result_d1_high += final_result["D+1_high"]
                final_result_d1_low += final_result["D+1_low"]
                final_result_d1_close += final_result["D+1_close"]
                final_result_gap_size_ratio += final_result["gap_size_ratio"]
                final_result_vol_ma10_ratio += final_result["vol_ma10_ratio"]
                final_close_ma3_ratio += final_result["close/ma3 ratio"]
                final_close_ma5_ratio += final_result["close/ma5 ratio"]
                final_close_ma10_ratio += final_result["close/ma10 ratio"]
                final_close_ma20_ratio += final_result["close/ma20 ratio"]
                final_close_ma60_ratio += final_result["close/ma60 ratio"]
                final_close_ma120_ratio += final_result["close/ma120 ratio"]
                final_ma_converge_ratio += final_result["ma_converge_ratio"]
                final_result_profit += final_result["profit"]
                final_result_profit_rate += final_result["profit_rate"]

            print(i + 1, "/", len(codename_list), " 완료")

        final_result2 = {"date": final_result_date, "codename": final_codename, "D+0_open": final_result_d0_open,
                         "D+0_high": final_result_d0_high, "D+0_low": final_result_d0_low,
                         "D+0_close": final_result_d0_close, "D+0_change_ratio": final_result_d0_change_ratio,
                         "D+1_high": final_result_d1_high, "D+1_low": final_result_d1_low,
                         "D+1_close": final_result_d1_close,
                         "Vol_ratio": final_result_vol_ma10_ratio,
                         "gap_size_ratio": final_result_gap_size_ratio,
                         "close/ma3 ratio": final_close_ma3_ratio, "close/ma5 ratio": final_close_ma5_ratio,
                         "close/ma10 ratio": final_close_ma10_ratio, "close/ma20 ratio": final_close_ma20_ratio,
                         "close/ma60 ratio": final_close_ma60_ratio, "close/ma120 ratio": final_close_ma120_ratio,
                         "ma_converge_ratio": final_ma_converge_ratio,
                         "profit": final_result_profit, "profit_rate": final_result_profit_rate}

        print(len(final_result_date))

        final_result2_df = DataFrame(final_result2)

        sorted_result_df = final_result2_df.sort_values(by="date", ascending=False)

        # sqlite3로 저장
        # con = sqlite3.connect("c:/users/백/kosdaq_result"+ low_X_str + "~" + high_X_str + ".db")
        # final_result2_df.to_sql("결과", con, if_exists="replace")

        # 엑셀로 결과 저장
        self.dsstock_none_gui.simul_data_to_excel(sorted_result_df)
        print("엑셀저장 완료")

    def verify_change_ratio_button(self):  # 등락률 검증 시뮬레이션

        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권 기준 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")  # 대신증권 기준 코드와 코드네임 불러오기
        codename_list = df["name"]  # 코드네임을 리스트로 저장

        low_X = self.doubleSpinBox_13.value()
        high_X = self.doubleSpinBox_14.value()

        final_result_date = []
        final_codename = []
        final_result_d0_open = []
        final_result_d0_close = []
        final_result_d0_change_ratio = []
        final_result_d1_close = []
        final_result_vol_ma10_ratio = []
        final_result_gap_size_ratio = []
        final_close_ma3_ratio = []
        final_close_ma5_ratio = []
        final_close_ma10_ratio = []
        final_close_ma20_ratio = []
        final_close_ma60_ratio = []
        final_close_ma120_ratio = []
        final_ma_converge_ratio = []
        final_result_profit = []
        final_result_profit_rate = []

        for i, codename in enumerate(codename_list):  # 뺑뺑이 돌리기

            print(str(codename) + "진입")

            final_result = self.dsstock_none_gui.verify_change_ratio(codename, low_X, high_X)  # 날짜
            final_date = list(final_result["date"])
            print(len(final_date))

            if len(final_date) > 0:
                final_result_date += final_result["date"]
                final_codename += final_result["codename"]

                final_result_d0_open += final_result["D+0_open"]
                final_result_d0_close += final_result["D+0_close"]
                final_result_d0_change_ratio += final_result["D+0_change_ratio"]
                final_result_d1_close += final_result["D+1_close"]
                final_result_gap_size_ratio += final_result["gap_size_ratio"]
                final_result_vol_ma10_ratio += final_result["vol_ma10_ratio"]
                final_close_ma3_ratio += final_result["close/ma3 ratio"]
                final_close_ma5_ratio += final_result["close/ma5 ratio"]
                final_close_ma10_ratio += final_result["close/ma10 ratio"]
                final_close_ma20_ratio += final_result["close/ma20 ratio"]
                final_close_ma60_ratio += final_result["close/ma60 ratio"]
                final_close_ma120_ratio += final_result["close/ma120 ratio"]
                final_ma_converge_ratio += final_result["ma_cvg_ratio"]
                final_result_profit += final_result["profit"]
                final_result_profit_rate += final_result["profit_rate"]

            print(i + 1, "/", len(codename_list), " 완료")

        final_result2 = {"date": final_result_date, "codename": final_codename, "D+0_open": final_result_d0_open,
                         "D+0_close": final_result_d0_close, "D+0_change_ratio": final_result_d0_change_ratio,
                         "D+1_close": final_result_d1_close, "Vol_ratio": final_result_vol_ma10_ratio,
                         "gap_size_ratio": final_result_gap_size_ratio,
                         "close/ma3 ratio": final_close_ma3_ratio, "close/ma5 ratio": final_close_ma5_ratio,
                         "close/ma10 ratio": final_close_ma10_ratio, "close/ma20 ratio": final_close_ma20_ratio,
                         "close/ma60 ratio": final_close_ma60_ratio, "close/ma120 ratio": final_close_ma120_ratio,
                         "ma_cvg_ratio": final_ma_converge_ratio,
                         "profit": final_result_profit, "profit_rate": final_result_profit_rate}

        print(len(final_result_date))

        final_result2_df = DataFrame(final_result2)

        sorted_result_df = final_result2_df.sort_values(by="date", ascending=False)

        # sqlite3로 저장
        # con = sqlite3.connect("c:/users/백/kosdaq_result"+ low_X_str + "~" + high_X_str + ".db")
        # final_result2_df.to_sql("결과", con, if_exists="replace")

        # 엑셀로 결과 저장
        self.dsstock_none_gui.simul_data_to_excel(sorted_result_df)
        print("엑셀저장 완료")

    def veriyfy_gap_rising_button(self):  # 갭상승 종목 시뮬레이션

        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권 기준 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")  # 대신증권 기준 코드와 코드네임 불러오기
        codename_list = df["name"]  # 코드네임을 리스트로 저장

        low_X = self.doubleSpinBox_11.value()
        high_X = self.doubleSpinBox_12.value()

        final_result_date = []
        final_codename = []
        final_result_d0_open = []
        final_result_d0_close = []
        final_result_d0_change_ratio = []
        final_result_d1_close = []
        final_result_gap_size_ratio = []
        final_result_vol_ma10_ratio = []
        final_result_profit = []
        final_result_profit_rate = []

        for i, codename in enumerate(codename_list):  # 뺑뺑이 돌리기

            print(codename)

            final_result = self.dsstock_none_gui.verify_gap_size(codename, low_X, high_X)

            final_result_date += final_result["date"]
            final_codename += final_result["codename"]
            final_result_d0_open += final_result["D+0_open"]
            final_result_d0_close += final_result["D+0_close"]
            final_result_d0_change_ratio += final_result["D+0_change_ratio"]
            final_result_d1_close += final_result["D+1_close"]
            final_result_gap_size_ratio += final_result["gap_size_ratio"]
            final_result_vol_ma10_ratio += final_result["vol_ma10_ratio"]
            final_result_profit += final_result["profit"]
            final_result_profit_rate += final_result["profit_rate"]

            print(i + 1, "/", len(codename_list), " 완료")

        final_result2 = {"date": final_result_date, "codename": final_codename, "D+0_open": final_result_d0_open,
                         "D+0_close": final_result_d0_close,
                         "D+0_change_ratio": final_result_d0_change_ratio,
                         "D+1_close": final_result_d1_close, "gap_size_ratio": final_result_gap_size_ratio,
                         "vol_ma10_ratio": final_result_vol_ma10_ratio,
                         "profit": final_result_profit, "profit_rate": final_result_profit_rate}

        print(final_result2)

        final_result2_df = DataFrame(final_result2)
        print("OK3")
        sorted_result_df = final_result2_df.sort_values(by="date", ascending=False)

        print(sorted_result_df)
        print("File is saved as kosdaq_result_gap_rising")

        # sqlite3로 저장
        # con = sqlite3.connect("c:/users/백/kosdaq_result"+ low_X_str + "~" + high_X_str + ".db")
        # final_result2_df.to_sql("결과", con, if_exists="replace")

        # 엑셀로 저장
        self.dsstock_none_gui.simul_data_to_excel(sorted_result_df)

    def move_to_excel(self):
        wb = Workbook()
        ws = wb.create_sheet()

        filename = self.lineEdit_3.text()
        tablename = self.lineEdit_4.text()

        con = sqlite3.connect("c:/users/백/" + filename)
        data = pd.read_sql("SELECT * FROM " + tablename, con, index_col="index")  # 대신증권 기준 코드와 코드네임 불러오기

        # Dataframe을 엑셀로 뿌린다.
        for row in dataframe_to_rows(data, index=True, header=True):
            if len(row) > 1:
                ws.append(row)
        wb.save("c:/users/백/DB_to_Excel.xlsx")
        con.close()
        print("엑셀전달 완료")

    def trace_d1_change_button(self):
        con = sqlite3.connect("c:/users/백/DS_codedata.db")  # 대신증권 기준 코드와 코드네임 불러오기
        df = pd.read_sql("SELECT * FROM kosdaq", con, index_col="index")  # 대신증권 기준 코드와 코드네임 불러오기
        codename_list = df["name"]  # 코드네임을 리스트로 저장

        low_X = self.doubleSpinBox_16.value()
        high_X = self.doubleSpinBox_15.value()

        final_result_date = []
        final_codename = []
        final_result_d0_open = []
        final_result_d0_close = []
        final_result_d0_change_ratio = []
        final_result_d1_close = []
        final_result_vol_ma10_ratio = []
        final_result_gap_size_ratio = []
        final_close_ma3_ratio = []
        final_close_ma5_ratio = []
        final_close_ma10_ratio = []
        final_close_ma20_ratio = []
        final_close_ma60_ratio = []
        final_close_ma120_ratio = []
        final_result_profit = []
        final_result_profit_rate = []

        for i, codename in enumerate(codename_list):  # 뺑뺑이 돌리기

            print(codename)

            final_result = self.dsstock_none_gui.trace_d1_change(codename, low_X, high_X)

            final_result_date += final_result["date"]
            final_codename += final_result["codename"]
            final_result_d0_open += final_result["D+0_open"]
            final_result_d0_close += final_result["D+0_close"]
            final_result_d0_change_ratio += final_result["D+0_change_ratio"]
            final_result_d1_close += final_result["D+1_close"]
            final_result_gap_size_ratio += final_result["gap_size_ratio"]
            final_result_vol_ma10_ratio += final_result["vol_ma10_ratio"]
            final_close_ma3_ratio += final_result["close/ma3 ratio"]
            final_close_ma5_ratio += final_result["close/ma5 ratio"]
            final_close_ma10_ratio += final_result["close/ma10 ratio"]
            final_close_ma20_ratio += final_result["close/ma20 ratio"]
            final_close_ma60_ratio += final_result["close/ma60 ratio"]
            final_close_ma120_ratio += final_result["close/ma120 ratio"]
            final_result_profit += final_result["profit"]
            final_result_profit_rate += final_result["profit_rate"]

            print(i + 1, "/", len(codename_list), " 완료")

        final_result2 = {"date": final_result_date, "codename": final_codename, "D+0_open": final_result_d0_open,
                         "D+0_close": final_result_d0_close,
                         "D+0_change_ratio": final_result_d0_change_ratio,
                         "D+1_close": final_result_d1_close, "vol_ma10_ratio": final_result_vol_ma10_ratio,
                         "gap_size_ratio": final_result_gap_size_ratio,
                         "close/ma3 ratio": final_close_ma3_ratio, "close/ma5 ratio": final_close_ma5_ratio,
                         "close/ma10 ratio": final_close_ma10_ratio, "close/ma20 ratio": final_close_ma20_ratio,
                         "close/ma60 ratio": final_close_ma60_ratio, "close/ma120 ratio": final_close_ma120_ratio,
                         "profit": final_result_profit, "profit_rate": final_result_profit_rate}

        print(final_result2)

        final_result2_df = DataFrame(final_result2)
        sorted_result_df = final_result2_df.sort_values(by="date", ascending=False)

        print(sorted_result_df)
        print("File is saved as kosdaq_result_gap_rising")

        # sqlite3로 저장
        # con = sqlite3.connect("c:/users/백/kosdaq_result"+ low_X_str + "~" + high_X_str + ".db")
        # final_result2_df.to_sql("결과", con, if_exists="replace")

        # 엑셀로 저장
        self.dsstock_none_gui.simul_data_to_excel(sorted_result_df)
        print("최종완료")

    def test___(self):
        start_date = "201801"
        end_date = "201902"

        instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

        con = sqlite3.connect("c:/users/백/DS_codedata.db")
        kospi_kosdaq = self.comboBox.currentText()
        codedata = pd.read_sql("SELECT * FROM " + kospi_kosdaq, con, index_col="index")

        code_list = codedata["code"]
        name_list = codedata["name"]
        bong1 = "D"  # 일봉

        bong2 = "M"  # 월봉
        bong3 = "m"  # 분봉

        for i, code in enumerate(code_list):
            name = name_list[i]

            str_1 = str(i + 1)
            str_2 = str(len(code_list))

            instStockChart.SetInputValue(0, code)
            # instStockChart.SetInputValue(1, ord("1"))  #기간으로 요청
            instStockChart.SetInputValue(1, ord("2"))  # 개수로 요청
            # instStockChart.SetInputValue(2, end_date)
            # instStockChart.SetInputValue(3, start_date)
            instStockChart.SetInputValue(4, 1950)  # 요청개수
            # instStockChart.SetInputValue(5, (0, 2, 3, 4, 5, 6, 8, 37))
            instStockChart.SetInputValue(5, (0, 1, 2, 3, 4, 5, 6, 8, 37))  # 분봉전용
            instStockChart.SetInputValue(6, ord(bong3))
            instStockChart.SetInputValue(7, 10)  # 분틱차트 주기
            instStockChart.SetInputValue(9, ord("1"))

            # BlockRequest
            instStockChart.BlockRequest()

            time.sleep(0.25)  # 1종목 요청 후 X초 쉬고난뒤 다음 종목 요청

            # GetHeaderValue
            numdata = instStockChart.GetHeaderValue(3)
            print(numdata)
            numfield = instStockChart.GetHeaderValue(1)

            # GetDataValue : 0번열 : 날짜, 1: open, 2:high, 3:low, 4: close, 5:change, 6:vol
            date_list = []
            open_list = []
            high_list = []
            low_list = []
            close_list = []
            change_list = []
            volume_list = []
            change_ratio_list = []

            for j in range(numdata):
                date = instStockChart.GetDataValue(0, j)
                date_list.append(date)

            for j in range(numdata):
                open = instStockChart.GetDataValue(1, j)
                open_list.append(open)

            for j in range(numdata):
                high = instStockChart.GetDataValue(2, j)
                high_list.append(high)

            for j in range(numdata):
                low = instStockChart.GetDataValue(3, j)
                low_list.append(low)

            for j in range(numdata):
                close = instStockChart.GetDataValue(4, j)
                close_list.append(close)

            for j in range(numdata):
                change = instStockChart.GetDataValue(5, j)
                change_list.append(change)

            for j in range(numdata):
                volume = instStockChart.GetDataValue(6, j)
                volume_list.append(volume)

            for j in range(numdata):
                if j == numdata - 1:
                    change_ratio_list.append(0)

                    break
                change = change_list[j]
                close = close_list[j + 1]
                change_ratio = round(change / close, 5)

                change_ratio_list.append(change_ratio)

            ds_ohlcv = {"date": date_list, "open": open_list, "high": high_list, "low": low_list, "close": close_list,
                        "change": change_list, "volume": volume_list, "change_ratio": change_ratio_list}

            df = pd.DataFrame(ds_ohlcv, columns=["open", "high", "low", "close", "change", "volume", "change_ratio"],
                              index=ds_ohlcv["date"])

            today = datetime.datetime.today().strftime("%Y%m%d")
            # todaystr = str(today)

            con = sqlite3.connect("c:/users/백/stock_" + kospi_kosdaq + "_vol_ma.db")

            df.to_sql(name, con, if_exists="replace")

            lastmsg_here_def = str_1 + "/" + str_2 + name + " 완료"
            print(lastmsg_here_def)
            # self.statusbar.showMessage(lastmsg_here_def)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ds_stock = DS_stock()
    ds_stock.show()
    app.exec_()



if __name__ == "__main__":
    #create_table()
    #data_entry()
    #dynamic_data_entry()
    #run()
    #graph_data()
    #del_and_update()
    test()
