import streamlit as st
import datetime
from utils.helpers import format_date

def show_contact_details(contact_id=None):
    # Initialize session state for navigation
    if 'contacts_page' not in st.session_state:
        st.session_state.contacts_page = 'details'
    
    # Initialize session state for LLM instructions
    if 'show_llm_dialog' not in st.session_state:
        st.session_state.show_llm_dialog = False
    if 'llm_instructions' not in st.session_state:
        st.session_state.llm_instructions = """Always mention:
- Previous meeting at Tech Conference
- Interest in AI developments
- Recent product launches at TechCorp
- Shared connection through Product Management community"""

    # Initialize additional session state for the LLM prompt dialog
    if 'show_llm_prompt_dialog' not in st.session_state:
        st.session_state.show_llm_prompt_dialog = False

    # Function to handle navigation back to contacts list
    def navigate_to_contacts_list():
        st.session_state.contacts_page = 'list'
        st.rerun()

    # Function to toggle LLM prompt dialog
    def toggle_llm_prompt_dialog():
        st.session_state.show_llm_prompt_dialog = not st.session_state.show_llm_prompt_dialog
        st.rerun()

    # Header with back button and edit
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        # Make the back arrow button functional
        if st.button("← Back to Contacts", key="back_arrow"):
            navigate_to_contacts_list()
        st.markdown("<h1 style='margin: 0; display: inline-block; margin-left: 10px;'>Contact Details</h1>", unsafe_allow_html=True)
    
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
            <div class="metric-card">
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

        # Add Email Selection Dropdown
        st.markdown("""
            <div class="metric-card" style="margin-top: 1rem;">
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
                    <h4 style="margin: 0 0 0.5rem 0;">Choose the email you use to send to this contact</h4>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Create the dropdown with fake emails
        selected_email = st.selectbox(
            label="",  # Empty label since we have the header above
            options=[
                "john.business@company.com",
                "john.personal@gmail.com",
                "john.consulting@freelance.com"
            ],
            key="email_selection_dropdown"
        )

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
                    <a href="https://linkedin.com/in/johnsmith" target="_blank" style="text-decoration: none; color: inherit;">
                        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                            <div style="flex: 1;">
                                <p style="font-weight: bold; margin: 0 0 0.25rem 0;">LinkedIn Profile</p>
                                <p style="color: #666; margin: 0; font-size: 0.9rem;">Professional updates and posts</p>
                            </div>
                            <div style="width: 40px; height: 40px; border-radius: 50%; background-color: #00cc6620; 
                                       display: flex; align-items: center; justify-content: center; font-size: 20px;">
                                💼
                            </div>
                        </div>
                    </a>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Notes Card
        if 'contact_notes' not in st.session_state:
            st.session_state.contact_notes = ""
        if 'last_note_update' not in st.session_state:
            st.session_state.last_note_update = None

        st.markdown("""
            <div class="metric-card" style="margin-bottom: 1rem;">
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <h4 style="margin: 0;">Add a Note</h4>
                        <div style="color: #666; font-size: 0.9rem;">
                            {last_update}
                        </div>
                    </div>
                </div>
            </div>
        """.format(
            last_update=f"Last updated: {st.session_state.last_note_update.strftime('%b %d, %H:%M')}" if st.session_state.last_note_update else "No updates yet"
        ), unsafe_allow_html=True)

        # Notes text area with auto-save
        new_notes = st.text_area(
            "",
            value=st.session_state.contact_notes,
            height=100,
            key="contact_notes_input",
            placeholder="Type your note here...",
            label_visibility="collapsed"
        )

        # Update notes in session state if changed
        if new_notes != st.session_state.contact_notes:
            st.session_state.contact_notes = new_notes
            st.session_state.last_note_update = datetime.datetime.now()
            st.success("Note saved!", icon="✍️")

        # Topics Card (formerly Keywords & Topics)
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
                    <div class="draggable-topic" draggable="true" style="background: #f8f9fa; padding: 0.75rem; border-radius: 8px; cursor: move; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="color: #666;">⋮⋮</span>
                        <span class="category-button" style="background-color: #cccc0020; color: #cccc00;">Machine Learning</span>
                    </div>
                    <div class="draggable-topic" draggable="true" style="background: #f8f9fa; padding: 0.75rem; border-radius: 8px; cursor: move; display: flex; align-items: center; gap: 0.5rem;">
                        <span style="color: #666;">⋮⋮</span>
                        <span class="category-button" style="background-color: #cc000020; color: #cc0000;">SaaS</span>
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

    # Fixed action buttons at the bottom - use a container to position them
    with st.container():
        col1, col2, col3 = st.columns([6, 1, 1])
        with col3:
            # Place the buttons in the right column for right alignment
            st.button("⚡ Generate Now", type="secondary", use_container_width=True)
            st.button("💬 Internal Hidden", key="internal_hidden_btn", on_click=toggle_llm_prompt_dialog, use_container_width=True)

    # Show LLM Prompt Dialog using Streamlit components
    if st.session_state.show_llm_prompt_dialog:
        with st.container():
            st.subheader("LLM Prompt")
            st.caption("This is the prompt that would be sent to the LLM for email generation")
            
            # Fake data for the prompt
            contact_name = "John Smith"
            system_prompt = """You are an AI assistant that helps me nurture my professional and personal relationships.
                
When generating emails:
1. Use a tone appropriate for the relationship category (professional, personal, etc.)
2. Reference previous interactions and shared experiences when available
3. Include relevant, timely topics based on the recipient's interests and our relationship
4. Keep messages concise but meaningful
5. End with a clear next step or question to encourage response
6. Maintain authenticity - the email should sound like it's coming from me

The goal is to maintain and strengthen relationships through consistent, thoughtful communication."""
            
            content_sources = ["TechCorp Blog", "LinkedIn Profile"]
            topics = ["Artificial Intelligence", "Product Management", "Tech Conference", "Machine Learning", "SaaS"]
            categories = ["High Value", "Active Client", "Tech Industry"]
            category_instructions = {
                "High Value": "Focus on personalized advice and high-value insights. Offer exclusive information or opportunities when possible. Always reference past conversations and shared experiences.",
                "Active Client": "Keep communication professional but warm. Reference current projects and deadlines. Offer help or additional resources that might be valuable.",
                "Tech Industry": "Include relevant industry trends and news. Mention upcoming conferences or events. Share insights about competitor movements or market changes."
            }
            contact_instructions = """Always mention:
- Previous meeting at Tech Conference
- Interest in AI developments
- Recent product launches at TechCorp
- Shared connection through Product Management community"""
            
            # Format the prompt exactly as requested
            prompt = f"""HEADER: "Prompt to send {contact_name} to LLM for example generations. This is generation 1: Serious mode."

SYSTEM META: Here is the current system prompt: {system_prompt} This will be given to the LLM as the system prompt.

CORE EMAIL CONTENT: Core Instructions for this generation.
--Step A: Scrape the most recent content from these URLs {', '.join(content_sources)} summarize and then set this data summary as context for the prompt that follows. (Prioritize timely new information over older information.)

--Step B: Search Google for the most authoritative 3 sources on {', '.join(topics)} and then go to those sources and scrape the most recent content, summarize and then set this data summary as context for the prompt that follows. (Prioritize timely new information over older information.)

--Step C: Analyze 'All Notes' in the contact. Use this as context to make the email you write better. Pay attention to threads and continuity and tone and style of previous interactions.

--Step D: Load all of the rules (LLM) instructions for the following categories that this contact belongs to. 
Categories: {', '.join(categories)}
Instructions:
- High Value: {category_instructions["High Value"]}
- Active Client: {category_instructions["Active Client"]}
- Tech Industry: {category_instructions["Tech Industry"]}
Summarize and synthesize these into a single LLM guidance. Where there is a conflict between rules from two different categories, use your best judgment from the data in the notes section to prioritize which rule to prioritize.

--Step E: Load all of the rules (LLM) instructions for this contact which is on the contact details page:
{contact_instructions}
Add this to the LLM guidance from Step D. Where there is a conflict between rules from categories versus contact LLM instructions, prioritize the rules from the contact.

--Step F: Using all of the generated context in A,B,C,D,E write 3 subject lines that will be highly likely to resonate with this contact and get them to open the email.

--Step G: Using all of the generated in A,B,C,D,E write a short, powerful email to the contact with timely information and value add content from the research notes. Make this email match in tone everything you know from context and history.

--Step H: Using all of the generated in A,B,C,D,E write a medium length, powerful email to the contact with timely information and value add content from the research notes. Make this email match in tone everything you know from context and history.

--Step I: Using all of the generated in A,B,C,D,E write a short length, powerful email that is optimized to get a response and add deep value to the relationship. Make this email match in tone everything you know from context and history."""
            
            # Display the prompt in a code block
            st.code(prompt, language="text")
            
            # Buttons for actions
            col1, col2 = st.columns([5, 1])
            with col2:
                if st.button("Close", key="close_prompt_btn", on_click=toggle_llm_prompt_dialog):
                    pass  # The on_click handler handles the action
                
                # Simplified copy functionality
                if st.button("Copy", key="copy_prompt_btn"):
                    st.session_state.clipboard = prompt
                    st.success("Copied to clipboard!")

    # Add a simple fixed position back button at the bottom
    st.markdown("""
        <div style="position: fixed; bottom: 2rem; left: 2rem;">
            <div id="back-button-container"></div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add a plain Streamlit button for navigation
    if st.button("Back to Contacts", key="bottom_back_btn", type="primary", on_click=navigate_to_contacts_list):
        pass  # The on_click handler handles navigation

if __name__ == "__main__":
    show_contact_details() 