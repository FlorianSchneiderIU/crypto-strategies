import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# Data points
x_buy = np.array([1, 2, 4, 8, 12])
y_buy = np.array([10, 8, 6, 4, 2])
x_sell = 17
y_sell = 5

# Spline curve
x_all = np.append(x_buy, x_sell)
y_all = np.append(y_buy, y_sell)
x_new = np.linspace(x_all.min(), x_all.max(), 300)
spl = make_interp_spline(x_all, y_all, k=3)
y_smooth = spl(x_new)

# Plotting the chart
plt.figure(figsize=(10, 6))
plt.plot(x_new, y_smooth, color='orange', linewidth=2)

# Plotting buy points
for i in range(len(x_buy)):
    plt.scatter(x_buy[i], y_buy[i], color='green')
    plt.text(x_buy[i], y_buy[i], f'BUY {2**i}', fontsize=12, ha='right', va='bottom', backgroundcolor='white')

# Plotting sell point
plt.scatter(x_sell, y_sell, color='red')
plt.text(x_sell, y_sell, f'SELL {31}', fontsize=12, ha='left', va='bottom', backgroundcolor='white')

# Adding dotted lines
for i in range(len(x_buy)):
    plt.plot([x_buy[i], x_sell], [y_buy[i], y_sell], 'b--', linewidth=0.7)

# Customize plot
plt.xticks([])
plt.yticks([])
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Spot Martingale Trading')

plt.show()
