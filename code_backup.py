    def condition_filter_tutle_piramid(self):  # buy, hold, sell, stoploss   조건 필터열 삽입(전략을 시뮬레이션 한다), 터틀트레이딩-피라미드

        #####
        self.sound_play()

        self.kospi_kosdaq = self.comboBox_2.currentText()
        code_name = self.codeNname_load()  # 종목 코드 로드
        con = sqlite3.connect("c:/users/백/%s_data_add_manual.db" % self.kospi_kosdaq)  # 키움증권 다운로드 종목 데이터 베이스
        con2 = sqlite3.connect("c:/users/백/%s_condition_filter.db" % self.kospi_kosdaq)  # 새로저장할 파일
        print("DB파일을 불러옵니다.(c:/users/백/%s_data_add_manual.db)" % self.kospi_kosdaq)

        name_list = code_name["name"]  # 코드네임을 리스트로 저장
        # name_list = ["셀트리온", "현대차", "삼성전자", "두산중공업", "동원산업", "GS건설"]  # 실험용
        # name_list = ["오비고"]  # 실험용
        # name_list = ["셀트리온제약","천보"]  # 실험용

        for i, name in enumerate(name_list):
            print(name, "진입")

            df = pd.read_sql("SELECT * FROM " + "'" + name + "'", con, index_col='index')
            df_result = DataFrame()

            open_list = list(df['open'])
            high_list = list(df['high'])
            low_list = list(df['low'])  # 저가
            close_list = list(df['close'])  # 종가
            change_list = list(df['change_ratio'])
            open_ratio_list = []
            ma60_list = list(df['dp_ma60'])

            N_list = list(df['atr20(N)'])
            max_20_R_list = list(df['max_20_R'])
            min_10_R_list = list(df['min_10_R'])
            max_60_R_list = list(df['max_60_R'])
            min_20_R_list = list(df['min_20_R'])

            buy_price_list = []
            sell_price_list = []
            condition_fliter_list = []
            event_list = []  # 관망이면 0, 나머지는 전부 1

            stoploss_price_list = []
            stoploss_list = []
            hold_unit_list = []
            hold_day_list = []  # 보유일수
            profit_list = []
            profit_ratio_list = []
            plus_profit_ratio_list = []  # 피라미드 적용 수익률
            winnloss_list = []
            buy_type_list = []
            plus_buy_price_list = []  # 추가매수 가격 조건
            averarge_buy_price_list = []  # 평균 매수가
            num_plus_buy_list = []
            num_plus_buy = 0

            for j in range(len(close_list)):

                max_20_R = max_20_R_list[j]
                min_10_R = min_10_R_list[j]
                max_60_R = max_60_R_list[j]
                min_20_R = min_20_R_list[j]
                ma60 = ma60_list[j]
                close = close_list[j]
                low = low_list[j]
                N = N_list[j]
                hold_unit = 0
                stoploss_price = 0
                buy_type = 0
                plus_buy_price = 0

                if j == 0:

                    hold_unit_list.append(hold_unit)
                    hold_day = 0
                    hold_day_list.append(hold_day)
                    buy_price_list.append(0)
                    sell_price_list.append(0)
                    condition = "non"
                    condition_fliter_list.append(condition)
                    stoploss_price_list.append(stoploss_price)
                    stoploss_list.append("x")
                    profit = 0
                    profit_list.append(profit)
                    profit_ratio = 0
                    profit_ratio_list.append(profit_ratio)
                    plus_profit_ratio = 0
                    plus_profit_ratio_list.append(plus_profit_ratio)
                    event_list.append(0)

                    open_ratio_list.append(0)
                    winnloss = 0
                    winnloss_list.append(winnloss)
                    buy_type_list.append(buy_type)
                    plus_buy_price_list.append(plus_buy_price)
                    averarge_buy_price_list.append(0)
                    num_plus_buy_list.append(num_plus_buy)

                elif max_20_R == 0 and min_10_R == 0:  # 이상한 데이터 제거용
                    hold_unit_list.append(hold_unit)
                    hold_day = 0
                    hold_day_list.append(hold_day)
                    buy_price_list.append(0)
                    sell_price_list.append(0)
                    condition = "non"
                    condition_fliter_list.append(condition)
                    stoploss_price_list.append(stoploss_price)
                    stoploss_list.append("x")
                    profit = 0
                    profit_list.append(profit)
                    profit_ratio = 0
                    profit_ratio_list.append(profit_ratio)
                    plus_profit_ratio = 0
                    plus_profit_ratio_list.append(plus_profit_ratio)
                    event_list.append(0)

                    open_ratio_list.append(0)
                    winnloss = 0
                    winnloss_list.append(winnloss)
                    buy_type_list.append(buy_type)
                    plus_buy_price_list.append(plus_buy_price)
                    averarge_buy_price_list.append(0)
                    num_plus_buy_list.append(num_plus_buy)

                else:
                    hold_unit = hold_unit_list[j - 1]
                    if hold_unit > 0:

                        stoploss_price = stoploss_price_list[j - 1]
                        hold_day = hold_day_list[j - 1] + 1
                        buy_type = buy_type_list[j - 1]
                        plus_buy_price = plus_buy_price_list[j - 1]

                    else:
                        stoploss_price = 0
                        hold_day = 0
                        buy_type = 0
                        plus_buy_price = 0

                    d1_change = change_list[j - 1]
                    d1_open = open_list[j - 1]
                    d1_close = close_list[j - 1]
                    d1_high = high_list[j - 1]
                    d1_low = low_list[j - 1]
                    d1_truerange = d1_high - d1_low
                    open_ratio = (d1_open - d1_close) / d1_close
                    open_ratio_list.append(open_ratio)
                    winnloss = winnloss_list[j - 1]

                    if max_20_R == 0 and N != None and ma60 != None and ma60 > 1 and winnloss == 0 and hold_unit == 0:
                        # 신규매입 조건 : 20일 신고가, 직전거래에서 손해시(winnloss == 0) --- S1 적용

                        hold_unit = 1
                        hold_unit_list.append(hold_unit)
                        hold_day_list.append(hold_day)

                        condition = "buy_s1"
                        condition_fliter_list.append(condition)
                        buy_price = close
                        buy_price_list.append(buy_price)

                        stoploss = "x"
                        stoploss_list.append(stoploss)

                        stoploss_price = close - (2 * N)
                        stoploss_price_list.append(stoploss_price)

                        sell_price = 0
                        sell_price_list.append(sell_price)

                        profit = 0
                        profit_list.append(profit)
                        profit_ratio = 0
                        profit_ratio_list.append(profit_ratio)
                        plus_profit_ratio = 0
                        plus_profit_ratio_list.append(plus_profit_ratio)
                        event_list.append(1)
                        winnloss_list.append(winnloss)
                        buy_type = "S1"
                        buy_type_list.append(buy_type)
                        plus_buy_price = close + N
                        plus_buy_price_list.append(plus_buy_price)

                        averarge_buy_price = close
                        averarge_buy_price_list.append(averarge_buy_price)
                        num_plus_buy_list.append(num_plus_buy)

                    elif hold_unit > 0 and close > plus_buy_price:  # 추가 매수 조건
                        hold_unit = hold_unit + 1
                        hold_unit_list.append(hold_unit)
                        hold_day_list.append(hold_day)

                        num_plus_buy = num_plus_buy + 1  # 몇번째 추가 매수인지?
                        num_plus_buy_list.append(num_plus_buy)

                        condition = "buy" + str(num_plus_buy)
                        condition_fliter_list.append(condition)

                        buy_price = close
                        buy_price_list.append(buy_price)

                        averarge_buy_price = (averarge_buy_price_list[j - 1] * num_plus_buy) / (
                                    num_plus_buy + 1) + close / (num_plus_buy + 1)
                        #  ↑ 직전 평균값을 이용하여 현재 평균값을 구한다.
                        averarge_buy_price_list.append(averarge_buy_price)

                        stoploss = "x"
                        stoploss_list.append(stoploss)

                        # stoploss_price = close - (2 * N)
                        # stoploss_price_list.append(stoploss_price)                # 손절값을 직전 매수값 기준으로

                        stoploss_price = averarge_buy_price - (2 * N)  # 손절값을 평균매수값 기준으로 조정
                        stoploss_price_list.append(stoploss_price)

                        sell_price = 0
                        sell_price_list.append(sell_price)

                        profit = 0
                        profit_list.append(profit)
                        profit_ratio = 0
                        profit_ratio_list.append(profit_ratio)
                        plus_profit_ratio = 0
                        plus_profit_ratio_list.append(plus_profit_ratio)
                        event_list.append(1)
                        winnloss_list.append(winnloss)
                        buy_type = buy_type_list[j - 1]  # 청산 조건이 S1, S2가 다르므로 필요한 데이터
                        buy_type_list.append(buy_type)

                        plus_buy_price = close + N
                        plus_buy_price_list.append(plus_buy_price)

                    elif max_60_R == 0 and N != None and ma60 != None and ma60 > 1 and winnloss == 1 and hold_unit == 0:
                        # S2 매수조건 진입
                        hold_unit = 1
                        hold_unit_list.append(hold_unit)
                        hold_day_list.append(hold_day)

                        condition = "buy_s2"
                        condition_fliter_list.append(condition)
                        buy_price = close
                        buy_price_list.append(buy_price)

                        stoploss = "x"
                        stoploss_list.append(stoploss)

                        stoploss_price = close - (2 * N)
                        stoploss_price_list.append(stoploss_price)

                        sell_price = 0
                        sell_price_list.append(sell_price)

                        averarge_buy_price = close
                        averarge_buy_price_list.append(averarge_buy_price)

                        profit = 0
                        profit_list.append(profit)
                        profit_ratio = 0
                        profit_ratio_list.append(profit_ratio)
                        plus_profit_ratio = 0
                        plus_profit_ratio_list.append(plus_profit_ratio)
                        event_list.append(1)
                        winnloss_list.append(winnloss)
                        buy_type = "S2"
                        buy_type_list.append(buy_type)
                        plus_buy_price = close + N
                        plus_buy_price_list.append(plus_buy_price)
                        num_plus_buy_list.append(num_plus_buy)

                    elif hold_unit > 0 and low < stoploss_price or open_list[j] < stoploss_price:  # 손절

                        hold_unit = 0
                        hold_unit_list.append(hold_unit)
                        hold_day = hold_day_list[j - 1]
                        hold_day_list.append(hold_day)
                        condition_fliter_list.append("stoploss")
                        buy_price = buy_price_list[j - 1]
                        buy_price_list.append(buy_price)
                        averarge_buy_price = averarge_buy_price_list[j - 1]
                        averarge_buy_price_list.append(averarge_buy_price)

                        stoploss = "stoploss"
                        stoploss_list.append(stoploss)
                        stoploss_price = stoploss_price_list[j - 1]
                        stoploss_price_list.append(stoploss_price)

                        if open_list[j] < stoploss_price:
                            sell_price = open_list[j]
                        else:
                            sell_price = stoploss_price
                        sell_price_list.append(sell_price)

                        profit = sell_price - averarge_buy_price
                        profit_list.append(profit)

                        profit_ratio = (profit / averarge_buy_price) * 100
                        profit_ratio = round(profit_ratio, 2)
                        profit_ratio_list.append(profit_ratio)

                        plus_profit_ratio = profit_ratio * (num_plus_buy_list[j - 1] + 1)
                        plus_profit_ratio_list.append(plus_profit_ratio)

                        event_list.append(1)
                        winnloss = 0
                        winnloss_list.append(winnloss)
                        buy_type = buy_type_list[j - 1]
                        buy_type_list.append(buy_type)

                        num_plus_buy = num_plus_buy_list[j - 1]
                        num_plus_buy_list.append(num_plus_buy)
                        num_plus_buy = 0

                        plus_buy_price = 0
                        plus_buy_price_list.append(plus_buy_price)

                    elif min_10_R == 0 and buy_type == "S1" and hold_unit > 0:  # S1 청산 조건 : 종가기준 10일 최저가 하향 돌파

                        hold_unit = 0
                        hold_unit_list.append(hold_unit)
                        hold_day_list.append(hold_day)

                        buy_price = buy_price_list[j - 1]
                        buy_price_list.append(buy_price)
                        averarge_buy_price = averarge_buy_price_list[j - 1]
                        averarge_buy_price_list.append(averarge_buy_price)

                        stoploss = "x"
                        stoploss_list.append(stoploss)
                        stoploss_price = stoploss_price_list[j - 1]
                        stoploss_price_list.append(stoploss_price)
                        sell_price = close  # 종가기준 청산
                        condition_fliter_list.append("sell")

                        sell_price_list.append(sell_price)
                        profit = sell_price - averarge_buy_price
                        profit_list.append(profit)
                        profit_ratio = (profit / averarge_buy_price) * 100
                        profit_ratio = round(profit_ratio, 2)
                        profit_ratio_list.append(profit_ratio)

                        plus_profit_ratio = profit_ratio * (num_plus_buy_list[j - 1] + 1)
                        plus_profit_ratio_list.append(plus_profit_ratio)

                        event_list.append(1)

                        if profit > 0:
                            winnloss = 1  # 이득
                        else:
                            winnloss = 0  # 손해
                        winnloss_list.append(winnloss)
                        buy_type = buy_type_list[j - 1]
                        buy_type_list.append(buy_type)

                        num_plus_buy = num_plus_buy_list[j - 1]
                        num_plus_buy_list.append(num_plus_buy)
                        num_plus_buy = 0

                        plus_buy_price = 0
                        plus_buy_price_list.append(plus_buy_price)

                    elif min_20_R == 0 and buy_type == "S2" and hold_unit > 0:  # S2 청산 조건 : 종가기준 10일 최저가 하향 돌파

                        hold_unit = 0
                        hold_unit_list.append(hold_unit)
                        hold_day_list.append(hold_day)

                        buy_price = buy_price_list[j - 1]
                        buy_price_list.append(buy_price)
                        averarge_buy_price = averarge_buy_price_list[j - 1]
                        averarge_buy_price_list.append(averarge_buy_price)

                        stoploss = "x"
                        stoploss_list.append(stoploss)
                        stoploss_price = stoploss_price_list[j - 1]
                        stoploss_price_list.append(stoploss_price)
                        sell_price = close  # 종가기준 청산
                        condition_fliter_list.append("sell")

                        sell_price_list.append(sell_price)
                        profit = sell_price - averarge_buy_price
                        profit_list.append(profit)
                        profit_ratio = (profit / averarge_buy_price) * 100
                        profit_ratio = round(profit_ratio, 2)
                        profit_ratio_list.append(profit_ratio)

                        plus_profit_ratio = profit_ratio * (num_plus_buy_list[j - 1] + 1)
                        plus_profit_ratio_list.append(plus_profit_ratio)

                        event_list.append(1)

                        if profit > 0:
                            winnloss = 1  # 이득
                        else:
                            winnloss = 0  # 손해
                        winnloss_list.append(winnloss)
                        buy_type = buy_type_list[j - 1]
                        buy_type_list.append(buy_type)

                        num_plus_buy = num_plus_buy_list[j - 1]
                        num_plus_buy_list.append(num_plus_buy)
                        num_plus_buy = 0

                        plus_buy_price = 0
                        plus_buy_price_list.append(plus_buy_price)

                    elif hold_unit > 0:  # 홀드

                        hold_unit = hold_unit_list[j - 1]
                        hold_unit_list.append(hold_unit)
                        hold_day_list.append(hold_day)
                        condition_fliter_list.append("hold")
                        buy_price = buy_price_list[j - 1]
                        buy_price_list.append(buy_price)
                        averarge_buy_price = averarge_buy_price_list[j - 1]
                        averarge_buy_price_list.append(averarge_buy_price)

                        stoploss = "x"
                        stoploss_list.append(stoploss)
                        stoploss_price = stoploss_price_list[j - 1]
                        stoploss_price_list.append(stoploss_price)

                        sell_price = 0
                        sell_price_list.append(sell_price)

                        profit = 0
                        profit_list.append(profit)
                        profit_ratio = 0
                        profit_ratio_list.append(profit_ratio)
                        plus_profit_ratio = 0
                        plus_profit_ratio_list.append(plus_profit_ratio)
                        event_list.append(0)
                        # event_list.append(1)          # 홀드는 이벤트에 포함/불포함 선택한다.
                        winnloss_list.append(winnloss)
                        buy_type = buy_type_list[j - 1]
                        buy_type_list.append(buy_type)

                        plus_buy_price = plus_buy_price_list[j - 1]
                        plus_buy_price_list.append(plus_buy_price)

                        num_plus_buy = num_plus_buy_list[j - 1]
                        num_plus_buy_list.append(num_plus_buy)

                    else:  # 그외는 관망

                        hold_unit = 0
                        hold_unit_list.append(hold_unit)
                        hold_day = 0
                        hold_day_list.append(hold_day)
                        condition_fliter_list.append("non")  # 관망
                        buy_price = 0
                        buy_price_list.append(buy_price)
                        averarge_buy_price = 0
                        averarge_buy_price_list.append(averarge_buy_price)

                        stoploss = "x"
                        stoploss_list.append(stoploss)
                        stoploss_price = 0
                        stoploss_price_list.append(stoploss_price)

                        sell_price = 0
                        sell_price_list.append(sell_price)

                        profit = 0
                        profit_list.append(profit)
                        profit_ratio = 0
                        plus_profit_ratio = 0
                        plus_profit_ratio_list.append(plus_profit_ratio)
                        profit_ratio_list.append(profit_ratio)
                        event_list.append(0)
                        winnloss_list.append(winnloss)
                        buy_type = 0
                        buy_type_list.append(buy_type)

                        plus_buy_price = 0
                        plus_buy_price_list.append(plus_buy_price)

                        num_plus_buy = 0
                        num_plus_buy_list.append(num_plus_buy)

            df_result['date'] = df['date']
            df_result['name'] = df['name']
            df_result['open'] = df['open']
            df_result['high'] = df['high']
            df_result['low'] = df['low']
            df_result['close'] = df['close']
            df_result['change'] = df['change']
            df_result['change_ratio'] = df['change_ratio']
            df_result['dp_ma60'] = ma60_list
            # df_result['open_ratio'] = open_ratio_list
            # df_result['volume'] = df['volume']
            df_result['atr20'] = df['atr20(N)']
            df_result['max_20R'] = df['max_20_R']
            df_result['min_10R'] = df['min_10_R']
            df_result['max_60R'] = df['max_60_R']
            df_result['min_20R'] = df['min_20_R']
            df_result['sichong'] = df['si_chong']
            # df_result['vol_d1r'] = df['vol_d1_R']

            # df_result['up_ggori'] = u_tail_R_list
            # df_result['btm_ggori'] = l_tail_R_list

            df_result['buy_sell'] = condition_fliter_list
            df_result['buy_price'] = buy_price_list
            df_result['avr_buy_price'] = averarge_buy_price_list
            df_result['sell_price'] = sell_price_list
            df_result['stoploss_price'] = stoploss_price_list
            df_result['plus_buy_price'] = plus_buy_price_list
            df_result['stoploss'] = stoploss_list
            df_result['hold_unit'] = hold_unit_list
            df_result['hold_day'] = hold_day_list
            df_result['profit'] = profit_list
            df_result['profit_ratio'] = profit_ratio_list
            df_result['plus_profit_ratio'] = plus_profit_ratio_list
            df_result['event'] = event_list
            df_result['buy_type'] = buy_type_list
            df_result['num_plus_buy'] = num_plus_buy_list

            # self.simul_data_to_excel(df_result)         ###%%%% 엑셀로 보낸다
            df_result.to_sql(name, con2, if_exists="replace")
            print("%s / %s %s 완료" % (i + 1, len(name_list), name))
        print("최종완료")
        con.close()
        con2.close()
        ###$$$$$
        self.sound_play()

