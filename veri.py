from binance.client import Client
import talib as ta
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import math

class BinanceConnection:
    def __init__(self, file):
        self.connect(file)

    """ Creates Binance client """

    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)


def generateSupertrend(close_array, high_array, low_array, atr_period, atr_multiplier):

    try:
        atr = ta.ATR(high_array, low_array, close_array, atr_period)
    except:
        print('exception in atr:', sys.exc_info()[0], 'pair', pair, flush=True)
        print('filename', filename, flush=True)
        return False, False

    previous_final_upperband = 0
    previous_final_lowerband = 0
    final_upperband = 0
    final_lowerband = 0
    previous_close = 0
    previous_supertrend = 0
    supertrend = []
    supertrendc = 0

    for i in range(0, len(close_array)):
        if np.isnan(close_array[i]):
            pass
        else:
            highc = high_array[i]
            lowc = low_array[i]
            atrc = atr[i]
            closec = close_array[i]

            if math.isnan(atrc):
                atrc = 0

            basic_upperband = (highc + lowc) / 2 + atr_multiplier * atrc
            basic_lowerband = (highc + lowc) / 2 - atr_multiplier * atrc

            if basic_upperband < previous_final_upperband or previous_close > previous_final_upperband:
                final_upperband = basic_upperband
            else:
                final_upperband = previous_final_upperband

            if basic_lowerband > previous_final_lowerband or previous_close < previous_final_lowerband:
                final_lowerband = basic_lowerband
            else:
                final_lowerband = previous_final_lowerband

            if previous_supertrend == previous_final_upperband and closec <= final_upperband:
                supertrendc = final_upperband
            else:
                if previous_supertrend == previous_final_upperband and closec >= final_upperband:
                    supertrendc = final_lowerband
                else:
                    if previous_supertrend == previous_final_lowerband and closec >= final_lowerband:
                        supertrendc = final_lowerband
                    elif previous_supertrend == previous_final_lowerband and closec <= final_lowerband:
                        supertrendc = final_upperband

            supertrend.append(supertrendc)

            previous_close = closec

            previous_final_upperband = final_upperband

            previous_final_lowerband = final_lowerband

            previous_supertrend = supertrendc

    return supertrend

if __name__ == '__main__':
    filename = 'credentials.txt'

    connection = BinanceConnection(filename)

    interval = '1d'

    pair = 'BTCUSDT'

    limit = 500

    klines = connection.client.get_klines(symbol=pair, interval=interval, limit=limit)

    open_time = [int(entry[0]) for entry in klines]

    open = [float(entry[1]) for entry in klines]
    high = [float(entry[2]) for entry in klines]
    low = [float(entry[3]) for entry in klines]
    close = [float(entry[4]) for entry in klines]

    close_array = np.asarray(close)
    high_array = np.asarray(high)
    low_array = np.asarray(low)

    new_time = [datetime.fromtimestamp(time / 1000) for time in open_time]

    new_time_x = [date.strftime("%y-%m-%d") for date in new_time]

    supertrend = generateSupertrend(close_array, high_array, low_array, atr_period=10, atr_multiplier=2)

    plt.figure(figsize=(11, 6))
    plt.plot(new_time_x[400:], close_array[400:], label='Price')
    plt.plot(new_time_x[400:], supertrend[400:], label='Supertrend')
    plt.xticks(rotation=90, fontsize=5)
    plt.title("Supertrend Plot for BTC/USDT")
    plt.xlabel("Open Time")
    plt.ylabel("Value")
    plt.legend()
    plt.show()
plt.xticks(rotation=90, fontsize=5)
new_time = [datetime.fromtimestamp(time / 1000) for time in open_time]

new_time_x = [date.strftime("%y-%m-%d") for date in new_time]

son_kapanis = close_array[-1]
onceki_kapanis = close_array[-2]

son_supertrend_deger = supertrend[-1]
onceki_supertrend_deger = supertrend[-2]

# renk yeşile dönüyor, trend yükselişe geçti
if son_kapanis > son_supertrend_deger and onceki_kapanis < onceki_supertrend_deger:
	print('al sinyali')

# renk kırmızıya dönüyor, trend düşüşe geçti
if son_kapanis < son_supertrend_deger and onceki_kapanis > onceki_supertrend_deger:
        print('sat sinyali')


