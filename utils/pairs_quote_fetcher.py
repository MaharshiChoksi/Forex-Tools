import requests
import pandas as pd
import streamlit as st

def scrape_pairs():
    try:
        pairs = {"Pair": ['EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF', 'AUDUSD', 'USDCAD', 'NZDUSD',
                 'EURGBP', 'EURAUD', 'GBPJPY', 'GBPCAD', 'AUDNZD', 'EURCHF', 'CHFJPY', 'EURBRL',
                 'EURMXN', 'GBPBRL', 'GBPMXN', 'USDSGD', 'USDHKD', 'EURTRY', 'GBPTHB', 'AUDSGD',
                 'USDZAR', 'USDILS', 'USDBRL', 'USDMXN', 'EURJPY', 'AUDJPY', 'AUDCHF', 'NZDJPY', 
                 'AUDBRL', 'AUDMXN', 'CHFBRL', 'CHFMXN', 'GBPAUD', 'GBPNZD', 'XAUUSD', 'XAGUSD'
                ]}
        df = pd.DataFrame(pairs)
        return df
    except Exception as e:
        print(f"Error Occurred While Fetching Quotes: {e}")
        return

def scrape_quotes(pairs: pd.DataFrame):
    try:
        final_df = pd.DataFrame(columns=["Pair", "Quote"])
        for _sym in pairs['Pair']:
            # Fetch Web content
            quote_url = f"https://financialmodelingprep.com/stable/quote-short?symbol={_sym}&apikey={st.secrets.get("API_KEY")}"
            res = requests.get(url=quote_url)
            if res.status_code == 200:
                # Parse HTML
                data = res.json()
                for item in data:
                    temp_df = pd.DataFrame([{"Pair": item['symbol'], "Quote": item['price']}])
                    final_df = pd.concat([final_df, temp_df], ignore_index=True)
        final_df.drop(columns=['index'], inplace=True)
        final_df.reset_index(drop=True, inplace=True)
        return final_df
    except Exception as e:
        print(f"Error Occurred While Fetching Quotes: {e}")
        return

@st.cache_data(ttl=21600)
def fetch_quotes() -> pd.DataFrame:
    # Pairs
    pairs = scrape_pairs()
    if not isinstance(pairs, pd.DataFrame):
        return pd.DataFrame()
    
    # Quotes & Pairs
    final_pairs_quotes = scrape_quotes(pairs)
    if not isinstance(final_pairs_quotes, pd.DataFrame):
        return pd.DataFrame()
    return final_pairs_quotes
