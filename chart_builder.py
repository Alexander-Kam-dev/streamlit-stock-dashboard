import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_line_chart_with_indicators(data, ticker, indicator_params=None, display_options=None):
    """Create dynamic line chart with customizable indicators"""
    
    # Default parameters
    if indicator_params is None:
        indicator_params = {'ma_short_period': 20, 'ma_long_period': 50, 'rsi_period': 14}
    if display_options is None:
        display_options = {'show_ma_short': True, 'show_ma_long': False, 'show_rsi': True, 'show_bb': False, 'show_volume': True}
    
    # Determine number of rows based on what's being shown
    rows = 1  # Always show price
    if display_options.get('show_rsi', True):
        rows += 1
    if display_options.get('show_volume', True):
        rows += 1
    
    # Create subplot titles dynamically
    subplot_titles = ['Price + Indicators']
    if display_options.get('show_rsi', True):
        subplot_titles.append(f'RSI ({indicator_params.get("rsi_period", 14)})')
    if display_options.get('show_volume', True):
        subplot_titles.append('Volume')
    
    # Adjust row heights based on number of rows
    if rows == 3:
        row_heights = [0.6, 0.2, 0.2]
    elif rows == 2:
        row_heights = [0.7, 0.3]
    else:
        row_heights = [1.0]
    
    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=subplot_titles,
        row_heights=row_heights
    )
    
    # Price line (always shown)
    fig.add_trace(go.Scatter(
        x=data.index, y=data['Close'],
        mode='lines', name=f"{ticker} Close",
        line=dict(color='blue', width=2)
    ), row=1, col=1)
    
    # Short MA (if enabled)
    if display_options.get('show_ma_short', True):
        ma_short_col = f'MA{indicator_params.get("ma_short_period", 20)}'
        if ma_short_col in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index, y=data[ma_short_col],
                mode='lines', name=ma_short_col,
                line=dict(color='red', width=2)
            ), row=1, col=1)
    
    # Long MA (if enabled)
    if display_options.get('show_ma_long', False):
        ma_long_col = f'MA{indicator_params.get("ma_long_period", 50)}'
        if ma_long_col in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index, y=data[ma_long_col],
                mode='lines', name=ma_long_col,
                line=dict(color='purple', width=2)
            ), row=1, col=1)
    
    # Bollinger Bands (if enabled)
    if display_options.get('show_bb', False):
        if 'BB_Upper' in data.columns and 'BB_Lower' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index, y=data['BB_Upper'],
                mode='lines', name='BB Upper',
                line=dict(color='gray', width=1), showlegend=False
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=data.index, y=data['BB_Lower'],
                mode='lines', name='BB Lower',
                line=dict(color='gray', width=1),
                fill='tonexty', fillcolor='rgba(128,128,128,0.1)',
                showlegend=False
            ), row=1, col=1)
    
    # Track current row for RSI and Volume
    current_row = 2
    
    # RSI (if enabled)
    if display_options.get('show_rsi', True):
        rsi_col = f'RSI{indicator_params.get("rsi_period", 14)}'
        if rsi_col in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index, y=data[rsi_col],
                mode='lines', name=rsi_col,
                line=dict(color='orange', width=2)
            ), row=current_row, col=1)
            
            # RSI reference lines
            fig.add_hline(y=30, line_dash="dash", line_color="red", row=current_row, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="green", row=current_row, col=1)
            current_row += 1
    
    # Volume (if enabled)
    if display_options.get('show_volume', True):
        fig.add_trace(go.Bar(
            x=data.index, y=data['Volume'],
            name='Volume', marker_color='lightblue',
            showlegend=False
        ), row=current_row, col=1)
    
    fig.update_layout(
        title=f"{ticker} - Interactive Technical Analysis",
        height=700, showlegend=True
    )
    
    # Hide x-axis labels for all rows except the last one
    for i in range(1, rows):
        fig.update_xaxes(showticklabels=False, row=i, col=1)
    
    return fig

