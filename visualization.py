import geopandas as gpd
from io import StringIO
from keplergl import KeplerGl
import pandas as pd
import pydeck as pdk
import streamlit as st
from streamlit_keplergl import keplergl_static

from datasets import read_s3_file, load_data
from configs import kepler_config

def main():
    """
    Core App
    """
    # st.set_page_config(layout="wide")

    st.title("MIT Analytics Lab: Leuven Multi-Modal Mobility Hubs Dashboard")
    st.markdown("---")
    st.markdown("""### Part 1 - Visualizing the data
This part of the dashboard is to take a look at the current status of Leuveun sustainable mobility.""")


    ## LOAD DATA
    demand_gdf, parking_gdf, bicycle_gdf = load_data(bicycle_path = 'bike_distance_matrix.csv', parking_path = 'cleaned_parkings.csv', demand_path = 'dest_demand_zones.csv')

    ## GET INPUTS
    # Morning or evening
    times = ['Morning', 'Evening']
    time_of_day = st.radio("Select time of day:", times, horizontal=True)

    # Options
    options = ['Parking', 'Bicycle']
    selected_options = st.multiselect('Select options:', options)

    if time_of_day == 'Morning':
        selected_columns = ['dest', 'geometry', 'cars_7am']  # Need to sum it with 8am 
        target_variable = 'cars_7am'
        clean_variable = 'Cars 7AM'
    else:
        selected_columns = ['dest', 'geometry', 'cars_4pm']
        target_variable = 'cars_4pm'
        clean_variable = 'Cars 4PM'

    demand_gdf = demand_gdf[selected_columns]

    parking_label = 'label'
    parking_spots = 'number_of_spots'

    config = kepler_config(target_variable, clean_variable, selected_options, parking_label, parking_spots, selected_columns)

    ## CREATE MAP
    map_1 = KeplerGl(height=800)
    map_1.config = config

    map_1.add_data(data=demand_gdf, name='data_1')

    if 'Parking' in selected_options:
        map_1.add_data(data=parking_gdf, name='parking_data')

    if 'Bicycle' in selected_options:
        map_1.add_data(data=bicycle_gdf, name='bicycle_data')

    keplergl_static(map_1)

    st.markdown("---")
    st.markdown("""### Part 2 - Optimization Model for Hub Locations""")


main()