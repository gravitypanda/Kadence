import streamlit as st
import random
from datetime import datetime
from models.schemas import Category, CadenceFrequency
from utils.sample_data import generate_sample_categories
from utils.helpers import format_date

# Initialize session state for categories if not exists
if 'categories_filter' not in st.session_state:
    st.session_state.categories_filter = "all"
if 'show_category_actions' not in st.session_state:
    st.session_state.show_category_actions = False
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'categories' not in st.session_state:
    st.session_state.categories = generate_sample_categories()
if 'editing_category_id' not in st.session_state:
    st.session_state.editing_category_id = None
if 'trigger_rerun' not in st.session_state:
    st.session_state.trigger_rerun = False
if 'selected_contact_id' not in st.session_state:
    st.session_state.selected_contact_id = None

# Function to handle edit button clicks - sets state but doesn't call rerun
def handle_edit_click(category_id):
    st.session_state.editing_category_id = category_id
    st.session_state.trigger_rerun = True

def show_categories():
    # Check if we need to rerun from a previous callback
    if st.session_state.trigger_rerun:
        st.session_state.trigger_rerun = False
        st.rerun()
    
    # Check if a contact has been selected for viewing
    if st.session_state.selected_contact_id:
        # In a real app, this would navigate to the contact details page
        # For now, just display a contact details card
        
        # Find the selected contact
        selected_contact = None
        for contact in st.session_state.contacts:
            if contact.id == st.session_state.selected_contact_id:
                selected_contact = contact
                break
        
        if selected_contact:
            # Back button at the top
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("←", key="back_button"):
                    st.session_state.selected_contact_id = None
                    st.rerun()
            with col2:
                st.title(f"Contact Details")
            
            # Get categories for this contact
            contact_categories = []
            for cat_id in selected_contact.categories:
                for category in st.session_state.categories:
                    if category.id == cat_id:
                        contact_categories.append(category)
                        break
            
            # Display contact details in a card layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Contact info card
                st.markdown("""
                <style>
                .contact-card {
                    background-color: white;
                    border: 1px solid rgba(49, 51, 63, 0.2);
                    border-radius: 12px;
                    padding: 20px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                }
                .contact-header {
                    display: flex;
                    align-items: center;
                    margin-bottom: 15px;
                }
                .contact-avatar {
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    background-color: #f0f2f6;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 24px;
                    margin-right: 15px;
                }
                .contact-name {
                    font-size: 1.5rem;
                    font-weight: bold;
                    margin: 0;
                }
                .contact-email {
                    color: #666;
                    margin: 5px 0 0 0;
                }
                .contact-detail {
                    margin: 15px 0;
                    padding-bottom: 15px;
                    border-bottom: 1px solid #f0f2f6;
                }
                .detail-label {
                    font-size: 0.85rem;
                    color: #666;
                    margin-bottom: 5px;
                }
                .detail-value {
                    font-weight: 500;
                }
                .category-chips {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 8px;
                    margin-top: 10px;
                }
                .category-chip {
                    background-color: #e0e5f0;
                    color: #0066cc;
                    padding: 5px 10px;
                    border-radius: 16px;
                    font-size: 0.8rem;
                    font-weight: 500;
                }
                </style>
                
                <div class="contact-card">
                    <div class="contact-header">
                        <div class="contact-avatar">👤</div>
                        <div>
                            <h2 class="contact-name">{selected_contact.name}</h2>
                            <p class="contact-email">{selected_contact.email}</p>
                        </div>
                    </div>
                    
                    <div class="contact-detail">
                        <div class="detail-label">Phone</div>
                        <div class="detail-value">{selected_contact.phone or "Not provided"}</div>
                    </div>
                    
                    <div class="contact-detail">
                        <div class="detail-label">Next Outreach Date</div>
                        <div class="detail-value">{format_date(selected_contact.next_outreach_date)}</div>
                    </div>
                    
                    <div class="contact-detail">
                        <div class="detail-label">Last Contact</div>
                        <div class="detail-value">{format_date(selected_contact.last_contact) if selected_contact.last_contact else "Never"}</div>
                    </div>
                    
                    <div class="contact-detail">
                        <div class="detail-label">Cadence Frequency</div>
                        <div class="detail-value">{selected_contact.cadence_frequency.capitalize()}</div>
                    </div>
                    
                    <div class="contact-detail">
                        <div class="detail-label">Categories</div>
                        <div class="category-chips">
                            {"".join([f'<span class="category-chip">{cat.name}</span>' for cat in contact_categories])}
                        </div>
                    </div>
                    
                    <div class="contact-detail" style="border-bottom: none;">
                        <div class="detail-label">Personal Instructions</div>
                        <div class="detail-value">{selected_contact.personal_instructions or "No personal instructions provided"}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.button("✏️ Edit Contact", use_container_width=True)
                with col2:
                    st.button("📧 Generate Email", type="primary", use_container_width=True)
            
            with col2:
                # Upcoming dates card
                st.markdown("""
                <div class="contact-card">
                    <h3 style="margin-top: 0; margin-bottom: 15px;">Special Dates</h3>
                    
                    <div class="contact-detail" style="border-bottom: none;">
                """, unsafe_allow_html=True)
                
                if selected_contact.special_dates:
                    for date_type, date_value in selected_contact.special_dates.items():
                        st.markdown(f"""
                        <div style="margin-bottom: 10px;">
                            <div class="detail-label">{date_type.capitalize()}</div>
                            <div class="detail-value">{date_value.strftime('%B %d, %Y')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="color: #666; font-style: italic;">No special dates recorded</div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Keywords card
                st.markdown("""
                <div class="contact-card" style="margin-top: 20px;">
                    <h3 style="margin-top: 0; margin-bottom: 15px;">Keywords</h3>
                    
                    <div class="category-chips">
                """, unsafe_allow_html=True)
                
                if selected_contact.keywords:
                    for keyword in selected_contact.keywords:
                        st.markdown(f"""
                        <span class="category-chip">{keyword}</span>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="color: #666; font-style: italic;">No keywords assigned</div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Websites card
                st.markdown("""
                <div class="contact-card" style="margin-top: 20px;">
                    <h3 style="margin-top: 0; margin-bottom: 15px;">Relevant Websites</h3>
                """, unsafe_allow_html=True)
                
                if selected_contact.relevant_websites:
                    for website in selected_contact.relevant_websites:
                        st.markdown(f"""
                        <div style="margin-bottom: 10px;">
                            <a href="{website}" target="_blank" style="color: #0066cc; text-decoration: none; word-break: break-all;">{website}</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="color: #666; font-style: italic;">No websites recorded</div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("Contact not found")
            if st.button("← Back to Categories"):
                st.session_state.selected_contact_id = None
                st.rerun()
        
        # Return early to avoid showing the categories view
        return
        
    st.title("Categories Management")
    st.markdown("Organize your contacts and tailor AI suggestions", help="Create and manage categories to organize contacts and customize AI behavior")

    # Filter and search controls in a row
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Search bar
        search_query = st.text_input("🔍 Search categories", key="category_search", placeholder="Search by name or description...")
    
    with col2:
        # Filter dropdown
        filter_option = st.selectbox(
            "Filter by status",
            options=["All Categories", "Active Only", "Inactive Only"],
            key="category_filter"
        )

    # Apply CSS styling for cards
    st.markdown("""
    <style>
    /* Card/Tile styling */
    .category-card {
        background-color: white;
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        position: relative;
        overflow: hidden;
        transition: all 0.2s ease;
    }
    .category-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    .category-name {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 5px;
        color: #333;
    }
    .category-description {
        margin-bottom: 12px;
        font-size: 0.9rem;
        color: #555;
    }
    .category-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    .active-badge {
        background-color: #e6f7ee;
        color: #00a86b;
    }
    .inactive-badge {
        background-color: #f0f2f6;
        color: #666;
    }

    /* LLM Prompt styling */
    .llm-prompt {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 12px;
        margin: 15px 0;
    }
    .prompt-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #555;
        margin: 0 0 8px 0;
    }
    .prompt-text {
        font-size: 0.85rem;
        color: #666;
        font-style: italic;
        line-height: 1.4;
    }

    /* Overdue contacts styling */
    .overdue-contacts {
        border-top: 1px solid #eee;
        margin-top: 15px;
        padding-top: 15px;
    }
    .overdue-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #555;
        margin: 0 0 10px 0;
    }
    .contact-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid #f0f2f6;
    }
    .contact-row:last-child {
        border-bottom: none;
    }
    .contact-info {
        display: flex;
        flex-direction: column;
    }
    .contact-name {
        font-size: 0.85rem;
        font-weight: 500;
        color: #333;
    }
    .contact-date {
        font-size: 0.75rem;
        color: #888;
    }
    .contact-link {
        background-color: #e0e5f0;
        color: #0066cc;
        font-size: 0.75rem;
        font-weight: 500;
        padding: 4px 8px;
        border-radius: 4px;
        text-decoration: none;
    }
    .contact-link:hover {
        background-color: #d0d5e0;
    }

    /* Style for the Streamlit edit button */
    .stButton button {
        display: block;
        width: 100%;
        text-align: center;
        padding: 8px 0;
        background-color: #f0f2f6 !important;
        color: #333 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        cursor: pointer;
        font-size: 0.9rem;
        margin-top: 15px;
        border: none !important;
        box-shadow: none !important;
    }
    .stButton button:hover {
        background-color: #e0e5f0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Determine filter type based on dropdown selection
    filter_type = "all"
    if filter_option == "Active Only":
        filter_type = "active"
    elif filter_option == "Inactive Only":
        filter_type = "inactive"
    
    # Display categories in a grid layout
    display_categories(filter_type, search_query)

    # Add Category button
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    if st.button("➕ Add Category", type="primary", use_container_width=True):
        st.session_state.editing_category_id = "new"
        st.rerun()

def display_categories(filter_type, search_query=""):
    # Create a 3-column grid for the cards
    cols = st.columns(3)
    
    # Filter categories based on selected filter
    filtered_categories = st.session_state.categories
    if filter_type == "active":
        filtered_categories = [c for c in filtered_categories if c.precedence_order > 0]
    elif filter_type == "inactive":
        filtered_categories = [c for c in filtered_categories if c.precedence_order == 0]

    # Apply search filter if query exists
    if search_query:
        filtered_categories = [c for c in filtered_categories if 
            search_query.lower() in c.name.lower() or 
            (c.description and search_query.lower() in c.description.lower())]

    # Display message if no categories found
    if not filtered_categories:
        st.info(f"No categories found" + (" matching your search" if search_query else ""))
        return

    # Distribute categories across columns
    categories_per_column = {}
    for i, category in enumerate(filtered_categories):
        col_idx = i % 3
        if col_idx not in categories_per_column:
            categories_per_column[col_idx] = []
        categories_per_column[col_idx].append(category)
    
    # Display categories in each column
    for col_idx, column in enumerate(cols):
        if col_idx in categories_per_column:
            with column:
                for category in categories_per_column[col_idx]:
                    # Create a container for each card
                    with st.container():
                        # Create a unique key for this category's edit button
                        edit_key = f"edit_btn_{category.id}"
                        
                        # Use placeholder text for the LLM prompt snippet
                        category_name = category.name.lower()
                        
                        # Different placeholder prompts based on category name to make it more realistic
                        if "client" in category_name or "customer" in category_name:
                            llm_snippet = "When reaching out to clients, reference their recent projects, ask about business growth, and offer relevant insights from our industry. Maintain professional but warm tone."
                        elif "friend" in category_name or "personal" in category_name:
                            llm_snippet = "Keep communication casual and friendly. Ask about family, recent trips, or shared interests. Reference past conversations and inside jokes when appropriate."
                        elif "network" in category_name or "professional" in category_name:
                            llm_snippet = "Focus on professional development topics, industry trends, and potential collaboration opportunities. Maintain formal tone while being personable."
                        else:
                            llm_snippet = "When generating emails for this category, focus on professional tone, mention recent industry news, and ask about their current projects. Include a personal touch based on previous conversations."
                        
                        # Simplified display for overdue contacts
                        if "client" in category_name or "customer" in category_name:
                            contact1_name = "Acme Corp (John Smith)"
                            contact1_date = "5 days overdue"
                            contact2_name = "TechSolutions Inc."
                            contact2_date = "Due today"
                            contact3_name = "Global Enterprises"
                            contact3_date = "Due in 3 days"
                        elif "friend" in category_name or "personal" in category_name:
                            contact1_name = "Emma Williams"
                            contact1_date = "2 weeks overdue"
                            contact2_name = "James Taylor"
                            contact2_date = "1 month overdue"
                            contact3_name = "Sophia Garcia"
                            contact3_date = "Due next week"
                        else:
                            contact1_name = "Sarah Johnson"
                            contact1_date = "3 days overdue"
                            contact2_name = "Michael Chen"
                            contact2_date = "1 week overdue"
                            contact3_name = "Alex Rodriguez"
                            contact3_date = "Due tomorrow"
                        
                        # Display card content with simplified layout
                        st.markdown(f"""
                        <div class="category-card">
                            <div class="category-name">{category.name}</div>
                            <div class="category-description">{category.description or "No description"}</div>
                            
                            LLM Instructions
                            {llm_snippet}
                            
                            Upcoming Contacts
                            {contact1_name} - {contact1_date}
                            {contact2_name} - {contact2_date}
                            {contact3_name} - {contact3_date}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add a visible Streamlit button styled to match the design
                        if st.button("Edit Category", key=edit_key, on_click=handle_edit_click, args=(category.id,), use_container_width=True):
                            pass  # The on_click handler will take care of the action

def set_editing_category(category_id):
    st.session_state.editing_category_id = category_id
    st.rerun()

def toggle_category_status(category_id, is_active):
    for i, cat in enumerate(st.session_state.categories):
        if cat.id == category_id:
            if is_active:
                # Deactivate: set precedence to 0
                st.session_state.categories[i].precedence_order = 0
            else:
                # Activate: set precedence to 1 (or any positive number)
                st.session_state.categories[i].precedence_order = 1
            break
    st.rerun()

if __name__ == "__main__":
    show_categories() 