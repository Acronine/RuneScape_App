import streamlit as st

from runescape_query_engine import RuneScapeEngine

st.set_page_config(
    page_title="RuneScape",
    page_icon="⚔"
    )
c = RuneScapeEngine()

st.title("RuneScape App")
# c.autoplay_audio(r'Background(1).ogg')