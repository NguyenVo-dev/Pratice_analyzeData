import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
from datetime import datetime, timedelta

# Suppress warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='pandas.io.formats.format')

ticker = ["TME", "TCTZF", "HACK", "IHAK"]

# Get current date for reference
current_date = datetime.now().strftime('%Y-%m-%d')
print(f"Current date: {current_date}")

# Download price data with proper date range
print("Downloading market data...")
try:
    # Use 6 months historical data (ending at current date)
    data = yf.download(ticker, period="6mo", auto_adjust=True)
    print("Download completed!\n")
except Exception as e:
    print(f"Download error: {e}")
    # Fallback: try with specific start date
    start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
    data = yf.download(ticker, start=start_date, auto_adjust=True)

# Data overview with proper date checking
print("="*60)
print("DATA OVERVIEW")
print("="*60)
print(f"Data shape: {data.shape}")
print(f"Date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")
print(f"Trading days: {len(data)}")
print()

# Check for future dates and filter if necessary
if data.index[-1] > datetime.now():
    print("⚠️  Warning: Data contains future dates. Filtering to current date...")
    data = data[data.index <= datetime.now()]
    print(f"Filtered date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}")

# Handle missing values
data = data.ffill().bfill()  # Forward and backward fill

# Check if we have valid data
if data.empty:
    print("❌ No valid data available after filtering.")
