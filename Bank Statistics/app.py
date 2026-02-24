import streamlit as st
import pandas as pd
from pathlib import Path
import os
from dotenv import load_dotenv
import sys

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from create_bank_table import extract_bank_info, normalize_author_name
from tally_authors import simple_yaml_parse_authors

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ESTELA Problem Bank Statistics",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 ESTELA Problem Bank Statistics")

# Sidebar for configuration
st.sidebar.header("Configuration")

# Get course folders from .env
course_folders_str = os.getenv('COURSE_FOLDERS', 'PHY I Mechanics')
course_folders = [folder.strip() for folder in course_folders_str.split(',')]
default_course = os.getenv('DEFAULT_COURSE', 'PHY I Mechanics')

# Course selection dropdown
selected_course = st.sidebar.selectbox(
    "Select Course Folder",
    options=course_folders,
    index=course_folders.index(default_course) if default_course in course_folders else 0
)

# Valid bank pattern input
default_pattern = os.getenv('DEFAULT_BANK_PATTERN', 'PHY1')
bank_pattern = st.sidebar.text_input(
    "Valid Bank Folder Pattern",
    value=default_pattern,
    help="Enter the starting pattern for valid bank folders (e.g., PHY1)"
)

# Get base directory
script_dir = Path(__file__).parent
base_dir = script_dir.parent / selected_course

# Function to collect bank data
@st.cache_data
def load_bank_data(course_folder, pattern):
    """Load all bank data based on course folder and pattern."""
    base_path = script_dir.parent / course_folder
    
    if not base_path.exists():
        return pd.DataFrame()
    
    # Find all .yaml and .yml files
    yaml_files = list(base_path.glob("**/*.yaml")) + list(base_path.glob("**/*.yml"))
    
    # Filter to valid files
    main_files = []
    for yaml_file in yaml_files:
        try:
            rel_path = yaml_file.relative_to(base_path)
            parts = rel_path.parts
            
            # Check if file name starts with pattern
            if not yaml_file.name.startswith(pattern):
                continue
            
            # Check if directly under a folder starting with pattern
            if len(parts) >= 2:
                parent_folder = parts[-2]
                if parent_folder.startswith(pattern):
                    main_files.append(yaml_file)
        except ValueError:
            continue
    
    # Extract information from each file
    bank_data = []
    for yaml_file in sorted(main_files):
        info = extract_bank_info(yaml_file, base_path)
        if info:
            bank_data.append(info)
    
    return pd.DataFrame(bank_data)

# Load data
with st.spinner('Loading problem banks...'):
    df = load_bank_data(selected_course, bank_pattern)

if df.empty:
    st.warning(f"No valid problem banks found in '{selected_course}' with pattern '{bank_pattern}'")
else:
    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Banks", len(df))
    
    with col2:
        st.metric("Total Problems", df['Number of problems'].sum())
    
    with col3:
        st.metric("Unique Authors", df['Author'].nunique())
    
    with col4:
        st.metric("Topics", df['Topic'].nunique())
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 All Banks", "👥 By Author", "📚 By Topic"])
    
    with tab1:
        st.subheader("All Problem Banks")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            topic_filter = st.multiselect(
                "Filter by Topic",
                options=sorted(df['Topic'].unique()),
                default=None
            )
        
        with col2:
            author_filter = st.multiselect(
                "Filter by Author",
                options=sorted(df['Author'].unique()),
                default=None
            )
        
        with col3:
            type_filter = st.multiselect(
                "Filter by Problem Type",
                options=sorted(df['Problem Type'].unique()),
                default=None
            )
        
        # Apply filters
        filtered_df = df.copy()
        if topic_filter:
            filtered_df = filtered_df[filtered_df['Topic'].isin(topic_filter)]
        if author_filter:
            filtered_df = filtered_df[filtered_df['Author'].isin(author_filter)]
        if type_filter:
            filtered_df = filtered_df[filtered_df['Problem Type'].isin(type_filter)]
        
        # Display table
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "BankId": st.column_config.TextColumn("Bank ID", width="medium"),
                "Title": st.column_config.TextColumn("Title", width="large"),
                "Description": st.column_config.TextColumn("Description", width="large"),
                "Number of problems": st.column_config.NumberColumn("# Problems", width="small"),
                "Problem Type": st.column_config.TextColumn("Type", width="small")
            }
        )
        
        st.caption(f"Showing {len(filtered_df)} of {len(df)} banks")
    
    with tab2:
        st.subheader("Banks by Author")
        
        # Group by author
        author_stats = df.groupby('Author').agg({
            'BankId': 'count',
            'Number of problems': 'sum'
        }).reset_index()
        author_stats.columns = ['Author', 'Banks Authored', 'Total Problems']
        author_stats = author_stats.sort_values('Banks Authored', ascending=False)
        
        # Display stats
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.dataframe(
                author_stats,
                use_container_width=True,
                hide_index=True
            )
        
        with col2:
            # Bar chart
            st.bar_chart(
                author_stats.set_index('Author')['Banks Authored'],
                use_container_width=True
            )
        
        # Detailed breakdown
        st.subheader("Detailed Breakdown")
        selected_author = st.selectbox(
            "Select author to view their banks",
            options=sorted(df['Author'].unique())
        )
        
        author_banks = df[df['Author'] == selected_author][['Topic', 'BankId', 'Title', 'Number of problems', 'Problem Type']]
        st.dataframe(author_banks, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Banks by Topic")
        
        # Group by topic
        topic_stats = df.groupby('Topic').agg({
            'BankId': 'count',
            'Number of problems': 'sum'
        }).reset_index()
        topic_stats.columns = ['Topic', 'Number of Banks', 'Total Problems']
        
        # Display stats
        st.dataframe(
            topic_stats,
            use_container_width=True,
            hide_index=True
        )
        
        # Bar chart
        st.bar_chart(
            topic_stats.set_index('Topic')['Number of Banks'],
            use_container_width=True
        )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### Actions")

if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

if st.sidebar.button("💾 Export to CSV"):
    csv = df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name="problem_banks_export.csv",
        mime="text/csv"
    )
