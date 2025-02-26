import streamlit as st
import datetime
from utils.helpers import format_date
import uuid

# Initialize user email addresses if not exists
if 'user_email_addresses' not in st.session_state:
    st.session_state.user_email_addresses = [
        {"id": str(uuid.uuid4()), "email": "john.doe@example.com", "label": "Personal", "is_default": True},
        {"id": str(uuid.uuid4()), "email": "john.doe@company.com", "label": "Work", "is_default": False}
    ]

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
    if 'llm_instructions' not in st.session_state:
        st.session_state.llm_instructions = """Always mention:
- Previous meeting at Tech Conference
- Interest in AI developments
- Recent product launches at TechCorp
- Shared connection through Product Management community"""
    
    def toggle_email_preview():
        st.session_state.show_email_preview = not st.session_state.show_email_preview
        if st.session_state.show_email_preview:
            st.session_state.generated_email = generate_sample_email()
        st.rerun()
    
    def generate_sample_email():
        return {
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
    
    # Function to handle navigation back to contacts list
    def navigate_to_contacts_list():
        st.session_state.view = 'contacts_list'
        st.rerun()

    # Header with back button, link to contacts, and edit
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        # Make the back arrow button functional by using st.button instead of HTML
        if st.button("←", key="back_arrow"):
            navigate_to_contacts_list()
        st.markdown("<h1 style='margin: 0; display: inline-block; margin-left: 10px;'>Contact Details</h1>", unsafe_allow_html=True)
    
    # Add button to return to contacts list with the SVG icon
    with col2:
        if st.button(
            "Back to Contacts",
            key="back_to_contacts_btn",
            help="Return to the full contacts list view",
            use_container_width=True
        ):
            navigate_to_contacts_list()
    
    with col3:
        st.button("✏️ Edit", use_container_width=True)

    # Main content columns
    left_col, right_col = st.columns([1, 1])

    with left_col:
        # Contact Profile Card
        st.markdown("""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <div style="width: 80px; height: 80px; border-radius: 50%; background-color: #f0f2f6; 
                               display: flex; align-items: center; justify-content: center; font-size: 32px;">
                        👤
                    </div>
                    <div>
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <h2 style="margin: 0;">John Smith</h2>
                        </div>
                        <p style="color: #666; margin: 0.5rem 0;">Product Manager at Tech Corp</p>
                        <div style="display: flex; gap: 1rem; margin-top: 0.5rem;">
                            <button style="background: none; border: 1px solid #ddd; padding: 4px 12px; border-radius: 4px;">
                                ✉️ john@techcorp.com
                            </button>
                            <button style="background: none; border: 1px solid #ddd; padding: 4px 12px; border-radius: 4px;">
                                📞 +1 234 567 890
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # LLM Instructions Button
        if st.button("🎯 LLM Instructions for this contact", key="llm_button", type="secondary"):
            st.session_state.show_llm_dialog = True

        # Show LLM Instructions Dialog
        if st.session_state.show_llm_dialog:
            with st.container():
                st.markdown("### Edit LLM Instructions")
                st.markdown("Customize how the AI should interact with this contact.")
                
                # Text area for instructions
                new_instructions = st.text_area(
                    "",  # Empty label since we have the header above
                    value=st.session_state.llm_instructions,
                    height=200,
                    key="llm_instructions_input",
                    help="These instructions will guide the AI in generating personalized messages for this contact."
                )
                
                # Buttons for actions
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("Cancel", key="cancel_llm_dialog"):
                        st.session_state.show_llm_dialog = False
                        st.rerun()
                with col2:
                    if st.button("Save Changes", key="save_llm_dialog", type="primary"):
                        st.session_state.llm_instructions = new_instructions
                        st.session_state.show_llm_dialog = False
                        st.success("LLM instructions updated successfully!")
                        st.rerun()

        # Categories Card
        st.markdown("""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0;">Categories</h3>
                    <button style="background: none; border: 1px solid #ddd; padding: 4px 12px; border-radius: 4px;">
                        Manage Categories
                    </button>
                </div>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="category-button" style="background-color: #0066cc20; color: #0066cc;">High Value</span>
                    <span class="category-button" style="background-color: #00cc6620; color: #00cc66;">Active Client</span>
                    <span class="category-button" style="background-color: #cc00cc20; color: #cc00cc;">Tech Industry</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Special Dates Card
        st.markdown("""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <h3 style="margin: 0 0 1rem 0;">Special Dates</h3>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="color: #666; margin: 0 0 0.25rem 0;">Birthday</p>
                            <p style="font-weight: bold; margin: 0;">March 15</p>
                        </div>
                        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #0066cc20; 
                                   display: flex; align-items: center; justify-content: center; font-size: 20px;">
                            🎂
                        </div>
                    </div>
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <p style="color: #666; margin: 0 0 0.25rem 0;">Work Anniversary</p>
                            <p style="font-weight: bold; margin: 0;">September 1</p>
                        </div>
                        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #00cc6620; 
                                   display: flex; align-items: center; justify-content: center; font-size: 20px;">
                            🎉
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Outreach Cadence Card
        st.markdown("""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0;">Outreach Cadence</h3>
                    <div style="display: flex; gap: 0.5rem;">
                        <button style="background: none; border: 1px solid #ddd; padding: 4px 12px; border-radius: 4px;">
                            Adjust Cadence
                        </button>
                        <button style="background: #0066cc; color: white; border: none; padding: 4px 12px; border-radius: 4px;">
                            Start Now
                        </button>
                        <button style="background: none; border: 1px solid #0066cc; color: #0066cc; padding: 4px 12px; border-radius: 4px;">
                            Start When
                        </button>
                    </div>
                </div>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                        <div>
                            <p style="color: #666; margin: 0 0 0.25rem 0;">Current Cadence</p>
                            <p style="font-weight: bold; margin: 0;">Monthly</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="color: #666; margin: 0 0 0.25rem 0;">Next Outreach</p>
                            <p style="font-weight: bold; margin: 0;">Mar 15, 2024</p>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <p style="color: #666; margin: 0 0 0.25rem 0;">Last Contact</p>
                            <p style="font-weight: bold; margin: 0;">Feb 15, 2024</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="color: #666; margin: 0 0 0.25rem 0;">Days Until Due</p>
                            <p style="font-weight: bold; margin: 0;">12 days</p>
                        </div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Email Selection Card
        st.markdown("""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0;">Which email do I use with this contact?</h3>
                </div>
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
        """, unsafe_allow_html=True)
        
        # Fixed selectbox with proper label
        st.selectbox(
            label="Email address to use",  # Added proper label
            options=[
                "work@company.com (Work Email)",
                "personal@gmail.com (Personal)",
                "business@freelance.com (Freelance)"
            ],
            index=0,
            key="contact_email_preference",
            help="Select which email address to use when communicating with this contact",
            label_visibility="collapsed"  # This hides the label while keeping it accessible
        )
        
        st.markdown("""
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Topics Card
        st.markdown("""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0;">Topics</h3>
                    <button style="background: none; border: 1px solid #ddd; padding: 4px 12px; border-radius: 4px;">
                        Edit Topics
                    </button>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <div class="draggable-topic" draggable="true" style="background: #f8f9fa; padding: 0.75rem; border-radius: 8px; cursor: move; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="color: #666;">⋮⋮</span>
                        <span class="category-button" style="background-color: #0066cc20; color: #0066cc;">Artificial Intelligence</span>
                    </div>
                    <div class="draggable-topic" draggable="true" style="background: #f8f9fa; padding: 0.75rem; border-radius: 8px; cursor: move; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="color: #666;">⋮⋮</span>
                        <span class="category-button" style="background-color: #00cc6620; color: #00cc66;">Product Management</span>
                    </div>
                    <div class="draggable-topic" draggable="true" style="background: #f8f9fa; padding: 0.75rem; border-radius: 8px; cursor: move; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="color: #666;">⋮⋮</span>
                        <span class="category-button" style="background-color: #cc00cc20; color: #cc00cc;">Tech Conference</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Add Note Input Field (MOVED UP)
        st.markdown("""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
                    <h4 style="margin: 0 0 0.5rem 0;">Add a Note</h4>
                    <textarea style="width: 100%; min-height: 100px; padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 0.5rem;"
                              placeholder="Type your note here..."></textarea>
                    <button style="background: #0066cc; color: white; border: none; padding: 0.5rem 1rem; border-radius: 4px; float: right;">
                        Add Note
                    </button>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Recent Interactions Card (MOVED DOWN)
        st.markdown("""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0;">Recent Interactions</h3>
                    <button style="background: none; border: none; color: #0066cc; cursor: pointer;">
                        View All
                    </button>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Timeline entries
        interactions = [
            {
                "date": "Mar 1, 2024",
                "type": "Email Sent",
                "description": "Discussed upcoming product feature release"
            },
            {
                "date": "Feb 15, 2024",
                "type": "Meeting",
                "description": "Quarterly review and roadmap discussion"
            },
            {
                "date": "Jan 30, 2024",
                "type": "Note Added",
                "description": "Updated contact information and role"
            }
        ]

        for interaction in interactions:
            st.markdown(f"""
                <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                    <div style="min-width: 100px; text-align: left; color: #666;">
                        {interaction['date']}
                    </div>
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; flex: 1;">
                        <p style="font-weight: bold; margin: 0 0 0.25rem 0;">{interaction['type']}</p>
                        <p style="color: #666; margin: 0;">{interaction['description']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with right_col:
        # Content Sources Card
        st.markdown("""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0;">Content Sources</h3>
                    <button style="background: #0066cc; color: white; border: none; padding: 4px 12px; border-radius: 4px;">
                        Add Another
                    </button>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                    <a href="https://techcorp.com/blog" target="_blank" style="text-decoration: none; color: inherit;">
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                            <div style="flex: 1;">
                                <p style="font-weight: bold; margin: 0 0 0.25rem 0;">TechCorp Blog</p>
                                <p style="color: #666; margin: 0; font-size: 0.9rem;">Company blog with product updates</p>
                            </div>
                            <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #0066cc20; 
                                       display: flex; align-items: center; justify-content: center; font-size: 20px;">
                                📰
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Recent Interactions Card
        st.markdown("""
            <div class="metric-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3 style="margin: 0;">Recent Interactions</h3>
                    <button style="background: none; border: none; color: #0066cc; cursor: pointer;">
                        View All
                    </button>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Timeline entries
        interactions = [
            {
                "date": "Mar 1, 2024",
                "type": "Email Sent",
                "description": "Discussed upcoming product feature release"
            },
            {
                "date": "Feb 15, 2024",
                "type": "Meeting",
                "description": "Quarterly review and roadmap discussion"
            },
            {
                "date": "Jan 30, 2024",
                "type": "Note Added",
                "description": "Updated contact information and role"
            }
        ]

        for interaction in interactions:
            st.markdown(f"""
                <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                    <div style="min-width: 100px; text-align: left; color: #666;">
                        {interaction['date']}
                    </div>
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; flex: 1;">
                        <p style="font-weight: bold; margin: 0 0 0.25rem 0;">{interaction['type']}</p>
                        <p style="color: #666; margin: 0;">{interaction['description']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Add some space at the bottom for the fixed buttons
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)

    # Add a simple button at the bottom of the page
    st.markdown("### Quick Actions")
    
    # Create two columns for the buttons
    col1, col2 = st.columns(2)
    
    # Add the Generate Now button
    with col1:
        if st.button("⚡ Generate Now", key="generate_now_btn", use_container_width=True):
            # Generate a sample email and show it
            st.session_state.show_email_preview = True
            st.session_state.generated_email = generate_sample_email()
            st.rerun()
    
    # Add the Internal Hidden button
    with col2:
        if st.button("💬 Internal Hidden", key="internal_hidden_btn", use_container_width=True):
            st.session_state.show_llm_dialog = True
            st.rerun()

    # Show email preview if requested
    if st.session_state.show_email_preview and st.session_state.generated_email:
        # Create a simple modal-like container
        st.markdown("---")
        st.subheader("Generated Email Draft")
        
        # Display the email content
        st.markdown(f"**Subject:** {st.session_state.generated_email['subject']}")
        st.text_area("Email Body", value=st.session_state.generated_email['body'], height=300, disabled=True)
        
        # Add action buttons
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

    # Add styles
    st.markdown("""
        <style>
        /* Button styles */
        button[data-testid="baseButton-secondary"] {
            background-color: white !important;
            color: #0066cc !important;
            border: 1px solid #0066cc !important;
            border-radius: 4px !important;
            padding: 0.5rem 1rem !important;
            cursor: pointer !important;
        }
        
        button[data-testid="baseButton-primary"] {
            background-color: #0066cc !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 0.5rem 1rem !important;
            cursor: pointer !important;
        }
        
        /* Make the sidebar buttons more visible */
        [data-testid="stSidebar"] {
            z-index: 1002;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_contact_details() 