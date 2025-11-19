"""
Paper trading system for simulating stock trades with virtual portfolio
"""
import streamlit as st
from datetime import datetime
import pandas as pd
from realtime_prices import get_price_service

class Trade:
    """Represents a single trade"""
    
    def __init__(self, ticker, trade_type, quantity, price, timestamp=None):
        self.ticker = ticker.upper()
        self.trade_type = trade_type  # 'BUY' or 'SELL'
        self.quantity = int(quantity)
        self.price = float(price)
        self.timestamp = timestamp or datetime.now()
        self.total_value = self.quantity * self.price
    
    def to_dict(self):
        """Convert trade to dictionary"""
        return {
            'ticker': self.ticker,
            'type': self.trade_type,
            'quantity': self.quantity,
            'price': self.price,
            'total_value': self.total_value,
            'timestamp': self.timestamp
        }

class Position:
    """Represents a portfolio position"""
    
    def __init__(self, ticker):
        self.ticker = ticker.upper()
        self.quantity = 0
        self.avg_price = 0.0
        self.total_cost = 0.0
    
    def add_shares(self, quantity, price):
        """Add shares to position (BUY)"""
        new_total_cost = self.total_cost + (quantity * price)
        new_quantity = self.quantity + quantity
        
        if new_quantity > 0:
            self.avg_price = new_total_cost / new_quantity
        
        self.quantity = new_quantity
        self.total_cost = new_total_cost
    
    def remove_shares(self, quantity):
        """Remove shares from position (SELL)"""
        self.quantity -= quantity
        if self.quantity <= 0:
            self.quantity = 0
            self.avg_price = 0.0
            self.total_cost = 0.0
        else:
            self.total_cost = self.quantity * self.avg_price
    
    def get_current_value(self, current_price):
        """Calculate current value of position"""
        return self.quantity * current_price
    
    def get_pnl(self, current_price):
        """Calculate profit/loss"""
        current_value = self.get_current_value(current_price)
        return current_value - self.total_cost
    
    def get_pnl_percent(self, current_price):
        """Calculate profit/loss percentage"""
        if self.total_cost == 0:
            return 0.0
        return (self.get_pnl(current_price) / self.total_cost) * 100

class PaperTradingAccount:
    """Manages paper trading account"""
    
    def __init__(self, initial_balance=100000):
        self.initial_balance = float(initial_balance)
        self.cash_balance = float(initial_balance)
        self.positions = {}  # ticker -> Position
        self.trade_history = []
        self.created_at = datetime.now()
    
    def execute_trade(self, ticker, trade_type, quantity, price=None):
        """Execute a trade (BUY or SELL)"""
        ticker = ticker.upper()
        
        # Get current price if not provided
        if price is None:
            price_service = get_price_service()
            price_data = price_service.get_live_price(ticker)
            if not price_data:
                return False, "Could not fetch current price"
            price = price_data['price']
        
        # Validate trade
        if trade_type == 'BUY':
            total_cost = quantity * price
            if total_cost > self.cash_balance:
                return False, f"Insufficient funds. Need ${total_cost:.2f}, have ${self.cash_balance:.2f}"
            
            # Execute buy
            self.cash_balance -= total_cost
            
            if ticker not in self.positions:
                self.positions[ticker] = Position(ticker)
            
            self.positions[ticker].add_shares(quantity, price)
            
        elif trade_type == 'SELL':
            if ticker not in self.positions or self.positions[ticker].quantity < quantity:
                available = self.positions.get(ticker, Position(ticker)).quantity
                return False, f"Insufficient shares. Have {available}, trying to sell {quantity}"
            
            # Execute sell
            total_value = quantity * price
            self.cash_balance += total_value
            self.positions[ticker].remove_shares(quantity)
            
            # Remove position if empty
            if self.positions[ticker].quantity == 0:
                del self.positions[ticker]
        
        else:
            return False, "Invalid trade type"
        
        # Record trade
        trade = Trade(ticker, trade_type, quantity, price)
        self.trade_history.append(trade)
        
        return True, f"Successfully executed {trade_type} of {quantity} shares at ${price:.2f}"
    
    def get_portfolio_value(self):
        """Calculate total portfolio value"""
        price_service = get_price_service()
        
        # Get current prices for all positions
        tickers = list(self.positions.keys())
        if not tickers:
            return self.cash_balance
        
        prices = price_service.get_multiple_prices(tickers)
        
        positions_value = 0
        for ticker, position in self.positions.items():
            if ticker in prices:
                positions_value += position.get_current_value(prices[ticker]['price'])
        
        return self.cash_balance + positions_value
    
    def get_total_pnl(self):
        """Calculate total profit/loss"""
        current_value = self.get_portfolio_value()
        return current_value - self.initial_balance
    
    def get_total_pnl_percent(self):
        """Calculate total profit/loss percentage"""
        if self.initial_balance == 0:
            return 0.0
        return (self.get_total_pnl() / self.initial_balance) * 100
    
    def get_positions_df(self):
        """Get positions as DataFrame"""
        if not self.positions:
            return pd.DataFrame()
        
        price_service = get_price_service()
        tickers = list(self.positions.keys())
        prices = price_service.get_multiple_prices(tickers)
        
        positions_data = []
        for ticker, position in self.positions.items():
            if ticker in prices:
                current_price = prices[ticker]['price']
                positions_data.append({
                    'Ticker': ticker,
                    'Quantity': position.quantity,
                    'Avg Price': position.avg_price,
                    'Current Price': current_price,
                    'Total Cost': position.total_cost,
                    'Current Value': position.get_current_value(current_price),
                    'P&L': position.get_pnl(current_price),
                    'P&L %': position.get_pnl_percent(current_price)
                })
        
        return pd.DataFrame(positions_data)
    
    def get_trade_history_df(self):
        """Get trade history as DataFrame"""
        if not self.trade_history:
            return pd.DataFrame()
        
        trades_data = [trade.to_dict() for trade in self.trade_history]
        df = pd.DataFrame(trades_data)
        df = df.sort_values('timestamp', ascending=False)
        return df
    
    def reset_account(self):
        """Reset account to initial state"""
        self.cash_balance = self.initial_balance
        self.positions = {}
        self.trade_history = []
        self.created_at = datetime.now()

def get_trading_account():
    """Get or create trading account from session state"""
    if 'trading_account' not in st.session_state:
        st.session_state['trading_account'] = PaperTradingAccount()
    return st.session_state['trading_account']
