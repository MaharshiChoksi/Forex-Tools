import streamlit as st
import base64
from pathlib import Path
import pandas as pd
from utils.pairs_quote_fetcher import fetch_quotes

from tabs.margin_calc import show_margin
from tabs.pos_size_calc import show_posSize
from tabs.pnl_calc import show_pnl
from tabs.pip_value_calc import show_pipValue

st.set_page_config(page_title="Forex Tools", layout="wide")


# --- helper to embed local background image as data-uri ---
def _get_base64_of_bin_file(bin_file_path: Path) -> str:
    with open(bin_file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(local_img_path: Path):
    if not local_img_path.exists():
        return
    img_b64 = _get_base64_of_bin_file(local_img_path)
    css = f"""
    <style>
    .stApp {{
      background-image: url("data:image/jpg;base64,{img_b64}");
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
    }}
    .content-block {{
      background: rgba(255,255,255,0.85);
      padding: 18px;
      border-radius: 8px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# place a background image at: assets/background.jpg (project root)
assets_bg = Path(__file__).parents[0] / "assets" / "background.jpg"
set_background(assets_bg)

# Create a placeholder for tabs
tab_placeholder = st.empty()

data = pd.DataFrame()
with st.spinner("Fetching Pairs and Quotes..."):
    try:
        data = fetch_quotes()

    # if(data.isnull().all().any() or data is None or data.empty):
        with tab_placeholder.container():
            tab_names = ["Margin Calculator", "Position Size Calculator", "PNL Calculator", "Pip Value Calculator"]

        # Use radio for persistent tab selection
        if "selected_tab" not in st.session_state:
            st.session_state.selected_tab = tab_names[0]
        
        selected_tab = st.radio("Go to Calculator:", tab_names, index=tab_names.index(st.session_state.selected_tab))
        if selected_tab == "Margin Calculator":
            show_margin(data)
        elif selected_tab == "Position Size Calculator":
            show_posSize(data)
        elif selected_tab == "PNL Calculator":
            show_pnl(data)
        elif selected_tab == "Pip Value Calculator":
            show_pipValue(data)
    except Exception as e:
        tab_placeholder.error(f"!!! Error while fetching Quotes !!!: {data}")

