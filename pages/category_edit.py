import streamlit as st
import random
from models.schemas import Category, Contact
from datetime import datetime

def show_category_edit(category_id: str = None):
    # Find the category being edited
    edited_category = None
    if category_id and category_id != "new":
        for category in st.session_state.categories:
            if category.id == category_id:
                edited_category = category
                break
    
    # Initialize session state for edit form with fake data based on category
    if edited_category:
        category_name = edited_category.name
        category_description = edited_category.description or ""
        
        # Generate fake LLM instructions based on category name
        category_name_lower = category_name.lower()
        if "client" in category_name_lower or "customer" in category_name_lower:
            llm_instructions = "When reaching out to clients, reference their recent projects, ask about business growth, and offer relevant insights from our industry. Maintain professional but warm tone."
        elif "prospect" in category_name_lower:
            # 30% chance to add call-to-action for prospects
            if random.random() < 0.3:
                llm_instructions = "Focus on value proposition and recent success stories. Always include a clear call-to-action like 'Let's hop on a call to discuss how we can help you achieve similar results.' End with a specific time suggestion."
            else:
                llm_instructions = "Highlight industry trends and pain points we solve. Share relevant case studies and testimonials. Keep it focused on their specific industry challenges."
        elif "friend" in category_name_lower or "personal" in category_name_lower:
            llm_instructions = "Keep communication casual and friendly. Ask about family, recent trips, or shared interests. Reference past conversations and inside jokes when appropriate."
        elif "network" in category_name_lower or "professional" in category_name_lower:
            llm_instructions = "Focus on professional development topics, industry trends, and potential collaboration opportunities. Maintain formal tone while being personable."
        elif "real estate" in category_name_lower:
            llm_instructions = "Include local market updates and property value trends. End with 'Looking forward to helping you with your next real estate journey!'"
        elif "pickleball" in category_name_lower or "sport" in category_name_lower:
            llm_instructions = "Always include a PS about playing soon. Reference recent games or tournaments."
        elif "business" in category_name_lower:
            llm_instructions = "Maintain professional tone. Include recent business wins or industry news."
        else:
            llm_instructions = "When generating emails for this category, focus on professional tone, mention recent industry news, and ask about their current projects. Include a personal touch based on previous conversations."
    else:
        # Default values for new category
        category_name = ""
        category_description = ""
        llm_instructions = ""
    
    # Set session state values
    if 'category_name' not in st.session_state or edited_category:
        st.session_state.category_name = category_name
    if 'category_description' not in st.session_state or edited_category:
        st.session_state.category_description = category_description
    if 'category_color' not in st.session_state:
        st.session_state.category_color = "#0066cc"
    if 'category_instructions' not in st.session_state or edited_category:
        st.session_state.category_instructions = llm_instructions
    if 'show_delete_modal' not in st.session_state:
        st.session_state.show_delete_modal = False

    # Header with back button and delete
    col1, col2 = st.columns([6, 1])
    with col1:
        header_col1, header_col2 = st.columns([1, 5])
        with header_col1:
            if st.button("←", key="back_button"):
                st.session_state.editing_category_id = None
                st.rerun()
        with header_col2:
            title = "Edit Category" if edited_category else "New Category"
            st.markdown(f"<h1 style='margin: 0;'>{title}</h1>", unsafe_allow_html=True)
    with col2:
        if st.button("🗑️ Delete", type="secondary", use_container_width=True):
            st.session_state.show_delete_modal = True

    # Main content in two columns
    left_col, right_col = st.columns([2, 1])

    with left_col:
        # Category details card
        st.markdown("""
            <div class="metric-card">
                <div style="padding: 1.5rem;">
        """, unsafe_allow_html=True)

        # Category name
        st.text_input("Category Name", 
                     value=st.session_state.category_name,
                     key="category_name_input",
                     placeholder="Enter category name")

        # Description
        st.text_area("Description",
                    value=st.session_state.category_description,
                    key="category_description_input",
                    placeholder="Enter category description",
                    height=100)

        # Color picker
        st.color_picker("Color",
                       value=st.session_state.category_color,
                       key="category_color_input")

        # LLM Instructions
        st.text_area("LLM Instructions to always use for this category",
                    value=st.session_state.category_instructions,
                    key="category_instructions_input",
                    placeholder="Enter instructions for AI interactions",
                    height=150)

        st.markdown("</div></div>", unsafe_allow_html=True)

    with right_col:
        # Associated contacts card
        contact_count = 0
        if category_id and category_id != "new":
            contact_count = len([c for c in st.session_state.contacts if category_id in c.categories])
        
        st.markdown(f"""
            <div class="metric-card" style="height: 100%;">
                <div style="padding: 1.5rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3 style="margin: 0;">Associated Contacts</h3>
                        <span style="color: #666;">
                            {contact_count} contacts
                        </span>
                    </div>
        """, unsafe_allow_html=True)

        # Contact search
        st.text_input("🔍", placeholder="Search contacts...", key="contact_search")

        # Contacts list
        if category_id and category_id != "new":
            contacts = [c for c in st.session_state.contacts if category_id in c.categories]
            for contact in contacts:
                st.markdown(f"""
                    <div style="display: flex; align-items: center; gap: 1rem; padding: 0.75rem;
                               background: #f8f9fa; border-radius: 0.5rem; margin-bottom: 0.5rem;">
                        <div style="width: 40px; height: 40px; border-radius: 50%; 
                                   background: #e0e5f0; display: flex; align-items: center; 
                                   justify-content: center; font-size: 1.2rem;">
                            👤
                        </div>
                        <div style="flex: 1;">
                            <div style="font-weight: 500;">{contact.name}</div>
                            <div style="color: #666; font-size: 0.9rem;">{contact.email}</div>
                        </div>
                        <div style="color: #666; font-size: 0.9rem;">
                            {contact.last_contact.strftime('%b %d, %Y') if contact.last_contact else 'Never'}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="color: #666; font-style: italic; text-align: center; padding: 2rem 0;">
                    No contacts associated yet
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    # Action buttons
    col1, col2 = st.columns([6, 1])
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.session_state.editing_category_id = None
            st.rerun()
    with col2:
        if st.button("Save", type="primary", use_container_width=True):
            # Save changes
            st.session_state.editing_category_id = None
            st.rerun()

    # Delete confirmation modal
    if st.session_state.show_delete_modal:
        with st.container():
            st.markdown("""
                <div class="modal">
                    <div class="modal-content">
                        <h2>Delete Category</h2>
                        <p>Are you sure you want to delete this category? This action cannot be undone.</p>
                        <div style="display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1rem;">
                            <button onclick="closeDeleteModal()" style="padding: 0.5rem 1rem; border: 1px solid #ddd;
                                    background: none; border-radius: 0.25rem; cursor: pointer;">
                                Cancel
                            </button>
                            <button onclick="deleteCategory()" style="padding: 0.5rem 1rem; background: #dc3545;
                                    color: white; border: none; border-radius: 0.25rem; cursor: pointer;">
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # Add modal styles and JavaScript
    st.markdown("""
        <style>
        .modal {
            display: block;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
        }
        .modal-content {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 2rem;
            border-radius: 0.5rem;
            width: 90%;
            max-width: 500px;
        }
        </style>
        
        <script>
        function closeDeleteModal() {
            window.streamlitUpdateState({
                'show_delete_modal': false
            });
        }
        
        function deleteCategory() {
            // Handle category deletion
            window.streamlitUpdateState({
                'editing_category_id': null,
                'show_delete_modal': false
            });
            window.streamlitRerun();
        }
        </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_category_edit() 