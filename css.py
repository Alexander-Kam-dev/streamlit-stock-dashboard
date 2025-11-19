import streamlit as st

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
            padding: 1.5rem 0;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .dashboard-header h1 {
            color: #FFFFFF;
            margin: 0;
            font-weight: 700;
        }
        
        /* Main content area text - ensure all text is white in dark mode */
        .main .stMarkdown,
        .main .stMarkdown h1,
        .main .stMarkdown h2,
        .main .stMarkdown h3,
        .main .stMarkdown h4,
        .main .stMarkdown p,
        .main .stMarkdown span,
        .main .stMarkdown strong,
        .main p,
        .main span,
        .main div,
        .main h1,
        .main h2,
        .main h3,
        .main h4,
        .element-container p,
        .element-container span,
        .element-container div,
        .stMarkdown p,
        .stMarkdown span,
        .stMarkdown div,
        .stMarkdown strong,
        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3,
        .stMarkdown h4 {
            color: #FFFFFF !important;
        }
        
        /* Plotly chart titles and text */
        .js-plotly-plot .plotly .gtitle,
        .js-plotly-plot .plotly text,
        .js-plotly-plot .plotly .g-gtitle text,
        svg.main-svg text,
        .plotly-notifier,
        g.g-gtitle text {
            fill: #FFFFFF !important;
            color: #FFFFFF !important;
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
            padding: 1.5rem 0;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .dashboard-header h1 {
            color: #262730;
            margin: 0;
            font-weight: 700;
        }
        </style>
        """, unsafe_allow_html=True)