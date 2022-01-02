import pandas as pd
import numpy as np
from pandas_datareader import data
import matplotlib.pyplot as plt

# 구글 주가 데이터 불러오기
def load_financial_data(start_date, end_date, output_file):
    try:
        df = pd.read_pickle(output_file)
        print('File data found...reading GOOG data')
    except FileNotFoundError:
        print('File not found...downloading the GOOG data')
        df = data.DataReader('GOOG', 'yahoo', start_date, end_date)
        df.to_pickle(output_file)
    return df

goog_data = load_financial_data(start_date='2001-01-01', end_date='2018-01-01', output_file='goog_data_large.pkl')
window_size = 20

signals = pd.DataFrame(index=goog_data.index)
signals['orders'] = 0
# signals['high'] = goog_data['Adj Close'].shift(1).rolling(window=window_size).max()
signals['high'] = goog_data['Adj Close'].rolling(window=window_size).max()
signals['close'] = goog_data['Adj Close']
signals['max_R'] = (goog_data['Adj Close'] - signals['high']) / signals['high']

signals['low'] = goog_data['Adj Close'].rolling(window=window_size).min()
signals['min_R'] = (goog_data['Adj Close'] - signals['low']) / signals['low']

signals['buy_entry'] = signals.max_R == 0
signals['buy_exit'] = signals.min_R == 0
print(signals)



def turtle_trading(financial_data, window_size):
    signals = pd.DataFrame(index=financial_data.index)
    signals['orders'] = 0
    # 고가에 대한 윈도우 크기
    signals['high'] = financial_data['Adj Close'].shift(1).rolling(window=window_size).max()      # 전일 기준 최고가
    # 저가에 대한 윈도우 크기
    signals['low'] = financial_data['Adj Close'].shift(1).rolling(window=window_size).min()
    # 평균에 대한 윈도우 크기
    signals['avg'] = financial_data['Adj Close'].shift(1).rolling(window=window_size).mean()
    signals['buy_entry'] = financial_data['Adj Close'] > signals.high
    signals['buy_exit'] = financial_data['Adj Close'] < signals.avg

    init=True
    position=0

    for k in range(len(signals)):
        if signals['long_entry'][k] and position==0:
            signals.orders.values[k] = 1
            position = 1
        elif signals['short_entry'][k] and position==0:
            signals.orders.values[k] = -1
            position = -1
        elif signals['short_exit'][k] and position>0:
            signals.orders.values[k] = -1
            position = 0
        elif signals['long_exit'][k] and position<0:
            signals.orders.values[k] = 1
            position = 0
        else:
            signals.orders.values[k] = 0
    return signals