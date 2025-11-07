import base64
from pathlib import Path
import streamlit as st

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
assets_bg = Path(__file__) / "assets" / "background.jpg"
set_background(assets_bg)

# --- Navigation: Margin Calc, Possize,  PNL Calc, Pip Size, Pip Value ---
tab_margin, tab_pos_size, tab_Pnl, tab_pip_size, tab_pip_value = st.tabs(["Margin Calculator", "Position Size Calculator", " PNL Calculator", "Pip Size Calculator", "Pip Value Calculator"])

with tab_margin:
  st.title("Forex Margin Calculator")


with tab_pos_size:
  st.title("Forex Position Size Calculator")


with tab_Pnl:
  st.title("Forex P&L Calculator")


with tab_pip_size:
  st.title("Pip Size Calculator")


with tab_pip_value:
  st.title("Pip Value Calculator")
