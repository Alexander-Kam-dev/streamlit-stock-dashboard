import streamlit as st

# Import our custom modules
from data_fetcher import fetch_stock_data_with_timeframe, validate_ticker, validate_ticker_exists, get_watchlist_prices
from indicators import add_all_indicators
from chart_builder import create_line_chart_with_indicators, create_candlestick_chart_with_indicators
from utils import display_technical_summary, display_data_info


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

def apply_theme_css(theme="light"):
    """Apply custom CSS styling based on theme"""
    
    if theme == "dark":
        # Dark theme CSS
        st.markdown("""
        <style>
        /* Main app background */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA !important;
        }
                            
        /* Hide Streamlit Main Menu & Toolbar completely */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        
        /* Sidebar styling - make it black with white text */
        .css-1d391kg, 
        .css-1rs6os,
        .css-17eq0hr,
        .css-16huue1,
        .css-1lcbmhc,
        .stSidebar,
        .stSidebar > div,
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div {
            background-color: #000000 !important;
        }
        
        /* All sidebar text elements - comprehensive targeting */
        .css-1d391kg *, 
        .css-1rs6os *,
        .css-17eq0hr *,
        .css-16huue1 *,
        .css-1lcbmhc *,
        .stSidebar *,
        [data-testid="stSidebar"] *,
        .css-1d391kg .stMarkdown, 
        .css-1d391kg .stText, 
        .css-1d391kg p, 
        .css-1d391kg span, 
        .css-1d391kg div,
        .css-1d391kg h1,
        .css-1d391kg h2,
        .css-1d391kg h3,
        .css-1d391kg h4,
        .css-1d391kg label,
        .stSidebar .stMarkdown,
        .stSidebar .stText,
        .stSidebar p,
        .stSidebar span,
        .stSidebar div,
        .stSidebar h1,
        .stSidebar h2,
        .stSidebar h3,
        .stSidebar h4,
        .stSidebar label {
            color: #FFFFFF !important;
        }
        
        /* Sidebar input fields */
        .css-1d391kg input,
        .stSidebar input,
        [data-testid="stSidebar"] input {
            background-color: #333333 !important;
            color: #FFFFFF !important;
            border: 1px solid #555555 !important;
        }
        
        /* Sidebar select boxes */
        .css-1d391kg .stSelectbox > div > div,
        .stSidebar .stSelectbox > div > div,
        [data-testid="stSidebar"] .stSelectbox > div > div {
            background-color: #333333 !important;
            color: #FFFFFF !important;
        }
        
        /* Sidebar checkbox labels */
        .stSidebar .stCheckbox label,
        .stSidebar .stCheckbox span,
        [data-testid="stSidebar"] .stCheckbox label,
        [data-testid="stSidebar"] .stCheckbox span {
            color: #FFFFFF !important;
        }
        
        /* Sidebar slider labels and text */
        .stSidebar .stSlider label,
        .stSidebar .stSlider span,
        .stSidebar .stSlider div,
        [data-testid="stSidebar"] .stSlider label,
        [data-testid="stSidebar"] .stSlider span,
        [data-testid="stSidebar"] .stSlider div {
            color: #FFFFFF !important;
        }
        
        /* Metric containers */
        [data-testid="metric-container"] {
            background-color: #262730;
            border: 1px solid #404040;
            border-radius: 0.5rem;
            padding: 1rem;
        }
        
        
        /* Buttons - More specific targeting */
        .stButton > button,
        .stButton button,
        button[data-testid="baseButton-secondary"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border: 1px solid #333333 !important;
            border-radius: 0.5rem;
            transition: all 0.3s;
        }

        .stButton > button:hover,
        .stButton button:hover,
        button[data-testid="baseButton-secondary"]:hover {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
        }
                    
        /* Primary buttons */
        .stButton > button[kind="primary"] {
            background-color: #00D4AA;
            color: #0E1117;
            font-weight: bold;
        }
        
        .stButton > button[kind="primary"]:hover {
            background-color: #00B894;
        }
        
        /* Secondary buttons (watchlist tickers, etc.) - black with white text */
        .stButton > button[data-testid*="secondary"] {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border: 1px solid #333333;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background-color: #1a1a1a !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
        }
        
        /* Custom containers */
        .theme-container {
            background-color: #1E1E1E;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #404040;
            margin: 1rem 0;
        }
        
        /* Watchlist specific styling in dark mode */
        .theme-container .stMarkdown,
        .theme-container .stText,
        .theme-container p,
        .theme-container span,
        .theme-container div {
            color: #FFFFFF !important;
        }
        
        /* Header styling */
        .dashboard-header {
            background: linear-gradient(90deg, #FF6B35 0%, #00D4AA 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .dashboard-header h1 {
            color: white;
            margin: 0;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        </style>
        """, unsafe_allow_html=True)
    
    else:
        # Light theme CSS
        st.markdown("""
        <style>
        /* Main app background */
        .stApp {
            background-color: #FFFFFF;
            color: #262730;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #F0F2F6;
        }
        
        /* Metric containers */
        [data-testid="metric-container"] {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 0.5rem;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #FF6B35;
            color: white;
            border: none;
            border-radius: 0.5rem;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #E55A2B;
            transform: translateY(-2px);
        }
        
        /* Primary buttons */
        .stButton > button[kind="primary"] {
            background-color: #00D4AA;
            color: white;
            font-weight: bold;
        }
        
        .stButton > button[kind="primary"]:hover {
            background-color: #00B894;
        }
        
        /* Secondary buttons (watchlist tickers, etc.) */
        .stButton > button[kind="secondary"] {
            background-color: #E9ECEF;
            color: #262730 !important;
            border: 1px solid #CED4DA;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background-color: #DEE2E6;
            color: #1C1E21 !important;
            transform: translateY(-1px);
        }
        
        /* Custom containers */
        .theme-container {
            background-color: #F8F9FA;
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #E0E0E0;
            margin: 1rem 0;
        }
        
        /* Header styling */
        .dashboard-header {
            background: linear-gradient(90deg, #FF6B35 0%, #00D4AA 100%);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .dashboard-header h1 {
            color: white;
            margin: 0;
            font-weight: 700;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        </style>
        """, unsafe_allow_html=True)


