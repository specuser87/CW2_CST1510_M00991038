"""
Week 9: Data Science Dashboard
Dataset management and resource analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Data Science", page_icon="📊", layout="wide")

# Check if logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please login first")
    st.stop()

# Get database
db = st.session_state.db

st.title("📊 Data Science Dashboard")
st.markdown(f"**Logged in as:** {st.session_state.username} ({st.session_state.role})")
st.markdown("---")

# ==================== KEY METRICS ====================
st.subheader("📈 Dataset Overview")

# Get all datasets
datasets = db.get_all_datasets()
df = pd.DataFrame(datasets, columns=[
    'id', 'dataset_name', 'source_department', 'upload_date', 
    'file_size_mb', 'row_count', 'owner'
])

if not df.empty:
    # Calculate metrics
    total_datasets = len(df)
    total_size = df['file_size_mb'].sum()
    total_rows = df['row_count'].sum()
    avg_size = df['file_size_mb'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Datasets", total_datasets)
    with col2:
        st.metric("Total Storage", f"{total_size:.1f} MB", delta=f"{avg_size:.1f} MB avg")
    with col3:
        st.metric("Total Rows", f"{total_rows:,}")
    with col4:
        largest_dataset = df.loc[df['file_size_mb'].idxmax(), 'dataset_name']
        st.metric("Largest Dataset", largest_dataset[:15] + "...")

# ==================== VISUALIZATIONS ====================
st.markdown("---")
st.subheader("📊 Analytics & Insights")

if not df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        # Storage by Department
        st.markdown("#### Storage Distribution by Department")
        dept_storage = df.groupby('source_department')['file_size_mb'].sum().sort_values(ascending=False)
        fig = px.bar(
            x=dept_storage.index,
            y=dept_storage.values,
            title="Storage Usage by Department",
            labels={'x': 'Department', 'y': 'Storage (MB)'},
            color=dept_storage.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Dataset Size Distribution
        st.markdown("#### Dataset Size Distribution")
        fig = px.histogram(
            df,
            x='file_size_mb',
            nbins=20,
            title="Dataset Size Frequency",
            labels={'file_size_mb': 'File Size (MB)', 'count': 'Number of Datasets'},
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Row Count vs File Size Scatter
    st.markdown("#### Dataset Complexity Analysis")
    fig = px.scatter(
        df,
        x='row_count',
        y='file_size_mb',
        color='source_department',
        size='file_size_mb',
        hover_data=['dataset_name', 'owner'],
        title="Row Count vs File Size",
        labels={'row_count': 'Number of Rows', 'file_size_mb': 'File Size (MB)'}
    )
    st.plotly_chart(fig, use_container_width=True)

# ==================== DATA TABLE ====================
st.markdown("---")
st.subheader("🗂️ All Datasets")

if not df.empty:
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        filter_dept = st.multiselect(
            "Filter by Department",
            options=df['source_department'].unique(),
            default=df['source_department'].unique()
        )
    with col2:
        size_range = st.slider(
            "File Size Range (MB)",
            min_value=float(df['file_size_mb'].min()),
            max_value=float(df['file_size_mb'].max()),
            value=(float(df['file_size_mb'].min()), float(df['file_size_mb'].max()))
        )
    
    # Apply filters
    filtered_df = df[
        (df['source_department'].isin(filter_dept)) &
        (df['file_size_mb'] >= size_range[0]) &
        (df['file_size_mb'] <= size_range[1])
    ]
    
    # Display table
    st.dataframe(
        filtered_df[['dataset_name', 'source_department', 'upload_date', 'file_size_mb', 'row_count', 'owner']],
        use_container_width=True,
        hide_index=True
    )
    
    st.caption(f"Showing {len(filtered_df)} of {len(df)} datasets")
else:
    st.info("No datasets found. Add some data to get started.")

# ==================== CRUD OPERATIONS ====================
st.markdown("---")
st.subheader("➕ Manage Datasets")

tab1, tab2, tab3 = st.tabs(["Create", "Update", "Delete"])

with tab1:
    st.markdown("#### Add New Dataset")
    with st.form("create_dataset"):
        col1, col2 = st.columns(2)
        with col1:
            dataset_name = st.text_input("Dataset Name", placeholder="Customer_Data_2024")
            source_department = st.selectbox("Source Department", ["IT", "Cyber", "Finance", "HR", "Marketing"])
            upload_date = st.date_input("Upload Date", value=datetime.now())
        with col2:
            file_size_mb = st.number_input("File Size (MB)", min_value=0.1, value=10.0, step=0.1)
            row_count = st.number_input("Row Count", min_value=1, value=1000, step=100)
            owner = st.text_input("Owner", value=st.session_state.username)
        
        if st.form_submit_button("Add Dataset", use_container_width=True):
            if dataset_name:
                success = db.create_dataset(
                    dataset_name, source_department, upload_date.strftime('%Y-%m-%d'),
                    file_size_mb, row_count, owner
                )
                if success:
                    st.success(f"✅ Dataset '{dataset_name}' added!")
                    st.rerun()
                else:
                    st.error(f"❌ Dataset '{dataset_name}' already exists")
            else:
                st.error("Please enter a dataset name")

with tab2:
    st.markdown("#### Update Dataset")
    if not df.empty:
        with st.form("update_dataset"):
            update_name = st.selectbox("Select Dataset", df['dataset_name'].tolist())
            
            col1, col2 = st.columns(2)
            with col1:
                new_size = st.number_input("New File Size (MB)", min_value=0.1, value=10.0, step=0.1)
            with col2:
                new_rows = st.number_input("New Row Count", min_value=1, value=1000, step=100)
            
            if st.form_submit_button("Update Dataset", use_container_width=True):
                db.update_dataset(
                    update_name,
                    file_size_mb=new_size,
                    row_count=new_rows
                )
                st.success(f"✅ Dataset '{update_name}' updated!")
                st.rerun()
    else:
        st.info("No datasets to update")

with tab3:
    st.markdown("#### Delete Dataset")
    if not df.empty:
        with st.form("delete_dataset"):
            delete_name = st.selectbox("Select Dataset to Delete", df['dataset_name'].tolist())
            st.warning("⚠️ This action cannot be undone!")
            
            if st.form_submit_button("Delete Dataset", use_container_width=True, type="primary"):
                db.delete_dataset(delete_name)
                st.success(f"✅ Dataset '{delete_name}' deleted!")
                st.rerun()
    else:
        st.info("No datasets to delete")

# ==================== INSIGHTS & RECOMMENDATIONS ====================
st.markdown("---")
st.subheader("💡 Data Governance Insights")

if not df.empty:
    # Find largest datasets
    large_datasets = df.nlargest(3, 'file_size_mb')
    
    # Department with most storage
    dept_usage = df.groupby('source_department')['file_size_mb'].sum()
    highest_dept = dept_usage.idxmax()
    highest_usage = dept_usage.max()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **📦 Storage Recommendations:**
        - Largest dataset: {large_datasets.iloc[0]['dataset_name']} ({large_datasets.iloc[0]['file_size_mb']:.1f} MB)
        - Top 3 datasets consume {large_datasets['file_size_mb'].sum():.1f} MB ({(large_datasets['file_size_mb'].sum()/total_size*100):.1f}% of total)
        - Consider archiving datasets older than 6 months
        """)
    
    with col2:
        st.warning(f"""
        **🏢 Department Analysis:**
        - {highest_dept} department uses the most storage: {highest_usage:.1f} MB
        - Total departments: {df['source_department'].nunique()}
        - Recommendation: Implement data lifecycle policies for {highest_dept}
        """)
    
    # Resource consumption alert
    if total_size > 500:
        st.error(f"""
        ⚠️ **Storage Alert:** Total storage exceeds 500 MB ({total_size:.1f} MB)
        - Consider implementing data archiving policies
        - Review datasets for potential deletion or compression
        """)
        


