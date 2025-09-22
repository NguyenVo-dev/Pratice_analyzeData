import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ticker=["TME","TCTZF","HACK","IHAK"]

data = yf.download(ticker, period="6mo", interval="1d")

print(data.head())
normalized_data = data['Close'] / data['Close'].iloc[0]

plt.figure(figsize=(12, 6))
plt.plot(normalized_data)

plt.title('Normalized Stock Performance (Base=100)')
plt.xlabel('Date')
plt.ylabel('Normalized Price')
plt.legend(normalized_data.columns) # Use the column names (tickers) as labels
plt.grid(True)
plt.show()
