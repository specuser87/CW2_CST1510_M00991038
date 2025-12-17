import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Cybersecurity", page_icon="", layout="wide")

# Check if logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning(" Please login first")
    st.stop()

# Get database
db = st.session_state.db

st.title(" Cybersecurity Incident Dashboard")
st.markdown(f"**Logged in as:** {st.session_state.username} ({st.session_state.role})")
st.markdown("---")

# ==================== KEY METRICS ====================
st.subheader(" Key Metrics")

# Get all incidents
incidents = db.get_all_incidents()
df = pd.DataFrame(incidents, columns=[
    'id', 'incident_id', 'threat_type', 'severity', 'status', 
    'date_reported', 'date_resolved', 'assigned_analyst'
])

if not df.empty:
    # Calculate metrics
    total_incidents = len(df)
    open_incidents = len(df[df['status'] == 'Open'])
    resolved_incidents = len(df[df['status'] == 'Resolved'])
    high_severity = len(df[df['severity'] == 'High'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Incidents", total_incidents, delta=f"{open_incidents} open")
    with col2:
        st.metric("Open Incidents", open_incidents, delta="-2 from last week", delta_color="inverse")
    with col3:
        st.metric("Resolved", resolved_incidents)
    with col4:
        st.metric("High Severity", high_severity, delta=" Critical")
# ==================== VISUALIZATIONS ====================
st.markdown("---")
st.subheader(" Analytics & Insights")

if not df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Threat Type Distribution
        st.markdown("#### Threat Type Distribution")
        threat_counts = df['threat_type'].value_counts()
        fig = px.pie(
            values=threat_counts.values, 
            names=threat_counts.index,
            title="Incidents by Threat Type",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Severity Breakdown
        st.markdown("#### Severity Levels")
        severity_counts = df['severity'].value_counts()
        fig = px.bar(
            x=severity_counts.index,
            y=severity_counts.values,
            title="Incidents by Severity",
            labels={'x': 'Severity', 'y': 'Count'},
            color=severity_counts.values,
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Status Timeline
    st.markdown("#### Status Overview")
    status_counts = df['status'].value_counts()
    fig = go.Figure(data=[
        go.Bar(
            x=status_counts.index,
            y=status_counts.values,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
    ])
    fig.update_layout(
        title="Incidents by Status",
        xaxis_title="Status",
        yaxis_title="Count",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== DATA TABLE ====================
st.markdown("---")
st.subheader(" All Incidents")

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
        filter_severity = st.multiselect(
            "Filter by Severity",
            options=df['severity'].unique(),
            default=df['severity'].unique()
        )
    with col3:
        filter_threat = st.multiselect(
            "Filter by Threat Type",
            options=df['threat_type'].unique(),
            default=df['threat_type'].unique()
        )
    
    # Apply filters
    filtered_df = df[
        (df['status'].isin(filter_status)) &
        (df['severity'].isin(filter_severity)) &
        (df['threat_type'].isin(filter_threat))
    ]
    
    # Display table
    st.dataframe(
        filtered_df[['incident_id', 'threat_type', 'severity', 'status', 'date_reported', 'assigned_analyst']],
        use_container_width=True,
        hide_index=True
    )
    
    st.caption(f"Showing {len(filtered_df)} of {len(df)} incidents")
else:
    st.info("No incidents found. Add some data to get started.")

# ==================== CRUD OPERATIONS ====================
st.markdown("---")
st.subheader(" Manage Incidents")

tab1, tab2, tab3 = st.tabs(["Create", "Update", "Delete"])

with tab1:
    st.markdown("#### Create New Incident")
    with st.form("create_incident"):
        col1, col2 = st.columns(2)
        with col1:
            incident_id = st.text_input("Incident ID", placeholder="INC-001")
            threat_type = st.selectbox("Threat Type", ["Phishing", "Malware", "Ransomware", "DDoS", "Data Breach"])
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        with col2:
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"])
            date_reported = st.date_input("Date Reported", value=datetime.now())
            assigned_analyst = st.text_input("Assigned Analyst", value=st.session_state.username)
        
        if st.form_submit_button("Create Incident", use_container_width=True):
            if incident_id:
                success = db.create_incident(
                    incident_id, threat_type, severity, status,
                    date_reported.strftime('%Y-%m-%d'), assigned_analyst=assigned_analyst
                )
                if success:
                    st.success(f"Incident {incident_id} created!")
                    st.rerun()
                else:
                    st.error(f"Incident {incident_id} already exists")
            else:
                st.error("Please enter an Incident ID")

with tab2:
    st.markdown("#### Update Incident Status")
    if not df.empty:
        with st.form("update_incident"):
            update_id = st.selectbox("Select Incident", df['incident_id'].tolist())
            new_status = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"])
            date_resolved = st.date_input("Date Resolved (if applicable)")
            
            if st.form_submit_button("Update Incident", use_container_width=True):
                db.update_incident(
                    update_id, 
                    status=new_status,
                    date_resolved=date_resolved.strftime('%Y-%m-%d') if new_status == "Resolved" else None
                )
                st.success(f" Incident {update_id} updated!")
                st.rerun()
    else:
        st.info("No incidents to update")

with tab3:
    st.markdown("#### Delete Incident")
    if not df.empty:
        with st.form("delete_incident"):
            delete_id = st.selectbox("Select Incident to Delete", df['incident_id'].tolist())
            st.warning(" This action cannot be undone!")
            
            if st.form_submit_button("Delete Incident", use_container_width=True, type="primary"):
                db.delete_incident(delete_id)
                st.success(f" Incident {delete_id} deleted!")
                st.rerun()
    else:
        st.info("No incidents to delete")

# ==================== INSIGHTS ====================
st.markdown("---")
st.subheader(" Key Insights")

if not df.empty:
    # Most common threat
    most_common_threat = df['threat_type'].mode()[0]
    threat_count = len(df[df['threat_type'] == most_common_threat])
    
    # High severity open incidents
    high_open = len(df[(df['severity'] == 'High') & (df['status'] == 'Open')])
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        ** Most Common Threat:** {most_common_threat}
        - {threat_count} incidents ({(threat_count/total_incidents*100):.1f}% of total)
        - Recommendation: Increase training on {most_common_threat} prevention
        """)
    
    with col2:
        st.warning(f"""
        ** High Priority Alert:** {high_open} high-severity incidents are open
        - Immediate attention required
        - Assign additional analysts if needed
        """)