import streamlit as st
import feedparser
import requests
import time
from datetime import datetime

# Import our custom modules
from data_fetcher import fetch_stock_data_with_timeframe, validate_ticker, validate_ticker_exists, get_watchlist_prices
from indicators import add_all_indicators
from chart_builder import create_line_chart_with_indicators, create_candlestick_chart_with_indicators
from utils import display_technical_summary, display_data_info
from css import apply_theme_css

# Import new trading features
from trading_ui import display_price_alerts_section, display_paper_trading_section
from price_alerts import get_alert_manager
from realtime_prices import get_price_service


# Configure page
st.set_page_config(
    page_title="Modular Finance Dashboard",
    layout="wide"
)

def get_theme_colors(theme="light"):
    """Get color scheme for charts based on theme"""
    if theme == "dark":
        return {
            'background': '#0E1117',
            'paper': '#262730',
            'text': '#FAFAFA',
            'grid': '#404040',
            'primary': '#FF6B35',
            'secondary': "#000000",
            'success': '#28a745',
            'danger': '#dc3545'
        }
    else:
        return {
            'background': '#FFFFFF',
            'paper': '#FFFFFF', 
            'text': '#262730',
            'grid': '#E0E0E0',
            'primary': '#FF6B35',
            'secondary': '#00D4AA',
            'success': '#28a745',
            'danger': '#dc3545'
        }




        

@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_stock_news(ticker, max_articles=5):
    """Fetch stock news from Yahoo Finance RSS feed
    
    Cached for 10 minutes to avoid excessive RSS feed requests.
    Cache key is based on ticker and max_articles.
    """
    try:
        # Yahoo Finance RSS feed for specific stock
        url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
        
        # Parse RSS feed
        feed = feedparser.parse(url)
        
        news_articles = []
        for entry in feed.entries[:max_articles]:
            article = {
                'title': entry.title,
                'summary': getattr(entry, 'summary', 'No summary available'),
                'link': entry.link,
                'published': getattr(entry, 'published', 'Date not available'),
                'source': 'Yahoo Finance'
            }
            news_articles.append(article)
        
        return news_articles
    
    except Exception as e:
        st.error(f"Error fetching news: {str(e)}")
        return []

