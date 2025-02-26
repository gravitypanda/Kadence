import streamlit as st
import uuid
from datetime import datetime, date
from models.schemas import Contact, CadenceFrequency, Category

def render_category_form(category: Category = None, is_edit: bool = False):
    """Render the category form for adding/editing categories"""
    with st.form("category_form"):
        name = st.text_input("Category Name", value=category.name if category else "")
        description = st.text_area(
            "Description",
            value=category.description if category else "",
            help="Brief description of this category"
        )
        
        rule_text = st.text_area(
            "AI Instructions",
            value=category.rule_text if category else "",
            help="Instructions for the AI on how to handle contacts in this category"
        )
        
        # Precedence order
        existing_orders = [cat.precedence_order for cat in st.session_state.categories]
        max_order = max(existing_orders) if existing_orders else 0
        
        precedence = st.number_input(
            "Precedence Order",
            min_value=1,
            max_value=max_order + 1,
            value=category.precedence_order if category else max_order + 1,
            help="Higher numbers take precedence when rules conflict"
        )
        
        submitted = st.form_submit_button("Save Category")
        
        if submitted:
            if not name or not rule_text:
                st.error("Category name and AI instructions are required!")
                return False
            
            category_data = {
                "id": category.id if category else str(uuid.uuid4()),
                "name": name,
                "description": description if description else None,
                "rule_text": rule_text,
                "precedence_order": precedence
            }
            
            new_category = Category(**category_data)
            
            if is_edit:
                st.session_state.categories = [
                    new_category if c.id == category.id else c 
                    for c in st.session_state.categories
                ]
                st.success("Category updated successfully!")
            else:
                st.session_state.categories.append(new_category)
                st.success("Category added successfully!")
            
            return True
    
    return False

def render_contact_form(contact: Contact = None, is_edit: bool = False):
    """Render the contact form for adding/editing contacts"""
    with st.form("contact_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            name = st.text_input("Name", value=contact.name if contact else "")
            email = st.text_input("Email", value=contact.email if contact else "")
            phone = st.text_input("Phone (optional)", value=contact.phone if contact else "")
            
            # Categories
            selected_categories = st.multiselect(
                "Categories",
                options=[cat.name for cat in st.session_state.categories],
                default=[cat.name for cat in st.session_state.categories if cat.id in (contact.categories if contact else [])]
            )
            
            # Map category names back to IDs
            category_ids = [
                cat.id for cat in st.session_state.categories 
                if cat.name in selected_categories
            ]
            
            # Special dates
            birthday = st.date_input(
                "Birthday",
                value=contact.special_dates.get("birthday") if contact else None,
                format="MM/DD/YYYY"
            )
            
            # Cadence
            cadence = st.selectbox(
                "Outreach Cadence",
                options=list(CadenceFrequency),
                index=list(CadenceFrequency).index(contact.cadence_frequency) if contact else 1
            )
        
        with col2:
            st.subheader("AI Content Sources")
            
            # Personal instructions
            instructions = st.text_area(
                "Personal Instructions",
                value=contact.personal_instructions if contact else "",
                help="Add specific instructions for AI-generated messages"
            )
            
            # Relevant websites
            websites = st.text_area(
                "Relevant Websites",
                value="\n".join(contact.relevant_websites) if contact else "",
                help="Enter one website URL per line"
            )
            
            # Keywords
            keywords = st.text_area(
                "Keywords & Topics",
                value="\n".join(contact.keywords) if contact else "",
                help="Enter one keyword/topic per line"
            )
        
        submitted = st.form_submit_button("Save Contact")
        
        if submitted:
            # Create/update contact object
            contact_data = {
                "id": contact.id if contact else str(uuid.uuid4()),
                "name": name,
                "email": email,
                "phone": phone if phone else None,
                "special_dates": {"birthday": birthday} if birthday else {},
                "categories": category_ids,
                "personal_instructions": instructions if instructions else None,
                "cadence_frequency": cadence,
                "next_outreach_date": datetime.now(),  # This would be calculated based on cadence
                "relevant_websites": [url.strip() for url in websites.split("\n") if url.strip()],
                "keywords": [kw.strip() for kw in keywords.split("\n") if kw.strip()],
                "last_contact": contact.last_contact if contact else None
            }
            
            new_contact = Contact(**contact_data)
            
            if is_edit:
                # Update existing contact
                st.session_state.contacts = [
                    new_contact if c.id == contact.id else c 
                    for c in st.session_state.contacts
                ]
                st.success("Contact updated successfully!")
            else:
                # Add new contact
                st.session_state.contacts.append(new_contact)
                st.success("Contact added successfully!")
            
            return True
    
    return False

# Main contacts page
st.title("👥 Contacts")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["Contact List", "Add Contact", "Categories"])

