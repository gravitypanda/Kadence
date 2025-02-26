import streamlit as st
from datetime import datetime, timedelta
import calendar
import random
import pandas as pd

def get_fake_names():
    return [
        "John Smith", "Emma Wilson", "Michael Brown", "Sarah Davis", "James Johnson",
        "Lisa Anderson", "David Miller", "Jennifer White", "Robert Taylor", "Mary Martinez",
        "William Lee", "Patricia Moore", "Thomas Clark", "Elizabeth Hall", "Joseph Young"
    ]

def create_month_calendar(year, month):
    # Get the calendar for the specified month
    cal = calendar.monthcalendar(year, month)
    
    # Convert to DataFrame for easier display
    df = pd.DataFrame(cal, columns=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
    
    # Replace 0s with empty strings
    df = df.replace(0, '')
    
    return df

def generate_events(year, month):
    events = {}
    names = get_fake_names()
    today = datetime.now().date()
    
    # Generate 15 random events
    for _ in range(15):
        day = random.randint(1, 28)  # Avoid edge cases with month lengths
        date = datetime(year, month, day).date()
        name = random.choice(names)
        
        if date not in events:
            events[date] = []
        
        # Color based on date
        if date > today:
            # Future events in blue
            color = "blue"
        else:
            # Past events randomly in red or green
            color = "green" if random.random() > 0.4 else "red"
        
        events[date].append((name, color))
    
    return events

def show_calendar():
    st.title("📅 Calendar")
    
    # Get current date
    if 'selected_date' not in st.session_state:
        st.session_state.selected_date = datetime.now()
    
    # Calendar navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("← Previous"):
            # Move to previous month
            first_day = st.session_state.selected_date.replace(day=1)
            st.session_state.selected_date = first_day - timedelta(days=1)
            st.rerun()
    
    with col2:
        current_month = st.session_state.selected_date.strftime("%B %Y")
        st.markdown(f"<h3 style='text-align: center;'>{current_month}</h3>", unsafe_allow_html=True)
    
    with col3:
        if st.button("Next →"):
            # Move to next month
            last_day = st.session_state.selected_date.replace(day=28)
            st.session_state.selected_date = last_day + timedelta(days=4)
            st.session_state.selected_date = st.session_state.selected_date.replace(day=1)
            st.rerun()
    
    # Get calendar data
    year = st.session_state.selected_date.year
    month = st.session_state.selected_date.month
    cal_df = create_month_calendar(year, month)
    events = generate_events(year, month)
    
    # Create calendar grid with events
    st.markdown("""
        <style>
        .calendar-cell {
            border: 1px solid #ddd;
            padding: 8px;
            min-height: 100px;
            vertical-align: top;
        }
        .calendar-header {
            background-color: #f8f9fa;
            font-weight: bold;
            text-align: center;
            padding: 8px;
        }
        .day-number {
            font-weight: bold;
            margin-bottom: 4px;
        }
        .event {
            font-size: 0.9em;
            margin: 2px 0;
            padding: 2px;
            border-radius: 3px;
        }
        .event-blue { color: #0066cc; }
        .event-red { color: #dc3545; }
        .event-green { color: #28a745; }
        </style>
    """, unsafe_allow_html=True)
    
    # Create calendar table
    html_calendar = '<table style="width: 100%; border-collapse: collapse;">'
    
    # Add headers
    html_calendar += '<tr>'
    for day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']:
        html_calendar += f'<th class="calendar-header">{day}</th>'
    html_calendar += '</tr>'
    
    # Add calendar cells with events
    for week in cal_df.values:
        html_calendar += '<tr>'
        for day in week:
            html_calendar += '<td class="calendar-cell">'
            if day != '':
                # Add day number
                html_calendar += f'<div class="day-number">{day}</div>'
                
                # Add events for this day
                current_date = datetime(year, month, int(day)).date()
                if current_date in events:
                    for name, color in events[current_date]:
                        html_calendar += f'<div class="event event-{color}">{name}</div>'
            
            html_calendar += '</td>'
        html_calendar += '</tr>'
    
    html_calendar += '</table>'
    
    # Display calendar
    st.markdown(html_calendar, unsafe_allow_html=True)

if __name__ == "__main__":
    show_calendar() 