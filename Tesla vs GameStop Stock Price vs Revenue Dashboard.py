import warnings
warnings.filterwarnings('ignore')
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# print('✅ Libraries imported successfully')

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,  subplot_titles=("Historical Share Price", "Historical Revenue"),
                        vertical_spacing=0.3)
    # Limit ranges per lab instructions
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True),
                             y=stock_data_specific.Close.astype('float'), name='Share Price'),
                  row=1, col=1)

    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True),
                             y=revenue_data_specific.Revenue.astype('float'), name='Revenue'),
                  row=2, col=1)

    fig.update_xaxes(title_text='Date', row=1, col=1)
    fig.update_xaxes(title_text='Date', row=2, col=1)
    fig.update_yaxes(title_text='Price ($US)', row=1, col=1)
    fig.update_yaxes(title_text='Revenue ($US Millions)', row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    fig.show()

#✅ Q1 — Extract Tesla Stock Data Using yfinance
'''Task: Create a Ticker for TSLA, download full history with period='max', reset index, and display the first 5 rows. Screenshot: From this header down to the output of tesla_data.head().'''

tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period='max')
tesla_data.reset_index(inplace=True)

print(tesla_data.head())

#✅ Q2 — Web‑scrape Tesla Quarterly Revenue (BeautifulSoup or read_html)
'''Task: Download the page and extract the Tesla Quarterly Revenue table into tesla_revenue with columns Date and Revenue, clean it, and show last 5 rows. Screenshot: From this header down to tesla_revenue.tail().'''
url_tsla_rev = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data = requests.get(url_tsla_rev).text
soup = BeautifulSoup(html_data, 'html.parser')
tsla_tables = pd.read_html(str(soup))
tesla_revenue = None
for df in tsla_tables:
    if 'Tesla Quarterly Revenue' in ' '.join(map(str, df.columns)) or 'Tesla Quarterly Revenue' in df.to_string():
        tesla_revenue = df.copy()
        break
if tesla_revenue is None:
    tesla_revenue = tsla_tables[0].copy()
tesla_revenue.columns = ['Date','Revenue']

tesla_revenue['Revenue'] = tesla_revenue['Revenue'].astype(str).str.replace(r',|\$', '', regex=True)

tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != '']

print(tesla_revenue.tail())

# ✅ Q3 — Extract GameStop Stock Data Using yfinance
'''Task: Create a Ticker for GME, download full history, reset index, and display the first 5 rows. Screenshot: From this header down to gme_data.head().'''

gme = yf.Ticker('GME')
gme_data = gme.history(period='max')
gme_data.reset_index(inplace=True)

print(gme_data.head())

#✅ Q4 — Web‑scrape GameStop Quarterly Revenue
'''Task: Download the page and extract the GME Quarterly Revenue table into gme_revenue with columns Date and Revenue, clean it, and show last 5 rows. Screenshot: From this header down to gme_revenue.tail().'''
url_gme_rev = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
html_data_2 = requests.get(url_gme_rev).text
soup2 = BeautifulSoup(html_data_2, 'html.parser')
gme_tables = pd.read_html(str(soup2))
gme_revenue = None
for df in gme_tables:
    if 'GameStop Quarterly Revenue' in ' '.join(map(str, df.columns)) or 'GameStop Quarterly Revenue' in df.to_string():
        gme_revenue = df.copy()
        break
if gme_revenue is None:
    gme_revenue = gme_tables[0].copy()

gme_revenue.columns = ['Date','Revenue']
gme_revenue['Revenue'] = gme_revenue['Revenue'].astype(str).str.replace(r',|\$', '', regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != '']

print(gme_revenue.tail())

#✅ Q5 — Plot Tesla Stock and Revenue Dashboard
'''Task: Use make_graph(tesla_data, tesla_revenue, 'Tesla') and take a screenshot of the resulting figure. Screenshot: The full figure that appears after this cell.'''

make_graph(tesla_data, tesla_revenue, 'Tesla')

#✅ Q6 — Plot GameStop Stock and Revenue Dashboard
'''Task: Use make_graph(gme_data, gme_revenue, 'GameStop') and take a screenshot of the resulting figure. Screenshot: The full figure that appears after this cell.'''

make_graph(gme_data, gme_revenue, 'GameStop')



