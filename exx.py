def gap_rising_2(self, name):  #조건을 시뮬레이션한 결과값을 원데이터에 0,1로 표시하고 저장
    df = self.load_stock_data(name)
    close_list = df["close"]
    open_list = df["open"]

    C_gap_rising_list = []  #C = Condition(조건)


    for i, open in enumerate(open_list):

        if (len(open_list) - 1) > i > 0:  # 다음날 바로 매도 하기때문에 0은 제외, 맨처음데이터는 제외(전일 데이터가 없기 때문)
            dm1_close = close_list[df.index[i + 1]]  # 전일 종가
            d0_close = close_list[df.index[i]]  # 당일 종가

            if (open > dm1_close) and (d0_close > dm1_close):
                C_gap_rising_list.append(0)
            else:
                C_gap_rising_list.append(1)
    df["C_gap_rising"] = C_gap_rising_list


    con = sqlite3.connect("c:/users/백/stock_kosdaq_vol_ma.db")
    # con = sqlite3.connect("c:/users/백/DS_kosdaq_" + todaystr + ".db")
    df.to_sql(name, con, if_exists="replace")


    return result
