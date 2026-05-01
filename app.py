import streamlit as st
import yfinance as yf

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Meriam.business | Value Investing", page_icon="📈")

# 2. MASTER CSS
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
    .disclaimer { font-size: 11px !important; color: #444444 !important; text-align: center; margin-top: 40px; padding: 15px; border-top: 1px solid #0068C9; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# 3. HEADER
st.markdown('<p class="main-title">THE VALUE INVESTING GUIDE</p>', unsafe_allow_html=True)
st.markdown('<p class="brand-name">BY MERIAM.BUSINESS</p>', unsafe_allow_html=True)

if 'show_results' not in st.session_state:
    st.session_state.show_results = False

def meriam_value_investing_report():
    if not st.session_state.show_results:
        target_ticker = st.text_input("Enter Ticker (e.g. AAPL, MSFT, DH.TN...):", placeholder="TYPE HERE...").upper()
        
        if target_ticker:
            try:
                stock = yf.Ticker(target_ticker)
                info = stock.info
                if not info or info.get('trailingPE') is None:
                    st.warning(f"⚠️ Data for {target_ticker} unavailable. Manual Mode:")
                    is_manual = True
                else:
                    st.success(f"✅ Data Found!")
                    is_manual = False
            except Exception:
                st.warning(f"⚠️ Connection Error. Manual Mode:")
                is_manual = True

            if is_manual:
                col_a, col_b = st.columns(2)
                with col_a:
                    per = st.number_input("1. PER", value=0.0, step=0.1, format="%g")
                    pb = st.number_input("2. P/B Ratio", value=0.0, step=0.1, format="%g")
                    roe = st.number_input("3. ROE %", value=0.0, step=0.1, format="%g") / 100
                    de = st.number_input("4. Debt-to-Equity", value=0.0, step=0.1, format="%g")
                    cash = st.radio("5. Cash > Debt?", ('Yes', 'No')) == 'Yes'
                with col_b:
                    curr = st.number_input("6. Current Ratio", value=0.0, step=0.1, format="%g")
                    margin = st.number_input("7. Net Margin %", value=0.0, step=0.1, format="%g") / 100
                    div = st.number_input("8. Div Yield %", value=0.0, step=0.1, format="%g") / 100
                    growth = st.number_input("9. Rev Growth %", value=0.0, step=0.1, format="%g") / 100
                    fcf = st.radio("10. Positive FCF?", ('Yes', 'No')) == 'Yes'
            else:
                per = info.get('trailingPE', 0); pb = info.get('priceToBook', 0)
                roe = info.get('returnOnEquity', 0); de = (info.get('debtToEquity', 0) or 0) / 100
                cash = (info.get('totalCash', 0) or 0) > (info.get('totalDebt', 0) or 0)
                curr = info.get('currentRatio', 0); margin = info.get('profitMargins', 0)
                div = info.get('dividendYield', 0) or 0; growth = info.get('revenueGrowth', 0) or 0
                fcf = (info.get('freeCashflow', 0) or 0) > 0
                st.info("Live data loaded.")

            if st.button("GENERATE REPORT"):
                st.session_state.data = {
                    'ticker': target_ticker, 'per': per, 'pb': pb, 'roe': roe, 'de': de,
                    'cash': cash, 'curr': curr, 'margin': margin,
                    'div': div, 'growth': growth, 'fcf': fcf
                }
                st.session_state.show_results = True
                st.rerun()

    else:
        d = st.session_state.data
        score = 0
        if 0 < d['per'] < 15: score += 1
        if 0 < d['pb'] < 3: score += 1
        if d['roe'] >= 0.15: score += 1
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
            st.markdown(f'<div class="metric-card">ROE: {d["roe"] * 100:.1f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Debt-to-Eq: {d["de"]:.2f}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card">Margin: {d["margin"] * 100:.1f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Div Yield: {d["div"] * 100:.1f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Current Ratio: {d["curr"]:.2f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Growth: {d["growth"] * 100:.1f}%</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card">Positive FCF: {"YES" if d["fcf"] else "NO"}</div>', unsafe_allow_html=True)

        st.markdown(f"## FINAL SCORE: {score} / 10")
        verdict = "HIGHLY INVEST" if score >= 8 else "MODERATELY INVEST" if score >= 5 else "WAIT" if score >= 3 else "DO NOT INVEST!"
        st.write(f"### FINAL RESULT: {verdict}")

        if st.button("← ANALYZE ANOTHER"):
            st.session_state.show_results = False
            st.rerun()

meriam_value_investing_report()

st.markdown('<div class="disclaimer"><b>DISCLAIMER:</b> For educational use only. Meriam.business does not provide professional financial advice.Ivesting in stocks involves risk.</div>', unsafe_allow_html=True)
