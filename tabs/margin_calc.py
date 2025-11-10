import streamlit as st
import pandas as pd

def show_margin(data: pd.DataFrame):
  st.title("Margin Calculator")

  with st.form(key="margin_form", border=True, width="stretch", height="stretch"):

    # Input Fields
    # ====> 1). Pair
    _pairsList = data["Pairs"].to_list()
    _pairInput = st.selectbox(label="Currency Pair", options=_pairsList, index=0)
    _currencyPairs = ['USD', 'CHF', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'NZD']

    # ====> 2). Account Currency
    _accCurrInput = st.selectbox(label="Account Currency", options=_currencyPairs, index=0)

    # ====> 3). Leverage Ratio
    _leverageRatios = ["1:1", "1:5", "1:10", "1:20", "1:25", "1:30",
                        "1:50", "1:66", "1:100", "1:125", "1:150", 
                        "1:200", "1:300", "1:400", "1:500", "1:1000"]
    _leverageInput = st.selectbox(label="Margin Ratio", options=_leverageRatios, index=6)

    # ====> 4). Traded Lots
    _tradeLots = st.number_input(label="Traded Size (Lots)", min_value=0.001, max_value=100.00, value=0.001, step=0.001, format="%.3f")

    # ====> 5). Quote
    # Display currency pair's price respect base currency as account currency
    _QuoteWithAccCurrency = 1
    _pairWithAccCurrency = ""
    # If quote not account currency
    if(_pairInput[0:3] != _accCurrInput):
      _pairWithAccCurrency = _pairInput[0:3] + _accCurrInput
      value = data.loc[data['Pairs'] == _pairWithAccCurrency, 'Quotes'].iloc[0]
      if value is not None:
        _QuoteWithAccCurrency = value
      st.write(f"{_pairWithAccCurrency}: {_QuoteWithAccCurrency}")
    # If quote account currency
    else:
      value = data.loc[data['Pairs'] == _pairInput, 'Quotes'].iloc[0]
      if value is not None:
        _QuoteWithAccCurrency = value
    
    res_placeholder = st.empty()
    
    # ====> 6). Calculate button
    submit_button = st.form_submit_button(label='Calculate')

    if submit_button:
     if(_tradeLots == None or _tradeLots == 0):
       st.error("!!! Input Required for Traded Lots !!!")
      # Compute lots size
     else:
      with res_placeholder.container():
        contract_size = 100000  # Standard Lot
        if "XAU" in _pairInput:
          contract_size = 100 # Gold Standard Lot
        elif "XAG" in _pairInput:
          contract_size = 5000 # Silver Standard Lot

        st.write(f"Using Standard Contact Size: {contract_size}")
        leverage = _leverageInput.rsplit(':')[1]
        _computedMarginReq = ((contract_size * float(_tradeLots)) / int(leverage)) * _QuoteWithAccCurrency
        if _computedMarginReq:
          st.success(f"Required Margin: {_computedMarginReq}")
