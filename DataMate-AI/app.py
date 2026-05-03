import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Vinayak AI", layout="wide", initial_sidebar_state="collapsed")

# Hide all Streamlit chrome
st.markdown("""
<style>
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# Read and render the chatbot HTML
# AI responses are handled via api_server.py (FastAPI at localhost:8000)
with open("chatbot_ui.html", "r", encoding="utf-8") as f:
    html = f.read()

components.html(html, height=900, scrolling=False)
