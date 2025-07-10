
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("HRDataset_v14.csv")

# Page setup
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")
st.title("👥 Human Resources Analytics Dashboard")

# Sidebar filters
st.sidebar.header("🔎 Filter Data")
departments = st.sidebar.multiselect("Select Department", options=df["Department"].unique(), default=df["Department"].unique())
genders = st.sidebar.multiselect("Select Gender", options=df["GenderID"].unique(), default=df["GenderID"].unique())

# Apply filters
df_filtered = df[(df["Department"].isin(departments)) & (df["GenderID"].isin(genders))]

# KPIs
total_employees = len(df_filtered)
avg_age = round(df_filtered["Age"].mean(), 1)
avg_performance = round(df_filtered["PerformanceScore"].mean(), 2)
active_count = df_filtered[df_filtered["Termd"] == 0].shape[0]
terminated_count = df_filtered[df_filtered["Termd"] == 1].shape[0]

st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Employees", total_employees)
col2.metric("Average Age", avg_age)
col3.metric("Avg. Performance", avg_performance)
col4.metric("Active / Terminated", f"{active_count} / {terminated_count}")

# --- Charts ---
st.markdown("### 📈 Visual Insights")

# Age distribution
fig_age = px.histogram(df_filtered, x="Age", nbins=20, title="Age Distribution", color_discrete_sequence=["#636EFA"])
# Gender distribution
fig_gender = px.pie(df_filtered, names="Sex", title="Gender Distribution", hole=0.4)
# Department count
fig_dept = px.bar(df_filtered["Department"].value_counts().reset_index(), x='index', y='Department',
                  labels={'index':'Department', 'Department':'Count'}, title="Department Breakdown")
# Termination Reasons
fig_term_reason = px.histogram(df_filtered[df_filtered["Termd"]==1], x="TermReason", title="Termination Reasons", color_discrete_sequence=["#EF553B"])
# Performance score distribution
fig_perf = px.histogram(df_filtered, x="PerformanceScore", title="Performance Score Distribution", nbins=10)

# Layout
col1, col2 = st.columns(2)
col1.plotly_chart(fig_age, use_container_width=True)
col2.plotly_chart(fig_gender, use_container_width=True)

col3, col4 = st.columns(2)
col3.plotly_chart(fig_dept, use_container_width=True)
col4.plotly_chart(fig_term_reason, use_container_width=True)

st.plotly_chart(fig_perf, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | Dataset © Carla Patalano & Rich Huebner").

 

 