### AI_test.py ### 20201125 백업
def past_Day_ohlc(self, name):  # 전시점 tech 넣기

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
        v20 = df['vma20_R']

        # dp_ma3 = df['dp_ma3']
        dp_ma5 = df['dp_ma5']
        dp_ma10 = df['dp_ma10']
        dp_ma20 = df['dp_ma20']

        # dp_ma60 = df['dp_ma60']
        # dp_ma120 = df['dp_ma120']
        # dp_ma480= df['dp_ma480']

        vol_d1_R = df['vol_d1_R']
        # bband30_upR = df['bbands30_upR']
        # bband30_downR = df['bbands30_downR']
        # bbands_width= df['bbands_width']
        # macd_line = df['macd_line5,34,7']
        # macd_sig = df['macd_sig5,34,7']
        # macd_histo = df['macd_histo5,34,7']
        print("완료2")

        # rsi20 = df['rsi20']

        bf1_open_list = []
        bf1_close_list = []
        bf1_high_list = []
        bf1_low_list = []
        bf1_change_R_list = []
        bf1_v20maR_list = []

        # bf1_dp_ma3 = []
        bf1_dp_ma5 = []
        bf1_dp_ma10 = []
        bf1_dp_ma20 = []

        # bf1_dp_ma60 = []
        # bf1_dp_ma120 = []
        # bf1_dp_ma480 = []

        bf1_vol_d1_R = []
        bf1_bband30_upR = []
        bf1_bband30_downR = []
        bf1_bbands_width = []
        bf1_macd_line = []
        bf1_macd_sig = []
        bf1_macd_histo = []

        bf1_rsi20 = []

        for i in range(len(op)):

            if i == 0:  # 가장 과거 데이터는 전일 정보가 없으므로 0추가 (과거 → 현재), 0부터 1을 더뺀다
                bf1_open_list.append(0)
                bf1_close_list.append(0)
                bf1_high_list.append(0)
                bf1_low_list.append(0)
                bf1_change_R_list.append(0)
                bf1_v20maR_list.append(0)

                # bf1_dp_ma3.append(0)
                bf1_dp_ma5.append(0)
                bf1_dp_ma10.append(0)
                bf1_dp_ma20.append(0)

                # bf1_dp_ma60.append(0)
                # bf1_dp_ma120.append(0)
                # bf1_dp_ma480.append(0)

                bf1_vol_d1_R.append(0)
                bf1_bband30_upR.append(0)
                bf1_bband30_downR.append(0)
                bf1_bbands_width.append(0)
                bf1_macd_line.append(0)
                bf1_macd_sig.append(0)
                bf1_macd_histo.append(0)

                bf1_rsi20.append(0)

            else:  # 둘째날 데이터

                bf1_open_list.append(op[ i -1])
                bf1_close_list.append(cl[ i -1])
                bf1_high_list.append(hi[ i -1])
                bf1_low_list.append(lo[ i -1])
                bf1_change_R_list.append(ch[ i -1])
                bf1_v20maR_list.append(v20[ i -1])

                # bf1_dp_ma3.append(dp_ma3[i-1])
                bf1_dp_ma5.append(dp_ma5[ i -1])
                bf1_dp_ma10.append(dp_ma10[ i -1])
                bf1_dp_ma20.append(dp_ma20[ i -1])

                # bf1_dp_ma60.append(dp_ma60[i-1])
                #
                # bf1_dp_ma120.append(dp_ma120[i-1])
                # bf1_dp_ma480.append(dp_ma480[i-1])

                bf1_vol_d1_R.append(vol_d1_R[ i -1])
                bf1_bband30_upR.append(bband30_upR[ i -1])
                bf1_bband30_downR.append(bband30_downR[ i -1])
                bf1_bbands_width.append(bbands_width[ i -1])
                bf1_macd_line.append(macd_line[ i -1])
                bf1_macd_sig.append(macd_sig[ i -1])
                bf1_macd_histo.append(macd_histo[ i -1])

                bf1_rsi20.append(rsi20[ i -1])

        df['bf1_open'] = bf1_open_list
        df['bf1_close'] = bf1_close_list
        df['bf1_high'] = bf1_high_list
        df['bf1_low'] = bf1_low_list
        df['bf1_change_R'] =bf1_change_R_list
        df['bf1_v20maR'] = bf1_v20maR_list
        # df['bf1_dp_ma3'] = bf1_dp_ma3
        df['bf1_dp_ma5'] = bf1_dp_ma5
        df['bf1_dp_ma10'] = bf1_dp_ma10
        df['bf1_dp_ma20'] = bf1_dp_ma20

        # df['bf1_dp_ma60'] =bf1_dp_ma60
        # df['bf1_dp_ma120'] =bf1_dp_ma120

        df['bf1_vol_d1_R'] = bf1_vol_d1_R
        df['bf1_bband30_upR'] = bf1_bband30_upR
        df['bf1_bband30_downR'] = bf1_bband30_downR
        df['bf1_bbands_width'] = bf1_bbands_width

        df['bf1_rsi20'] = bf1_rsi20

    con.close()
    return df


