import yfinance as yf
import pandas as pd
import streamlit as st

def fetch_stock_data(ticker, period="5y"):
    """Fetch and clean stock data from Yahoo Finance"""
    try:
        data = yf.download(ticker, period=period, progress=False)
        if data.empty:
            return None
        
        # Fix MultiIndex columns if they exist
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)
        
        return data
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def resample_data_to_timeframe(data, timeframe):
    """
    Resample daily data to different timeframes for trading analysis
    
    Args:
        data: DataFrame with OHLCV data
        timeframe: str ('1D', '1W', '1M', '3M')
    
    Returns:
        Resampled DataFrame with proper OHLCV aggregation
    """
    if timeframe == '1D':
        return data  # Already daily data
    
    # Define resampling rules for OHLCV data
    agg_dict = {
        'Open': 'first',    # First open of the period
        'High': 'max',      # Highest high of the period  
        'Low': 'min',       # Lowest low of the period
        'Close': 'last',    # Last close of the period
        'Volume': 'sum'     # Total volume of the period
    }
    
    # Map timeframes to pandas frequency codes
    freq_map = {
        '1W': 'W-FRI',      # Weekly, ending Friday
        '1M': 'M',          # Monthly, end of month
        '3M': '3M'          # Quarterly, end of quarter
    }
    
    if timeframe not in freq_map:
        st.warning(f"Unsupported timeframe: {timeframe}")
        return data
    
    try:
        # Resample the data
        resampled = data.resample(freq_map[timeframe]).agg(agg_dict)
        
        # Remove any rows with NaN values (incomplete periods)
        resampled = resampled.dropna()
        
        return resampled
    except Exception as e:
        st.error(f"Error resampling data: {str(e)}")
        return data

def fetch_stock_data_with_timeframe(ticker, timeframe='1D', period='2y'):
    """
    Fetch stock data and resample to specified timeframe
    
    Args:
        ticker: Stock symbol
        timeframe: Trading timeframe ('1D', '1W', '1M', '3M')  
        period: Data range ('1y', '2y', '5y')
    
    Returns:
        DataFrame resampled to the specified timeframe
    """
    # Fetch base daily data
    data = fetch_stock_data(ticker, period)
    
    if data is None:
        return None
    
    # Resample to desired timeframe
    return resample_data_to_timeframe(data, timeframe)

def validate_ticker(ticker):
    """Validate if ticker symbol is reasonable"""
    if not ticker or len(ticker) > 10:
        return False
    return ticker.replace('.', '').replace('-', '').isalnum()