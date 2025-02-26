import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def generate_fake_timeseries(days, base_value, volatility, trend=0):
    dates = [datetime.now() - timedelta(days=x) for x in range(days)]
    values = [base_value + trend * x + np.random.normal(0, volatility) for x in range(days)]
    return pd.DataFrame({'date': dates, 'value': values})

def show_analytics():
    st.title("📈 Analytics Dashboard")
    
    # Time period selector and export
    col1, col2 = st.columns([3, 1])
    with col1:
        time_periods = {
            '7d': 'Last 7 Days',
            '30d': 'Last 30 Days',
            '90d': 'Last 90 Days',
            'ytd': 'Year to Date',
            'all': 'All Time'
        }
        selected_period = st.select_slider(
            'Time Period',
            options=list(time_periods.keys()),
            value='30d',
            format_func=lambda x: time_periods[x]
        )
    
    with col2:
        st.download_button(
            "📥 Export Report",
            data="Placeholder for export data",
            file_name=f"kadence_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    # Key metrics with sparklines
    st.markdown("### Key Performance Indicators")
    
    # Generate fake time series data for sparklines
    contacts_ts = generate_fake_timeseries(30, 100, 5, 1)
    active_ts = generate_fake_timeseries(30, 40, 3, 0.5)
    response_ts = generate_fake_timeseries(30, 70, 2, -0.1)
    time_ts = generate_fake_timeseries(30, 2, 0.2, -0.01)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=contacts_ts['date'], y=contacts_ts['value'],
                                mode='lines', line=dict(color='#0066cc', width=1)))
        fig.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=50,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        
        st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <p style="color: #666; margin: 0;">Total Contacts</p>
                <h2 style="margin: 0.5rem 0; color: #0066cc;">127</h2>
                <p style="color: #00cc66; margin: 0; font-size: 0.9rem;">↑ 12% from last period</p>
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=active_ts['date'], y=active_ts['value'],
                                mode='lines', line=dict(color='#0066cc', width=1)))
        fig.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=50,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        
        st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <p style="color: #666; margin: 0;">Active Conversations</p>
                <h2 style="margin: 0.5rem 0; color: #0066cc;">43</h2>
                <p style="color: #00cc66; margin: 0; font-size: 0.9rem;">↑ 8% from last period</p>
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col3:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=response_ts['date'], y=response_ts['value'],
                                mode='lines', line=dict(color='#0066cc', width=1)))
        fig.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=50,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        
        st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <p style="color: #666; margin: 0;">Response Rate</p>
                <h2 style="margin: 0.5rem 0; color: #0066cc;">68%</h2>
                <p style="color: #cc0000; margin: 0; font-size: 0.9rem;">↓ 3% from last period</p>
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col4:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_ts['date'], y=time_ts['value'],
                                mode='lines', line=dict(color='#0066cc', width=1)))
        fig.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            height=50,
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        
        st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <p style="color: #666; margin: 0;">Avg Response Time</p>
                <h2 style="margin: 0.5rem 0; color: #0066cc;">1.8d</h2>
                <p style="color: #00cc66; margin: 0; font-size: 0.9rem;">↑ Better by 0.3d</p>
            </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Engagement Overview
    st.markdown("### 📊 Engagement Overview")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Activity Trends", "Response Analysis", "Category Performance"])
    
    with tab1:
        # Generate fake daily activity data
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        data = pd.DataFrame({
            'date': dates,
            'emails_sent': np.random.randint(5, 20, 30),
            'responses_received': np.random.randint(3, 15, 30),
            'new_contacts': np.random.randint(0, 5, 30)
        })
        
        # Create multi-line chart
        fig = px.line(data, x='date', y=['emails_sent', 'responses_received', 'new_contacts'],
                      labels={'value': 'Count', 'variable': 'Metric'},
                      title='Daily Activity Trends')
        fig.update_layout(hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)
        
        # Activity breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            # Hourly activity heatmap
            hours = list(range(24))
            days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            activity = np.random.randint(0, 10, size=(7, 24))
            
            fig = px.imshow(activity,
                           labels=dict(x="Hour of Day", y="Day of Week", color="Activity Level"),
                           x=hours,
                           y=days,
                           aspect="auto",
                           title="Activity Heatmap")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Weekly patterns
            weekly_data = pd.DataFrame({
                'day': days,
                'avg_activity': np.random.uniform(20, 100, 7)
            })
            
            fig = px.bar(weekly_data, x='day', y='avg_activity',
                        title="Average Activity by Day of Week")
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        # Response time distribution
        response_times = np.random.exponential(2, 1000)
        fig = px.histogram(response_times, nbins=30,
                          labels={'value': 'Response Time (days)', 'count': 'Frequency'},
                          title='Response Time Distribution')
        st.plotly_chart(fig, use_container_width=True)
        
        # Response rate by time of day
        col1, col2 = st.columns(2)
        
        with col1:
            hourly_data = pd.DataFrame({
                'hour': range(24),
                'response_rate': np.random.uniform(0.4, 0.9, 24)
            })
            
            fig = px.line(hourly_data, x='hour', y='response_rate',
                         title='Response Rate by Hour',
                         labels={'response_rate': 'Response Rate', 'hour': 'Hour of Day'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Response quality distribution
            quality_data = pd.DataFrame({
                'quality': ['Short', 'Medium', 'Long', 'Detailed'],
                'percentage': np.random.uniform(0, 100, 4)
            })
            
            fig = px.pie(quality_data, values='percentage', names='quality',
                        title='Response Quality Distribution')
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        # Category performance metrics
        categories = ['Business Referral', 'Real Estate Client', 'Pickleball', 'Local Business', 'Tech Industry']
        category_data = pd.DataFrame({
            'category': categories,
            'contacts': np.random.randint(10, 50, len(categories)),
            'response_rate': np.random.uniform(0.5, 0.9, len(categories)),
            'avg_response_time': np.random.uniform(1, 5, len(categories)),
            'engagement_score': np.random.uniform(60, 95, len(categories))
        })
        
        # Radar chart for category performance
        fig = go.Figure()
        
        for idx, category in enumerate(category_data['category']):
            fig.add_trace(go.Scatterpolar(
                r=[category_data.loc[idx, 'response_rate'] * 100,
                   category_data.loc[idx, 'contacts'],
                   category_data.loc[idx, 'engagement_score'],
                   category_data.loc[idx, 'avg_response_time'] * 20],
                theta=['Response Rate', 'Total Contacts', 'Engagement Score', 'Avg Response Time'],
                fill='toself',
                name=category
            ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title='Category Performance Overview'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Category metrics table
        st.markdown("#### Detailed Category Metrics")
        
        # Format the data for display
        display_df = category_data.copy()
        display_df['response_rate'] = display_df['response_rate'].apply(lambda x: f"{x*100:.1f}%")
        display_df['avg_response_time'] = display_df['avg_response_time'].apply(lambda x: f"{x:.1f} days")
        display_df['engagement_score'] = display_df['engagement_score'].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(
            display_df,
            column_config={
                "category": "Category",
                "contacts": "Total Contacts",
                "response_rate": "Response Rate",
                "avg_response_time": "Avg Response Time",
                "engagement_score": "Engagement Score"
            },
            hide_index=True
        )

    # Relationship Health Score
    st.markdown("### 🎯 Relationship Health")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Overall health score gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=78,
            title={'text': "Overall Relationship Health"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#0066cc"},
                'steps': [
                    {'range': [0, 50], 'color': "#ff4b4b"},
                    {'range': [50, 75], 'color': "#ffa500"},
                    {'range': [75, 100], 'color': "#00cc66"}
                ]
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Health factors breakdown
        factors = pd.DataFrame({
            'factor': ['Response Rate', 'Engagement Frequency', 'Conversation Quality', 'Network Growth', 'Follow-up Rate'],
            'score': np.random.uniform(60, 95, 5)
        })
        
        fig = px.bar(factors, x='factor', y='score',
                    title="Health Factors Breakdown",
                    labels={'score': 'Score', 'factor': 'Factor'},
                    color='score',
                    color_continuous_scale=['#ff4b4b', '#ffa500', '#00cc66'])
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Action Items and Insights
    st.markdown("### 🎯 Recommended Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="margin-top: 0;">Priority Follow-ups</h4>
                <ul style="padding-left: 1.5rem;">
                    <li>Respond to John Smith's email from 3 days ago</li>
                    <li>Schedule follow-up with Tech Industry group (5 contacts)</li>
                    <li>Re-engage with inactive Real Estate contacts</li>
                    <li>Plan quarterly check-in with Business Referral network</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="margin-top: 0;">Key Insights</h4>
                <ul style="padding-left: 1.5rem;">
                    <li>Response rates are highest on Tuesday mornings</li>
                    <li>Tech Industry category shows strongest engagement</li>
                    <li>20% increase in network growth this month</li>
                    <li>Consider adjusting outreach timing for Local Business category</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show_analytics() 