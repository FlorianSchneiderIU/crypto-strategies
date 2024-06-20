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

def calculate_optimal_value(data, initial_cash=10000, commission=0.001):
    cash = initial_cash
    holdings = False  # Initially not holding any position
    earnings = 0

    for i in range(len(data) - 1):
        current_win = data['Close'].iloc[i] > data['Open'].iloc[i]
        next_win = data['Close'].iloc[i + 1] > data['Open'].iloc[i + 1]

        # Buy condition: Not holding and change from loss to win
        if not holdings and not current_win and next_win:
            buy_price = data['Close'].iloc[i]
            # Subtract commission from cash
            cash -= cash * commission
            holdings = True  # Now holding a position

        # Sell condition: Holding and change from win to loss
        elif holdings and current_win and not next_win:
            sell_price = data['Close'].iloc[i]
            percent_change = (sell_price - buy_price) / buy_price
            profit = percent_change * cash
            # Subtract commission from profit
            profit -= profit * commission
            cash += profit
            earnings += profit
            holdings = False  # Sold the position

    return earnings, cash