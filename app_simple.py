import streamlit as st
from pages.contact_details_new import show_contact_details

# Set page config
st.set_page_config(
    page_title="meetkadence",
    page_icon="📬",
    layout="wide"
)

# Show the contact details page
show_contact_details() 