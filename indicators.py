import pandas as pd

def calculate_rsi(prices, period=14):
    """Calculate RSI step by step"""
    delta = prices.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1/period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_moving_average(prices, window=20):
    """Calculate simple moving average"""
    return prices.rolling(window=window).mean()

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    sma = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return sma, upper_band, lower_band

def add_all_indicators(data, params=None):
    """Add all technical indicators to dataframe with custom parameters"""
    data = data.copy()
    
    # Default parameters
    if params is None:
        params = {
            'ma_short_period': 20,
            'ma_long_period': 50,
            'rsi_period': 14,
            'bb_period': 20,
            'bb_std': 2.0
        }
    
    # Add moving averages
    data[f'MA{params["ma_short_period"]}'] = calculate_moving_average(data['Close'], params['ma_short_period'])
    data[f'MA{params["ma_long_period"]}'] = calculate_moving_average(data['Close'], params['ma_long_period'])
    
    # Add RSI
    data[f'RSI{params["rsi_period"]}'] = calculate_rsi(data['Close'], params['rsi_period'])
    
    # Add Bollinger Bands
    bb_mid, bb_upper, bb_lower = calculate_bollinger_bands(
        data['Close'], 
        params['bb_period'], 
        params['bb_std']
    )
    data['BB_Mid'] = bb_mid
    data['BB_Upper'] = bb_upper
    data['BB_Lower'] = bb_lower
    
    # Keep backward compatibility
    data['MA20'] = data[f'MA{params["ma_short_period"]}']  # For existing charts
    data['RSI14'] = data[f'RSI{params["rsi_period"]}']      # For existing charts
    
    return data