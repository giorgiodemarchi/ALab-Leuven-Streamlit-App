import pandas as pd
import geopandas as gpd
import numpy as np
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

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = True
    st.session_state.demand_gdf, st.session_state.parking_gdf, st.session_state.bicycle_gdf, st.session_state.multi_modal_hubs_gdf, st.session_state.bus_gdf, st.session_state.model_output_dfs = load_data()

# Use data from session state
demand_gdf = st.session_state.demand_gdf
parking_gdf = st.session_state.parking_gdf
bicycle_gdf = st.session_state.bicycle_gdf
multi_modal_hubs_gdf = st.session_state.multi_modal_hubs_gdf
bus_gdf = st.session_state.bus_gdf
model_output_dfs = st.session_state.model_output_dfs

r1_1, r1_2, r1_3, r1_4 = st.columns((1,2,4,1))

with r1_2:
    ### MAP 1
    st.markdown("""#### Explore the current status of Leuveun sustainable mobility""")

    display_choice = st.radio("Select what to visualize:", ['Transportation demand', 'Transportation Infrastructure'], horizontal=True)

    if display_choice == 'Transportation demand':
        times = ['Morning', 'Evening']
        time_of_day = st.radio("Select time of day:", times, horizontal=True)
    else:
        st.markdown("""""")
        parkings_selected = st.toggle("Show parkings", value=True)
        st.markdown("""""")
        hubs_selected = st.toggle("Show active multi-modal hubs", value=True)
        st.markdown("""""")
        bike_network = st.toggle("Show bike network", value=True)
        st.markdown("""""")
        public_network = st.toggle("Show public transportation network", value=True)

with r1_3:


    #folium_map = create_map(demand_gdf, time_of_day, 
    #                        parking_gdf, parkings_selected, 
    #                        multi_modal_hubs_gdf, hubs_selected, 
    #                        bicycle_gdf, bike_network, 
    #                        public_network)

    # Display the map in the Streamlit app
    #folium_static(folium_map)
    
    if display_choice == 'Transportation demand':

        map_0 = KeplerGl(height=500)
        # Remove layers based on the time of day
        if time_of_day == 'Morning':
            demand_config = json.load(open("kepler_configs/config_demand.json"))
            del demand_config['config']['visState']['layers'][1]
            map_0.config = demand_config
        else:
            demand_config = json.load(open("kepler_configs/config_demand.json"))
            del demand_config['config']['visState']['layers'][0]
            map_0.config = demand_config
        
        demand_gdf_json = demand_gdf.to_json()
        map_0.add_data(data=demand_gdf_json, name='zh3y8x52m')
        keplergl_static(map_0)

    if display_choice == 'Transportation Infrastructure':
        kepler_config = json.load(open("kepler_configs/config.json"))
        map_2 = KeplerGl(height=500)
        map_2.config = kepler_config
        if parkings_selected:
            map_2.add_data(data=parking_gdf, name='uq0612x6m')
        if hubs_selected:
            map_2.add_data(data=multi_modal_hubs_gdf, name='4cfur20k7f')
        if bike_network:
            map_2.add_data(data=bicycle_gdf, name='culgs8x6')
        if public_network:
            map_2.add_data(data=bus_gdf, name='9nomcba5p')
    
        keplergl_static(map_2)


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


st.markdown("""""")
st.markdown("<h3 style='text-align: center;'>Model Output: Hubs and KPIs</h3>", unsafe_allow_html=True)
st.markdown("""""")

r3_1, r3_2, r3_3, r3_4 =  st.columns((1,3,3,1))

with r3_2:

    st.markdown("<h4 style='text-align: center;'>Multi-Modal Hubs</h4>", unsafe_allow_html=True)
    
    map_2 = KeplerGl(height=450, read_only=True)
    map_2.config = kepler_config_big_map

    map_2.add_data(data=hubs, name='osayxfchxj')
    keplergl_static(map_2)


with r3_3:

    st.markdown("<h4 style='text-align: center;'>KPIs</h4>", unsafe_allow_html=True)
    kpi_df = pd.DataFrame({'KPI':['CO2 Emissions', 'Travel Time'], 'Change':['-10%', '+3%']})
    st.table(kpi_df)
    
    st.markdown("<h4 style='text-align: center;'>Hubs Details</h4>", unsafe_allow_html=True)
    hubs_info_df = df = pd.DataFrame(np.random.randn(10, 4), columns=['Hub','Location','Parking Spots','Prescription'])
    st.table(hubs_info_df)


st.markdown("<br><br><h4 style='text-align: center;'>More visualization to come !</h4>", unsafe_allow_html=True)