def display_news_section(ticker):
    """Display news section for the selected ticker with lazy loading"""
    st.markdown('<div class="theme-container">', unsafe_allow_html=True)
    
    # Use expander for lazy loading - news only fetched when expanded
    with st.expander(f"Latest News for {ticker}", expanded=False):
        # Fetch news only when expander is opened
        with st.spinner(f"Loading latest news for {ticker}..."):
            news_articles = fetch_stock_news(ticker)
        
        if news_articles:
            for i, article in enumerate(news_articles):
                st.markdown(f"### {article['title']}")
                st.write(f"**Source:** {article['source']} | **Published:** {article['published']}")
                st.write(f"{article['summary']}")
                st.markdown(f"[Read Full Article]({article['link']})")
                if i < len(news_articles) - 1:  # Don't add separator after last article
                    st.markdown("---")
        else:
            st.info(f"No recent news found for {ticker}")
        
        # Add refresh button
        st.markdown("")  # Add spacing
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Refresh News", key=f"refresh_news_{ticker}"):
                # Clear cache for this ticker's news
                fetch_stock_news.clear()
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Initialize theme in session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Apply theme CSS
    apply_theme_css(st.session_state.theme)
    
    # Custom header
    st.markdown("""
    <div class="dashboard-header">
        <h1>Professional Finance Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize control variables
    timeframe_changed = False
    
    # ============================================
    # CHECK PRICE ALERTS ON STARTUP
    # ============================================
    alert_manager = get_alert_manager()
    triggered_alerts = alert_manager.check_all_alerts()
    if triggered_alerts:
        for alert in triggered_alerts:
            st.toast(f"🔔 {alert.ticker} {alert.alert_type} ${alert.target_price:.2f}", icon="🔔")
    
    # ============================================
    # SIDEBAR CONTROLS
    # ============================================
    with st.sidebar:
        st.header("Dashboard Controls")
        
        # Theme Toggle Section
        st.subheader("Theme")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Light", use_container_width=True, 
                        type="primary" if st.session_state.theme == 'light' else "secondary",
                        help="Switch to light theme"):
                st.session_state.theme = 'light'
                st.rerun()
        
        with col2:
            if st.button("Dark", use_container_width=True,
                        type="primary" if st.session_state.theme == 'dark' else "secondary",
                        help="Switch to dark theme"):
                st.session_state.theme = 'dark'
                st.rerun()
        
        # Theme status indicator with enhanced styling
        if st.session_state.theme == 'dark':
            st.success(f"**Active:** {st.session_state.theme.title()} Mode")
        else:
            st.info(f"**Active:** {st.session_state.theme.title()} Mode")
        
        st.markdown("---")
        
        # Stock Selection
        st.subheader("Stock Selection")
        # Check if a stock was selected from watchlist
        if 'selected_ticker' in st.session_state:
            default_ticker = st.session_state['selected_ticker']
            # Update the text input value in session state so it reflects immediately
            st.session_state['ticker_input'] = default_ticker
            # Clear the selection so it doesn't persist
            del st.session_state['selected_ticker']
            timeframe_changed = True  # Trigger data fetch for selected stock
        else:
            default_ticker = st.session_state.get('ticker_input', "AAPL")
        # Use session state for ticker input to ensure immediate update
        ticker = st.text_input("Stock Ticker", value=default_ticker, key="ticker_input", help="Enter a valid stock symbol (e.g., AAPL, MSFT, GOOGL)").upper()
        if not validate_ticker(ticker):
            st.error("Invalid ticker symbol")
            st.stop()
        st.success(f"Selected: **{ticker}**")
        # Data Fetch Button (right after ticker selection)
        if st.button("Fetch Data", type="primary", use_container_width=True):
            timeframe_changed = True  # Trigger data fetch
        
        # Chart Type Selection  
        st.subheader("Chart Type")
        chart_type = st.selectbox("Select Chart Style", ["Line Chart", "Candlestick Chart"])
        
        # Trading Timeframe Selection
        st.subheader("Timeframe")
        st.write("Select candle interval:")
        
        timeframes = [
            ("1D", "1D", "Daily", "Each candle = 1 day"),
            ("1W", "1W", "Weekly", "Each candle = 1 week"), 
            ("1M", "1M", "Monthly", "Each candle = 1 month"),
            ("3M", "3M", "Quarterly", "Each candle = 3 months")
        ]
        
        selected_timeframe = "1D"  # Default
        selected_timeframe_desc = "Daily"
        
        # Create timeframe buttons in sidebar
        for label, tf_code, desc, tooltip in timeframes:
            if st.button(f"{label} - {desc}", key=f"tf_{tf_code}", help=tooltip, use_container_width=True):
                selected_timeframe = tf_code
                selected_timeframe_desc = desc
                st.session_state['selected_timeframe'] = selected_timeframe
                st.session_state['selected_timeframe_desc'] = selected_timeframe_desc
                # Clear old data when timeframe changes
                if 'stock_data' in st.session_state:
                    del st.session_state['stock_data']
                timeframe_changed = True
        
        # Get timeframe from session state if it exists
        if 'selected_timeframe' in st.session_state:
            selected_timeframe = st.session_state['selected_timeframe']
            selected_timeframe_desc = st.session_state['selected_timeframe_desc']
        
        st.info(f"**Active:** {selected_timeframe_desc}")
        
        # Display Options (First - choose what to show)
        st.markdown("---")
        st.subheader("Display Options")
        show_ma_short = st.checkbox("Show Short MA", True)
        show_ma_long = st.checkbox("Show Long MA", False)
        show_rsi = st.checkbox("Show RSI", True)
        show_bb = st.checkbox("Show Bollinger Bands", False)
        show_volume = st.checkbox("Show Volume", True)
        
        # Technical Indicator Parameters (Second - fine-tune the settings)
        st.markdown("---")
        st.subheader("Indicator Settings")
        
        # Moving Average periods
        ma_short_period = st.slider("Short MA Period", 5, 50, 20, 5, help="Short-term moving average period")
        ma_long_period = st.slider("Long MA Period", 20, 200, 50, 10, help="Long-term moving average period") 
        
        # RSI settings
        rsi_period = st.slider("RSI Period", 5, 30, 14, 1, help="RSI calculation period")
        
        # Bollinger Bands settings  
        bb_period = st.slider("Bollinger Bands Period", 10, 50, 20, 5, help="Bollinger Bands period")
        bb_std = st.slider("Bollinger Bands Std Dev", 1.0, 3.0, 2.0, 0.1, help="Standard deviation multiplier")
        
        # Auto-Refresh Controls
        st.markdown("---")
        st.subheader("⚡ Auto-Refresh")
        auto_refresh = st.checkbox("Enable Auto-Refresh", value=False, key="auto_refresh_enabled", 
                                   help="Automatically refresh prices and charts")
        
        if auto_refresh:
            refresh_interval = st.select_slider(
                "Refresh Interval",
                options=[5, 10, 15, 30, 60],
                value=15,
                format_func=lambda x: f"{x} seconds",
                key="refresh_interval"
            )
            
            # Display last refresh time
            if 'last_refresh' not in st.session_state:
                st.session_state['last_refresh'] = datetime.now()
            
            st.caption(f"Last refresh: {st.session_state['last_refresh'].strftime('%H:%M:%S')}")
    

    # Create main layout: Charts (left) + Watchlist (right)
    main_col, watchlist_col = st.columns([3, 1])

    # ============================================
    # MAIN CONTENT AREA WITH WATCHLIST
    # ============================================
    
    
    with watchlist_col:
        st.markdown('<div class="theme-container">', unsafe_allow_html=True)
        st.subheader("Watchlist")
        
        # Initialize watchlist in session state
        if 'watchlist' not in st.session_state:
            st.session_state['watchlist'] = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']  # Default stocks
        
        # Add new stock to watchlist
        st.write("**Add Stock:**")
        col1, col2 = st.columns([2, 1])
        with col1:
            new_stock = st.text_input("", placeholder="Enter ticker (e.g., NVDA)", label_visibility="collapsed").upper()
        with col2:
            if st.button("Add", help="Add to watchlist"):
                if new_stock:
                    if new_stock in st.session_state['watchlist']:
                        st.warning("Already in watchlist!")
                    elif not validate_ticker(new_stock):
                        st.error("Invalid ticker format!")
                    else:
                        # Show spinner while validating ticker exists
                        with st.spinner(f"Validating {new_stock}..."):
                            if validate_ticker_exists(new_stock):
                                st.session_state['watchlist'].append(new_stock)
                                # Clear price cache so it refreshes with new stock
                                if 'watchlist_prices' in st.session_state:
                                    del st.session_state['watchlist_prices']
                                st.success(f"Added {new_stock}!")
                                st.rerun()
                            else:
                                st.error(f"Ticker {new_stock} not found!")
                else:
                    st.warning("Please enter a ticker!")
        
        # Display watchlist
        col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
        with col_header1:
            st.write("**Your Stocks:**")
        with col_header2:
            if st.button("Refresh", key="refresh_prices", help="Refresh prices"):
                if 'watchlist_prices' in st.session_state:
                    del st.session_state['watchlist_prices']
                st.rerun()
        
        if st.session_state['watchlist']:
            # Use real-time prices for watchlist
            price_service = get_price_service()
            prices_data = price_service.get_multiple_prices(st.session_state['watchlist'])
            
            # Convert to simple price dict for compatibility
            prices = {ticker: data['price'] for ticker, data in prices_data.items()}
            
            for i, stock in enumerate(st.session_state['watchlist']):
                # Create clean row for each stock with proper alignment
                ticker_col, price_col, remove_col = st.columns([2, 1, 1])
                
                with ticker_col:
                    # Stock ticker button
                    if st.button(f"{stock}", key=f"load_{stock}", help=f"Load {stock} chart", 
                                type="secondary", use_container_width=True):
                        st.session_state['selected_ticker'] = stock
                        st.rerun()
                
                with price_col:
                    # Price display with change indicator
                    price = prices.get(stock)
                    if price is not None:
                        # Get full price data for change indicator
                        price_data = prices_data.get(stock)
                        if price_data and 'change_percent' in price_data:
                            change_pct = price_data['change_percent']
                            color = "green" if change_pct >= 0 else "red"
                            arrow = "▲" if change_pct >= 0 else "▼"
                            st.markdown(f"<span style='color: {color};'>${price:.2f} {arrow}</span>", 
                                      unsafe_allow_html=True)
                        else:
                            st.write(f"${price:.2f}")
                    else:
                        st.write("$---.--")
                
                with remove_col:
                    # Remove button
                    if st.button("Remove", key=f"remove_{stock}", help=f"Remove {stock}"):
                        st.session_state['watchlist'].remove(stock)
                        # Also remove from price cache
                        if 'watchlist_prices' in st.session_state and stock in st.session_state['watchlist_prices']:
                            del st.session_state['watchlist_prices'][stock]
                        st.rerun()
        else:
            st.write("*No stocks in watchlist*")
        
        # Quick add popular stocks
        st.write("**Quick Add:**")
        popular_stocks = ['AMZN', 'META', 'NFLX', 'NVDA', 'AMD', 'UBER', 'SHOP']
        cols = st.columns(2)
        for i, stock in enumerate(popular_stocks):
            with cols[i % 2]:
                if st.button(stock, key=f"quick_{stock}", use_container_width=True, type="secondary"):
                    if stock not in st.session_state['watchlist']:
                        st.session_state['watchlist'].append(stock)
                        # Clear price cache so it refreshes with new stock
                        if 'watchlist_prices' in st.session_state:
                            del st.session_state['watchlist_prices']
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close watchlist container
    
    # Main chart area (left side)
    with main_col:
        
        # Always collect current parameters and display options
        indicator_params = {
            'ma_short_period': ma_short_period,
            'ma_long_period': ma_long_period,
            'rsi_period': rsi_period,
            'bb_period': bb_period,
            'bb_std': bb_std
        }
        
        display_options = {
            'show_ma_short': show_ma_short,
            'show_ma_long': show_ma_long,
            'show_rsi': show_rsi,
            'show_bb': show_bb,
            'show_volume': show_volume
        }
        
        # Check if we need to recalculate indicators (only when parameters change)
        params_changed = False
        if 'indicator_params' in st.session_state:
            if st.session_state['indicator_params'] != indicator_params:
                params_changed = True
        
        # Fetch data only when needed (timeframe change or fetch button)
        if timeframe_changed:
            with st.spinner(f"Fetching {selected_timeframe_desc} data for {ticker}..."):
                data = fetch_stock_data_with_timeframe(ticker, selected_timeframe, period='2y')
                
                if data is None:
                    st.error(f"No data found for {ticker}")
                    # Clear session state
                    for key in ['stock_data', 'current_ticker', 'indicator_params', 'display_options']:
                        if key in st.session_state:
                            del st.session_state[key]
                else:
                    # Add all technical indicators with current parameters
                    data_with_indicators = add_all_indicators(data, indicator_params)
                    
                    # Store in session state
                    st.session_state['stock_data'] = data_with_indicators
                    st.session_state['current_ticker'] = ticker
                    st.session_state['indicator_params'] = indicator_params
                    
                    st.success(f"Successfully loaded {len(data)} days of data!")
        
        # Recalculate indicators if parameters changed (but data exists)
        elif params_changed and 'stock_data' in st.session_state:
            raw_data = fetch_stock_data_with_timeframe(ticker, selected_timeframe, period='2y')
            if raw_data is not None:
                data_with_indicators = add_all_indicators(raw_data, indicator_params)
                st.session_state['stock_data'] = data_with_indicators
                st.session_state['indicator_params'] = indicator_params
        
        # Always update display options (no recalculation needed)
        st.session_state['display_options'] = display_options
        
        # Display results
        if 'stock_data' in st.session_state:
            data = st.session_state['stock_data']
            ticker = st.session_state['current_ticker']
            
            # Display live price at the top
            price_service = get_price_service()
            live_price_data = price_service.get_live_price(ticker)
            
            if live_price_data:
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                with col1:
                    st.markdown(f"### {ticker}")
                with col2:
                    st.metric("Live Price", f"${live_price_data['price']:.2f}")
                with col3:
                    change_color = "green" if live_price_data['change'] >= 0 else "red"
                    st.metric("Change", f"${live_price_data['change']:.2f}", 
                             delta=f"{live_price_data['change_percent']:.2f}%")
                with col4:
                    st.caption(f"Updated: {live_price_data['timestamp'].strftime('%H:%M:%S')}")
            else:
                st.markdown(f"### {ticker}")
            
            st.markdown("---")
            
            # Main chart area (TOP PRIORITY - show charts first)
            st.markdown('<div class="theme-container">', unsafe_allow_html=True)
            st.write("## Interactive Charts")
            
            # Get theme colors for chart styling
            theme_colors = get_theme_colors(st.session_state.theme)
            
            # Use current parameters from sidebar (for instant updates)
            current_indicator_params = st.session_state.get('indicator_params', indicator_params)
            current_display_options = display_options  # Always use live sidebar values
            
            if chart_type == "Line Chart":
                fig = create_line_chart_with_indicators(data, ticker, current_indicator_params, current_display_options)
            else:
                fig = create_candlestick_chart_with_indicators(data, ticker, current_indicator_params, current_display_options)
            
            # Apply theme styling to the chart
            fig.update_layout(
                plot_bgcolor=theme_colors['background'],
                paper_bgcolor=theme_colors['paper'],
                font=dict(color=theme_colors['text']),
                title_font=dict(color=theme_colors['text'], size=20),
                xaxis=dict(gridcolor=theme_colors['grid']),
                yaxis=dict(gridcolor=theme_colors['grid'])
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # News section (below charts, before technical analysis)
            display_news_section(ticker)
            
            # NEW: Price Alerts Section
            display_price_alerts_section()
            
            # NEW: Paper Trading Section (pass current ticker for quick trades)
            display_paper_trading_section(ticker)
            
            # Technical Analysis Summary (below trading sections)
            st.markdown("---")
            display_technical_summary(data, ticker)
            
            # Data Overview (below summary)
            display_data_info(data)
            
            # Additional options in expandable section
            with st.expander("Advanced Options"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Download Data as CSV"):
                        csv = data.to_csv()
                        st.download_button(
                            label="Download CSV",
                            data=csv,
                            file_name=f"{ticker}_{selected_timeframe_desc}_data.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.checkbox("Show Raw Data"):
                        st.write("**Data Columns:**", list(data.columns))
                        st.write("**RSI14 values (last 5):**", data['RSI14'].tail().tolist() if 'RSI14' in data.columns else "RSI14 column missing!")
                        st.dataframe(data.tail(10))
    
    # ============================================
    # AUTO-REFRESH LOGIC
    # ============================================
    if st.session_state.get('auto_refresh_enabled', False):
        refresh_interval = st.session_state.get('refresh_interval', 15)
        
        # Update last refresh time
        st.session_state['last_refresh'] = datetime.now()
        
        # Force cache clear for watchlist prices and alerts
        if 'watchlist_prices' in st.session_state:
            del st.session_state['watchlist_prices']
        
        # Check alerts on refresh
        alert_manager = get_alert_manager()
        triggered_alerts = alert_manager.check_all_alerts()
        if triggered_alerts:
            for alert in triggered_alerts:
                st.toast(f"🔔 {alert.ticker} {alert.alert_type} ${alert.target_price:.2f}", icon="🔔")
        
        # Use sleep and rerun to refresh
        time.sleep(refresh_interval)
        st.rerun()


if __name__ == "__main__":
    main()