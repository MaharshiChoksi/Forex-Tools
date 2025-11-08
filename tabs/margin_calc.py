import streamlit as st
import pandas as pd

def show_margin(data: pd.DataFrame):
  st.title("Margin Calculator")

  with st.form(key="margin_form"):
    st.write("Enter values for calculation: ")

    # Input Fields
    # ====> 1). Pair
    print(data)
    _pairsList = data["Pair"].to_list()
    _pairInput = st.selectbox("Currency Pair", _pairsList, _pairsList[0])
    _currencyPairs = ['USD', 'CHF', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'NZD']

    # ====> 2). Account Currency
    _accCurrInput = st.selectbox("Account Currency", _currencyPairs, _currencyPairs[0])

    # ====> 3). Leverage Ratio
    _leverageRatios = ["1:1", "1:5", "1:10", "1:20", "1:25", "1:30",
                        "1:50", "1:66", "1:100", "1:125", "1:150", 
                        "1:200", "1:300", "1:400", "1:500", "1:1000"]
    _leverageInput = st.selectbox("Margin Ratio", _leverageRatios, _leverageRatios[6])

    # ====> 4). Traded Lots
    _tradeLots = st.number_input("Traded Size (Lots)", min_value=0, max_value=100, format="%.3f")

    # ====> 5). Quote
    # Display currency pair's price respect base currency as account currency
    _QuoteWithAccCurrency = 0
    _pairWithAccCurrency = ""
    # If quote as acc currency
    if(_pairInput[0:3] == _accCurrInput):
      value = data.loc[data[_pairInput] == _pairInput, 'Quote'].item()
      _QuoteWithAccCurrency = value
    # If quote not acc currency
    else:
      _pairWithAccCurrency = _pairInput[0:3] + _accCurrInput[3:6]
      value = data.loc[data[_pairWithAccCurrency] == _pairWithAccCurrency, 'Quote'].item()
      if(value):
        _QuoteWithAccCurrency = value
        st.write(f"{_pairWithAccCurrency}: {_QuoteWithAccCurrency}")
    
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
        if _pairInput.contains("XAU"):
          contract_size = 100 # Gold Standard Lot
        elif _pairInput.contains("XAG"):
          contract_size = 5000 # Silver Standard Lot

        st.write(f"Using Standard Contact Size: {contract_size}")
        _computedMarginReq = ((contract_size * _tradeLots) / _leverageInput) * _QuoteWithAccCurrency
        if _computedMarginReq:
          st.success(f"Required Margin: {_computedMarginReq}")
