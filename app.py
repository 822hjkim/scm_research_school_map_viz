import streamlit as st
import pandas as pd
import plotly.express as px

# Setup page title
st.set_page_config(page_title="School Rankings Map", layout="wide")
st.title("School Rankings Geographical Analysis")

# Load data (Cached for performance)
@st.cache_data
def load_data():
    return pd.read_csv('geocoded_schools_success.csv')

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("Filter Data")

# 1. Journal Category Dropdown
categories = df['Journal Category'].dropna().unique().tolist()
selected_category = st.sidebar.selectbox("Select Journal Category", categories)

# 2. Rank Slider
min_rank = int(df['Rank'].min())
max_rank = int(df['Rank'].max())
selected_rank_range = st.sidebar.slider(
    "Select Rank Range", 
    min_value=min_rank, 
    max_value=max_rank, 
    value=(min_rank, 50) # Default to top 50
)

# --- Apply Filters ---
filtered_df = df[
    (df['Journal Category'] == selected_category) & 
    (df['Rank'] >= selected_rank_range[0]) & 
    (df['Rank'] <= selected_rank_range[1])
]

# --- Render Map ---
st.write(f"### Showing {len(filtered_df)} schools for '{selected_category}' (Rank {selected_rank_range[0]} - {selected_rank_range[1]})")

fig = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Affiliation",
    hover_data=["Rank", "School Weight"],
    color="Rank",
    color_continuous_scale="Plasma_r",
    zoom=1.2,
    height=600
)

fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0})
fig.update_traces(marker=dict(size=10, opacity=0.8))

# Display the Plotly figure in Streamlit
st.plotly_chart(fig, use_container_width=True)