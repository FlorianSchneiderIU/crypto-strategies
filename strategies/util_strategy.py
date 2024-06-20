from backtesting import Strategy

class UtilStrategy(Strategy):
    def __init__(self, broker, data, params):
        super().__init__(broker, data, params)
        
    def calculate_avg_buy_price(self):
        total_cost = sum(trade.size * trade.entry_price for trade in self.trades)
        total_size = sum(trade.size for trade in self.trades)
        return total_cost / total_size if total_size > 0 else 0

    def next(self):
        # Implement your strategy logic here
        pass
    
    def print_statistics(self):
        print(f"Timeframe: {self.data.index[-1]}")
        print(f"Equity: {self.equity}")
        