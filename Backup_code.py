def merge_db(self, codename):  # 데이터베이스 합치기
    # 데이터 불러오기
    con = sqlite3.connect("c:/users/백/stock_kosdaq2.db")
    jum = "'"
    inputstr = "SELECT * FROM " + jum + codename + jum
    self.merge_data = pd.read_sql(inputstr, con, index_col="index")  # 변수로 데이터를 읽어옴

    con = sqlite3.connect("c:/users/백/stock_kosdaq.db")  # 합체할 데이터
    self.merge_data.to_sql(codename, con)