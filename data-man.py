import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

data = yf.download('AAPL', start='2023-01-01', end='2023-12-31')

# data.columns = data.columns.get_level_values(1)

print(data.head())
print(data.describe())

data['Close'].plot()
plt.title('AAPL Closing Prices')
plt.show()

