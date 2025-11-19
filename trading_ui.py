"""
UI components for price alerts and paper trading features
"""
import streamlit as st
from datetime import datetime
import pandas as pd
from price_alerts import get_alert_manager
from paper_trading import get_trading_account
from realtime_prices import get_price_service

def display_price_alerts_section():
    """Display price alerts management UI"""
    st.markdown('<div class="theme-container">', unsafe_allow_html=True)
    
    with st.expander("🔔 Price Alerts", expanded=False):
        alert_manager = get_alert_manager()
        
        # Add new alert section
        st.subheader("Create New Alert")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            alert_ticker = st.text_input("Ticker", key="alert_ticker_input").upper()
        
        with col2:
            alert_type = st.selectbox("Alert When Price", ["Above", "Below"], key="alert_type")
        
        with col3:
            target_price = st.number_input("Target Price ($)", min_value=0.01, value=100.0, key="alert_price")
        
        if st.button("Create Alert", type="primary"):
            if alert_ticker:
                alert_type_lower = alert_type.lower()
                condition = f"{alert_ticker} reaches {alert_type_lower} ${target_price:.2f}"
                alert_manager.add_alert(alert_ticker, alert_type_lower, target_price, condition)
                st.success(f"✅ Alert created: {condition}")
                st.rerun()
            else:
                st.error("Please enter a ticker symbol")
        
        st.markdown("---")
        
        # Display active alerts
        active_alerts = alert_manager.get_active_alerts()
        
        if active_alerts:
            st.subheader("Active Alerts")
            
            for i, alert in enumerate(active_alerts):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{alert.ticker}** {alert.alert_type} ${alert.target_price:.2f}")
                    st.caption(f"Created: {alert.created_at.strftime('%Y-%m-%d %H:%M')}")
                
                with col2:
                    # Show current price
                    price_service = get_price_service()
                    price_data = price_service.get_live_price(alert.ticker)
                    if price_data:
                        st.metric("Current", f"${price_data['price']:.2f}")
                
                with col3:
                    if st.button("Delete", key=f"delete_alert_{i}"):
                        alert_manager.remove_alert(i)
                        st.rerun()
                
                st.markdown("---")
        else:
            st.info("No active alerts. Create one above!")
        
        # Check for triggered alerts
        if st.button("🔄 Check Alerts Now"):
            triggered = alert_manager.check_all_alerts()
            if triggered:
                for alert in triggered:
                    st.success(f"🔔 ALERT TRIGGERED: {alert.ticker} {alert.alert_type} ${alert.target_price:.2f}")
            else:
                st.info("No alerts triggered")
        
        # Display triggered alerts history
        triggered_alerts = alert_manager.get_triggered_alerts()
        if triggered_alerts:
            st.subheader("Triggered Alerts")
            for alert in triggered_alerts[-5:]:  # Show last 5
                st.write(f"✅ {alert.ticker} {alert.alert_type} ${alert.target_price:.2f} - Triggered at {alert.triggered_at.strftime('%Y-%m-%d %H:%M')}")
            
            if st.button("Clear Triggered Alerts"):
                alert_manager.clear_triggered_alerts()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_paper_trading_section(ticker=None):
    """Display paper trading UI"""
    st.markdown('<div class="theme-container">', unsafe_allow_html=True)
    
    with st.expander("💼 Paper Trading", expanded=False):
        account = get_trading_account()
        
        # Account summary
        st.subheader("Account Summary")
        
        portfolio_value = account.get_portfolio_value()
        total_pnl = account.get_total_pnl()
        total_pnl_percent = account.get_total_pnl_percent()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Portfolio Value", f"${portfolio_value:,.2f}")
        
        with col2:
            st.metric("Cash Balance", f"${account.cash_balance:,.2f}")
        
        with col3:
            pnl_delta = f"${abs(total_pnl):,.2f}"
            st.metric("Total P&L", pnl_delta, delta=f"{total_pnl_percent:.2f}%")
        
        with col4:
            st.metric("Initial Balance", f"${account.initial_balance:,.2f}")
        
        st.markdown("---")
        
        # Trade execution
        st.subheader("Execute Trade")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Pre-fill with current ticker if available
            trade_ticker = st.text_input("Ticker", value=ticker if ticker else "", key="trade_ticker").upper()
        
        with col2:
            trade_type = st.selectbox("Action", ["BUY", "SELL"], key="trade_type")
        
        with col3:
            quantity = st.number_input("Quantity", min_value=1, value=1, key="trade_quantity")
        
        with col4:
            st.write("")  # Spacing
            st.write("")  # Spacing
            execute_btn = st.button("Execute Trade", type="primary", use_container_width=True)
        
        if execute_btn:
            if trade_ticker:
                success, message = account.execute_trade(trade_ticker, trade_type, quantity)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter a ticker symbol")
        
        st.markdown("---")
        
        # Current positions
        st.subheader("Current Positions")
        positions_df = account.get_positions_df()
        
        if not positions_df.empty:
            # Format the dataframe
            positions_df['Avg Price'] = positions_df['Avg Price'].apply(lambda x: f"${x:.2f}")
            positions_df['Current Price'] = positions_df['Current Price'].apply(lambda x: f"${x:.2f}")
            positions_df['Total Cost'] = positions_df['Total Cost'].apply(lambda x: f"${x:,.2f}")
            positions_df['Current Value'] = positions_df['Current Value'].apply(lambda x: f"${x:,.2f}")
            positions_df['P&L'] = positions_df['P&L'].apply(lambda x: f"${x:,.2f}")
            positions_df['P&L %'] = positions_df['P&L %'].apply(lambda x: f"{x:.2f}%")
            
            st.dataframe(positions_df, use_container_width=True, hide_index=True)
        else:
            st.info("No open positions")
        
        st.markdown("---")
        
        # Trade history
        st.subheader("Trade History")
        trades_df = account.get_trade_history_df()
        
        if not trades_df.empty:
            # Show last 10 trades
            display_df = trades_df.head(10).copy()
            display_df['price'] = display_df['price'].apply(lambda x: f"${x:.2f}")
            display_df['total_value'] = display_df['total_value'].apply(lambda x: f"${x:,.2f}")
            display_df['timestamp'] = pd.to_datetime(display_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export trades
            if st.button("Download Trade History CSV"):
                csv = trades_df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name=f"trade_history_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No trades yet")
        
        st.markdown("---")
        
        # Account management
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset Account", help="Reset to initial balance and clear all trades"):
                account.reset_account()
                st.success("Account reset successfully!")
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
