import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
import ta
from pages.utils.plotly_figure import plotly_table
from pages.utils.plotly_figure import filter_data, close_chart, Moving_Average, RSI, MACD, candlestick


st.set_page_config(
    page_title = "Stock Analysis",
    page_icon = "page_with_curl",
    layout = "wide",
)

st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input("Enter the Stock Symbol", "TSLA")

with col2:
    start_date = st.date_input("Start Date", datetime.date(today.year - 1, today.month, today.day))

with col3:
    end_date = st.date_input("End Date", datetime.date(today.year, today.month, today.day))

data = yf.download(ticker, start=start_date, end=end_date)

st.subheader(ticker)

stock = yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])

st.write("**Sector:**", stock.info['sector'])
st.write("**Industry:**", stock.info['industry'])
st.write("**Country:**", stock.info['country'])
st.write("**Full Time Employees:**", stock.info['fullTimeEmployees'])
st.write("**website:**", stock.info['website'])

col1, col2 = st.columns(2)

with col1:
    df = pd.DataFrame(index = ['Market Cap', 'Beta', 'EPS', 'PE Ratio'])
    df[''] = [stock.info['marketCap'], stock.info['beta'], stock.info['trailingEps'], stock.info['trailingPE']]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

with col2:
    df = pd.DataFrame(index = ['Quote Ratio', 'Revenue per share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'])
    df[''] = [stock.info['quickRatio'], stock.info['revenuePerShare'], stock.info['profitMargins'], stock.info['debtToEquity'], stock.info['returnOnEquity']]
    fig_df = plotly_table(df)
    st.plotly_chart(fig_df, use_container_width=True)

data = yf.download(ticker, start = start_date, end = end_date)

col1, col2, col3 = st.columns(3)
daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
col1.metric("Daily Change", str(round(data['Close'].iloc[-1],2)), str(round(daily_change,2)))

last_10_df = data.tail(10).sort_index(ascending = False).round(3)
fig_df = plotly_table(last_10_df)

st.write('##### Historical Data (Last 10 days)')
st.plotly_chart(fig_df, use_container_width=True)


col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1]*12)

num_period = ''

with col1:
    if st.button('5D'):
        num_period = '5d'

with col2:
    if st.button('1M'):
        num_period = '1mo'

with col3:
    if st.button('6M'):
        num_period = '6mo'

with col4:
    if st.button('YTD'):
        num_period = 'ytd'

with col5:
    if st.button('1Y'):
        num_period = '1y'

with col6:
    if st.button('5Y'):
        num_period = '5y'

with col7:
    if st.button('MAX'):
        num_period = 'max'

col1, col2, col3 = st.columns([1,1,4])
with col1:
    chart_type = st.selectbox('',('Candle', 'Line'))
with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('',('RSI', 'MACD'))
    else:
        indicators = st.selectbox('', ('RSI', 'Moving Average', 'MACD'))


ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period = 'max')
data1 = ticker_.history(period = 'max')
if num_period == '':
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1,'1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1,'1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True) 

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1,'1y'), use_container_width=True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_Average(data1, '1y'), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1,'1y'), use_container_width=True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width=True)

else:
    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1,num_period), use_container_width=True)
        st.plotly_chart(RSI(data1, num_period), use_container_width=True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1,num_period), use_container_width=True)
        st.plotly_chart(MACD(data1, num_period), use_container_width=True) 

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1,num_period), use_container_width=True)
        st.plotly_chart(RSI(data1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_Average(data1, num_period), use_container_width=True)

    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1,num_period), use_container_width=True)
        st.plotly_chart(MACD(data1, num_period), use_container_width=True)



st.markdown("### Opening Price")
st.line_chart(data.Open)

st.markdown("### Closing Price")
st.line_chart(data.Close)

st.markdown("### High Price")
st.line_chart(data.High)

st.markdown("### Low Price")
st.line_chart(data.Low)

st.markdown("### Volume")
st.line_chart(data.Volume)


st.write("")
st.markdown(
    ":gray[✨ Made with ❤️ and passion by **Akash**. ©2025 [theyug.com](https://theyug.com) - All Rights Reserved.]"
)