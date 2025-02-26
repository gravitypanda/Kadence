import streamlit as st
st.set_page_config(
    page_title="meetkadence",
    page_icon="📬",
    layout="wide"
)

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from utils.sample_data import generate_sample_categories, generate_sample_contacts
from utils.helpers import format_date, get_contact_categories, generate_mock_email_draft
from faker import Faker

from pages.contact_details import show_contact_details
from pages.categories import show_categories
from pages.category_edit import show_category_edit
from pages.calendar import show_calendar
from pages.analytics import show_analytics

# Define base64 encoded image for fallback
fallback_image_b64 = """
iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAADWUlEQVR4nO2ZTUhUURTH/8/SNB2baVqoWJug5kerXARFH6uIwGgRQdHXqk0fEFhEC6FFRCZYtChaZUQFbvpYVLQoaBG0KAyKiKgwrYwep3vkPZlmZnw+38ybN8M8+G/ee+/c87/n3HPPPXeIDTbYoDoQqcSJp3Y+QLcBtACoBdCV9I8AeAvgGYAnRPy5KgihspHYnU0ArgAIAZgbQ/sFgE4Ad4n4UyUYoLxGOEjsPA/gOoCtRU77AuAygC4i/lFOJspnhKXEvgDQC2BLktg/AO8BvJL0LFmVLQA2AFgKYB2AdWlzvgdwlIgflctMeYzEQ3UGD9XptMd9AO4T8UsFc60FcBjAybQHkQF0xMN2vxQ75THCKaVJQ/UV0lYiPmDj+msAXALgS+pOAGgh4rGir1fGUL0Ud1/TPSJuL4UJGc9PxHcBdGiaZgCdsulXGiOXtXKewBkiZluLInFnA9iZdBHgAoCLxXDk6YlwyrkN4JjWfZWI75V6ITUe50OPRbfbU7szETvtALq17pNE/NzJQgBeAniqtZ0qBatrIxxvNwOYozUfciPxMZEj4m4AB7QxwTgfjuKoFmQrm11HQ3UTgDta0zUinsiHbEmYiO+lMbsAQJsnjrg2DaW0iVvLcfLQVYZK2LPqgHbdZGfGMiPPU8W4iBct22CnUwVzU9ppNMxNpdEaSh9JaeQ6V+7Mw1VjpM7l60zn0hjZleV6LQmXbZgTHpVoYa78Xa5hxxzw2MLVN5Lqwrch9V6Y9OBIIWPXGkl1nC8AXnv0JgSvZewKI3FO3AXgpkePbgLYLWPnw43QO5vqvxDpvY13zgxvI78BHAHQTsQflZOLRJfBsRvKSHxHMoDnAHYAaCfi/pSOE0UVx3PcDIBlI4zGPfwigF1EPKzNvQvAAwANZdxVf46H9XRsT9+n+GZVfW3fEsCIMDGe9hKxN8PcXSpTZWCin4gPZRrEyxPJHSZOEjuXKYeQsa4BOKEKowVSGcwh4gdE3ABAPZlM+Wce6j4T8XEidiWo1ZmxVx3iRLwXgCK+L+n/DuANET8tNrUva0WxKijKrRUAuwEEATQq8aS+LqnvGIB+AD1E/Lhs/2ywwQZVhf+ZGRB+UN3BWAAAAABJRU5ErkJggg==
"""

# Initialize session state
if 'categories' not in st.session_state:
    st.session_state.categories = generate_sample_categories()
if 'contacts' not in st.session_state:
    st.session_state.contacts = generate_sample_contacts(st.session_state.categories)
if 'selected' not in st.session_state:
    st.session_state.selected = 'Dashboard'
if 'trigger_rerun' not in st.session_state:
    st.session_state.trigger_rerun = False
if 'selected_contact_id' not in st.session_state:
    st.session_state.selected_contact_id = None

# Initialize session state for contact details
if 'viewing_contact_id' not in st.session_state:
    st.session_state.viewing_contact_id = None

# Add a callback component to handle button clicks
from streamlit.components.v1 import html

