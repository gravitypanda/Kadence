import streamlit as st
from datetime import datetime
from utils.helpers import format_date, get_contact_categories
from pages.contact_details import show_contact_details

def show_contacts():
    # Initialize session state
    if 'contacts_page' not in st.session_state:
        st.session_state.contacts_page = 'list'
    if 'selected_contact_id' not in st.session_state:
        st.session_state.selected_contact_id = None

    # Show either the list or the details view
    if st.session_state.contacts_page == 'list':
        show_contacts_list()
    else:
        show_contact_details(st.session_state.selected_contact_id)

def show_contacts_list():
    st.title("👥 Contacts")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍", placeholder="Search contacts...")
    with col2:
        filter_by = st.selectbox("Filter by", ["All", "Recent", "Due Soon", "Inactive"])
    
    # Display contacts in a grid
    contacts = st.session_state.contacts
    
    # Filter contacts based on search and filter
    if search:
        contacts = [c for c in contacts if search.lower() in c.name.lower() or search.lower() in c.email.lower()]
    
    if filter_by == "Recent":
        contacts = sorted(contacts, key=lambda x: x.last_contact if x.last_contact else datetime.min, reverse=True)
    elif filter_by == "Due Soon":
        contacts = sorted(contacts, key=lambda x: x.next_outreach_date)
    elif filter_by == "Inactive":
        contacts = [c for c in contacts if not c.last_contact or (datetime.now() - c.last_contact).days > 30]
    
    # Create a grid of contact cards
    cols = st.columns(3)
    for i, contact in enumerate(contacts):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                            <div style="width: 48px; height: 48px; border-radius: 50%; background: #f0f2f6; 
                                       display: flex; align-items: center; justify-content: center; font-size: 24px;">
                                👤
                            </div>
                            <div>
                                <h3 style="margin: 0;">{contact.name}</h3>
                                <p style="color: #666; margin: 0;">{contact.email}</p>
                            </div>
                        </div>
                """, unsafe_allow_html=True)
                
                # Categories
                categories = get_contact_categories(contact, st.session_state.categories)
                if categories:
                    st.markdown('<div style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem;">', unsafe_allow_html=True)
                    for cat in categories[:2]:  # Show only first 2 categories
                        st.markdown(f"""
                            <span style="background: {cat.color if hasattr(cat, 'color') else '#0066cc20'}; 
                                       color: {cat.color.replace('20', '') if hasattr(cat, 'color') else '#0066cc'}; 
                                       padding: 2px 8px; border-radius: 12px; font-size: 0.8rem;">
                                {cat.name}
                            </span>
                        """, unsafe_allow_html=True)
                    if len(categories) > 2:
                        st.markdown(f'<span style="color: #666; font-size: 0.8rem;">+{len(categories)-2} more</span>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Last contact and next outreach
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                        <div style="color: #666; font-size: 0.8rem;">Last Contact</div>
                        <div>{format_date(contact.last_contact) if contact.last_contact else 'Never'}</div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div style="color: #666; font-size: 0.8rem;">Next Outreach</div>
                        <div>{format_date(contact.next_outreach_date)}</div>
                    """, unsafe_allow_html=True)
                
                # View details button
                if st.button("View Details", key=f"view_{contact.id}"):
                    st.session_state.selected_contact_id = contact.id
                    st.session_state.contacts_page = 'details'
                    st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)

    # Add contact button
    st.sidebar.button("➕ Add Contact", type="primary", use_container_width=True)

if __name__ == "__main__":
    show_contacts() 