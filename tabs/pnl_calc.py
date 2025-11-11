import streamlit as st
import pandas as pd

def show_pnl(data: pd.DataFrame):
  st.title("P&L Calculator")

  with st.container(border=True, width="stretch", height="stretch", gap="small"):
    # Input Fields
    # ====> 1). Pair
    _pairsList = data["Pairs"].to_list()
    _pairInput = st.selectbox(label="Currency Pair", options=_pairsList, index=0)

    # ====> 2). Account Currency
    _currencyPairs = ['USD', 'CHF', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'NZD']
    _accCurrInput = st.selectbox(label="Account Currency", options=_currencyPairs, index=0)
    
    # ====> 3). Trade Size (Lots)
    _tradeLots = st.number_input(label="Trade Size (in Lots)", min_value=0.001, max_value=100.00, value=1.00, step=0.001, format="%.3f")

    # ====> 4). Open Price
    _openPrice = st.number_input(label="Open Price", min_value=0.00001, step=0.00001, format="%.5f")

    # ====> 5). Close Price
    _closePrice = st.number_input(label="Close Price", min_value=0.00001, step=0.00001, format="%.5f")
    
    # ====> 6). Trade Direction
    _direction = st.radio("Trade Direction", ("Long", "Short"))

    res_placeholder = st.empty()

    # ====> 7). Calculate button
    submit_button = st.button(label='Calculate')

    if submit_button:
      if _openPrice <= 0 or _closePrice <= 0:
        st.toast(body="Please fill in all fields with valid values !", duration="long")
      else:
        with res_placeholder.container():
          contract_size = 100000  # Standard Lot
          # Calculate pnl
          pnl = 0
          if _direction == "Long":
            pnl = (_closePrice - _openPrice) * _tradeLots * contract_size
          else:
            pnl = (_openPrice - _closePrice) * _tradeLots * contract_size
          
          # profit to quote currency
          if _pairInput[3:6] == _accCurrInput:
            pnl = round(pnl, 2)
            st.success(f"{_accCurrInput}: {pnl}")
          else:
            pnl /= data.loc[data['Pairs'] == f"{_accCurrInput}{_pairInput[3:6]}", 'Quotes'].iloc[0]
            pnl = round(pnl, 2)
            st.success(f"{_accCurrInput}: {pnl}")
