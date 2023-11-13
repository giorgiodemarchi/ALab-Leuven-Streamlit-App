import pandas as pd
import geopandas as gpd
import streamlit as st
import json
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
from streamlit_folium import folium_static

from datasets import load_data
from map_utils import create_map




st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center;'>Leuven Multi-Modal Mobility Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""-""")

demand_gdf, parking_gdf, bicycle_gdf, multi_modal_hubs_gdf, model_output_dfs = load_data(bicycle_path = 'cycling_network.gpkg', 
                                                                                        parking_path = 'dashboard_cleaned_parkings.csv', 
                                                                                        demand_path = 'dashboard_cleaned_demand.geojson',
                                                                                        current_hubs_path = 'dashboard_cleaned_multimodal_hubs.csv')


r1_1, r1_2, r1_3, r1_4 = st.columns((1,2,4,1))

with r1_2:
    ### MAP 1
    st.markdown("""#### Explore the current status of Leuveun sustainable mobility""")
    times = ['Morning', 'Evening']
    time_of_day = st.radio("Select time of day:", times, horizontal=True)
    st.markdown("""""")
    parkings_selected = st.toggle("Show parkings", value=False)
    st.markdown("""""")

    hubs_selected = st.toggle("Show active multi-modal hubs", value=False)
    st.markdown("""""")

    bike_network = st.toggle("Show bike network", value=False)
    st.markdown("""""")

    public_network = st.toggle("Show public transportation network", value=False)
with r1_3:


    folium_map = create_map(demand_gdf, time_of_day, 
                            parking_gdf, parkings_selected, 
                            multi_modal_hubs_gdf, hubs_selected, 
                            bicycle_gdf, bike_network, 
                            public_network)

    # Display the map in the Streamlit app
    folium_static(folium_map)


st.markdown("""---""")
st.markdown("<h2 style='text-align: center;'>Model Output: Optimal Multi-Modal Hubs Network</h2>", unsafe_allow_html=True)
st.markdown("""""")

r2_1, r2_2, r2_3 = st.columns((1,6,1))



with r2_2:
    st.markdown("<p style='text-align: center;'><strong>Usage instructions<\strong>: Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Id venenatis a condimentum vitae sapien. Massa enim nec dui nunc mattis enim ut. At erat pellentesque adipiscing commodo elit at. Duis ultricies lacus sed turpis tincidunt id aliquet. Rhoncus est pellentesque elit ullamcorper. Venenatis urna cursus eget nunc scelerisque viverra mauris in. Ultrices neque ornare aenean euismod elementum nisi. Quis risus sed vulputate odio ut enim blandit volutpat. Gravida quis blandit turpis cursus in. Venenatis tellus in metus vulputate eu scelerisque.</p>", unsafe_allow_html=True)


    ## Load Output Data
    h_t_z_bike = model_output_dfs[0]
    h_t_z_public = model_output_dfs[1]
    hubs = model_output_dfs[2]
    z_t_h_cars = model_output_dfs[3]
    z_t_z_cars = model_output_dfs[4]

    kepler_config_big_map = json.load(open("full_map_config.json"))

    map_1 = KeplerGl(height=600)
    map_1.config = kepler_config_big_map

    map_1.add_data(data=demand_gdf, name='u0hmlhh9')
    
    map_1.add_data(data=h_t_z_bike, name='80ajktlm')
    map_1.add_data(data=h_t_z_public, name='od92cjex8')

    map_1.add_data(data=z_t_h_cars, name='no4eo4w4b')

    map_1.add_data(data=z_t_z_cars, name='77njwmcqp')

    map_1.add_data(data=hubs, name='osayxfchxj')
    
    keplergl_static(map_1)


st.markdown("<br><br><h4 style='text-align: center;'>More visualization to come !</h4>", unsafe_allow_html=True)