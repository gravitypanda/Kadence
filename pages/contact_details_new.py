import streamlit as st
import datetime
from utils.helpers import format_date
import uuid

# Initialize session state for email preview
if 'show_email_preview' not in st.session_state:
    st.session_state.show_email_preview = False
if 'generated_email' not in st.session_state:
    st.session_state.generated_email = None

def show_contact_details(contact_id=None):
    # Initialize session state for navigation
    if 'view' not in st.session_state:
        st.session_state.view = 'contact_details'
    
    # Initialize session state for LLM instructions
    if 'show_llm_dialog' not in st.session_state:
        st.session_state.show_llm_dialog = False
    
    # Header
    st.title("Contact Details")
    
    # Main content in two columns
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        # Contact info
        st.subheader("John Smith")
        st.write("Product Manager at Tech Corp")
        st.write("📧 john@techcorp.com")
        st.write("📱 +1 234 567 890")
        
        # Categories
        st.subheader("Categories")
        st.write("High Value, Active Client, Tech Industry")
        
        # Special dates
        st.subheader("Special Dates")
        st.write("🎂 Birthday: March 15")
        st.write("🎉 Work Anniversary: September 1")
    
    with right_col:
        # Outreach info
        st.subheader("Outreach Information")
        st.write("Cadence: Monthly")
        st.write("Next Outreach: Mar 15, 2024")
        st.write("Last Contact: Feb 15, 2024")
        
        # Content sources
        st.subheader("Content Sources")
        st.write("TechCorp Blog - Company blog with product updates")
    
    # Generate Now button
    st.subheader("Quick Actions")
    
    if st.button("⚡ Generate Now", key="generate_now_btn"):
        # When button is clicked, show email preview
        if 'generated_email' not in st.session_state or st.session_state.generated_email is None:
            # Generate a sample email
            st.session_state.generated_email = {
                "subject": "Following up on our Tech Conference discussion",
                "body": """Hi John,

I hope this email finds you well! I've been thinking about our conversation at the Tech Conference last month about AI developments in product management.

I noticed TechCorp's recent announcement about your new AI-powered feature suite – congratulations on the launch! The integration approach you've taken aligns perfectly with what we discussed regarding user-centric AI implementation.

I'd love to hear more about how the launch has been received and share some insights from our recent AI initiatives as well. Perhaps we could schedule a quick catch-up call next week?

Also, I saw your post in the Product Management community about agile transformation. Your perspective on balancing innovation with stability really resonated with our current challenges.

Looking forward to connecting!

Best regards,
[Your name]

P.S. Are you planning to attend next month's PM Summit? It would be great to continue our discussion on AI ethics in person."""
            }
        
        st.session_state.show_email_preview = True
        st.rerun()
    
    # Show email preview if requested
    if st.session_state.show_email_preview and st.session_state.generated_email:
        # Create a container for the email preview
        with st.container():
            st.subheader("Generated Email Draft")
            
            # Display the email content
            st.markdown(f"**Subject:** {st.session_state.generated_email['subject']}")
            st.text_area("Email Body", value=st.session_state.generated_email['body'], height=300, disabled=True)
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Close", key="close_email_modal"):
                    st.session_state.show_email_preview = False
                    st.rerun()
            with col2:
                if st.button("Send to Inbox", key="send_to_inbox"):
                    st.success("Draft sent to your inbox!")
                    st.session_state.show_email_preview = False
                    st.rerun()

if __name__ == "__main__":
    show_contact_details() 