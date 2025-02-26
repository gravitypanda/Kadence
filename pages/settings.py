import streamlit as st
from models.schemas import SystemSettings
import uuid

# Initialize system settings in session state if not exists
if 'system_settings' not in st.session_state:
    st.session_state.system_settings = SystemSettings()

# Initialize user email addresses if not exists
if 'user_email_addresses' not in st.session_state:
    st.session_state.user_email_addresses = [
        {"id": str(uuid.uuid4()), "email": "john.doe@example.com", "label": "Personal", "is_default": True},
        {"id": str(uuid.uuid4()), "email": "john.doe@company.com", "label": "Work", "is_default": False}
    ]

def show_settings():
    st.title("⚙️ Settings")
    
    # Create tabs for different settings sections
    tab1, tab2, tab3, tab4 = st.tabs(["Account", "My Email Addresses", "Email Settings", "System Prompts"])
    
    with tab1:
        st.header("Account Settings")
        
        # User information section
        with st.container():
            st.subheader("User Information")
            col1, col2 = st.columns(2)
            
            with col1:
                current_name = "John Doe"  # In a real app, this would come from user data
                new_name = st.text_input("Name", value=current_name)
                
                # Get default email from user_email_addresses
                default_email = next((email["email"] for email in st.session_state.user_email_addresses if email["is_default"]), "")
                st.text_input("Default Email", value=default_email, disabled=True, 
                              help="This is your default email. You can change it in the 'My Email Addresses' tab.")
            
            with col2:
                st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
        
        # Save button for account settings
        if st.button("Save Account Changes"):
            # Validate password match
            if new_password and new_password != confirm_password:
                st.error("New passwords do not match!")
            else:
                # Update the system settings
                st.success("Account information updated successfully!")
                
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
    
    with tab2:
        st.header("My Email Addresses")
        
        st.write("Manage the different email addresses you use in various contexts. Set one as your default.")
        
        # Display existing email addresses
        for i, email_data in enumerate(st.session_state.user_email_addresses):
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    new_email = st.text_input("Email Address", value=email_data["email"], key=f"email_{i}")
                
                with col2:
                    new_label = st.text_input("Label", value=email_data["label"], key=f"label_{i}", 
                                             help="E.g., Work, Personal, Business")
                
                with col3:
                    is_default = st.checkbox("Default", value=email_data["is_default"], key=f"default_{i}")
                
                with col4:
                    if st.button("Remove", key=f"remove_{i}"):
                        # Don't allow removing the last email address
                        if len(st.session_state.user_email_addresses) > 1:
                            st.session_state.user_email_addresses.pop(i)
                            st.rerun()
                        else:
                            st.error("You must have at least one email address.")
                
                # Update the email data
                email_data["email"] = new_email
                email_data["label"] = new_label
                
                # Handle default email logic
                if is_default and not email_data["is_default"]:
                    # Unset any other default emails
                    for other_email in st.session_state.user_email_addresses:
                        other_email["is_default"] = False
                    email_data["is_default"] = True
                elif not is_default and email_data["is_default"]:
                    # Don't allow unsetting the default if it's the only default
                    if sum(1 for e in st.session_state.user_email_addresses if e["is_default"]) <= 1:
                        st.warning("You must have at least one default email address.")
                        email_data["is_default"] = True
                    else:
                        email_data["is_default"] = False
            
            st.divider()
        
        # Add new email address
        if st.button("+ Add Another Email Address"):
            st.session_state.user_email_addresses.append({
                "id": str(uuid.uuid4()),
                "email": "",
                "label": "",
                "is_default": False
            })
            st.rerun()
        
        # Save button for email addresses
        if st.button("Save Email Addresses"):
            # Ensure at least one email is set as default
            if not any(email["is_default"] for email in st.session_state.user_email_addresses):
                # Set the first email as default if none is selected
                st.session_state.user_email_addresses[0]["is_default"] = True
                
            # Update the system settings with the default email
            default_email = next((email["email"] for email in st.session_state.user_email_addresses if email["is_default"]), "")
            st.session_state.system_settings.user_email = default_email
            
            st.success("Email addresses updated successfully!")
    
    with tab3:
        st.header("Email Settings")
        
        # Email preferences
        with st.container():
            st.subheader("Email Preferences")
            
            bcc_email = st.text_input(
                "BCC Email Address",
                value=st.session_state.system_settings.bcc_email or "",
                help="The email address to BCC for logging sent emails (usually your meetkadence address)"
            )
            
            st.checkbox("Send me email notifications for new contacts", value=True)
            st.checkbox("Send me weekly activity summaries", value=True)
            st.checkbox("Send me tips and best practices", value=False)
            
            st.subheader("Email Signature")
            default_signature = """
            Best regards,
            John Doe
            CEO | Kadence
            john.doe@example.com
            (555) 123-4567
            """
            signature = st.text_area("Email Signature", value=default_signature, height=150)
        
        # Save button for email settings
        if st.button("Save Email Settings"):
            # Update the system settings
            st.session_state.system_settings.bcc_email = bcc_email if bcc_email else None
            st.success("Email settings updated successfully!")
    
    with tab4:
        st.header("System Prompts")
        
        # System prompt for email generation
        with st.container():
            st.subheader("Email Generation Prompt")
            
            default_prompt = """
            You are an AI assistant that helps me nurture my professional and personal relationships.
            
            When generating emails:
            1. Use a tone appropriate for the relationship category (professional, personal, etc.)
            2. Reference previous interactions and shared experiences when available
            3. Include relevant, timely topics based on the recipient's interests and our relationship
            4. Keep messages concise but meaningful
            5. End with a clear next step or question to encourage response
            6. Maintain authenticity - the email should sound like it's coming from me
            
            The goal is to maintain and strengthen relationships through consistent, thoughtful communication.
            """
            
            system_prompt = st.text_area(
                "System-wide AI Instructions",
                value=st.session_state.system_settings.system_prompt or default_prompt,
                help="These instructions will apply to all AI-generated messages",
                height=300
            )
            
            st.info("This prompt guides the AI when generating emails to your contacts. Customize it to match your communication style and relationship goals.")
        
        # Save button for system prompts
        if st.button("Save System Prompts"):
            # Update the system settings
            st.session_state.system_settings.system_prompt = system_prompt
            st.success("System prompts updated successfully!")
    
    # App information at the bottom
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("Kadence v1.0.0")
    with col2:
        st.caption("© 2023 Kadence")
    with col3:
        st.caption("[Privacy Policy](https://example.com) | [Terms of Service](https://example.com)")

# This allows the page to be run directly for testing
if __name__ == "__main__":
    show_settings() 