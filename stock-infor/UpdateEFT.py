import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_enhanced_etf_data(ticker):
    """Get enhanced ETF data using yfinance + manual enrichment"""
    
    print(f"\n{'='*70}")
    print(f"ENHANCED ETF DATA FOR {ticker}")
    print(f"{'='*70}")
    
    try:
        etf = yf.Ticker(ticker)
        
        # What we can get from yfinance
        print("FROM YFINANCE:")
        print("-" * 40)
        
        # Basic info that's usually available
        info = etf.info
        basic_info = {
            'Name': info.get('longName', 'N/A'),
            'Symbol': info.get('symbol', 'N/A'),
            'Current Price': f"${info.get('currentPrice', 'N/A')}",
            'Previous Close': f"${info.get('previousClose', 'N/A')}",
            'Volume': f"{info.get('volume', 'N/A'):,}",
            'Market Cap': f"${info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else 'N/A',
            '52W High': f"${info.get('fiftyTwoWeekHigh', 'N/A')}",
            '52W Low': f"${info.get('fiftyTwoWeekLow', 'N/A')}"
        }
        
        for key, value in basic_info.items():
            print(f"{key}: {value}")
        
        # ETF-specific data (often missing in yfinance)
        etf_specific = {
            'Total Assets': info.get('totalAssets'),
            'Expense Ratio': info.get('annualReportExpenseRatio'),
            'YTD Return': info.get('ytdReturn'),
            'Fund Family': info.get('fundFamily'),
            'Category': info.get('category')
        }
        
        print(f"\nETF-SPECIFIC DATA (often limited in yfinance):")
        for key, value in etf_specific.items():
            if value:
                if key == 'Total Assets':
                    print(f"{key}: ${value:,.0f}")
                elif key == 'Expense Ratio':
                    print(f"{key}: {value:.2%}")
                elif key == 'YTD Return':
                    print(f"{key}: {value:.2%}")
                else:
                    print(f"{key}: {value}")
            else:
                print(f"{key}: NOT AVAILABLE in yfinance")
        
        # Manual enrichment for HACK and IHAK
        manual_data = get_manual_etf_enrichment(ticker)
        print(f"\nMANUAL ENRICHMENT:")
        for key, value in manual_data.items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Error: {e}")

def get_manual_etf_enrichment(ticker):
    """Provide manual enrichment for ETF-specific data"""
    
    enrichment_data = {
        'HACK': {
            'ETF Provider': 'ETFMG',
            'Expense Ratio': '0.60%',
            'AUM': '~$1.5B',
            'Index Tracked': 'Prime Cyber Defense Index',
            'Strategy': 'Pure-play cybersecurity companies',
            'Inception': '2014-11-11',
            'Holdings': '~60 companies',
            'Top Holdings': 'CRWD, PANW, ZS, OKTA, CHKP'
        },
        'IHAK': {
            'ETF Provider': 'iShares',
            'Expense Ratio': '0.47%',
            'AUM': '~$400M',
            'Index Tracked': 'NYSE FactSet Global Cybersecurity Index',
            'Strategy': 'Global cybersecurity technology companies',
            'Inception': '2019-06-13',
            'Holdings': '~40 companies',
            'Top Holdings': 'CRWD, PANW, ZS, OKTA, FTNT'
        }
    }
    
    return enrichment_data.get(ticker, {})

for etf in ['HACK', 'IHAK']:
    get_enhanced_etf_data(etf)
