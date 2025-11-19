"""
Price alert system for monitoring stock price targets
"""
import streamlit as st
from datetime import datetime
import pandas as pd
from realtime_prices import get_price_service

class PriceAlert:
    """Represents a single price alert"""
    
    def __init__(self, ticker, alert_type, target_price, condition, created_at=None):
        self.ticker = ticker.upper()
        self.alert_type = alert_type  # 'above' or 'below'
        self.target_price = float(target_price)
        self.condition = condition  # Description
        self.created_at = created_at or datetime.now()
        self.triggered = False
        self.triggered_at = None
    
    def check_trigger(self, current_price):
        """Check if alert should be triggered"""
        if self.triggered:
            return False
        
        if self.alert_type == 'above' and current_price >= self.target_price:
            self.triggered = True
            self.triggered_at = datetime.now()
            return True
        elif self.alert_type == 'below' and current_price <= self.target_price:
            self.triggered = True
            self.triggered_at = datetime.now()
            return True
        
        return False
    
    def to_dict(self):
        """Convert alert to dictionary for storage"""
        return {
            'ticker': self.ticker,
            'alert_type': self.alert_type,
            'target_price': self.target_price,
            'condition': self.condition,
            'created_at': self.created_at,
            'triggered': self.triggered,
            'triggered_at': self.triggered_at
        }

class AlertManager:
    """Manages all price alerts"""
    
    def __init__(self):
        self.alerts = []
    
    def add_alert(self, ticker, alert_type, target_price, condition):
        """Add a new price alert"""
        alert = PriceAlert(ticker, alert_type, target_price, condition)
        self.alerts.append(alert)
        return alert
    
    def remove_alert(self, index):
        """Remove an alert by index"""
        if 0 <= index < len(self.alerts):
            del self.alerts[index]
    
    def check_all_alerts(self):
        """Check all active alerts and return triggered ones"""
        price_service = get_price_service()
        triggered_alerts = []
        
        # Get unique tickers
        tickers = list(set(alert.ticker for alert in self.alerts if not alert.triggered))
        
        if not tickers:
            return triggered_alerts
        
        # Fetch current prices
        prices = price_service.get_multiple_prices(tickers)
        
        # Check each alert
        for alert in self.alerts:
            if not alert.triggered and alert.ticker in prices:
                current_price = prices[alert.ticker]['price']
                if alert.check_trigger(current_price):
                    triggered_alerts.append(alert)
        
        return triggered_alerts
    
    def get_active_alerts(self):
        """Get all active (non-triggered) alerts"""
        return [alert for alert in self.alerts if not alert.triggered]
    
    def get_triggered_alerts(self):
        """Get all triggered alerts"""
        return [alert for alert in self.alerts if alert.triggered]
    
    def clear_triggered_alerts(self):
        """Remove all triggered alerts"""
        self.alerts = [alert for alert in self.alerts if not alert.triggered]

def get_alert_manager():
    """Get or create alert manager from session state"""
    if 'alert_manager' not in st.session_state:
        st.session_state['alert_manager'] = AlertManager()
    return st.session_state['alert_manager']
