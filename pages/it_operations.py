"""
Week 9: IT Operations Dashboard
Service desk ticket management and performance analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="IT Operations", page_icon="💻", layout="wide")

# Check if logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.stop()

# Get database
db = st.session_state.db

st.title("💻 IT Operations Dashboard")
st.markdown(f"**Logged in as:** {st.session_state.username} ({st.session_state.role})")
st.markdown("---")

# ==================== KEY METRICS ====================
st.subheader("🎫 Service Desk Metrics")

# Get all tickets
tickets = db.get_all_tickets()
df = pd.DataFrame(tickets, columns=[
    'id', 'ticket_id', 'category', 'priority', 'status', 
    'assigned_staff', 'date_created', 'date_resolved', 'resolution_time_hours'
])

if not df.empty:
    # Calculate metrics
    total_tickets = len(df)
    open_tickets = len(df[df['status'] == 'Open'])
    resolved_tickets = len(df[df['status'] == 'Resolved'])
    avg_resolution = df[df['resolution_time_hours'].notna()]['resolution_time_hours'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Tickets", total_tickets, delta=f"{open_tickets} open")
    with col2:
        st.metric("Open Tickets", open_tickets, delta="+5 from yesterday", delta_color="inverse")
    with col3:
        st.metric("Resolved", resolved_tickets, delta=f"{(resolved_tickets/total_tickets*100):.0f}%")
    with col4:
        st.metric("Avg Resolution Time", f"{avg_resolution:.1f}h" if not pd.isna(avg_resolution) else "N/A")

# ==================== VISUALIZATIONS ====================
st.markdown("---")
st.subheader("📊 Performance Analytics")

if not df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Tickets by Category
        st.markdown("#### Tickets by Category")
        category_counts = df['category'].value_counts()
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Ticket Distribution by Category",
            color_discrete_sequence=px.colors.sequential.Teal
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Priority Levels
        st.markdown("#### Priority Breakdown")
        priority_counts = df['priority'].value_counts()
        fig = px.bar(
            x=priority_counts.index,
            y=priority_counts.values,
            title="Tickets by Priority",
            labels={'x': 'Priority', 'y': 'Count'},
            color=priority_counts.values,
            color_continuous_scale='Oranges'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Staff Performance Analysis
    st.markdown("#### Staff Performance")
    staff_performance = df.groupby('assigned_staff').agg({
        'ticket_id': 'count',
        'resolution_time_hours': 'mean'
    }).reset_index()
    staff_performance.columns = ['Staff', 'Tickets Handled', 'Avg Resolution Time (hrs)']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=staff_performance['Staff'],
        y=staff_performance['Tickets Handled'],
        name='Tickets Handled',
        marker_color='lightblue'
    ))
    fig.add_trace(go.Scatter(
        x=staff_performance['Staff'],
        y=staff_performance['Avg Resolution Time (hrs)'],
        name='Avg Resolution Time',
        yaxis='y2',
        mode='lines+markers',
        marker=dict(color='red', size=10),
        line=dict(width=2)
    ))
    
    fig.update_layout(
        title="Staff Workload vs Performance",
        xaxis_title="Staff Member",
        yaxis_title="Tickets Handled",
        yaxis2=dict(
            title="Avg Resolution Time (hrs)",
            overlaying='y',
            side='right'
        ),
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Status Distribution
    st.markdown("#### Status Overview")
    status_counts = df['status'].value_counts()
    fig = px.funnel(
        y=status_counts.index,
        x=status_counts.values,
        title="Ticket Status Funnel"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== DATA TABLE ====================
st.markdown("---")
st.subheader("🗂️ All Tickets")

if not df.empty:
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.multiselect(
            "Filter by Status",
            options=df['status'].unique(),
            default=df['status'].unique()
        )
    with col2:
        filter_priority = st.multiselect(
            "Filter by Priority",
            options=df['priority'].unique(),
            default=df['priority'].unique()
        )
    with col3:
        filter_category = st.multiselect(
            "Filter by Category",
            options=df['category'].unique(),
            default=df['category'].unique()
        )
    
    # Apply filters
    filtered_df = df[
        (df['status'].isin(filter_status)) &
        (df['priority'].isin(filter_priority)) &
        (df['category'].isin(filter_category))
    ]
    
    # Display table
    st.dataframe(
        filtered_df[['ticket_id', 'category', 'priority', 'status', 'assigned_staff', 'date_created', 'resolution_time_hours']],
        use_container_width=True,
        hide_index=True
    )
    
    st.caption(f"Showing {len(filtered_df)} of {len(df)} tickets")
else:
    st.info("No tickets found. Add some data to get started.")

# ==================== CRUD OPERATIONS ====================
st.markdown("---")
st.subheader("➕ Manage Tickets")

tab1, tab2, tab3 = st.tabs(["Create", "Update", "Delete"])

with tab1:
    st.markdown("#### Create New Ticket")
    with st.form("create_ticket"):
        col1, col2 = st.columns(2)
        with col1:
            ticket_id = st.text_input("Ticket ID", placeholder="TKT-001")
            category = st.selectbox("Category", ["Hardware", "Software", "Network", "Security", "Other"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Critical"])
        with col2:
            status = st.selectbox("Status", ["Open", "In Progress", "Waiting for User", "Resolved", "Closed"])
            assigned_staff = st.text_input("Assigned Staff", value=st.session_state.username)
            date_created = st.date_input("Date Created", value=datetime.now())
        
        if st.form_submit_button("Create Ticket", use_container_width=True):
            if ticket_id:
                success = db.create_ticket(
                    ticket_id, category, priority, status, assigned_staff,
                    date_created.strftime('%Y-%m-%d')
                )
                if success:
                    st.success(f"✅ Ticket {ticket_id} created!")
                    st.rerun()
                else:
                    st.error(f"❌ Ticket {ticket_id} already exists")
            else:
                st.error("Please enter a Ticket ID")

with tab2:
    st.markdown("#### Update Ticket")
    if not df.empty:
        with st.form("update_ticket"):
            update_id = st.selectbox("Select Ticket", df['ticket_id'].tolist())
            
            col1, col2 = st.columns(2)
            with col1:
                new_status = st.selectbox("New Status", ["Open", "In Progress", "Waiting for User", "Resolved", "Closed"])
            with col2:
                resolution_hours = st.number_input("Resolution Time (hours)", min_value=0.0, value=0.0, step=0.5)
            
            date_resolved = st.date_input("Date Resolved (if applicable)")
            
            if st.form_submit_button("Update Ticket", use_container_width=True):
                db.update_ticket(
                    update_id,
                    status=new_status,
                    date_resolved=date_resolved.strftime('%Y-%m-%d') if new_status in ["Resolved", "Closed"] else None,
                    resolution_time_hours=resolution_hours if resolution_hours > 0 else None
                )
                st.success(f"✅ Ticket {update_id} updated!")
                st.rerun()
    else:
        st.info("No tickets to update")

with tab3:
    st.markdown("#### Delete Ticket")
    if not df.empty:
        with st.form("delete_ticket"):
            delete_id = st.selectbox("Select Ticket to Delete", df['ticket_id'].tolist())
            st.warning("⚠️ This action cannot be undone!")
            
            if st.form_submit_button("Delete Ticket", use_container_width=True, type="primary"):
                db.delete_ticket(delete_id)
                st.success(f"✅ Ticket {delete_id} deleted!")
                st.rerun()
    else:
        st.info("No tickets to delete")

# ==================== INSIGHTS & RECOMMENDATIONS ====================
st.markdown("---")
st.subheader("💡 Performance Insights")

if not df.empty:
    # Find slowest staff member
    staff_avg_time = df[df['resolution_time_hours'].notna()].groupby('assigned_staff')['resolution_time_hours'].mean()
    if not staff_avg_time.empty:
        slowest_staff = staff_avg_time.idxmax()
        slowest_time = staff_avg_time.max()
    else:
        slowest_staff = "N/A"
        slowest_time = 0
    
    # Find most common issue
    most_common_category = df['category'].mode()[0]
    category_count = len(df[df['category'] == most_common_category])
    
    # High priority open tickets
    high_open = len(df[(df['priority'] == 'High') & (df['status'] == 'Open')])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📊 Workload Analysis:**
        - Most common issue: {most_common_category} ({category_count} tickets, {(category_count/total_tickets*100):.1f}%)
        - {high_open} high-priority tickets are currently open
        - Recommendation: Allocate more resources to {most_common_category} support
        """)
    
    with col2:
        if slowest_staff != "N/A":
            st.warning(f"""
            **⚠️ Performance Alert:**
            - Staff member with slowest avg resolution: {slowest_staff} ({slowest_time:.1f} hours)
            - Consider additional training or workload redistribution
            - Review "Waiting for User" status tickets for delays
            """)
        else:
            st.success("""
            **✅ Good Performance:**
            - No significant performance issues detected
            - Continue monitoring resolution times
            """)
    
    # Process bottleneck analysis
    waiting_tickets = len(df[df['status'] == 'Waiting for User'])
    if waiting_tickets > 0:
        st.error(f"""
        🚨 **Process Bottleneck Detected:**
        - {waiting_tickets} tickets are in "Waiting for User" status
        - This may indicate communication delays or unclear requirements
        - Recommendation: Implement automated user reminders and clearer ticket descriptions
        """)