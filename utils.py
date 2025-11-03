import streamlit as st

def display_technical_summary(data, ticker):
    """Display summary of technical indicators"""
    st.write("## 📊 Technical Analysis Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**📈 Moving Average (MA20)**")
        if not data['MA20'].isna().all():
            latest_ma20 = data['MA20'].iloc[-1]
            current_price = data['Close'].iloc[-1]
            trend = "🟢 Bullish" if current_price > latest_ma20 else "🔴 Bearish"
            st.metric("MA20", f"${latest_ma20:.2f}", f"{trend}")
    
    with col2:
        st.write("**⚡ RSI (14-period)**")
        if not data['RSI14'].isna().all():
            latest_rsi = data['RSI14'].iloc[-1]
            if latest_rsi > 70:
                signal = "🔴 Overbought"
                delta_color = "inverse"
            elif latest_rsi < 30:
                signal = "🟢 Oversold"
                delta_color = "normal"
            else:
                signal = "🟡 Neutral"
                delta_color = "off"
            st.metric("RSI14", f"{latest_rsi:.1f}", signal)
    
    with col3:
        st.write("**📊 Bollinger Bands**")
        if not data['BB_Upper'].isna().all():
            current_price = data['Close'].iloc[-1]
            bb_upper = data['BB_Upper'].iloc[-1]
            bb_lower = data['BB_Lower'].iloc[-1]
            
            if current_price > bb_upper:
                bb_signal = "🔴 Above Upper"
            elif current_price < bb_lower:
                bb_signal = "🟢 Below Lower"
            else:
                bb_signal = "🟡 Within Bands"
            
            st.metric("Position", bb_signal)

def display_data_info(data):
    """Display basic data information"""
    st.write("## 📋 Data Overview")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Days", len(data))
    with col2:
        st.metric("Date Range", f"{data.index.min().date()} to {data.index.max().date()}")
    with col3:
        st.metric("Latest Close", f"${data['Close'].iloc[-1]:.2f}")