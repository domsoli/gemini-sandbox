
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    return pd.read_parquet('insurance_dataset.parquet')

df = load_data()

# Sidebar
st.sidebar.title('Filters')

# Coverage filter
coverage = st.sidebar.selectbox(
    'Select Coverage',
    options=df['coverage'].unique(),
    index=0
)

# Open claims filter
open_claims_only = st.sidebar.checkbox('Show only open claims')

# Bin size input
num_bins = st.sidebar.number_input('Select the number of bins:', min_value=10, max_value=500, value=100, step=10)

# Filter the data
filtered_df = df[df['coverage'] == coverage]
if open_claims_only:
    filtered_df = filtered_df[filtered_df['claim_status_open'] == True]

# X-axis range inputs
min_val = 0.0
p99 = 1.0
if not filtered_df.empty:
    min_val = filtered_df['claims_cost'].min()
    p99 = filtered_df['claims_cost'].quantile(0.99)

x_min = st.sidebar.number_input('Min X value', value=min_val, format="%.2f")
x_max = st.sidebar.number_input('Max X value', value=p99, format="%.2f")

# Main page
st.title('Insurance Claims Data Visualization')

# Plot cost distribution
st.subheader('Claim Cost Distribution')


filtered_df = filtered_df[(filtered_df['claims_cost'] < x_max) & (filtered_df['claims_cost'] > x_min)]

fig = px.histogram(filtered_df, x='claims_cost', nbins=num_bins, log_y=True, range_x=[x_min, x_max])
st.plotly_chart(fig)
