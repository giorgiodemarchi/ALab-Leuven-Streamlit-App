import pandas as pd
import geopandas as gpd
import numpy as np
import streamlit as st
import json
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
import base64
import matplotlib.pyplot as plt

from datasets import load_data
from plot_utils import plot_gamma

st.set_page_config(layout="wide")

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# Convert image to base64 string
encoded_image = get_image_base64("logo-nobg.png")

# HTML to display the image
image_html = f"""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{encoded_image}' style='width: 300px;'>
    </div>
"""

st.markdown(image_html, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Leuven Multi-Modal Mobility Dashboard</h1>", unsafe_allow_html=True)

st.markdown("""""")
st.markdown("<p style='text-align: center;'>Welcome! This dashboard provides an overview of the project carried out as part of the MIT Analytics Lab initiative.<br>In the first secion of the dashboard, you can explore the current status of Leuven transportation infrastracture, as well as the transportation demand by zone.<br>The second section gives an overview of our optimization models, which design a network of multimodal hubs while minimizing travel time and CO2 emissions due to transport.</p>", unsafe_allow_html=True)
st.markdown("""---""")

if 'data_loaded' not in st.session_state:
    try:
        st.session_state.data_loaded = True
        st.session_state.demand_gdf, st.session_state.parking_gdf, st.session_state.bicycle_gdf, st.session_state.multi_modal_hubs_gdf, st.session_state.bus_gdf, st.session_state.version_df_dict = load_data()
    except Exception as e:
        st.error("Internal Error :( Apologies!")
        st.error(e)

# Use data from session state
demand_gdf = st.session_state.demand_gdf
parking_gdf = st.session_state.parking_gdf
bicycle_gdf = st.session_state.bicycle_gdf
multi_modal_hubs_gdf = st.session_state.multi_modal_hubs_gdf
bus_gdf = st.session_state.bus_gdf

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

    st.markdown("""---""")
    st.markdown("""*To see the legend, click on the icon on the top right of the map""")
with r1_3:

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

def convert_gamma(selected_gamma):
    if selected_gamma == 'Aggressive':
        return 0.86, 'gamma086'
    elif selected_gamma == 'Moderate':
        return 1.7, 'gamma170'
    else:
        return 2.57, 'gamma257'

with r2_2:
    st.markdown("<p style='text-align: center;'>This section is meant to give an overview of the output of the our optimization model. The model aims at designing a network of multi-modal hubs that minimizes travel time and CO2 emissions due to transport. In order to do so, it evaluates the installation of around 100 different candidate and selects the hubs that yields the best change in the objective. A key parameter of our model is the maximum number of hubs to be installed. This is function of the investment budget and hence we offer four different network designs for four different number of maximum hubs. The large map below displays the output for all 30 million variables included in the model. Because of the number of variables displayed, this visualization is meant for advanced users only. It is possible to regulate the map, change colors, and filter variables by opening the menu at top left. The legend is available on top right.  </p>", unsafe_allow_html=True)
    st.markdown("""""")

    data = {
    'Gamma': [0.86, 0.86, 0.86, 0.86, 1.7, 1.7, 1.7, 1.7, 2.57, 2.57, 2.57, 2.57],
    'Maximum Hubs': ['10', '15', '20', '25', '10', '15', '20', '25', '10', '15', '20', '25'],
    'CO2 Decrease Against Baseline (%)': [-7.5, -9.3, -11.1, -12, -3, -3.9, -4.6, -5.4, -1.9, -2.6, -3.1, -3.6],
    'Time Increase Against Baseline (%)': [11.3, 14.2, 17.1, 17.2, 1.5, 2.1, 2.4, 2.8, 0.3, 0.4, 0.5, 0.6]
    }

    kpi_tot_df = pd.DataFrame(data)
    fig = plot_gamma(kpi_tot_df)
    st.pyplot(fig)

    st.markdown("""""")
    
    _, subcol1, subcol2, _ = st.columns((2,1,1,2))
    with subcol1:
        models = ['10', '15', '20', '25']
        selected_model = st.radio("Select number of hubs", models, horizontal=False)
        version = int(selected_model)    

    with subcol2:
        gamma = ['Aggressive', 'Medium','Conservative'] 
        selected_gamma = st.radio("Select willingness to trade-off CO2 for travel time", gamma, horizontal=False)
        num_gamma, str_gamma = convert_gamma(selected_gamma)

    st.markdown("""""")
    st.markdown("""""")

    # Read the data for the selected version
    h_t_z_bike = st.session_state.version_df_dict[version][str_gamma][0]
    z_t_h_bike = st.session_state.version_df_dict[version][str_gamma][1]

    h_t_z_public = st.session_state.version_df_dict[version][str_gamma][2]
    z_t_h_public = st.session_state.version_df_dict[version][str_gamma][3]

    z_t_h_cars = st.session_state.version_df_dict[version][str_gamma][4]
    z_t_z_cars = st.session_state.version_df_dict[version][str_gamma][5]

    hubs = st.session_state.version_df_dict[version][str_gamma][6]
    hubs = hubs[hubs['value']==1]

    # Create map
    map_1 = KeplerGl(height=600)
    kepler_config_big_map = json.load(open("kepler_configs/full_map_config.json"))
    map_1.config = kepler_config_big_map

    demand_gdf_json = demand_gdf.to_json()
    map_1.add_data(data=demand_gdf_json, name='Demand/Zones-data')

    map_1.add_data(data=z_t_h_bike, name='Bike-Zone-To-Hub')
    map_1.add_data(data=h_t_z_bike, name='Bike-Hub-To-Zone')

    map_1.add_data(data=h_t_z_public, name='Public-Hub-To-Zone')
    map_1.add_data(data=z_t_h_public, name='Public-Zone-To-Hub') #

    map_1.add_data(data=z_t_h_cars, name='Car-Zone-To-Hub')
    map_1.add_data(data=z_t_z_cars, name='Car-Zone-To-Zone') #eyec5whl

    map_1.add_data(data=hubs, name='Hubs')
    
    keplergl_static(map_1)

    st.markdown("""*To see the legend, click on the icon on the top right of the map""")

st.markdown("""""")
st.markdown("<br><h3 style='text-align: center;'>Model Output: Hubs and KPIs</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'>This version picked {len(hubs)} optimal hubs, which you can explore below. The resulting objective values are also reported in the table on the right.", unsafe_allow_html=True)
    
st.markdown("""""")


r3_1, r3_2, r3_3, r3_4 =  st.columns((1,3,2,1))

with r3_2:
    #st.markdown("<h4 style='text-align: center;'>Multi-Modal Hubs</h4>", unsafe_allow_html=True)
    map_2 = KeplerGl(height=400, read_only=True)
    map_2.config = kepler_config_big_map

    map_2.add_data(data=hubs, name='Hubs')
    keplergl_static(map_2)


with r3_3:


    kpi_df = kpi_tot_df[(kpi_tot_df['Maximum Hubs']==selected_model) & (kpi_tot_df['Gamma']==num_gamma)].transpose()
    kpi_df.columns = ['Value']
    st.table(kpi_df)


st.markdown("""""")
st.markdown("<br><h3 style='text-align: center;'>Granular Analysis</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Finally, this section provides a list of recommended locations (hubs), their addresses, and the final recommendation of our model. <br>You can further explore the expected flow in each one of the hub by selecting the hub in analysis on the map on the right.</p>", unsafe_allow_html=True)
st.markdown("""""")

r4_1, r4_2, r4_3, r4_4 =  st.columns((1,2,2,1))


with r4_2:
    # Hubs menu
    with st.expander('Show Hubs Details', expanded=True):
        st.markdown("<h4 style='text-align: center;'>Hubs Details</h4>", unsafe_allow_html=True)
        hubs_table_df = hubs[['hub_id','address']]
        hubs_table_df.columns = ['Hub ID', 'Address']
        st.table(hubs_table_df)

with r4_3:

    hub = st.multiselect("Select a hub", hubs['hub_id'].unique(), default=hubs['hub_id'].unique()[0])

    # Create map
    map_2 = KeplerGl(height=500, read_only=True)
    map_2.config = kepler_config_big_map

    demand_gdf_json = demand_gdf.to_json()
    map_2.add_data(data=demand_gdf_json, name='Demand/Zones-data')

    map_2.add_data(data=z_t_h_bike[z_t_h_bike['k'].isin(hub)], name='Bike-Zone-To-Hub')
    map_2.add_data(data=h_t_z_bike[h_t_z_bike['k'].isin(hub)], name='Bike-Hub-To-Zone')

    map_2.add_data(data=h_t_z_public[h_t_z_public['k'].isin(hub)], name='Public-Hub-To-Zone')
    map_2.add_data(data=z_t_h_public[h_t_z_public['k'].isin(hub)], name='Public-Zone-To-Hub') #

    map_2.add_data(data=z_t_h_cars[z_t_h_cars['k'].isin(hub)], name='Cars-Zone-To-Hub')

    map_2.add_data(data=hubs[hubs['hub_id'].isin(hub)], name='Hubs')
    keplergl_static(map_2)
    st.markdown("""*To see the legend, click on the icon on the top right of the map""")



