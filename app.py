import streamlit as st
import yfinance as yf

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Meriam.business | Value Investing", page_icon="📈")

# 2. MASTER CSS (Extra Bold, Mobile-First, Dashboard Look)
st.markdown("""
    <style>
    .stApp p, .stApp span, .stApp label, .stApp div {
        font-weight: 900 !important;
    }
    .stApp {
        background: linear-gradient(to bottom right, #f0f2f6, #0068C9);
        color: #1E3A8A;
    }
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 5rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    header { visibility: hidden; }

    .metric-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
        border-left: 6px solid #0000FF;
        font-size: 16px;
        color: #1E3A8A;
    }
    
    .main-title {
        font-size: 32px !important;
        font-weight: 900 !important;
        color: #0000FF !important;
        text-align: center;
        margin-bottom: 0px;
    }
    .brand-name {
        font-size: 20px !important;
        font-weight: 900 !important;
        color: #0000FF !important;
        text-align: center;
        margin-bottom: 20px;
    }
    .underlined-text {
        display: inline-block;
        border-bottom: 4px solid #0000FF;
        margin-bottom: 15px;
        font-weight: 900 !important;
        font-size: 22px;
    }
    .disclaimer {
        font-size: 11px !important;
        color: #444444 !important;
        text-align: center;
        margin-top: 40px;
        padding: 15px;
        border-top: 1px solid #0068C9;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown('<p class="main-title">THE VALUE INVESTING GUIDE</p>', unsafe_allow_html=True)
st.markdown('<p class="brand-name">BY MERIAM.BUSINESS</p>', unsafe_allow_html=True)

def meriam_value_investing_report():
    target_ticker = st.text_input("Enter Ticker (e.g. AAPL, MSFT, DH.TN):").upper()
    
    if target_ticker:
        # --- DATA ACQUISITION WITH PROTECTION ---
        try:
            stock = yf.Ticker(target_ticker)
            info = stock.info
            per = info.get('trailingPE')
            
            # If Yahoo returns an empty dict or no PER, force manual mode
            if per is None or per == 0:
                connection_success = False
            else:
                connection_success = True
        except Exception:
            connection_success = False

        if not connection_success:
            st.warning(f"⚠️ Data for {target_ticker} unavailable. Manual Mode Activated.")
            per = st.number_input("1. Enter PER:", value=0.0)
            pb = st.number_input("2. Enter P/B Ratio:", value=0.0)
            roe = st.number_input("3. Enter ROE %:", value=0.0) / 100
            de = st.number_input("4. Enter Debt-to-Equity:", value=0.0)
            cash_more_debt = st.radio("5. More Cash than Debt?", ('Yes', 'No')) == 'Yes'
            curr_ratio = st.number_input("6. Current Ratio:", value=0.0)
            net_margin = st.number_input("7. Net Profit Margin %:", value=0.0) / 100
            div_yield = st.number_input("8. Dividend Yield %:", value=0.0) / 100
            rev_growth = st.number_input("9. Revenue Growth %:", value=0.0) / 100
            fcf_pos = st.radio("10. Is Free Cash Flow Positive?", ('Yes', 'No')) == 'Yes'
        else:
            st.success(f"✅ Live Connection: {target_ticker}")
            pb = info.get('priceToBook', 0)
            roe = info.get('returnOnEquity', 0)
            de = (info.get('debtToEquity', 0) or 0) / 100
            cash_more_debt = (info.get('totalCash', 0) or 0) > (info.get('totalDebt', 0) or 0)
            curr_ratio = info.get('currentRatio', 0)
            net_margin = info.get('profitMargins', 0)
            div_yield = info.get('dividendYield', 0) or 0
            rev_growth = info.get('revenueGrowth', 0) or 0
            fcf_pos = (info.get('freeCashflow', 0) or 0) > 0

        # --- THE 10-POINT SCORING LOGIC ---
        score = 0
        if 0 < per < 15: score += 1
        if 0 < pb < 3: score += 1
        if roe > 0.15: score += 1
        if de < 1.0: score += 1
        if cash_more_debt: score += 1
        if curr_ratio >= 1.5: score += 1
        if net_margin > 0.10: score += 1
        if div_yield > 0.02: score += 1
        if rev_growth > 0: score += 1
        if fcf_pos: score += 1

        # --- DISPLAY ---
        st.markdown('<div class="underlined-text">THE VALUE INVESTING REPORT</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card">Stock: {target_ticker}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">PER: {per:.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">P/B: {pb:.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">ROE: {roe * 100:.2f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Debt-to-Eq: {de:.2f}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card">Margin: {net_margin * 100:.2f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Div Yield: {div_yield * 100:.2f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Current Ratio: {curr_ratio:.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Rev Growth: {rev_growth * 100:.2f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Positive FCF: {"YES" if fcf_pos else "NO"}</div>', unsafe_allow_html=True)

        st.markdown(f"## FINAL SCORE: {score} / 10")
        
        if score >= 8: verdict = "HIGHLY INVEST"
        elif 5 <= score < 8: verdict = "RECOMMEND"
        elif 3 <= score < 5: verdict = "WAIT"
        else: verdict = "DO NOT INVEST"
            
        st.write(f"### FINAL RESULT: {verdict}")

# 4. FOOTER & EXECUTION
meriam_value_investing_report()

st.markdown("""
    <div class="disclaimer">
        <b>DISCLAIMER:</b> This tool is for educational purposes only. 
        Meriam.business does not provide professional financial advice. 
        Investing in stocks involves risk.
    </div>
    """, unsafe_allow_html=True)
