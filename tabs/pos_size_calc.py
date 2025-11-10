import streamlit as st
import pandas as pd

def show_posSize(data: pd.DataFrame):
    st.title("Position Size Calculator")
    # Input Fields
    # ====> 1). Pair
    _pairsList = data["Pairs"].to_list()
    _pairInput = st.selectbox(label="Currency Pair", options=_pairsList, index=0)
    _currencyPairs = ['USD', 'CHF', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'NZD']

    # ====> 2). Account Currency
    _accCurrInput = st.selectbox(label="Account Currency", options=_currencyPairs, index=0)

    # ====> 3). Account Size
    _accSize = st.number_input(label="Account Size", min_value=1.00, value=1000.00, step=0.01, format="%.2f")

    # ====> 4). Risk Ratio selection
    risk_type = st.radio("Select Risk Type", ("%", "$"))
    risk = 0.00
    if risk_type == "%":
      # ====> 4-A). Risk Ratio (%)
      risk = st.number_input(label="Risk Ratio (%)", min_value=0.01, max_value=100.00, value=1.00, step=0.01, format="%.2f")
    else:
      # ====> 4-B). Risk Ratio ($)
      risk = st.number_input(label="Risk Ratio ($)", min_value=0.01, max_value=_accSize, step=0.01, format="%.2f")

    # ====> 5). Stop-Loss, Pips
    _slPips = st.number_input(label="Stop Loss (in Pips)", min_value=1.00, step=0.0001, format="%.4f")

    # ====> 6). Trade Size (Lots)
    _tradeLots = st.number_input(label="Trade Size (in Lots)", min_value=0.001, max_value=100.00, value=1.00, step=0.001, format="%.3f")

    # ====> 7). Quote
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
    submit_button = st.button(label='Calculate')

    if submit_button:
      if _accSize <= 0 or risk <= 0 or _slPips <= 0 or _tradeLots <= 0:
        st.toast(body="Please fill in all fields with valid values !", duration="long")
      else:
        with res_placeholder.container():
          contract_size = 100000  # Standard Lot
          # Calculate Money at risk
          _money_at_risk = 0
          if risk_type == "%":
            _money_at_risk = _accSize * (risk / 100)
          else:
            _money_at_risk = risk
          # Calculating Lots Size
          sizing_Lots = _money_at_risk / (_slPips * 10)
          # Calculate Units
          units_to_trade = sizing_Lots * contract_size
          
          res_dict = dict()
          if risk_type == "%":
            res_dict["Money At Risk ($)"] = [_money_at_risk]
          else:
            res_dict["Risk (%)"] = [(_money_at_risk / _accSize) * 100]
          
          res_dict["Units"] = units_to_trade
          res_dict["Sizing (Lots)"] = sizing_Lots

          res_matrix = pd.DataFrame(res_dict).round(3)
          st.success('   ||   '.join([f"{col}: {val}" for col, val in res_matrix.iloc[0].items()]))