def create_candlestick_chart_with_indicators(data, ticker, indicator_params=None, display_options=None):
    """Create candlestick chart with dynamic overlays"""
    
    # Default parameters
    if indicator_params is None:
        indicator_params = {'ma_short_period': 20, 'ma_long_period': 50}
    if display_options is None:
        display_options = {'show_ma_short': True, 'show_ma_long': False, 'show_bb': False, 'show_volume': True}
    
    # Determine number of rows based on what's being shown
    rows = 1  # Always show price
    if display_options.get('show_rsi', True):
        rows += 1
    if display_options.get('show_volume', True):
        rows += 1
    
    # Dynamic subplot titles and heights
    subplot_titles = ['Candlestick + Indicators']
    if rows == 3:
        row_heights = [0.6, 0.2, 0.2]
        if display_options.get('show_rsi', True):
            subplot_titles.append(f'RSI ({indicator_params.get("rsi_period", 14)})')
        if display_options.get('show_volume', True):
            subplot_titles.append('Volume')
    elif rows == 2:
        row_heights = [0.7, 0.3]
        if display_options.get('show_rsi', True):
            subplot_titles.append(f'RSI ({indicator_params.get("rsi_period", 14)})')
        elif display_options.get('show_volume', True):
            subplot_titles.append('Volume')
    else:
        row_heights = [1.0]
    
    fig = make_subplots(
        rows=rows, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=subplot_titles,
        row_heights=row_heights
    )
    
    # Candlesticks (always shown)
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'], high=data['High'],
        low=data['Low'], close=data['Close'],
        name=f"{ticker} OHLC"
    ), row=1, col=1)
    
    # Short MA overlay (if enabled)
    if display_options.get('show_ma_short', True):
        ma_short_col = f'MA{indicator_params.get("ma_short_period", 20)}'
        if ma_short_col in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index, y=data[ma_short_col],
                mode='lines', name=ma_short_col,
                line=dict(color='red', width=2)
            ), row=1, col=1)
    
    # Long MA overlay (if enabled)
    if display_options.get('show_ma_long', False):
        ma_long_col = f'MA{indicator_params.get("ma_long_period", 50)}'
        if ma_long_col in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index, y=data[ma_long_col],
                mode='lines', name=ma_long_col,
                line=dict(color='purple', width=2)
            ), row=1, col=1)
    
    # Bollinger Bands overlay (if enabled)
    if display_options.get('show_bb', False):
        if 'BB_Upper' in data.columns and 'BB_Lower' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index, y=data['BB_Upper'],
                mode='lines', name='BB Upper',
                line=dict(color='gray', width=1), showlegend=False
            ), row=1, col=1)
            
            fig.add_trace(go.Scatter(
                x=data.index, y=data['BB_Lower'],
                mode='lines', name='BB Lower',
                line=dict(color='gray', width=1),
                fill='tonexty', fillcolor='rgba(128,128,128,0.1)',
                showlegend=False
            ), row=1, col=1)
    
    # Track current row for RSI and Volume
    current_row = 2
    
    # RSI (if enabled)
    if display_options.get('show_rsi', True):
        rsi_col = f'RSI{indicator_params.get("rsi_period", 14)}'
        if rsi_col in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index, y=data[rsi_col],
                mode='lines', name=rsi_col,
                line=dict(color='orange', width=2)
            ), row=current_row, col=1)
            
            # RSI reference lines
            fig.add_hline(y=30, line_dash="dash", line_color="red", row=current_row, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="green", row=current_row, col=1)
            current_row += 1
    
    # Volume (if enabled)
    if display_options.get('show_volume', True):
        fig.add_trace(go.Bar(
            x=data.index, y=data['Volume'],
            name='Volume', marker_color='lightblue',
            showlegend=False
        ), row=current_row, col=1)
    
    fig.update_layout(
        title=f"{ticker} - Interactive Candlestick Chart",
        height=600, xaxis_rangeslider_visible=False
    )
    
    # Hide x-axis labels for all rows except the last one
    for i in range(1, rows):
        fig.update_xaxes(showticklabels=False, row=i, col=1)
    
    return fig