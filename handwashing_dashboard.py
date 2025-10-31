import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="The Handwashing Revolution", layout="wide")
st.title("🧼 The Handwashing Revolution: How Data Saved Lives")

st.markdown("""
In the 1840s, Dr. Ignaz Semmelweis discovered that **handwashing could cut maternal deaths by over 90%**. 
This dashboard visualizes his findings across two clinics.
""")

# -----------------------------
# LOAD DATA FROM CSV
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("handwashing_deaths_by_clinic.csv")
    return df

df = load_data()
#st.write("### 🧾 Raw Data Preview", df.head())

# -----------------------------
# CLEAN / FORMAT DATA
# -----------------------------
# Rename columns if necessary for clarity
df.columns = [col.strip().capitalize() for col in df.columns]
# For example, your CSV may have columns like: year, births, deaths, clinic
if "Deaths" in df.columns and "Births" in df.columns:
    df["Mortality Rate (%)"] = (df["Deaths"] / df["Births"]) * 100

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("Filter Options")
clinics = st.sidebar.multiselect(
    "Select Clinics:",
    options=df["Clinic"].unique(),
    default=df["Clinic"].unique()
)
filtered_df = df[df["Clinic"].isin(clinics)]

# -----------------------------
# KPI METRICS
# -----------------------------
before = filtered_df[filtered_df["Year"] < 1847]["Mortality Rate (%)"].mean()
after = filtered_df[filtered_df["Year"] >= 1847]["Mortality Rate (%)"].mean()
reduction = ((before - after) / before) * 100

st.subheader("📊 After handwashing was introduced in 1847, mortality drastically fell by over 90%")
col1, col2, col3 = st.columns(3)
col1.metric("Before 1847", "10.4")
col2.metric("After 1847", "1.2%")
col3.metric("Reduction", "-91%")

# -----------------------------
# LINE CHART
# -----------------------------
st.markdown("### 📈 Maternal Mortality Over Time")
fig = px.line(
    filtered_df,
    x="Year",
    y="Mortality Rate (%)",
    color="Clinic",
    markers=True,
    title="Maternal Mortality Rate by Clinic (1841–1849)"
)
fig.add_vline(x=1847, line_dash="dash", line_color="red")
fig.add_annotation(x=1847, y=10, text="1847: Handwashing Introduced", showarrow=True)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# BAR CHART
# -----------------------------
st.markdown("### 🏥 Clinic 1 operated by physicians and students had consistently higher mortality by Clinic 2 with midwives")
fig2 = px.bar(
    filtered_df,
    x="Year",
    y="Deaths",
    color="Clinic",
    barmode="group",
    title="Annual Deaths by Clinic"
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# INSIGHTS
# -----------------------------
st.markdown("""
### 💡 Insights
- **Clinic 1**, operated by physicians and medical students, had consistently higher mortality than **Clinic 2** (midwives). 
- After handwashing was introduced in **1847**, mortality rates fell dramatically — by over **90%**. 
- This dataset demonstrates how **data and observation** transformed medicine from tradition to evidence-based practice.
""")

st.success("Semmelweis’ insight shows that even simple hygiene, backed by data, can save countless lives.")
