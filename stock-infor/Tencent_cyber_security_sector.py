import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore', category=RuntimeWarning, module='pandas.io.formats.format')

ticker=["TME","TCTZF","HACK","IHAK"]

data = yf.download(ticker, period="6mo", interval="1d")

print(data.head())

# Check for missing data
print("Data overview:")
print(f"Shape: {data.shape}")
print(f"Columns: {data.columns.tolist()}")
print(f"Date range: {data.index[0]} to {data.index[-1]}")
print()

# Handle missing values in price data
data = data.ffill()  # Forward fill missing values
normalized_data = data['Close'] / data['Close'].iloc[0]

plt.figure(figsize=(12, 6))
plt.plot(normalized_data)

plt.title('Normalized Stock Performance (Base=100)')
plt.xlabel('Date')
plt.ylabel('Normalized Price')
plt.legend(normalized_data.columns) # Use the column names (tickers) as labels
plt.grid(True)
plt.show()

# Financial Reports Analysis
print("\n" + "="*50)
print("FINANCIAL REPORTS ANALYSIS")
print("="*50)

for ticker_symbol in ticker:
    try:
        print(f"\n{'='*30}")
        print(f"ANALYZING: {ticker_symbol}")
        print(f"{'='*30}")
        
        # Create ticker object
        stock = yf.Ticker(ticker_symbol)
        
        # Get financial statements
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow
        
        # Display key financial metrics
        print(f"\nKey Financial Metrics for {ticker_symbol}:")
        
        # Income Statement metrics
        if not financials.empty:
            try:
                revenue = financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in financials.index else financials.loc['Revenue'].iloc[0]
                net_income = financials.loc['Net Income'].iloc[0]
                gross_profit = financials.loc['Gross Profit'].iloc[0]
                print(f"Revenue: ${revenue:,.0f}")
                print(f"Net Income: ${net_income:,.0f}")
                print(f"Gross Profit: ${gross_profit:,.0f}")
                
                # Calculate margins
                gross_margin = (gross_profit / revenue) * 100
                net_margin = (net_income / revenue) * 100
                print(f"Gross Margin: {gross_margin:.1f}%")
                print(f"Net Margin: {net_margin:.1f}%")
            except KeyError as e:
                print(f"Missing financial data point: {e}")
        
        # Balance Sheet metrics
        if not balance_sheet.empty:
            try:
                total_assets = balance_sheet.loc['Total Assets'].iloc[0]
                total_liabilities = balance_sheet.loc['Total Liabilities Net Minority Interest'].iloc[0]
                shareholders_equity = balance_sheet.loc['Total Equity Gross Minority Interest'].iloc[0]
                
                print(f"Total Assets: ${total_assets:,.0f}")
                print(f"Total Liabilities: ${total_liabilities:,.0f}")
                print(f"Shareholders Equity: ${shareholders_equity:,.0f}")
                
                # Calculate ratios
                debt_to_equity = (total_liabilities / shareholders_equity) if shareholders_equity != 0 else float('inf')
                print(f"Debt-to-Equity Ratio: {debt_to_equity:.2f}")
            except KeyError as e:
                print(f"Missing balance sheet data: {e}")
        
        # Cash Flow metrics
        if not cashflow.empty:
            try:
                operating_cashflow = cashflow.loc['Operating Cash Flow'].iloc[0]
                free_cashflow = cashflow.loc['Free Cash Flow'].iloc[0]
                print(f"Operating Cash Flow: ${operating_cashflow:,.0f}")
                print(f"Free Cash Flow: ${free_cashflow:,.0f}")
            except KeyError as e:
                print(f"Missing cash flow data: {e}")
        
        # Additional info
        info = stock.info
        print(f"\nAdditional Info:")
        print(f"Sector: {info.get('sector', 'N/A')}")
        print(f"Industry: {info.get('industry', 'N/A')}")
        print(f"Market Cap: ${info.get('marketCap', 'N/A'):,}")
        print(f"P/E Ratio: {info.get('trailingPE', 'N/A')}")
        print(f"Forward P/E: {info.get('forwardPE', 'N/A')}")
        
    except Exception as e:
        print(f"Error analyzing {ticker_symbol}: {e}")

# Create a summary financial comparison
print("\n" + "="*50)
print("FINANCIAL SUMMARY COMPARISON")
print("="*50)

summary_data = []

for ticker_symbol in ticker:
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        financials = stock.financials
        
        if not financials.empty:
            revenue = financials.loc['Total Revenue'].iloc[0] if 'Total Revenue' in financials.index else financials.loc['Revenue'].iloc[0]
            net_income = financials.loc['Net Income'].iloc[0]
        else:
            revenue = net_income = None
            
        summary_data.append({
            'Ticker': ticker_symbol,
            'Market Cap': info.get('marketCap', None),
            'Revenue': revenue,
            'Net Income': net_income,
            'P/E Ratio': info.get('trailingPE', None),
            'Sector': info.get('sector', 'N/A')
        })
    except Exception as e:
        print(f"Error getting summary for {ticker_symbol}: {e}")

# Create summary DataFrame
if summary_data:
    summary_df = pd.DataFrame(summary_data)
    print("\nFinancial Comparison Summary:")
    print(summary_df.to_string(index=False))