else:
    # Normalized price chart
    plt.figure(figsize=(14, 8))
    
    if 'Close' in data.columns:
        normalized_data = data['Close'] / data['Close'].iloc[0]
        
        plt.subplot(2, 1, 1)
        for column in normalized_data.columns:
            plt.plot(normalized_data.index, normalized_data[column], label=column, linewidth=2)
        
        plt.title('Normalized Price Performance (Base=100)', fontsize=14, fontweight='bold')
        plt.ylabel('Normalized Price')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Volume chart
        plt.subplot(2, 1, 2)
        if 'Volume' in data.columns:
            # Plot average volume (log scale for better visualization)
            volume_data = data['Volume'].replace(0, np.nan)  # Replace 0 with NaN
            for column in volume_data.columns:
                plt.plot(volume_data.index, volume_data[column], label=column, alpha=0.7)
            
            plt.title('Trading Volume', fontsize=14, fontweight='bold')
            plt.ylabel('Volume')
            plt.xlabel('Date')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.yscale('log')  # Log scale for volume
        
        plt.tight_layout()
        plt.show()

    # Calculate and display performance statistics
    print("\n" + "="*60)
    print("PERFORMANCE STATISTICS")
    print("="*60)
    
    if 'Close' in data.columns:
        close_prices = data['Close']
        
        performance_stats = []
        for ticker_symbol in ticker:
            if ticker_symbol in close_prices.columns:
                prices = close_prices[ticker_symbol].dropna()
                if len(prices) > 1:
                    total_return = ((prices.iloc[-1] / prices.iloc[0]) - 1) * 100
                    volatility = prices.pct_change().std() * np.sqrt(252) * 100  # Annualized
                    
                    performance_stats.append({
                        'Ticker': ticker_symbol,
                        'Start Price': f"${prices.iloc[0]:.2f}",
                        'End Price': f"${prices.iloc[-1]:.2f}",
                        'Total Return %': f"{total_return:.2f}%",
                        'Volatility %': f"{volatility:.1f}%",
                        'Days': len(prices)
                    })
        
        if performance_stats:
            stats_df = pd.DataFrame(performance_stats)
            print(stats_df.to_string(index=False))
        else:
            print("No performance data available.")

    # Enhanced Financial Analysis with better error handling
    print("\n" + "="*60)
    print("FINANCIAL ANALYSIS")
    print("="*60)

    def safe_format(value, format_type='currency'):
        """Safely format values handling NaN/None"""
        if value is None or pd.isna(value):
            return "N/A"
        try:
            if format_type == 'currency':
                return f"${value:,.0f}" if abs(value) < 1e12 else f"${value/1e9:,.1f}B"
            elif format_type == 'percent':
                return f"{value:.1f}%"
            elif format_type == 'decimal':
                return f"{value:.2f}"
            else:
                return str(value)
        except (ValueError, TypeError):
            return "N/A"

    for ticker_symbol in ticker:
        try:
            print(f"\n{'═'*50}")
            print(f"📊 ANALYZING: {ticker_symbol}")
            print(f"{'═'*50}")
            
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            
            # Basic info available for all securities
            print(f"Name: {info.get('longName', 'N/A')}")
            print(f"Type: {info.get('quoteType', 'N/A')}")
            print(f"Sector: {info.get('sector', 'N/A')}")
            print(f"Industry: {info.get('industry', 'N/A')}")
            print(f"Market Cap: {safe_format(info.get('marketCap'))}")
            print(f"Current Price: {safe_format(info.get('currentPrice'), 'decimal')}")
            
            # Determine security type and analyze accordingly
            quote_type = info.get('quoteType', '').upper()
            
            if quote_type == 'ETF':
                print(f"\n🔹 ETF Characteristics:")
                print(f"Expense Ratio: {safe_format(info.get('expenseRatio'), 'percent')}")
                print(f"Total Assets: {safe_format(info.get('totalAssets'))}")
                print(f"Dividend Yield: {safe_format(info.get('yield'), 'percent')}")
                print(f"52W Range: {safe_format(info.get('fiftyTwoWeekLow'), 'decimal')} - {safe_format(info.get('fiftyTwoWeekHigh'), 'decimal')}")
                
            else:  # Assume it's a stock
                print(f"\n🔹 Financial Statements:")
                
                # Get financial data with error handling
                financials = stock.financials
                balance_sheet = stock.balance_sheet
                cashflow = stock.cashflow
                
                # Income Statement
                if not financials.empty:
                    try:
                        revenue = financials.iloc[:, 0]['Total Revenue'] if 'Total Revenue' in financials.index else financials.iloc[:, 0].get('Revenue')
                        net_income = financials.iloc[:, 0].get('Net Income')
                        
                        if revenue and net_income:
                            print(f"Revenue: {safe_format(revenue)}")
                            print(f"Net Income: {safe_format(net_income)}")
                            net_margin = (net_income / revenue) * 100 if revenue != 0 else 0
                            print(f"Net Margin: {safe_format(net_margin, 'percent')}")
                    except:
                        print("Income statement data not available")
                
                # Key ratios
                print(f"\n🔹 Valuation Ratios:")
                print(f"P/E Ratio: {safe_format(info.get('trailingPE'), 'decimal')}")
                print(f"Forward P/E: {safe_format(info.get('forwardPE'), 'decimal')}")
                print(f"P/B Ratio: {safe_format(info.get('priceToBook'), 'decimal')}")
                
            # Performance metrics
            print(f"\n🔹 Performance Metrics:")
            week_change = info.get('52WeekChange')
            if week_change:
                print(f"52-Week Change: {safe_format(week_change * 100, 'percent')}")
            
            # Beta for risk measurement
            beta = info.get('beta')
            if beta:
                print(f"Beta (Volatility): {safe_format(beta, 'decimal')}")
            
        except Exception as e:
            print(f"❌ Error analyzing {ticker_symbol}: {str(e)[:100]}...")

    # Summary table
    print("\n" + "="*70)
    print("SUMMARY COMPARISON TABLE")
    print("="*70)

    summary_data = []
    for ticker_symbol in ticker:
        try:
            stock = yf.Ticker(ticker_symbol)
            info = stock.info
            
            # Get price performance from our downloaded data
            if 'Close' in data.columns and ticker_symbol in data['Close'].columns:
                prices = data['Close'][ticker_symbol].dropna()
                if len(prices) > 1:
                    performance = ((prices.iloc[-1] / prices.iloc[0]) - 1) * 100
                else:
                    performance = None
            else:
                performance = None
            
            summary_data.append({
                'Ticker': ticker_symbol,
                'Name': info.get('shortName', 'N/A')[:20],
                'Type': info.get('quoteType', 'N/A'),
                'Sector': info.get('sector', 'N/A'),
                'Price': info.get('currentPrice', None),
                'Market Cap': info.get('marketCap', None),
                'P/E Ratio': info.get('trailingPE', None),
                '6Mo Return %': performance,
                'Beta': info.get('beta', None)
            })
            
        except Exception as e:
            print(f"Error processing {ticker_symbol}: {e}")

    if summary_data:
        summary_df = pd.DataFrame(summary_data)
        
        # Format the summary table
        display_columns = ['Ticker', 'Name', 'Type', 'Sector', 'Price', 'Market Cap', 'P/E Ratio', '6Mo Return %', 'Beta']
        display_df = summary_df[display_columns].copy()
        
        # Format numeric columns
        for col in ['Price', 'Market Cap']:
            display_df[col] = display_df[col].apply(lambda x: safe_format(x) if pd.notna(x) else 'N/A')
        
        for col in ['P/E Ratio', 'Beta']:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')
        
        display_df['6Mo Return %'] = display_df['6Mo Return %'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else 'N/A')
        
        print(display_df.to_string(index=False, max_colwidth=15))
        print(f"\nLast updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
