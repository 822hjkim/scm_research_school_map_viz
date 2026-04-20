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

# 1. Journal Category Multiselect
categories = df['Journal Category'].dropna().unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Select Journal Categories", 
    options=categories, 
    default=categories
)

# 2. Rank Slider
min_rank = int(df['Rank'].min())
max_rank = int(df['Rank'].max())
selected_rank_range = st.sidebar.slider(
    "Select Rank Range", 
    min_value=min_rank, 
    max_value=max_rank, 
    value=(min_rank, 50)
)

# --- Apply Filters ---
filtered_df = df[
    (df['Journal Category'].isin(selected_categories)) & 
    (df['Rank'] >= selected_rank_range[0]) & 
    (df['Rank'] <= selected_rank_range[1])
].copy()

# --- Render Map ---
st.write(f"### Showing {len(filtered_df)} schools (Rank {selected_rank_range[0]} - {selected_rank_range[1]})")

# Map visualization
# color="Rank" restores your progression
# symbol="Journal Category" distinguishes the types of schools visually
fig = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    hover_name="Affiliation",
    hover_data={
        "Latitude": False, 
        "Longitude": False, 
        "Rank": True, 
        "School Weight": True, 
        "Journal Category": True
    },
    color="Rank",
    symbol="Journal Category", 
    color_continuous_scale="Plasma_r",
    size_max=15,
    zoom=1.2,
    height=700
)

# --- Layout and Interaction Configuration ---
fig.update_layout(
    mapbox_style="open-street-map", 
    margin={"r":0,"t":0,"l":0,"b":0},
    mapbox=dict(
        center={"lat": filtered_df["Latitude"].mean() if not filtered_df.empty else 0, 
                "lon": filtered_df["Longitude"].mean() if not filtered_df.empty else 0}, 
        zoom=1.2
    ),
    # Moving the legend and colorbar for better visibility
    coloraxis_colorbar=dict(title="Rank", thickness=20, len=0.5, y=0.2),
    legend=dict(title="Category", yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.5)")
)

fig.update_traces(marker=dict(size=12, opacity=0.8))

# Display in Streamlit with scrollZoom enabled
st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})