def main():
    # Initialize theme in session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Apply theme CSS
    apply_theme_css(st.session_state.theme)
    
    # Custom header with gradient styling
    st.markdown("""
    <div class="dashboard-header">
        <h1>📈 Professional Finance Dashboard</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize control variables
    timeframe_changed = False
    
    # ============================================
    # SIDEBAR CONTROLS
    # ============================================
    with st.sidebar:
        st.header("🎛️ Dashboard Controls")
        
        # Theme Toggle Section
        st.subheader("🎨 Theme")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🌞 Light", use_container_width=True, 
                        type="primary" if st.session_state.theme == 'light' else "secondary",
                        help="Switch to light theme"):
                st.session_state.theme = 'light'
                st.rerun()
        
        with col2:
            if st.button("🌙 Dark", use_container_width=True,
                        type="primary" if st.session_state.theme == 'dark' else "secondary",
                        help="Switch to dark theme"):
                st.session_state.theme = 'dark'
                st.rerun()
        
        # Theme status indicator with enhanced styling
        theme_emoji = "🌞" if st.session_state.theme == 'light' else "🌙"
        if st.session_state.theme == 'dark':
            st.success(f"{theme_emoji} **Active:** {st.session_state.theme.title()} Mode")
        else:
            st.info(f"{theme_emoji} **Active:** {st.session_state.theme.title()} Mode")
        
        st.markdown("---")
        
        # Stock Selection
        st.subheader("📊 Stock Selection")
        
        # Check if a stock was selected from watchlist
        if 'selected_ticker' in st.session_state:
            default_ticker = st.session_state['selected_ticker']
            # Clear the selection so it doesn't persist
            del st.session_state['selected_ticker']
            timeframe_changed = True  # Trigger data fetch for selected stock
        else:
            default_ticker = "AAPL"
        
        ticker = st.text_input("Stock Ticker", value=default_ticker, help="Enter a valid stock symbol (e.g., AAPL, MSFT, GOOGL)").upper()
        
        if not validate_ticker(ticker):
            st.error("⚠️ Invalid ticker symbol")
            st.stop()
        
        st.success(f"✅ Selected: **{ticker}**")
        
        # Data Fetch Button (right after ticker selection)
        if st.button("🔄 **Fetch Data**", type="primary", use_container_width=True):
            timeframe_changed = True  # Trigger data fetch
        
        # Chart Type Selection  
        st.subheader("📈 Chart Type")
        chart_type = st.selectbox("Select Chart Style", ["Line Chart", "Candlestick Chart"])
        
        # Trading Timeframe Selection
        st.subheader("⏰ Timeframe")
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
        
        st.info(f"📊 **Active:** {selected_timeframe_desc}")
        
        # Display Options (First - choose what to show)
        st.markdown("---")
        st.subheader("👀 Display Options")
        show_ma_short = st.checkbox("Show Short MA", True)
        show_ma_long = st.checkbox("Show Long MA", False)
        show_rsi = st.checkbox("Show RSI", True)
        show_bb = st.checkbox("Show Bollinger Bands", False)
        show_volume = st.checkbox("Show Volume", True)
        
        # Technical Indicator Parameters (Second - fine-tune the settings)
        st.markdown("---")
        st.subheader("⚙️ Indicator Settings")
        
        # Moving Average periods
        ma_short_period = st.slider("Short MA Period", 5, 50, 20, 5, help="Short-term moving average period")
        ma_long_period = st.slider("Long MA Period", 20, 200, 50, 10, help="Long-term moving average period") 
        
        # RSI settings
        rsi_period = st.slider("RSI Period", 5, 30, 14, 1, help="RSI calculation period")
        
        # Bollinger Bands settings  
        bb_period = st.slider("Bollinger Bands Period", 10, 50, 20, 5, help="Bollinger Bands period")
        bb_std = st.slider("Bollinger Bands Std Dev", 1.0, 3.0, 2.0, 0.1, help="Standard deviation multiplier")
    

    # Create main layout: Charts (left) + Watchlist (right)
    main_col, watchlist_col = st.columns([3, 1])

    # ============================================
    # MAIN CONTENT AREA WITH WATCHLIST
    # ============================================
    
    
    with watchlist_col:
        st.markdown('<div class="theme-container">', unsafe_allow_html=True)
        st.subheader("📋 Watchlist")
        
        # Initialize watchlist in session state
        if 'watchlist' not in st.session_state:
            st.session_state['watchlist'] = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']  # Default stocks
        
        # Add new stock to watchlist
        st.write("**Add Stock:**")
        col1, col2 = st.columns([2, 1])
        with col1:
            new_stock = st.text_input("", placeholder="Enter ticker (e.g., NVDA)", label_visibility="collapsed").upper()
        with col2:
            if st.button("➕", help="Add to watchlist"):
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
            if st.button("🔄", key="refresh_prices", help="Refresh prices"):
                if 'watchlist_prices' in st.session_state:
                    del st.session_state['watchlist_prices']
                st.rerun()
        
        if st.session_state['watchlist']:
            # Fetch prices if not cached
            if 'watchlist_prices' not in st.session_state:
                with st.spinner("Fetching prices..."):
                    st.session_state['watchlist_prices'] = get_watchlist_prices(st.session_state['watchlist'])
            
            prices = st.session_state['watchlist_prices']
            
            for i, stock in enumerate(st.session_state['watchlist']):
                # Create clean row for each stock with proper alignment
                ticker_col, price_col, remove_col = st.columns([2, 1, 1])
                
                with ticker_col:
                    # Stock ticker button
                    if st.button(f"📊 {stock}", key=f"load_{stock}", help=f"Load {stock} chart", 
                                type="secondary", use_container_width=True):
                        st.session_state['selected_ticker'] = stock
                        st.rerun()
                
                with price_col:
                    # Price display - aligned properly
                    price = prices.get(stock)
                    if price is not None:
                        st.write(f"${price:.2f}")
                    else:
                        st.write("$---.--")
                
                with remove_col:
                    # Remove button
                    if st.button("❌", key=f"remove_{stock}", help=f"Remove {stock}"):
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
                    st.error(f"❌ No data found for {ticker}")
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
                    
                    st.success(f"✅ Successfully loaded {len(data)} days of data!")
        
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
            
            # Main chart area (TOP PRIORITY - show charts first)
            st.markdown('<div class="theme-container">', unsafe_allow_html=True)
            st.write("## 📈 Interactive Charts")
            
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
                xaxis=dict(gridcolor=theme_colors['grid']),
                yaxis=dict(gridcolor=theme_colors['grid'])
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Technical Analysis Summary (below charts)
            st.markdown("---")
            display_technical_summary(data, ticker)
            
            # Data Overview (below summary)
            display_data_info(data)
            
            # Additional options in expandable section
            with st.expander("🔧 Advanced Options"):
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📥 Download Data as CSV"):
                        csv = data.to_csv()
                        st.download_button(
                            label="💾 Download CSV",
                            data=csv,
                            file_name=f"{ticker}_{selected_timeframe_desc}_data.csv",
                            mime="text/csv"
                        )
                
                with col2:
                    if st.checkbox("📋 Show Raw Data"):
                        st.write("**Data Columns:**", list(data.columns))
                        st.write("**RSI14 values (last 5):**", data['RSI14'].tail().tolist() if 'RSI14' in data.columns else "RSI14 column missing!")
                        st.dataframe(data.tail(10))


if __name__ == "__main__":
    main()