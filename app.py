import streamlit as st
st.set_page_config(page_title="Meriam.business | Value Investing", page_icon="📈")

import yfinance as yf
st.markdown("""
    <style>
    /* This only makes the text bold and nothing else */
    .stApp p, .stApp span, .stApp label {
        font-weight: bold !important;
        color: inherit; 
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #f0f2f6, #0068C9);
        color: #1E3A8A;
    }
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    </style>
    """, unsafe_allow_html=True)
st.markdown("""
    <style>
    .main-title {
        font-size: 42px !important;
        font-weight: 900 !important;
        color: #0000FF !important;
        text-align: center;
        margin-bottom: 0px;
        line-height: 1.1;
    }
    .brand-name {
        font-size: 26px !important;
        font-weight: 900 !important;
        color: #0000FF !important;
        text-align: center;
        letter-spacing: 1px;
    }

    /* PASTE THIS NEW PART HERE */
    .underlined-text {
        display: inline-block; /* Makes line end when text ends */
        border-bottom: 3px solid #0000FF; /* The lively blue line */
        padding-bottom: 2px;
        margin-bottom: 10px;
        font-weight: 900 !important;
        font-size: 20px;
    }
    </style>
    
    <p class="main-title">THE VALUE INVESTING GUIDE</p>
    <p class="brand-name">BY MERIAM.BUSINESS</p>
    """, unsafe_allow_html=True)
def meriam_value_investing_report():
    # 1. UNIVERSAL INPUT
    target_ticker = st.text_input("Enter the Stock Ticker (e.g AAPL, MSFT etc ): ").upper()
    
    if target_ticker:
        st.write(f"🔍 GENERATING VALUE INVESTING REPORT: {target_ticker} ")
        stock = yf.Ticker(target_ticker)
        info = stock.info
        
        # Check if Yahoo has the data (using PER as the test)
        per = info.get('trailingPE')
        
        # --- DATA ACQUISITION (AUTO OR MANUAL) ---
        if per is None or per == 0:
            st.warning(f"⚠️ Yahoo data not found for {target_ticker}. Manual Mode Activated.")
            st.write("Please enter the values from Tustex, IlBoursa, or the company's Annual Report:")
            
            per = st.number_input("1. Enter PER:", value=0.0)
            pb = st.number_input("2. Enter P/B Ratio:", value=0.0)
            roe = st.number_input("3. Enter ROE %:", value=0.0) / 100
            de = st.number_input("4. Enter Debt-to-Equity:", value=0.0)
            cash_more_debt = st.radio("5. More Cash than Debt?", ('Yes', 'No')) == 'Yes'
            curr_ratio = st.number_input("6. Current Ratio:", value=0.0)
            net_margin = st.number_input("7. Net Profit Margin %:", value=0.0) / 100
            div_yield = st.number_input("8. Dividend Yield % (0 if none):", value=0.0) / 100
            rev_growth = st.number_input("9. Revenue Growth %:", value=0.0) / 100
            fcf_pos = st.radio("10. Is Free Cash Flow Positive?", ('Yes', 'No')) == 'Yes'
        else:
            st.success("✅ Connection Active. Data loading...")
            pb = info.get('priceToBook', 0)
            roe = info.get('returnOnEquity', 0)
            de = (info.get('debtToEquity', 0) or 0) / 100
            cash_more_debt = info.get('totalCash', 0) > info.get('totalDebt', 0)
            curr_ratio = info.get('currentRatio', 0)
            net_margin = info.get('profitMargins', 0)
            div_yield = info.get('dividendYield', 0) or 0
            rev_growth = info.get('revenueGrowth', 0) or 0
            fcf_pos = (info.get('freeCashflow', 0) or 0) > 0

        # --- THE 10-POINT SCORING LOGIC ---
        score = 0
        if 0 < per < 10: score += 1
        if 0 < pb < 3: score += 1
        if roe > 0.15: score += 1
        if de < 1.0: score += 1
        if cash_more_debt: score += 1
        if curr_ratio >= 1.5: score += 1
        if net_margin > 0.10: score += 1
        if div_yield > 0.02: score += 1
        if rev_growth > 0: score += 1
        if fcf_pos: score += 1

        # --- THE PROFESSIONAL OUTPUT ---
        
        st.text(f"          THE VALUE INVESTING REPORT")
        st.write(f"**Stock Name:** {target_ticker}")
        st.write(f"**PER:** {per:.2f}")
        st.write(f"**P/B:** {pb:.2f}")
        st.write(f"**ROE:** {roe * 100:.2f}%")
        st.write(f"**Debt-to-Equity:** {de:.2f}")
        st.write(f"**Profit Margin:** {net_margin * 100:.2f}%")
        st.write(f"**Dividend Yield:** {div_yield * 100:.2f}%")
        st.write(f"**Current Ratio:** {curr_ratio:.2f}")
        st.write(f"**Positive FCF:** {'YES' if fcf_pos else 'NO'}")
       
        st.subheader(f"FINAL SCORE: {score} / 10")
       
        # --- YOUR CUSTOM GRADING SCALE ---
        if score >= 8:
            verdict = "HIGHLY INVEST"
        elif 5 <= score < 8:
            verdict = "RECOMMEND"
        elif 3 <= score < 5:
            verdict = "WAIT"
        else:
            verdict = "DO NOT INVEST"
            
        st.write(f"### FINAL RESULT: {verdict}")
        

# Run the report generator
meriam_value_investing_report()
