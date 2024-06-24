import numpy as np
import pandas as pd
from backtesting import Backtest
from numpy.random import default_rng

class StochasticBacktesting(Backtest):
    def run(self, n=1000, rel_change_percentage=0.005, **kwargs):
        start_data = self._data.copy(deep=False)
        for i in range(0, n):
            index_min = min(start_data.index)
            index_max = max(start_data.index)
            random_number = default_rng().random() * 0.9  # Only 90% of the data is used to have some space for the end time
            random_starting_time = index_min + (index_max - index_min) * random_number
            random_end_time = random_starting_time + (index_max - index_min) * 0.1
            data = start_data.copy(deep=False)
            data = data[(data.index <= random_end_time) & (data.index >= random_starting_time)]
            bt = Backtest(data, self._strategy, cash=10000, commission=0.008)
            current_stats = bt.run(**kwargs)
            current_stats_series = pd.Series(current_stats)
            exclude_keys = ["Duration", "End", "Start", "Max. Drawdown Duration", "Avg. Drawdown Duration", "Max. Trade Duration", "Avg. Trade Duration", "_strategy", "_equity_curve", "_trades"]
            current_stats_series = current_stats_series.drop(index=exclude_keys, errors='ignore')
            if i == 0:
                # For the first simulation, initialize accumulated_stats and averaged_stats
                accumulated_stats = current_stats_series
                averaged_stats = current_stats_series
            else:
                # Calculate the new accumulated stats
                new_accumulated_stats = accumulated_stats.add(current_stats_series, fill_value=0)
                # Calculate the new average
                new_averaged_stats = new_accumulated_stats / (i + 1)
                
                # Check if the change exceeds 0.5% for any statistic
                # Check if the change exceeds 0.5% for any statistic
                with np.errstate(divide='ignore', invalid='ignore'):
                    relative_change = np.where(averaged_stats != 0, 
                                               (new_averaged_stats - averaged_stats).abs() / np.where(averaged_stats == 0, 1, averaged_stats), 
                                               (new_averaged_stats - averaged_stats).abs())
                change_exceeds_threshold = relative_change > rel_change_percentage
                accumulated_stats = new_accumulated_stats
                averaged_stats = new_averaged_stats
                if not change_exceeds_threshold.any():
                    # print(f"Converged after {i} iterations")
                    break

        return averaged_stats
    
    def plot(self):
        pass