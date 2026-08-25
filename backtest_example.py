# Copyright 2019-2025, Orchard Forex
# https://orchardforex.com

import MetaTrader5 as mt5
import pandas as pd
import datetime

from backtesting import Backtest
from classes.simple_strategy import SimpleStrategy

# from backtesting import Backtest, Strategy
def main():

    if not mt5.initialize():
        log("terminal initialisation failed")
        return
    log("MT5 successfully initialised")

    # get history data from mt, only using one instrument / tf for now
    history = pd.DataFrame(mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_H1, 0, 1000))   
    history['time'] = pd.to_datetime(history['time'], unit='s')
    history.set_index('time', inplace=True)
    history.rename(columns={'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'tick_volume':'Volume'}, inplace=True)
    print(history)     

    test = Backtest(history, SimpleStrategy, cash=10000, hedging=True, finalize_trades=True)
    result = test.run()

    print(result)

    print(f'buy count = {result._strategy.buy_count}')
    print(f'sell count = {result._strategy.sell_count}')
    
    mt5.shutdown()
    return

def log(msg):

    now = datetime.datetime.now()
    now_str = now.strftime('%Y.%m.%d %H:%M:%S')
    msg = f"{now_str} {msg}"
    print(msg)

if __name__ == "__main__":
    main()

# pip install backtesting
# pip install backtesting --upgrade
# pip install bokeh --upgrade
# pip install jinja2==3.0.3 --force-reinstall
# pip install numpy==1.26.4 --force-reinstall

# pip install -U git+https://github.com/OrchardForexTutorials/pandas-ta.git --no-cache-dir
