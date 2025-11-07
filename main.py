import streamlit as st
import base64
from pathlib import Path
from utils.pairs_quote_fetcher import fetch_quotes

from pages.margin_calc import show_margin
from pages.pos_size_calc import show_posSize
from pages.pnl_calc import show_pnl
from pages.pip_size_calc import show_pipSize
from pages.pip_value_calc import show_pipValue

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

with st.spinner("Fetching Pairs and Quotes..."):
   data = fetch_quotes()

# Initialize session state to track the selected page
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Margin Calculator"  # Default pag

st.sidebar.title("Tools")

# Sidebar buttons for navigation
if st.sidebar.button("Margin Calculator"):
    st.session_state.selected_page = "Margin Calculator"
if st.sidebar.button("Position Size Calculator"):
    st.session_state.selected_page = "Position Size Calculator"
if st.sidebar.button("PNL Calculator"):
    st.session_state.selected_page = "PNL Calculator"
if st.sidebar.button("Pip Size Calculator"):
    st.session_state.selected_page = "Pip Size Calculator"
if st.sidebar.button("Pip Value Calculator"):
    st.session_state.selected_page = "Pip Value Calculator"

# Display the selected page
if st.session_state.selected_page == "Margin Calculator":
    show_margin()
elif st.session_state.selected_page == "Position Size Calculator":
    show_posSize()
elif st.session_state.selected_page == "PNL Calculator":
    show_pnl()
elif st.session_state.selected_page == "Pip Size Calculator":
    show_pipSize()
elif st.session_state.selected_page == "Pip Value Calculator":
    show_pipValue()