"""
Real-time price service for fetching live stock prices
"""
import yfinance as yf
import time
from datetime import datetime
import streamlit as st

class RealtimePriceService:
    """Service for fetching real-time stock prices"""
    
    def __init__(self):
        self.cache = {}
        self.last_update = {}
    
    def get_live_price(self, ticker, force_refresh=False):
        """Get live price for a ticker with caching"""
        current_time = time.time()
        
        # Check if we have recent cached data (within 5 seconds)
        if not force_refresh and ticker in self.cache:
            if current_time - self.last_update.get(ticker, 0) < 5:
                return self.cache[ticker]
        
        try:
            stock = yf.Ticker(ticker)
            # Get the most recent price
            hist = stock.history(period="1d", interval="1m")
            
            if not hist.empty:
                price_data = {
                    'price': hist['Close'].iloc[-1],
                    'change': hist['Close'].iloc[-1] - hist['Open'].iloc[0],
                    'change_percent': ((hist['Close'].iloc[-1] - hist['Open'].iloc[0]) / hist['Open'].iloc[0]) * 100,
                    'volume': hist['Volume'].iloc[-1],
                    'timestamp': datetime.now()
                }
                
                # Update cache
                self.cache[ticker] = price_data
                self.last_update[ticker] = current_time
                
                return price_data
            
            return None
            
        except Exception as e:
            st.warning(f"Error fetching live price for {ticker}: {str(e)}")
            return None
    
    def get_multiple_prices(self, tickers, force_refresh=False):
        """Get live prices for multiple tickers"""
        prices = {}
        for ticker in tickers:
            price_data = self.get_live_price(ticker, force_refresh)
            if price_data:
                prices[ticker] = price_data
        return prices

# Global instance
_price_service = None

def get_price_service():
    """Get or create the global price service instance"""
    global _price_service
    if _price_service is None:
        _price_service = RealtimePriceService()
    return _price_service
