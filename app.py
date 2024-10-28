import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page configuration to wide mode
st.set_page_config(layout="wide")

# Load Data
@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    # Filter for positive new cases only
    df = df[df['new_cases'] > 0]
    return df

df = load_data()

st.sidebar.image("BeaverLogo.png", use_column_width=True)
# Sidebar options for user selection
st.sidebar.title("COVID-19 Dashboard")
st.sidebar.subheader("By: Greg Beaver")

st.sidebar.write("Data Source: Our World in Data")
st.sidebar.write("Source: https://covid.ourworldindata.org/data/owid-covid-data.csv")

country = st.sidebar.selectbox("Select Country", sorted(df['location'].unique()), index=sorted(df['location'].unique()).index("Canada"))

# Global metrics for new cases, deaths, and vaccinations
total_cases = int(df['new_cases'].dropna().sum())
total_deaths = int(df['new_deaths'].dropna().sum())
total_vaccinations = int(df['new_vaccinations'].dropna().sum())

st.title("Global COVID-19 Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Cases", f"{total_cases:,}")
col2.metric("Total Deaths", f"{total_deaths:,}")
col3.metric("Total Vaccinations", f"{total_vaccinations:,}")




# Localized Overview for Selected Country
st.header(f"COVID-19 Overview for {country}")
country_data = df[df['location'] == country]

country_cases = int(country_data['new_cases'].dropna().sum())
country_deaths = int(country_data['new_deaths'].dropna().sum())
country_vaccinations = int(country_data['new_vaccinations'].dropna().sum())

col1, col2, col3 = st.columns(3)
col1.metric(f"Total Cases in {country}", f"{country_cases:,}")
col2.metric(f"Total Deaths in {country}", f"{country_deaths:,}")
col3.metric(f"Total Vaccinations in {country}", f"{country_vaccinations:,}")

# Display the filtered DataFrame
st.subheader("Filtered Data for Positive New Cases")
st.dataframe(df[df['location'] == country])

# Trends Over Time for the Selected Country
st.header(f"COVID-19 Trends for {country}")

# Plot daily cases
fig_cases = px.line(country_data, x='date', y='new_cases', title=f"Daily New Cases in {country}")
st.plotly_chart(fig_cases, use_container_width=True)

# Plot daily vaccinations
fig_vaccinations = px.line(country_data, x='date', y='new_vaccinations', title=f"Daily New Vaccinations in {country}")
st.plotly_chart(fig_vaccinations, use_container_width=True)

# Country Comparison with default for Canada and the United States
st.header("Compare COVID-19 Cases Between Canada and the United States")
countries = st.multiselect("Select Countries", sorted(df['location'].unique()), default=["Canada", "United States"])
comparison_data = df[df['location'].isin(countries)]

fig_comparison = px.line(comparison_data, x='date', y='new_cases', color='location', title="Daily New Cases Comparison")
st.plotly_chart(fig_comparison, use_container_width=True)

# Visualization: Cumulative Global Trends Over Time
st.header("Global COVID-19 Cumulative Trends")

# Prepare cumulative data for the global overview
global_data = df.groupby('date').agg({
    'new_cases': 'sum',
    'new_deaths': 'sum',
    'new_vaccinations': 'sum'
}).cumsum().reset_index()

# Plot cumulative trends for cases, deaths, and vaccinations
fig_cumulative = px.line(
    global_data, x='date',
    y=['new_cases', 'new_deaths', 'new_vaccinations'],
    labels={'value': 'Cumulative Count', 'variable': 'Metric'},
    title="Cumulative Global Trends in Cases, Deaths, and Vaccinations"
)
fig_cumulative.update_layout(yaxis_title="Cumulative Count")
st.plotly_chart(fig_cumulative, use_container_width=True)
st.write("Disclaimer: The data presented may not be accurate, it's a representation of what is in the data, and has not been validated.")