with tab1:
    # Search and filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search contacts", placeholder="Search by name or email...")
    with col2:
        category_filter = st.multiselect(
            "Filter by category",
            options=[cat.name for cat in st.session_state.categories]
        )
    
    # Contact list with actions
    for contact in st.session_state.contacts:
        # Apply search filter
        if search and search.lower() not in contact.name.lower() and search.lower() not in contact.email.lower():
            continue
            
        # Apply category filter
        if category_filter:
            contact_categories = [
                cat.name for cat in st.session_state.categories 
                if cat.id in contact.categories
            ]
            if not any(cat in contact_categories for cat in category_filter):
                continue
        
        with st.expander(f"{contact.name} ({contact.email})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # Contact details
                st.write("**Categories:**", ", ".join([
                    cat.name for cat in st.session_state.categories 
                    if cat.id in contact.categories
                ]))
                st.write("**Cadence:**", contact.cadence_frequency)
                if contact.personal_instructions:
                    st.write("**Instructions:**", contact.personal_instructions)
                
                # Content sources
                if contact.relevant_websites or contact.keywords:
                    st.write("**Content Sources:**")
                    if contact.relevant_websites:
                        st.write("- Websites:", ", ".join(contact.relevant_websites))
                    if contact.keywords:
                        st.write("- Topics:", ", ".join(contact.keywords))
            
            with col2:
                st.button("Edit", key=f"edit_{contact.id}", type="primary")
                st.button("Delete", key=f"delete_{contact.id}", type="secondary")
                
                if st.button("Generate Draft", key=f"draft_{contact.id}"):
                    st.info("Draft generation coming soon!")

with tab2:
    if hasattr(st.session_state, 'editing_contact'):
        st.subheader("Edit Contact")
        if render_contact_form(st.session_state.editing_contact, is_edit=True):
            del st.session_state.editing_contact
            st.experimental_rerun()
    else:
        st.subheader("Add New Contact")
        render_contact_form()

with tab3:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Manage Categories")
        # Sort categories by precedence order
        sorted_categories = sorted(
            st.session_state.categories,
            key=lambda x: x.precedence_order,
            reverse=True
        )
        
        # Category list with actions
        for category in sorted_categories:
            with st.expander(f"{category.name} (Priority: {category.precedence_order})"):
                if category.description:
                    st.write("**Description:**", category.description)
                st.write("**AI Instructions:**", category.rule_text)
                
                # Show usage count
                usage_count = sum(
                    1 for contact in st.session_state.contacts 
                    if category.id in contact.categories
                )
                st.write(f"**Used by {usage_count} contacts**")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_cat_{category.id}"):
                        st.session_state.editing_category = category
                        st.experimental_rerun()
                
                with col2:
                    if usage_count == 0:
                        if st.button("Delete", key=f"delete_cat_{category.id}"):
                            st.session_state.categories = [
                                c for c in st.session_state.categories 
                                if c.id != category.id
                            ]
                            st.success("Category deleted successfully!")
                            st.experimental_rerun()
                    else:
                        st.write("*In use*")
    
    with col2:
        st.subheader("Add Category")
        if hasattr(st.session_state, 'editing_category'):
            if render_category_form(st.session_state.editing_category, is_edit=True):
                del st.session_state.editing_category
                st.experimental_rerun()
        else:
            render_category_form() 