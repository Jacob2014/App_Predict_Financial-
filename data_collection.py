import pandas as pd
import MetaTrader5 as mt5

def fetch_moex_data(symbol='SBER', timeframe=mt5.TIMEFRAME_D1, n=100):
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
        return None

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n)
    if rates is None:
        print("No data for symbol:", symbol)
        mt5.shutdown()
        return None

    df_moex = pd.DataFrame(rates)
    df_moex['time'] = pd.to_datetime(df_moex['time'], unit='s')
    df_moex = df_moex.rename(columns={"time": "TRADEDATE", "close": "CLOSE"})
    mt5.shutdown()
    return df_moex

def fetch_binance_data(symbol='BTCUSDT'):
    import requests
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d'
    response = requests.get(url)
    data = response.json()
    df_binance = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
        'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
        'taker_buy_quote_asset_volume', 'ignore'
    ])
    df_binance['timestamp'] = pd.to_datetime(df_binance['timestamp'], unit='ms')
    df_binance['close'] = df_binance['close'].astype(float)
    return df_binance
