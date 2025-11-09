import yfinance as yf
import pandas as pd
import streamlit as st

def scrape_pairs():
    try:
        pairs = {"Pairs": ['EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF', 'AUDUSD', 'USDCAD', 'NZDUSD',
                 'EURGBP', 'EURAUD', 'GBPJPY', 'GBPCAD', 'AUDNZD', 'EURCHF', 'CHFJPY', 'EURBRL',
                 'EURMXN', 'GBPBRL', 'GBPMXN', 'USDSGD', 'USDHKD', 'EURTRY', 'GBPTHB', 'AUDSGD',
                 'USDZAR', 'USDILS', 'USDBRL', 'USDMXN', 'EURJPY', 'AUDJPY', 'AUDCHF', 'NZDJPY', 
                 'AUDBRL', 'AUDMXN', 'CHFBRL', 'CHFMXN', 'GBPAUD', 'GBPNZD']}
        df = pd.DataFrame(pairs)
        return df
    except Exception as e:
        print(f"Error Occurred While Fetching Quotes: {e}")
        return

def scrape_quotes(pairs: pd.DataFrame):
    try:
        final_df = pd.DataFrame()
        temp_dict = {
        }

        for _sym in pairs['Pairs']:
            # Fetch Web content
            res = yf.Ticker(f"{_sym}=X").info
            if res:
                temp_dict[_sym] = round(res['regularMarketPrice'], res['priceHint'])

        final_df = pd.DataFrame(temp_dict.items(), columns=["Pairs", "Quotes"])
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
    if not isinstance(final_pairs_quotes, pd.DataFrame) or final_pairs_quotes.empty:
        return pd.DataFrame()
    return final_pairs_quotes
