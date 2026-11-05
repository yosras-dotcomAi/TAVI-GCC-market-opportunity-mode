import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="GCC TAVI Market & Clinical Dashboard",
    page_icon="🫀",
    layout="wide"
)

# Load Datasets from data folder
@st.cache_data
def load_data():
    cases_df = pd.read_csv("data/GCC_TAVI_Granular_Cases_Model.csv")
    hospitals_df = pd.read_csv("data/Target_Hospitals_Scoring.csv")
    return cases_df, hospitals_df

cases_df, hospitals_df = load_data()

# Sidebar Filters
st.sidebar.title("🔍 Strategic Filters")
selected_country = st.sidebar.multiselect("Select Country", options=cases_df['Country'].unique(), default=cases_df['Country'].unique())
selected_device = st.sidebar.multiselect("Select TAVI System", options=cases_df['Device_Brand'].unique(), default=cases_df['Device_Brand'].unique())
selected_risk = st.sidebar.multiselect("Risk Stratification", options=cases_df['Risk_Stratification'].unique(), default=cases_df['Risk_Stratification'].unique())

# Filter Data
filtered_df = cases_df[
    (cases_df['Country'].isin(selected_country)) &
    (cases_df['Device_Brand'].isin(selected_device)) &
    (cases_df['Risk_Stratification'].isin(selected_risk))
]

# Title & Executive Summary
st.title("🫀 GCC TAVI Market Opportunity & Clinical Performance Model")
st.markdown("*A Data-Driven Analytics Platform for Abbott Navitor™ Expansion across GCC Tertiary Centers*")

# Top KPI Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total TAVI Volume", f"{len(filtered_df):,}")
col2.metric("Abbott Navitor Share", f"{(filtered_df['Device_Brand'] == 'Abbott Navitor').mean():.1%}")
col3.metric("Procedural Success Rate", f"{filtered_df['Procedural_Success'].mean():.1%}")
col4.metric("NUPCO Procurement Share (KSA)", f"{(filtered_df['Procurement_Channel'] == 'NUPCO Framework (KSA)').mean():.1%}")

st.divider()

# Tabs for Structured Layout
tab1, tab2, tab3 = st.tabs(["📊 Market Volume & Scenarios", "🩺 Clinical Outcomes & PVL", "🏦 Hospital & NUPCO Mapping"])

with tab1:
    st.subheader("TAVI Procedure Volume Trends by Country")
    fig_vol = px.histogram(filtered_df, x="Year", color="Country", barmode="group", title="Annual Procedure Volume (2023 - 2026)")
    st.plotly_chart(fig_vol, use_container_width=True)
    
    st.subheader("Market Share Breakdown by Device System")
    fig_share = px.pie(filtered_df, names="Device_Brand", title="GCC TAVI Brand Share", hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_share, use_container_width=True)

with tab2:
    st.subheader("30-Day Paravalvular Leak (PVL) Severity Comparison")
    fig_pvl = px.histogram(filtered_df, x="Device_Brand", color="PVL_Severity_30D", barmode="fill", title="PVL Safety Profile Across TAVI Systems")
    st.plotly_chart(fig_pvl, use_container_width=True)

with tab3:
    st.subheader("Target Hospital Network & Procurement Channels")
    fig_hosp = px.bar(filtered_df, x="Hospital_Name", color="Procurement_Channel", title="Procedure Volume by Center and Contract Framework")
    st.plotly_chart(fig_hosp, use_container_width=True)