def button_callback():
    # Only register the callback if not already done
    if 'callback_registered' not in st.session_state:
        components_js = """
        <script>
        // Function to capture button clicks
        function handleButtonClick(button) {
            // Get the contact ID from the button's data attribute
            const contactId = button.getAttribute('data-contact-id');
            // Update the session state via componentValue
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: contactId
            }, '*');
        }
        
        // Add the click handler to all email buttons
        window.addEventListener('load', function() {
            // Add a mutation observer to catch dynamically added buttons
            const observer = new MutationObserver(function(mutations) {
                document.querySelectorAll('[data-contact-id]').forEach(function(button) {
                    button.onclick = function() {
                        handleButtonClick(this);
                    };
                });
            });
            
            observer.observe(document.body, { 
                childList: true,
                subtree: true
            });
        });
        </script>
        """
        
        # Use the html component without a key parameter
        component_value = html(components_js, height=0)
        st.session_state.callback_registered = True
        
        # Update the session state if we received a value from the component
        if component_value:
            st.session_state.selected_contact_id = component_value
            st.rerun()
        
    return st.session_state.selected_contact_id

# Initialize callback registration state
if 'callback_registered' not in st.session_state:
    st.session_state.callback_registered = False

# Call the callback function to register the component
button_callback()

# Custom CSS
st.markdown("""
    <style>
    /* Hide unwanted navigation elements */
    .st-emotion-cache-nziaof,
    .st-emotion-cache-17lntkn,
    section[data-testid="stSidebar"] > div:nth-child(2) {
        display: none !important;
    }
    
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
        height: 220px;
        position: relative;
    }
    
    .contact-photo {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f0f2f6;
        font-size: 24px;
    }
    
    .contact-info {
        flex: 1;
        overflow: hidden;
    }
    
    .contact-categories {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        max-height: 50px;
        overflow-y: auto;
        padding-right: 4px;
    }
    
    .contact-email {
        font-size: 0.8rem;
        color: #444;
        margin: 0.5rem 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .contact-actions {
        display: flex;
        justify-content: space-between;
        position: absolute;
        bottom: 0.8rem;
        left: 1rem;
        right: 1rem;
    }
    
    .contact-actions button {
        background: none;
        border: none;
        cursor: pointer;
        color: #0066cc;
        font-size: 0.85rem;
        padding: 4px 8px;
    }
    
    .contact-actions .action-buttons {
        display: flex;
        gap: 0.5rem;
    }
    
    /* Accordion styling */
    .st-emotion-cache-eczf69 {
        max-width: 50%;
    }
    
    /* Category button styling */
    .category-button {
        display: inline-block;
        padding: 2px 8px;
        background-color: rgba(49, 51, 63, 0.1);
        border-radius: 12px;
        margin: 2px;
        font-size: 0.75rem;
        white-space: nowrap;
    }
    
    /* Hover effect for buttons */
    button:hover {
        opacity: 0.8;
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
        overflow: visible !important;
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
    
    /* Additional style for contact expander headers */
    .contact-expander-header div {
        flex: 1;
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
        "Calendar": "📅",
        "Analytics": "📈",
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
            st.rerun()

# Main content
if st.session_state.selected == "Dashboard":
    # Quick contact search bar (floating)
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    st.text_input("🔍", placeholder="Search contacts, categories, or jump to settings...", key="global_search")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Header and key metrics in cards
    st.title("Dashboard")
    
    # Create main layout for dashboard: two columns
    dash_left, dash_right = st.columns(2)
    
    # Create a two-column layout for the contacts section
    with dash_left:
        # Top people to reconnect with
        st.markdown("### 🤝 Top People to Reconnect With")
        
        # Sort contacts by last contact date
        reconnect_contacts = sorted(
            [c for c in st.session_state.contacts if c.last_contact],
            key=lambda x: x.last_contact
        )[:4]  # Show 4 contacts
        
        # Create a container for contacts
        contacts_container = st.container()
        with contacts_container:
            for i, contact in enumerate(reconnect_contacts):
                days_since = (datetime.now() - contact.last_contact).days
                
                # Get categories for this contact
                contact_categories = get_contact_categories(contact, st.session_state.categories)
                category_names = [cat.name for cat in contact_categories]
                
                # Create the contact card
                with st.container():
                    # Image file paths
                    image_paths = [
                        "people/markuphero-oqWsu5Aw4vg5Y9AdLllk.png",
                        "people/markuphero-WNR37VJCmiTHJrp5EJc1.png", 
                        "people/markuphero-3NyeNbNRmpuUZMf8vHQc.png", 
                        "people/markuphero-CShNdWhd3qXvCHQWGvMR.png"
                    ]
                    
                    # Use the standard expander with a text header
                    with st.expander(f"{contact.name} - {days_since} days since last contact"):
                        # Contact details in expanded view with image
                        col1, col2 = st.columns([0.15, 0.85])
                        
                        with col1:
                            # Use the actual image
                            st.image(image_paths[i % len(image_paths)], width=60)
                        
                        with col2:
                            st.write(f"### {contact.name}")
                            st.write(f"**{days_since} days** since last contact")
                            st.write(f"**Email:** {contact.email}")
                        
                        # Categories
                        st.write("**Categories:**")
                        for category in contact_categories:
                            st.markdown(f'<span class="category-button">{category.name}</span>', unsafe_allow_html=True)
                        
                        # Add some spacing before buttons
                        st.write("")
                        
                        # Use columns for buttons
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            st.button("Generate Draft", key=f"reconnect_draft_{contact.id}", type="primary", use_container_width=True)
                        with btn_col2:
                            st.button("View Profile", key=f"reconnect_profile_{contact.id}", use_container_width=True)
                
                st.write("")  # Add spacing between contacts
    
        # Email management tabs
        st.markdown("### 📧 Email Management")
        
        tab1, tab2 = st.tabs(["📥 Upcoming", "📤 History"])
        
        with tab1:
            # Initialize session state for LLM prompt dialog
            if 'show_dialog' not in st.session_state:
                st.session_state.show_dialog = False
            if 'dialog_contact' not in st.session_state:
                st.session_state.dialog_contact = None
            
            contacts_data = []
            for contact in sorted(st.session_state.contacts, key=lambda x: x.next_outreach_date):
                if contact.next_outreach_date.date() >= datetime.now().date():
                    categories = get_contact_categories(contact, st.session_state.categories)
                    category_names = [cat.name for cat in categories]
                    contacts_data.append({
                        "Due Date": contact.next_outreach_date.date(),
                        "Name": contact.name,
                        "Email": contact.email,
                        "Categories": ", ".join(category_names),
                        "Action": "✍️ Write Draft",  # Display text
                        "id": contact.id  # Keep track of the ID
                    })
            
            if contacts_data:
                # Create DataFrame without the ID column
                df = pd.DataFrame(contacts_data).drop(columns=['id'])
                
                # Display the dataframe with standard columns
                st.dataframe(
                    df,
                    column_config={
                        "Due Date": st.column_config.DateColumn("Due Date"),
                        "Name": st.column_config.TextColumn("Name"),
                        "Email": st.column_config.TextColumn("Email"),
                        "Categories": st.column_config.TextColumn("Categories"),
                        "Action": st.column_config.TextColumn(
                            "Action",
                            help="Click button below to write a draft email",
                            width="small",
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )
                
                # Add buttons below the table for each contact
                cols = st.columns(4)  # Create 4 columns for buttons
                for i, contact in enumerate(contacts_data):
                    with cols[i % 4]:
                        if st.button(f"Write Draft for {contact['Name']}", key=f"upcoming_draft_{i}_{contact['id']}", type="primary"):
                            st.session_state.selected_contact_id = contact['id']
                            st.session_state.dialog_contact = next((c for c in st.session_state.contacts if c.id == contact['id']), None)
                            st.session_state.show_dialog = True
                            st.rerun()
            else:
                st.info("No upcoming emails scheduled")
            
            # Handle dialog display
            if st.session_state.show_dialog and st.session_state.dialog_contact:
                contact = st.session_state.dialog_contact
                
                with st.container():
                    st.markdown("""
                    <style>
                    .email-dialog {
                        background-color: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                        margin: 20px 0;
                    }
                    </style>
                    <div class="email-dialog">
                    """, unsafe_allow_html=True)
                    
                    st.subheader(f"Email Prompt for {contact.name}")
                    st.caption("This prompt will be sent to the LLM to generate an email")
                    
                    # Get categories
                    categories = get_contact_categories(contact, st.session_state.categories)
                    category_names = [cat.name for cat in categories]
                    
                    # Mock data
                    system_prompt = """You are an AI assistant that helps me nurture my professional and personal relationships.
                        
When generating emails:
1. Use a tone appropriate for the relationship category (professional, personal, etc.)
2. Reference previous interactions and shared experiences when available
3. Include relevant, timely topics based on the recipient's interests and our relationship
4. Keep messages concise but meaningful
5. End with a clear next step or question to encourage response
6. Maintain authenticity - the email should sound like it's coming from me

The goal is to maintain and strengthen relationships through consistent, thoughtful communication."""
                    
                    content_sources = ["LinkedIn Profile", "Company Blog"]
                    topics = ["Business Networking", "Industry Updates", "Partnership Opportunities"]
                    
                    category_instructions = {}
                    for cat in categories:
                        category_instructions[cat.name] = f"Maintain {cat.name} relationship with professional tone. Reference shared experiences and interests."
                    
                    contact_instructions = """Always include:
- Reference to previous conversation/meeting
- Current industry trends
- Value proposition or helpful information
- Clear call to action or follow-up question"""
                    
                    # Format the prompt
                    prompt = f"""HEADER: "Prompt to send {contact.name} to LLM for example generations. This is generation 1: Serious mode."

SYSTEM META: Here is the current system prompt: {system_prompt} This will be given to the LLM as the system prompt.

CORE EMAIL CONTENT: Core Instructions for this generation.
--Step A: Scrape the most recent content from these URLs {', '.join(content_sources)} summarize and then set this data summary as context for the prompt that follows. (Prioritize timely new information over older information.)

--Step B: Search Google for the most authoritative 3 sources on {', '.join(topics)} and then go to those sources and scrape the most recent content, summarize and then set this data summary as context for the prompt that follows. (Prioritize timely new information over older information.)

--Step C: Analyze 'All Notes' in the contact. Use this as context to make the email you write better. Pay attention to threads and continuity and tone and style of previous interactions.

--Step D: Load all of the rules (LLM) instructions for the following categories that this contact belongs to. 
Categories: {', '.join(category_names)}
Instructions:
{chr(10).join([f"- {cat}: {instr}" for cat, instr in category_instructions.items()])}
Summarize and synthesize these into a single LLM guidance. Where there is a conflict between rules from two different categories, use your best judgment from the data in the notes section to prioritize which rule to prioritize.

--Step E: Load all of the rules (LLM) instructions for this contact which is on the contact details page:
{contact_instructions}
Add this to the LLM guidance from Step D. Where there is a conflict between rules from categories versus contact LLM instructions, prioritize the rules from the contact.

--Step F: Using all of the generated context in A,B,C,D,E write 3 subject lines that will be highly likely to resonate with this contact and get them to open the email.

--Step G: Using all of the generated in A,B,C,D,E write a short, powerful email to the contact with timely information and value add content from the research notes. Make this email match in tone everything you know from context and history.

--Step H: Using all of the generated in A,B,C,D,E write a medium length, powerful email to the contact with timely information and value add content from the research notes. Make this email match in tone everything you know from context and history.

--Step I: Using all of the generated in A,B,C,D,E write a short length, powerful email that is optimized to get a response and add deep value to the relationship. Make this email match in tone everything you know from context and history."""
                    
                    # Display prompt
                    st.code(prompt, language="text")
                    
                    # Buttons
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("Generate Email Draft", key="gen_email"):
                            st.success("Email draft generation started!")
                    with col2:
                        if st.button("Close", key="close_dialog"):
                            st.session_state.show_dialog = False
                            st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        
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
    
    # Right column for metrics and graphs
    with dash_right:
        # Key metrics in a more compact layout
        st.markdown("### 📊 Key Metrics")
        metric_col1, metric_col2 = st.columns(2)
        
        # Total Contacts
        with metric_col1:
            total_contacts = 127  # Random number between 100-150
            st.markdown("""
                <div class="metric-card">
                    <a href="#" style="text-decoration: none; color: inherit;">
                        <div class="metric-value">%d</div>
                        <div class="metric-label">Total Contacts</div>
                    </a>
                </div>
            """ % total_contacts, unsafe_allow_html=True)
        
        # Due Today
        with metric_col2:
            due_today = 4  # As requested
            st.markdown("""
                <div class="metric-card">
                    <a href="#" style="text-decoration: none; color: inherit;">
                        <div class="metric-value">%d</div>
                        <div class="metric-label">Due Today</div>
                    </a>
                </div>
            """ % due_today, unsafe_allow_html=True)
        
        # Second row of metrics
        metric_col3, metric_col4 = st.columns(2)
        
        # Due This Week
        with metric_col3:
            due_this_week = 14  # As requested
            st.markdown("""
                <div class="metric-card">
                    <a href="#" style="text-decoration: none; color: inherit;">
                        <div class="metric-value">%d</div>
                        <div class="metric-label">Due This Week</div>
                    </a>
                </div>
            """ % due_this_week, unsafe_allow_html=True)
        
        # Contact Growth This Month
        with metric_col4:
            growth_this_month = 8  # Example value
            st.markdown("""
                <div class="metric-card">
                    <a href="#" style="text-decoration: none; color: inherit;">
                        <div class="metric-value">%d</div>
                        <div class="metric-label">Growth This Month</div>
                    </a>
                </div>
            """ % growth_this_month, unsafe_allow_html=True)
            
        # Contact Growth Graph
        st.markdown("### 📈 Contact Growth")
        
        # Generate mock contact growth data
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        current_month = datetime.now().month
        
        # Last 12 months
        last_12_months = months[current_month-12:] + months[:current_month]
        
        # Mock growth data with an upward trend
        base_contacts = 80
        monthly_growth = [base_contacts]
        
        for i in range(1, 12):
            # Add some randomness to the growth
            growth_rate = np.random.normal(0.05, 0.02)  # Mean 5% growth with some variance
            new_contacts = int(monthly_growth[-1] * (1 + growth_rate))
            monthly_growth.append(new_contacts)
        
        # Create a DataFrame for the line chart
        chart_data = pd.DataFrame({
            'Month': last_12_months,
            'Contacts': monthly_growth
        })
        
        # Display the chart using Streamlit's line_chart
        st.line_chart(
            chart_data.set_index('Month'),
            use_container_width=True
        )
        
        # Performance insights below the graph
        st.markdown("### 🔍 Performance Insights")
        st.markdown("""
            <div class="metric-card">
                <div style="font-size: 1.1rem; font-weight: bold; color: #0066cc; margin-bottom: 0.5rem;">
                    Monthly Contact Activity
                </div>
                <p>Your network grew by <strong>8 contacts</strong> this month, a <strong>6.7%</strong> increase from last month.</p>
                <p>Most active categories: <strong>Business Referral</strong> and <strong>Real Estate Client</strong></p>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.selected == "Contacts":
    st.title("👥 Contacts")
    
    # Initialize view state if not exists
    if 'contact_view' not in st.session_state:
        st.session_state.contact_view = "grid"
    if 'selected_filter' not in st.session_state:
        st.session_state.selected_filter = "all"
    if 'selected_sort' not in st.session_state:
        st.session_state.selected_sort = "name"

    # If viewing a contact, show the contact details page
    if st.session_state.viewing_contact_id is not None:
        show_contact_details(st.session_state.viewing_contact_id)
    else:
        # Define image paths for contacts
        image_paths = [
            "people/markuphero-oqWsu5Aw4vg5Y9AdLllk.png",
            "people/markuphero-WNR37VJCmiTHJrp5EJc1.png", 
            "people/markuphero-3NyeNbNRmpuUZMf8vHQc.png", 
            "people/markuphero-CShNdWhd3qXvCHQWGvMR.png"
        ]
        
        # Generate fake contact data if not exists
        if 'fake_contacts' not in st.session_state:
            st.session_state.fake_contacts = []
            import random
            fake = Faker()
            
            categories = ["Family", "Work", "Friends", "Business", "School", "Sports", "Community", "Church", "Real Estate"]
            
            for i in range(40):
                # Random number of days since last contact (1-120 days)
                days_ago = random.randint(1, 120)
                last_contact_date = datetime.now() - timedelta(days=days_ago)
                
                # Random categories (1-3 categories per contact)
                num_categories = random.randint(1, 3)
                contact_categories = random.sample(categories, num_categories)
                
                # Add to fake contacts
                st.session_state.fake_contacts.append({
                    "id": i,
                    "name": fake.name(),
                    "email": fake.email(),
                    "phone": fake.phone_number(),
                    "last_contact": last_contact_date,
                    "days_since": days_ago,
                    "categories": contact_categories,
                    "image": image_paths[i % len(image_paths)]
                })
        
        # Always show filters in sidebar
        with st.sidebar:
            st.subheader("Filter & Sort")
            
            all_categories = ["All Categories", "Family", "Work", "Friends", "Business", "School", "Sports", "Community", "Church", "Real Estate"]
            
            selected_category = st.selectbox("Category", 
                             options=all_categories,
                             index=0,
                             key="filter_category")
            
            selected_sort = st.selectbox("Sort By",
                             options=["Name", "Last Interaction", "Next Outreach"],
                             index=0,
                             key="filter_sort")
            
            if st.button("Apply Filters", use_container_width=True):
                st.session_state.selected_filter = selected_category
                st.session_state.selected_sort = selected_sort
                st.rerun()
        
        # Filter contacts based on selected filter
        filtered_contacts = st.session_state.fake_contacts
        
        if st.session_state.selected_filter != "all" and st.session_state.selected_filter != "All Categories":
            filtered_contacts = [c for c in filtered_contacts if st.session_state.selected_filter in c["categories"]]
        
        # Sort contacts
        if st.session_state.selected_sort == "Name":
            filtered_contacts = sorted(filtered_contacts, key=lambda x: x["name"])
        elif st.session_state.selected_sort == "Last Interaction":
            filtered_contacts = sorted(filtered_contacts, key=lambda x: x["days_since"], reverse=True)
        
        # Top bar with search and actions
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query = st.text_input("🔍 Search contacts...", placeholder="Search by name, email, or category...")
            
            # Apply search filter if query exists
            if search_query:
                filtered_contacts = [c for c in filtered_contacts if (
                    search_query.lower() in c["name"].lower() or 
                    search_query.lower() in c["email"].lower() or
                    any(search_query.lower() in cat.lower() for cat in c["categories"])
                )]
        
        with col2:
            st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
            # Remove the columns and just show Add button
            st.button("➕ Add", type="primary", key="add_contact_button", use_container_width=True)
        
        # View toggle
        view_cols = st.columns([0.5, 0.5, 6])  # Adjusted column ratios to bring buttons closer
        with view_cols[0]:
            if st.button("📊", help="Grid View", type="primary" if st.session_state.contact_view == "grid" else "secondary"):
                st.session_state.contact_view = "grid"
                st.rerun()
        with view_cols[1]:
            if st.button("📋", help="List View", type="primary" if st.session_state.contact_view == "list" else "secondary"):
                st.session_state.contact_view = "list"
                st.rerun()
        
        # Active filters display
        if st.session_state.selected_filter != "all" and st.session_state.selected_filter != "All Categories":
            st.markdown(f"""
                <div style="display: inline-block; padding: 0.2rem 0.6rem; background-color: rgba(0, 102, 204, 0.1); 
                            border-radius: 16px; margin-bottom: 1rem; color: #0066cc;">
                    {st.session_state.selected_filter} ✕
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"<p>Showing {len(filtered_contacts)} contacts</p>", unsafe_allow_html=True)
        st.markdown("<hr style='margin: 0.5rem 0 1rem 0;'>", unsafe_allow_html=True)
        
        # Display contacts in grid or list view
        if st.session_state.contact_view == "grid":
            # Create 5 columns for the grid view
            cols = st.columns(5)
            
            # Display each contact in the appropriate column
            for i, contact in enumerate(filtered_contacts):
                with cols[i % 5]:
                    # Create a container for the entire card
                    with st.container():
                        # Display the contact card content
                        st.markdown(f"""
                            <div style="border: 1px solid rgba(49, 51, 63, 0.2); border-radius: 10px 10px 0 0; padding: 1rem; margin-bottom: 0; height: 180px; position: relative;">
                                <div class="contact-card">
                                    <div class="contact-photo">
                                        👤
                                    </div>
                                    <div class="contact-info">
                                        <div style="font-weight: bold; font-size: 0.95rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{contact['name']}</div>
                                        <div style="color: #666; font-size: 0.75rem;">{contact['days_since']} days since contact</div>
                                        <div class="contact-email">{contact['email']}</div>
                                        <div class="contact-categories">
                                            {''.join([f'<span class="category-button">{category}</span>' for category in contact["categories"]])}
                                        </div>
                                    </div>
                                </div>
                                <div class="contact-actions" style="position: absolute; bottom: 10px; left: 10px;">
                                    <div class="action-buttons">
                                        <button>✏️</button>
                                        <button>💬</button>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Add the View button in a container that looks like part of the card
                        button_col1, button_col2 = st.columns([2, 1])
                        with button_col2:
                            if st.button("View", key=f"view_grid_{contact['id']}", use_container_width=True):
                                st.session_state.viewing_contact_id = contact['id']
                                st.rerun()
                        
                        # Add styling to make the button container look like part of the card
                        st.markdown(f"""
                            <style>
                            /* Target this specific button container */
                            [data-testid="column"][data-column-index="1"] .stButton {{
                                margin-top: -1px;
                            }}
                            
                            /* Style this specific button to look integrated */
                            [data-testid="column"][data-column-index="1"] .stButton button[key="view_grid_{contact['id']}"] {{
                                border-top-left-radius: 0;
                                border-top-right-radius: 0;
                                border-bottom-left-radius: 10px;
                                border-bottom-right-radius: 10px;
                                background-color: #f8f9fa;
                                border-color: rgba(49, 51, 63, 0.2);
                            }}
                            </style>
                        """, unsafe_allow_html=True)
                        
                        # Add some spacing after each card
                        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        else:
            # List view
            for i, contact in enumerate(filtered_contacts):
                col1, col2 = st.columns([6, 1])
                
                with col1:
                    st.markdown(f"""
                        <div style="border: 1px solid rgba(49, 51, 63, 0.2); border-radius: 10px; padding: 1rem; margin-bottom: 0.5rem;">
                            <div class="contact-card" style="height: auto;">
                                <div class="contact-photo">
                                    👤
                                </div>
                                <div class="contact-info">
                                    <div style="font-weight: bold;">{contact['name']}</div>
                                    <div style="color: #666; font-size: 0.8rem;">
                                        {contact['email']} | Last contact: {contact['days_since']} days ago
                                    </div>
                                    <div class="contact-categories">
                    """, unsafe_allow_html=True)
                    
                    # List view category loop
                    for category in contact["categories"]:
                        st.markdown(f'<span class="category-button">{category}</span>', unsafe_allow_html=True)
                    
                    st.markdown("""
                                    </div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)  # Add some top spacing
                    if st.button("View", key=f"view_list_{contact['id']}", use_container_width=True, type="secondary"):
                        st.session_state.viewing_contact_id = contact['id']
                        st.rerun()

elif st.session_state.selected == "Categories":
    if 'editing_category_id' in st.session_state and st.session_state.editing_category_id is not None:
        show_category_edit(st.session_state.editing_category_id)
    else:
        show_categories()

elif st.session_state.selected == "Calendar":
    show_calendar()

elif st.session_state.selected == "Analytics":
    show_analytics()

elif st.session_state.selected == "Settings":
    # Import and show the settings page
    from pages.settings import show_settings
    show_settings()

elif st.session_state.selected == "Help":
    st.title("❓ Help")
    st.markdown("""
    ### Getting Started
    meetkadence helps you maintain meaningful relationships through consistent, personalized communication.
    
    ### Key Features
    - **Dashboard**: Overview of your contacts and upcoming communications
    - **Contacts**: Manage your network and set communication preferences
    - **Categories**: Organize contacts and set custom communication rules
    - **Calendar**: Manage your schedule and appointments
    - **Analytics**: Analyze your contact interactions and performance
    - **Settings**: Configure your email and system preferences
    
    ### Need Support?
    Visit our [documentation](https://docs.meetkadence.com) or [contact support](mailto:support@meetkadence.com)
    """) 