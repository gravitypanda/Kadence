import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.sample_data import generate_sample_categories, generate_sample_contacts
from utils.helpers import format_date, get_contact_categories, generate_mock_email_draft

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="meetkadence",
    page_icon="📬",
    layout="wide"
)

# Initialize session state
if 'categories' not in st.session_state:
    st.session_state.categories = generate_sample_categories()
if 'contacts' not in st.session_state:
    st.session_state.contacts = generate_sample_contacts(st.session_state.categories)
if 'selected' not in st.session_state:
    st.session_state.selected = 'Dashboard'

# Custom CSS
st.markdown("""
    <style>
    /* Clean sidebar styling */
    .css-1d391kg {
        padding-top: 0;
    }
    
    /* Reduce sidebar width */
    section[data-testid="stSidebar"] {
        width: 18rem !important;
    }
    section[data-testid="stSidebar"] > div {
        width: 18rem;
    }
    
    /* Target the exact SVG classes for the X icon */
    .eyeqlp51, 
    .st-emotion-cache-1pbsqtx,
    .ex0cdmw0 {
        display: none !important;
    }
    
    /* Add left arrow to the button containing the SVG */
    .eyeqlp51:parent,
    .st-emotion-cache-1pbsqtx:parent,
    .ex0cdmw0:parent,
    button:has(.eyeqlp51),
    button:has(.st-emotion-cache-1pbsqtx),
    button:has(.ex0cdmw0) {
        position: relative !important;
    }
    
    button:has(.eyeqlp51)::after,
    button:has(.st-emotion-cache-1pbsqtx)::after,
    button:has(.ex0cdmw0)::after {
        content: "←" !important;
        position: absolute !important;
        left: 50% !important;
        top: 50% !important;
        transform: translate(-50%, -50%) !important;
        font-size: 20px !important;
        font-weight: bold !important;
        color: rgb(49, 51, 63) !important;
    }
    
    /* Logo container */
    .logo-container {
        padding: 1rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .logo-container .logo {
        font-size: 2rem;
        line-height: 1;
    }
    .logo-container .title {
        font-size: 1.75rem;
        font-weight: 700;
        margin: 0;
        color: #000000;
        letter-spacing: -0.5px;
        text-transform: lowercase;
    }
    
    /* Button styling */
    .stButton button {
        background-color: transparent;
        border: 1px solid rgba(49, 51, 63, 0.2);
        color: #262730;
    }
    .stButton button:hover {
        border-color: #0066cc;
        color: #0066cc;
    }
    .stButton button[kind="primary"] {
        background-color: #0066cc;
        border-color: #0066cc;
        color: white;
    }
    .stButton button[kind="primary"]:hover {
        background-color: #0052a3;
        border-color: #0052a3;
    }
    
    /* Card styling */
    .metric-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0066cc;
    }
    .metric-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Contact card styling */
    .contact-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        padding: 0.5rem;
    }
    
    .contact-photo {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        object-fit: cover;
    }
    
    .contact-info {
        flex: 1;
    }
    
    /* Accordion styling */
    .st-emotion-cache-eczf69 {
        max-width: 50%;
    }
    
    /* Category button styling */
    .category-button {
        display: inline-block;
        background-color: #f0f2f6;
        border-radius: 16px;
        padding: 4px 12px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-size: 0.8rem;
        color: #0066cc;
        cursor: pointer;
    }
    
    .category-button:hover {
        background-color: #e0e5f0;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        display: flex !important;
        align-items: center !important;
        gap: 1rem !important;
        background-color: white !important;
        border-radius: 8px !important;
        border: 1px solid rgba(49, 51, 63, 0.1) !important;
        padding: 0.75rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Custom contact expander styling */
    .streamlit-expander {
        border: 1px solid rgba(49, 51, 63, 0.1) !important;
        border-radius: 8px !important;
        margin-bottom: 0.75rem !important;
    }
    
    /* Add a subtle hover effect to expanders */
    .streamlit-expander:hover {
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    /* Custom styling for contact expander headers */
    .contact-expander-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .contact-expander-header img {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        object-fit: cover;
    }
    
    /* Hide extra elements */
    section[data-testid="stSidebar"] > div:nth-child(2) {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # Logo and title at the top
    st.markdown("""
        <div class="logo-container">
            <div class="logo">📬</div>
            <h1 class="title">meetkadence</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation menu with icons
    pages = {
        "Dashboard": "📊",
        "Contacts": "👥",
        "Categories": "🏷️",
        "Settings": "⚙️",
        "Help": "❓"
    }
    
    for page, icon in pages.items():
        if st.button(
            f"{icon} {page}",
            key=f"nav_{page.lower()}",
            use_container_width=True,
            type="primary" if st.session_state.selected == page else "secondary"
        ):
            st.session_state.selected = page
            st.experimental_rerun()

# Main content
if st.session_state.selected == "Dashboard":
    # Quick contact search bar (floating)
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.text_input("🔍", placeholder="Search contacts, categories, or jump to settings...", key="global_search")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Header and key metrics in cards
    st.title("Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">%d</div>
                <div class="metric-label">Total Contacts</div>
            </div>
        """ % len(st.session_state.contacts), unsafe_allow_html=True)
    
    with col2:
        due_today = sum(1 for c in st.session_state.contacts if c.next_outreach_date.date() == datetime.now().date())
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">%d</div>
                <div class="metric-label">Due Today</div>
            </div>
        """ % due_today, unsafe_allow_html=True)
    
    with col3:
        due_this_week = sum(1 for c in st.session_state.contacts 
                           if datetime.now().date() <= c.next_outreach_date.date() <= (datetime.now() + timedelta(days=7)).date())
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">%d</div>
                <div class="metric-label">Due This Week</div>
            </div>
        """ % due_this_week, unsafe_allow_html=True)
    
    # Performance insights
    st.markdown("### 📈 Performance Insights")
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">85%</div>
                <div class="metric-label">Monthly Contact Rate</div>
                <small>42 contacts nurtured this month</small>
            </div>
        """, unsafe_allow_html=True)
    
    with insight_col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-value">12</div>
                <div class="metric-label">Avg. Daily Emails</div>
                <small>Based on last 30 days</small>
            </div>
        """, unsafe_allow_html=True)
    
    # Top people to reconnect with
    st.markdown("### 🤝 Top People to Reconnect With")
    
    # Sort contacts by last contact date
    reconnect_contacts = sorted(
        [c for c in st.session_state.contacts if c.last_contact],
        key=lambda x: x.last_contact
    )[:4]  # Increased to 4 contacts
    
    # Create a container with half width
    contacts_container = st.container()
    with contacts_container:
        col1, col2 = st.columns([1, 1])
        with col1:
            for i, contact in enumerate(reconnect_contacts):
                days_since = (datetime.now() - contact.last_contact).days
                
                # Get categories for this contact
                contact_categories = get_contact_categories(contact, st.session_state.categories)
                category_names = [cat.name for cat in contact_categories]
                
                # Image file paths
                image_paths = [
                    "people/markuphero-oqWsu5Aw4vg5Y9AdLllk.png",
                    "people/markuphero-WNR37VJCmiTHJrp5EJc1.png", 
                    "people/markuphero-3NyeNbNRmpuUZMf8vHQc.png", 
                    "people/markuphero-CShNdWhd3qXvCHQWGvMR.png"
                ]
                
                # Create a row for the contact with columns
                contact_row = st.container()
                with contact_row:
                    # Create a custom header with image for the expander
                    expander_header = f"""
                    <div class="contact-expander-header">
                        <img src="{image_paths[i]}" alt="{contact.name}">
                        <div>
                            <strong>{contact.name}</strong> - {days_since} days since last contact
                        </div>
                    </div>
                    """
                    
                    # Use the expander with custom header
                    with st.expander(expander_header, expanded=False):
                        # Contact details in the expanded view - with a single image
                        st.markdown(f"""
                            <div style="display: flex; align-items: flex-start; gap: 1rem; margin-bottom: 1rem;">
                                <div style="flex: 0 0 100px;">
                                    <img src="{image_paths[i]}" width="100" style="border-radius: 50%;">
                                </div>
                                <div style="flex: 1;">
                                    <h3 style="margin-top: 0;">{contact.name}</h3>
                                    <p><strong>{days_since} days</strong> since last contact</p>
                                    <p><strong>Email:</strong> {contact.email}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Categories as buttons
                        st.markdown("#### Categories")
                        category_html = ""
                        for cat_name in category_names:
                            category_html += f'<span class="category-button">{cat_name}</span>'
                        
                        st.markdown(f"""
                            <div style="margin-bottom: 1rem;">
                                {category_html}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Replace columns with HTML buttons
                        st.markdown(f"""
                            <div style="display: flex; gap: 0.5rem; margin-bottom: 1rem;">
                                <button style="flex: 1; background-color: #0066cc; color: white; border: none; padding: 0.5rem; border-radius: 4px; cursor: pointer;">
                                    Generate Draft
                                </button>
                                <button style="flex: 1; background-color: #f0f2f6; color: #0066cc; border: 1px solid #0066cc; padding: 0.5rem; border-radius: 4px; cursor: pointer;">
                                    View Profile
                                </button>
                            </div>
                        """, unsafe_allow_html=True)
    
    # Email management tabs
    st.markdown("### 📧 Email Management")
    tab1, tab2 = st.tabs(["📥 Upcoming", "📤 History"])
    
    with tab1:
        contacts_data = []
        for contact in sorted(st.session_state.contacts, key=lambda x: x.next_outreach_date):
            if contact.next_outreach_date.date() >= datetime.now().date():
                categories = get_contact_categories(contact, st.session_state.categories)
                category_names = [cat.name for cat in categories]
                contacts_data.append({
                    "Due Date": contact.next_outreach_date.date(),
                    "Name": contact.name,
                    "Email": contact.email,
                    "Categories": ", ".join(category_names)
                })
        
        if contacts_data:
            df = pd.DataFrame(contacts_data)
            st.dataframe(
                df,
                column_config={
                    "Due Date": st.column_config.DateColumn("Due Date"),
                    "Name": st.column_config.TextColumn("Name"),
                    "Email": st.column_config.TextColumn("Email"),
                    "Categories": st.column_config.TextColumn("Categories")
                },
                hide_index=True
            )
        else:
            st.info("No upcoming emails scheduled")
    
    with tab2:
        history_data = []
        for contact in st.session_state.contacts:
            if contact.last_contact:
                categories = get_contact_categories(contact, st.session_state.categories)
                category_names = [cat.name for cat in categories]
                history_data.append({
                    "Sent Date": contact.last_contact.date(),
                    "Name": contact.name,
                    "Email": contact.email,
                    "Categories": ", ".join(category_names),
                    "Status": "Sent ✓"
                })
        
        if history_data:
            df = pd.DataFrame(history_data)
            df = df.sort_values("Sent Date", ascending=False)
            st.dataframe(
                df,
                column_config={
                    "Sent Date": st.column_config.DateColumn("Sent Date"),
                    "Name": st.column_config.TextColumn("Name"),
                    "Email": st.column_config.TextColumn("Email"),
                    "Categories": st.column_config.TextColumn("Categories"),
                    "Status": st.column_config.TextColumn("Status", width="small")
                },
                hide_index=True
            )
        else:
            st.info("No email history available yet")

elif st.session_state.selected == "👥 Contacts":
    st.title("👥 Contacts")
    st.info("This section will allow you to manage your contacts")
    # Contacts management UI will be implemented in pages/contacts.py

elif st.session_state.selected == "🏷️ Categories":
    st.title("🏷️ Categories")
    st.info("This section will allow you to manage your categories")
    # Categories UI will be implemented in pages/categories.py

elif st.session_state.selected == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.info("This section will allow you to configure your system settings")
    # Settings UI will be implemented in pages/settings.py

elif st.session_state.selected == "Help":
    st.title("❓ Help")
    st.markdown("""
    ### Getting Started
    meetkadence helps you maintain meaningful relationships through consistent, personalized communication.
    
    ### Key Features
    - **Dashboard**: Overview of your contacts and upcoming communications
    - **Contacts**: Manage your network and set communication preferences
    - **Categories**: Organize contacts and set custom communication rules
    - **Settings**: Configure your email and system preferences
    
    ### Need Support?
    Visit our [documentation](https://docs.meetkadence.com) or [contact support](mailto:support@meetkadence.com)
    """) 