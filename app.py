import streamlit as st
import yfinance as yf

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Meriam.business | Value Investing", page_icon="📈")

# 2. MASTER CSS (Keep your bold, mobile-first look)
st.markdown("""
    <style>
    .stApp p, .stApp span, .stApp label, .stApp div { font-weight: 900 !important; }
    .stApp { background: linear-gradient(to bottom right, #f0f2f6, #0068C9); color: #1E3A8A; }
    [data-testid="stAppViewBlockContainer"] { padding-top: 5rem !important; padding-left: 1rem !important; padding-right: 1rem !important; }
    header { visibility: hidden; }
    .metric-card {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 15px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px; border-left: 6px solid #0000FF;
        font-size: 16px; color: #1E3A8A;
    }
    .main-title { font-size: 32px !important; font-weight: 900 !important; color: #0000FF !important; text-align: center; margin-bottom: 0px; }
    .brand-name { font-size: 20px !important; font-weight: 900 !important; color: #0000FF !important; text-align: center; margin-bottom: 20px; }
    .underlined-text { display: inline-block; border-bottom: 4px solid #0000FF; margin-bottom: 15px; font-weight: 900 !important; font-size: 22px; }
    .disclaimer { font-size: 11px !important; color: #444444 !important; text-align: center; margin-top: 40px; padding: 15px; border-top: 1px solid #0068C9; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown('<p class="main-title">THE VALUE INVESTING GUIDE</p>', unsafe_allow_html=True)
st.markdown('<p class="brand-name">BY MERIAM.BUSINESS</p>', unsafe_allow_html=True)

# Initialize Session State to track if we should show the results
if 'show_results' not in st.session_state:
    st.session_state.show_results = False

def meriam_value_investing_report():
    # Only show inputs if results are NOT currently being shown
    if not st.session_state.show_results:
        target_ticker = st.text_input("Enter Ticker (e.g. AAPL, MSFT, DH.TN):").upper()
        
        if target_ticker:
            # We skip live fetching for now to ensure Manual Mode works perfectly as you requested
            st.info(f"Manual Mode Activated for: {target_ticker}")
            
            # Organize inputs in columns for better layout
            col_a, col_b = st.columns(2)
            with col_a:
                per = st.number_input("1. Enter PER:", value=0.0)
                pb = st.number_input("2. Enter P/B Ratio:", value=0.0)
                roe = st.number_input("3. Enter ROE %:", value=0.0) / 100
                de = st.number_input("4. Enter Debt-to-Equity:", value=0.0)
                cash_more_debt = st.radio("5. More Cash than Debt?", ('Yes', 'No')) == 'Yes'
            with col_b:
                curr_ratio = st.number_input("6. Current Ratio:", value=0.0)
                net_margin = st.number_input("7. Net Profit Margin %:", value=0.0) / 100
                div_yield = st.number_input("8. Dividend Yield %:", value=0.0) / 100
                rev_growth = st.number_input("9. Revenue Growth %:", value=0.0) / 100
                fcf_pos = st.radio("10. Is Free Cash Flow Positive?", ('Yes', 'No')) == 'Yes'

            # THE BUTTON
            if st.button("GENERATE REPORT"):
                # Save data to session state so we don't lose it when the page reloads
                st.session_state.data = {
                    'ticker': target_ticker, 'per': per, 'pb': pb, 'roe': roe, 'de': de,
                    'cash': cash_more_debt, 'curr': curr_ratio, 'margin': net_margin,
                    'div': div_yield, 'growth': rev_growth, 'fcf': fcf_pos
                }
                st.session_state.show_results = True
                st.rerun()

    # If results are toggled ON, show the cards and hide the inputs
    else:
        d = st.session_state.data
        
        # Scoring Logic
        score = 0
        if 0 < d['per'] < 15: score += 1
        if 0 < d['pb'] < 3: score += 1
        if d['roe'] > 0.15: score += 1
        if d['de'] < 1.0: score += 1
        if d['cash']: score += 1
        if d['curr'] >= 1.5: score += 1
        if d['margin'] > 0.10: score += 1
        if d['div'] > 0.02: score += 1
        if d['growth'] > 0: score += 1
        if d['fcf']: score += 1

        st.markdown('<div class="underlined-text">THE VALUE INVESTING REPORT</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card">Stock: {d["ticker"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">PER: {d["per"]:.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">P/B: {d["pb"]:.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">ROE: {d["roe"] * 100:.2f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Debt-to-Eq: {d["de"]:.2f}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card">Margin: {d["margin"] * 100:.2f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Div Yield: {d["div"] * 100:.2f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Current Ratio: {d["curr"]:.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Rev Growth: {d["growth"] * 100:.2f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Positive FCF: {"YES" if d["fcf"] else "NO"}</div>', unsafe_allow_html=True)

        st.markdown(f"## FINAL SCORE: {score} / 10")
        
        if score >= 8: verdict = "HIGHLY INVEST"
        elif 5 <= score < 8: verdict = "RECOMMEND"
        elif 3 <= score < 5: verdict = "WAIT"
        else: verdict = "DO NOT INVEST"
            
        st.write(f"### FINAL RESULT: {verdict}")

        # Add a "Go Back" button to reset the view
        if st.button("← ANALYZE ANOTHER STOCK"):
            st.session_state.show_results = False
            st.rerun()

# 4. EXECUTION
meriam_value_investing_report()

st.markdown('<div class="disclaimer"><b>DISCLAIMER:</b> This tool is for educational purposes only. Meriam.business does not provide professional financial advice.</div>', unsafe_allow_html=True)
