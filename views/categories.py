import streamlit as st
import uuid
from models.schemas import Category

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
            # Validate inputs
            if not name or not rule_text:
                st.error("Category name and AI instructions are required!")
                return False
            
            # Create/update category object
            category_data = {
                "id": category.id if category else str(uuid.uuid4()),
                "name": name,
                "description": description if description else None,
                "rule_text": rule_text,
                "precedence_order": precedence
            }
            
            new_category = Category(**category_data)
            
            if is_edit:
                # Update existing category
                st.session_state.categories = [
                    new_category if c.id == category.id else c 
                    for c in st.session_state.categories
                ]
                st.success("Category updated successfully!")
            else:
                # Add new category
                st.session_state.categories.append(new_category)
                st.success("Category added successfully!")
            
            return True
    
    return False

# Main categories page
st.title("🏷️ Categories")

# Tabs for list view and add/edit
tab1, tab2 = st.tabs(["Category List", "Add Category"])

with tab1:
    # Sort categories by precedence order
    sorted_categories = sorted(
        st.session_state.categories,
        key=lambda x: x.precedence_order,
        reverse=True
    )
    
    # Category list with actions
    for category in sorted_categories:
        with st.expander(f"{category.name} (Priority: {category.precedence_order})"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                if category.description:
                    st.write("**Description:**", category.description)
                st.write("**AI Instructions:**", category.rule_text)
                
                # Show usage count
                usage_count = sum(
                    1 for contact in st.session_state.contacts 
                    if category.id in contact.categories
                )
                st.write(f"**Used by {usage_count} contacts**")
            
            with col2:
                if st.button("Edit", key=f"edit_{category.id}"):
                    st.session_state.editing_category = category
                    st.session_state.current_tab = "Add Category"
                    st.experimental_rerun()
            
            with col3:
                # Only allow deletion if category is not in use
                if usage_count == 0:
                    if st.button("Delete", key=f"delete_{category.id}"):
                        st.session_state.categories = [
                            c for c in st.session_state.categories 
                            if c.id != category.id
                        ]
                        st.success("Category deleted successfully!")
                        st.experimental_rerun()
                else:
                    st.write("*In use*")

with tab2:
    if hasattr(st.session_state, 'editing_category'):
        st.subheader("Edit Category")
        if render_category_form(st.session_state.editing_category, is_edit=True):
            del st.session_state.editing_category
            st.experimental_rerun()
    else:
        st.subheader("Add New Category")
        render_category_form() 