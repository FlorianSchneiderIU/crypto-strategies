from datetime import datetime
from backtesting import Backtest

from strategies.spot_martingale import MartingaleStrategy
from utils.common_utils import fetch_kucoin_data

def main():
    # Fetch historical data from KuCoin
    symbol = 'BTC/USDT'
    timeframe = '1d'
    start_date = datetime(2017, 10, 19)
    end_date = datetime(2019, 1, 1)
    data = fetch_kucoin_data(symbol=symbol, timeframe=timeframe, since=int(start_date.timestamp()) * 1000, until=int(end_date.timestamp()) * 1000)

    # Rename columns to match backtesting.py's expected names
    data.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)

    # Remove any potential missing values
    data.dropna(inplace=True)

    # Create an instance of the strategy
    strategy = MartingaleStrategy

    # Run backtest
    bt = Backtest(data, strategy, cash=10000, commission=.002)
    stats = bt.run()

    # Print backtest results
    print(stats)
    bt.plot()
    
    optimized_stats, heatmap, optimize_result = bt.optimize(
        initial_trade_size=[0.005,1],
        multiplier=[0.5,10],
        take_profit=[0.01,1],
        drop_threshold=[0.01, 0.02, 1],
        max_levels=[1,15],
        maximize='Equity Final [$]',  # Optimize for final equity value
        constraint=lambda param: param.initial_trade_size * ((param.multiplier ** param.max_levels - 1) / (param.multiplier - 1)) <= 1,
        return_heatmap=True,
        method='skopt',
        max_tries=1000,
        return_optimization=True
    )
    print(heatmap.sort_values().iloc[-3:])
    # Print optimized backtest results
    print(optimized_stats)

    # Plot the results
    bt.plot()

if __name__ == "__main__":
    main()
