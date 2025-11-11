import streamlit as st
import pandas as pd

def show_pipValue(data: pd.DataFrame):
  st.title("Pip Value Calculator")
  
  def pip_value(row, lots, acc_curr, pips, datadf):
    pair = row['Pairs']
    quote = row['Quotes']

    # Determine pip size
    pip_size = 0.01 if 'JPY' in pair else 0.0001
    units = lots * 100000

    # Case 1: If acc currency == Quote currency
    if acc_curr == pair[3:]:
      return f"{acc_curr} {round(pip_size * units * pips, 3)}"
    # Case 2: If acc currency == base currency
    elif acc_curr == pair[:3]:
      return f"{acc_curr} {round(pip_size * units * pips / quote, 3)}"
    # Case 3: account currency not in pair
    else:
      pip_value_quote = (pip_size * units) / quote
      # Find conversion rate quote -> acc currency
      cr_pair = f"{pair[:3]}{acc_curr}"
      inv_cr_pair = f"{acc_curr}{pair[:3]}"
      cr = 0
      if cr_pair in datadf['Pairs'].values:
        cr = datadf.loc[datadf['Pairs'] == cr_pair, 'Quotes'].iloc[0]
      elif inv_cr_pair in datadf['Pairs'].values:
        cr = 1 / datadf.loc[datadf['Pairs'] == inv_cr_pair, 'Quotes'].iloc[0]
      else:
        return "Unavailable"
      return f"{acc_curr} {round(pip_value_quote * cr * pips, 3)}"

  with st.container(border=True, width="stretch", height="stretch", gap="small"):
    # Input Fields
    # ====> 1). Account Currency
    _currencyPairs = ['USD', 'CHF', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'NZD']
    _accCurrInput = st.selectbox(label="Account Currency", options=_currencyPairs, index=0)

    # ====> 2). Trade Size
    _tradeLots = st.number_input(label="Trade Size (in Lots)", min_value=0.001, max_value=100.00, value=1.00, step=0.001, format="%.3f")

    # ====> 3). Pips
    _pips = st.number_input(label="Pips", min_value=0.00, value=1.00, step=0.0001, format="%.4f")

    # ====> 4). Calculate button
    submit_button = st.button(label='Calculate')

    res_placeholder = st.empty()

    if submit_button:
      if _tradeLots <= 0 or _pips <= 0:
        st.toast(body="Please fill in all fields with valid values !", duration="long")
      else:
        with res_placeholder.container():
          _datadfClone = data.copy(deep=True)

          _datadfClone['PipValues'] = _datadfClone.apply(pip_value, axis=1, args=(_tradeLots, _accCurrInput, _pips, data))
          st.table(_datadfClone, border='horizontal')          
