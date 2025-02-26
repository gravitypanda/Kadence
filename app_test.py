import streamlit as st
from pages.analytics import show_analytics

# Set page config
st.set_page_config(
    page_title="meetkadence",
    page_icon="📬",
    layout="wide"
)

# Show the analytics page
show_analytics() 