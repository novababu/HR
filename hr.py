import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

# --- Data Loading ---
@st.cache_data
def load_data(file_path):
    """Loads the HR dataset from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        # Convert date columns to datetime objects
        for col in ['DateofHire', 'DateofTermination', 'LastPerformanceReview_Date']:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Please make sure the file is in the correct directory.")
        return None

df = load_data('HRDataset_v14.csv')

if df is not None:

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")
    
    # Department Filter
    department = st.sidebar.multiselect(
        "Select Department",
        options=df["Department"].unique(),
        default=df["Department"].unique()
    )

    # Gender Filter
    gender = st.sidebar.multiselect(
        "Select Gender",
        options=df["Sex"].unique(),
        default=df["Sex"].unique()
    )

    # Employment Status Filter
    employment_status = st.sidebar.multiselect(
        "Select Employment Status",
        options=df["EmploymentStatus"].unique(),
        default=df["EmploymentStatus"].unique()
    )

    # --- Filtering Data ---
    df_filtered = df.query(
        "Department == @department & Sex == @gender & EmploymentStatus == @employment_status"
    )

    # --- Main Dashboard ---
    st.title("📊 HR Analytics Dashboard")
    st.markdown("---")

    # --- Key Performance Indicators (KPIs) ---
    total_employees = df_filtered.shape[0]
    active_employees = df_filtered[df_filtered["EmploymentStatus"] == 'Active'].shape[0]
    terminated_employees = total_employees - active_employees
    avg_salary = int(df_filtered["Salary"].mean())
    avg_engagement = round(df_filtered["EngagementSurvey"].mean(), 2)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Employees", f"{total_employees:,}")
    with col2:
        st.metric("Active Employees", f"{active_employees:,}")
    with col3:
        st.metric("Terminated Employees", f"{terminated_employees:,}")
    with col4:
        st.metric("Average Salary", f"${avg_salary:,}")
    with col5:
        st.metric("Avg. Engagement", avg_engagement)

    st.markdown("---")

    # --- Visualizations ---
    col1, col2 = st.columns(2)

    with col1:
        # Gender Distribution
        st.subheader("Gender Distribution")
        gender_dist = df_filtered['Sex'].value_counts()
        fig_gender = px.pie(
            values=gender_dist.values, 
            names=gender_dist.index, 
            title='Gender Distribution',
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
        st.plotly_chart(fig_gender, use_container_width=True)

        # Recruitment Sources
        st.subheader("Recruitment Sources")
        recruitment_source = df_filtered['RecruitmentSource'].value_counts()
        fig_recruitment = px.bar(
            x=recruitment_source.index, 
            y=recruitment_source.values,
            title='Top Recruitment Sources',
            labels={'x': 'Source', 'y': 'Count'}
        )
        st.plotly_chart(fig_recruitment, use_container_width=True)


    with col2:
        # Department Distribution
        st.subheader("Department Distribution")
        dept_dist = df_filtered['Department'].value_counts()
        fig_dept = px.bar(
            y=dept_dist.index, 
            x=dept_dist.values, 
            orientation='h',
            title='Employee Count by Department',
            labels={'y': 'Department', 'x': 'Number of Employees'}
        )
        st.plotly_chart(fig_dept, use_container_width=True)
        
        # Termination Reasons
        st.subheader("Top Termination Reasons")
        term_reason = df_filtered['TermReason'].value_counts().nlargest(5)
        fig_term = px.pie(
            values=term_reason.values, 
            names=term_reason.index, 
            title='Top 5 Termination Reasons',
        )
        st.plotly_chart(fig_term, use_container_width=True)


    st.markdown("---")
    st.subheader("Salary Analysis")
    
    col1, col2 = st.columns(2)

    with col1:
        # Salary by Department
        st.write("#### Salary Distribution by Department")
        fig_salary_dept = px.box(
            df_filtered, 
            x='Department', 
            y='Salary', 
            title='Salary Distribution by Department',
            color='Department'
        )
        st.plotly_chart(fig_salary_dept, use_container_width=True)

    with col2:
        # Salary vs. Performance Score
        st.write("#### Salary vs. Performance Score")
        fig_salary_perf = px.scatter(
            df_filtered, 
            x='PerformanceScore', 
            y='Salary', 
            color='Department',
            title='Salary vs. Performance Score'
        )
        st.plotly_chart(fig_salary_perf, use_container_width=True)

    # --- Data Table ---
    st.markdown("---")
    st.subheader("Employee Data")
    st.dataframe(df_filtered)

else:
    st.warning("Could not load data. Please check the file path and try again.")
