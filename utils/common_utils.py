# common_utils.py

import ccxt
import pandas as pd

def fetch_kucoin_data(symbol='BTC/USDT', timeframe='1d', since=None, until=None, limit=1000):
    """
    Fetches OHLCV data from the KuCoin exchange for a given symbol and timeframe.

    Args:
        symbol (str): The trading symbol to fetch data for (default: 'BTC/USDT').
        timeframe (str): The timeframe of the OHLCV data (default: '1d').
        since (int): The starting timestamp in milliseconds (optional).
        until (int): The ending timestamp in milliseconds (optional).
        limit (int): The maximum number of data points to fetch per request (default: 1000).

    Returns:
        pandas.DataFrame: A DataFrame containing the fetched OHLCV data.

    Raises:
        ValueError: If no OHLCV data is fetched from KuCoin.
    """
    kucoin = ccxt.kucoin()
    until = pd.to_datetime(until, unit='ms')  # Convert until to a Timestamp object
    all_data = []
    while True:
        ohlcv = kucoin.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
        if not ohlcv:
            break
        data = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        if symbol=='BTC/USDT':
            data['volume'] *= 1e8  # Convert volume to satoshis
            data[['open', 'high', 'low', 'close']] /= 1e8  # Convert prices to BTC
        all_data.append(data)
        since = ohlcv[-1][0] + 1  # Move to the next timestamp after the last fetched one
        if data['timestamp'].iloc[-1] >= until:
            break
    if not all_data:
        raise ValueError("No OHLCV data fetched from KuCoin.")
    all_data = pd.concat(all_data)
    all_data.set_index('timestamp', inplace=True)
    all_data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)
    return all_data[all_data.index <= until]
