import streamlit as st
from models.schemas import SystemSettings

# Initialize system settings in session state if not exists
if 'system_settings' not in st.session_state:
    st.session_state.system_settings = SystemSettings()

st.title("⚙️ Settings")

# System Settings Form
with st.form("settings_form"):
    st.subheader("Email Settings")
    user_email = st.text_input(
        "Your Email Address",
        value=st.session_state.system_settings.user_email or "",
        help="The email address where you'll receive AI-generated drafts"
    )
    
    bcc_email = st.text_input(
        "BCC Email Address",
        value=st.session_state.system_settings.bcc_email or "",
        help="The email address to BCC for logging sent emails (usually your meetkadence address)"
    )
    
    st.subheader("AI Settings")
    system_prompt = st.text_area(
        "System-wide AI Instructions",
        value=st.session_state.system_settings.system_prompt,
        help="These instructions will apply to all AI-generated messages",
        height=150
    )
    
    # Save settings
    if st.form_submit_button("Save Settings"):
        st.session_state.system_settings = SystemSettings(
            user_email=user_email if user_email else None,
            bcc_email=bcc_email if bcc_email else None,
            system_prompt=system_prompt
        )
        st.success("Settings saved successfully!")

# Display current settings
st.subheader("Current Configuration")
with st.expander("View Current Settings"):
    st.json({
        "user_email": st.session_state.system_settings.user_email,
        "bcc_email": st.session_state.system_settings.bcc_email,
        "system_prompt": st.session_state.system_settings.system_prompt
    })

# Export/Import Settings (placeholder for future functionality)
st.subheader("Backup & Restore")
col1, col2 = st.columns(2)

with col1:
    st.download_button(
        "Export Settings",
        "This feature will be implemented soon",
        disabled=True
    )

with col2:
    st.file_uploader(
        "Import Settings",
        type=["json"],
        disabled=True,
        help="This feature will be implemented soon"
    )

# Additional Settings Sections (placeholders for future functionality)
st.subheader("Advanced Settings")

# Email Integration
with st.expander("Email Integration"):
    st.info("Email integration settings will be available in a future update")
    st.checkbox("Enable email notifications", value=True, disabled=True)
    st.checkbox("Send read receipts", value=False, disabled=True)

# AI Configuration
with st.expander("AI Configuration"):
    st.info("Advanced AI settings will be available in a future update")
    st.slider("Response creativity", min_value=0.0, max_value=1.0, value=0.7, disabled=True)
    st.checkbox("Use GPT-4", value=True, disabled=True)

# Data Management
with st.expander("Data Management"):
    st.info("Data management features will be available in a future update")
    st.button("Export All Data", disabled=True)
    st.button("Clear All Data", disabled=True)

# API Keys
with st.expander("API Keys"):
    st.info("API key management will be available in a future update")
    st.text_input("OpenAI API Key", type="password", disabled=True)
    st.text_input("Email Service API Key", type="password", disabled=True) 