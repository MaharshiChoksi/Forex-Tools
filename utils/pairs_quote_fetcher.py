from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

quote_forex_url = r"https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_48-forex-128-currency-pairs--qc_1-alphabetical-order?p="
quote_commodity_url = r"https://www.centralcharts.com/en/price-list-ranking/ALL/asc/ts_529-gold-silver-coins--qc_1-alphabetical-order?p="
pages_limit = 5

def scrape_url(url):
    try:
        rows_data = []
        for i in range(1, pages_limit + 1):
            # Fetch Web content
            req = Request(url=url+str(i), headers={'User-Agent': 'Mozilla/5.0'})
            res = urlopen(req).read()
            # Parse HTML
            soup = BeautifulSoup(res, 'html.parser')
            # Get table
            try:
                table = soup.find_all('article')[0].find(class_="tabMini-wrapper").find('table')
                if table:
                    tbody = table.find('tbody')
                    if tbody:
                        for tr in tbody.find_all('tr'):
                            row = []
                            for td in tr.find_all('td')[:2]:
                                row.append(td.get_text(strip=True))
                            rows_data.append(row)
                else:
                    break
            except Exception as e:
                break
        # print("Final Rows Data:", rows_data)  # Print after all processing
        return rows_data
    except Exception as e:
        print("Error Occurred While Fetching Quotes")
        return

@st.cache_data(ttl=3600)
def fetch_quotes() -> pd.DataFrame:
    Commodity = dict()
    Forex = dict()
    # Commodity
    comm_data = scrape_url(quote_commodity_url)
    if isinstance(comm_data, list):
        for i in comm_data:
            if 'ounce silver usd' in i[0].lower() or 'ounce gold usd' in i[0].lower():
                Commodity[i[0].split('(')[1].split(')')[0]] = i[1]
    
    # Forex
    fx_data = scrape_url(quote_forex_url)
    if isinstance(fx_data, list):
        Forex = {key: value for key, value in fx_data}

    if(Forex or Commodity):
        Quotes = {key: Forex[key] + Commodity[key] for key in Forex}
        df = pd.DataFrame(Quotes)
        if(df.notnull or df != "None"):
            return df
