from strategies.util_strategy import UtilStrategy

# Define a Martingale strategy with take profit and additional parameters
class MartingaleStrategy(UtilStrategy):
    initial_trade_size = 0.01  # initial trade size as a fraction of cash
    multiplier = 2  # Martingale multiplier
    take_profit = 0.05  # Take profit percentage (5%)
    drop_threshold = 0.02  # Price drop percentage required to buy the next charge (2%)
    max_levels = 5  # Maximum levels for buying

    def init(self):
        self.trade_size = self.initial_trade_size  # reset trade size at the start
        self.current_level = 0  # current level of the Martingale strategy
        self.entry_price = None  # entry price for the current level
        self.initial_cash = self.equity  # Store the initial cash value
        self.update_info = True

    def next(self):
        avg_buy_price = self.calculate_avg_buy_price()
        if self.update_info:
            self.initial_cash = self._broker._cash  # Recalculate the initial cash after selling
            self.update_info = False
        # Check for take profit condition
        if avg_buy_price > 0 and self.data.Close[-1] > avg_buy_price * (1 + self.take_profit):
            self.position.close()
            self.trade_size = self.initial_trade_size
            self.current_level = 0
            self.entry_price = None
            self.update_info = True
            

        # Check if we can buy more (only if not exceeded max levels)
        elif is_open_instant(self.current_level) or price_dropped(self.data.Close[-1], self.entry_price, self.drop_threshold) and self.current_level < self.max_levels:
            buy_size = self.initial_cash * self.trade_size
            current_value_of_holdings = self.position.size*self.data.Close[-1]
            remaining_cash = self.equity-current_value_of_holdings
            fraction_to_buy = buy_size / remaining_cash # map trade_size regarding initial equity to remaining equity
            self.buy(size=fraction_to_buy)
            self.entry_price = self.data.Close[-1]
            self.trade_size *= self.multiplier
            self.current_level += 1

def is_open_instant(level):
    return level == 0

def price_dropped(close, entry_price, drop_threshold):
    return close < entry_price * (1 - drop_threshold)