### AI_test.py ### 20201125 백업
def add_past_Day_ohlc(self):
    self.kospi_kosdaq = self.comboBox_2.currentText()
    code_name = self.codeNname_load()  # 종목 코드 로드
    con2 = sqlite3.connect("c:/users/백/" + self.kospi_kosdaq + "_data.db")  # 키움증권 다운로드 종목 데이터 베이스

    name_list = code_name["name"]  # 코드네임을 리스트로 저장
    for i, name in enumerate(name_list):  # 뺑뺑이 돌리기
        print(name + " 진입")
        df = self.past_Day_ohlc(name)
        if len(df['open']) > 0:    #값이 없는 것은 pass
            df.to_sql(name, con2, if_exists="replace")
        print(i + 1, "/", len(name_list), name, " 완료")
    con2.close()
    print("past_day_ohlcv 최종완료")



### AI_test.py ### 20201125 백업
def D_N_ohlc(self, name):  # 1일~5일 ohlc확인  삭제 검토 할 것

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

        D1_v20maR_list = []

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

        v20mar = df['vma20_R']
        for i in range(len(op)):

            if i > len(op) - 1 - 1:  # 가장 최근 데이터는 익일 정보가 없으므로 0추가 (과거 → 현재), 0부터 1을 더뺀다
                D1_open_list.append(0)
                D1_close_list.append(0)
                D1_high_list.append(0)
                D1_low_list.append(0)
                D1_change_R_list.append(0)

                D1_v20maR_list.append(0)

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

            elif i > len(op) - 2 - 1:

                D1_open_list.append(op[i + 1])
                D1_close_list.append(cl[i + 1])
                D1_high_list.append(hi[i + 1])
                D1_low_list.append(lo[i + 1])
                D1_change_R_list.append(ch[i + 1])
                D1_v20maR_list.append(v20mar[i + 1])

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

            elif i > len(op) - 3 - 1:

                D1_open_list.append(op[i + 1])
                D1_close_list.append(cl[i + 1])
                D1_high_list.append(hi[i + 1])
                D1_low_list.append(lo[i + 1])
                D1_change_R_list.append(ch[i + 1])

                D1_v20maR_list.append(v20mar[i + 1])

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

            else:

                D1_open_list.append(op[i + 1])
                D1_close_list.append(cl[i + 1])
                D1_high_list.append(hi[i + 1])
                D1_low_list.append(lo[i + 1])
                D1_change_R_list.append(ch[i + 1])
                D1_v20maR_list.append(v20mar[i + 1])

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

        df['D1_open'] = D1_open_list
        df['D1_close'] = D1_close_list
        df['D1_high'] = D1_high_list
        df['D1_low'] = D1_low_list
        df['D1_changeR'] = D1_change_R_list

        df['D1_v20maR'] = D1_v20maR_list

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

    con.close()

    return df




### AI_test.py ### 20201125 백업
def add_D_N_ohlc(self):  #3일이후 ohlc 넣기
    self.kospi_kosdaq = self.comboBox_2.currentText()

    code_name = self.codeNname_load()  # 종목 코드 로드
    con2 = sqlite3.connect("c:/users/백/" + self.kospi_kosdaq + "_data.db")  # 키움증권 다운로드 종목 데이터 베이스
    name_list = code_name["name"]  # 코드네임을 리스트로 저장

    for i, name in enumerate(name_list):  # 뺑뺑이 돌리기
        # for i in [523,524,525,526]:  # 뺑뺑이 돌리기
        # name = name_list[i]
        print(name + " 진입")
        df = self.D_N_ohlc(name)
        print(len(df['open']))
        if len(df['open']) > 0:
            df.drop("level_0", axis=1, inplace=True)  # column을 삭제하는 가장 좋은 방법은 drop을 사용하는 것입니다.
            df.to_sql(name, con2, if_exists="replace")
        print(i + 1, "/", len(name_list), name, " 완료")
    con2.close()
    print("D+N_high_low 최종완료")
