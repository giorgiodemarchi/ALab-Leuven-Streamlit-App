import boto3
import pandas as pd
import geopandas as gpd
from io import StringIO, BytesIO
import streamlit as st
import numpy as np

def read_s3_file(file_path, type):
    """
    Reads files from S3 bucket
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=st.secrets['access_key'],
        aws_secret_access_key=st.secrets['secret_access_key']
    )

    bucket_name = 'alab-akkodis-project'
    object_key = file_path

    # Get the object from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)

    if type =='csv':
        # Read the object (in CSV format) as a pandas DataFrame
        df = pd.read_csv(StringIO(response['Body'].read().decode('utf-8')), index_col=0)

    if type == 'geojson':
        # Read the object (in GeoJSON format) as a GeoPandas GeoDataFrame
        df = gpd.read_file(BytesIO(response['Body'].read()), geometry='geometry')
    
    if type == 'gpkg':
        # Read the object (in GPKG format) as a GeoPandas GeoDataFrame
        df = gpd.read_file(BytesIO(response['Body'].read()), driver='GPKG')

    return df


def load_data():
    """
    Load all data from S3 and return geopandas dataframes
    """

    bicycle_path = 'cycling_network.gpkg'
    parking_path = 'dashboard_cleaned_parkings.csv'
    demand_path = 'dashboard_cleaned_demand.geojson'
    current_hubs_path = 'dashboard_cleaned_multimodal_hubs.csv'
    bus_stops_path = 'dashboard_cleaned_bus_stops.csv'


    # Demand data
    demand_gdf = read_s3_file(demand_path, type='geojson')
    #demand_gdf = demand_gdf.to_crs(epsg=3857)

    # Parking data
    df_parking = read_s3_file(parking_path, type='csv')
    parking_gdf = df_parking[['latitude','longitude', 'number_of_spots']]

    # Bicycle data
    bicycle_gdf = read_s3_file(bicycle_path, type='gpkg')
    bicycle_gdf = bicycle_gdf[['geometry']].reset_index()
    bicycle_gdf = bicycle_gdf.to_crs(epsg=4326)
    bicycle_gdf.columns = ['id','geometry']
    bicycle_gdf = bicycle_gdf.to_json()

    # Mutli-modal hub
    df_current_hubs = read_s3_file(current_hubs_path, type='csv')
    df_current_hubs = df_current_hubs[['latitude', 'longitude']]
    current_hubs_gdf = gpd.GeoDataFrame(df_current_hubs, geometry=gpd.points_from_xy(df_current_hubs['longitude'], df_current_hubs['latitude']))
    current_hubs_gdf = current_hubs_gdf.set_crs(epsg=3857, allow_override=True)

    # Bus Stops
    df_bus = read_s3_file(bus_stops_path, type= 'csv')
    df_bus = df_bus[['latitude', 'longitude']]
    bus_gdf = gpd.GeoDataFrame(df_bus, geometry=gpd.points_from_xy(df_bus['longitude'], df_bus['latitude']))
    bus_gdf = bus_gdf.set_crs(epsg=3857, allow_override=True)

    # Centroids lat and long
    centroids_df = read_s3_file('centroids_data.csv', type='csv')
    centroids_df = centroids_df.reset_index().reset_index().drop(columns=['index', 'Zone']).rename(columns={'level_0':'Zone'})

    # Hubs info
    hubs_info = read_s3_file('hubs_with_address.csv', type='csv')

    # MODEL OUTPUT dataframes
    versions = [10, 15, 20, 25]

    version_df_dict = {}

    for version in versions:
        base_path = "V4 Model Output/" + str(version) + "/"

        z_t_h_bike = read_s3_file(base_path + 'BH_solution.csv', type='csv')
        z_t_h_bike = z_t_h_bike.reset_index()

        h_t_z_bike = read_s3_file(base_path + 'BZ_solution.csv', type='csv')
        h_t_z_bike = h_t_z_bike.reset_index()

        h_t_z_public = read_s3_file(base_path + 'PZ_solution.csv', type='csv')
        h_t_z_public = h_t_z_public.reset_index()

        z_t_h_public = read_s3_file(base_path + 'PH_solution.csv', type='csv')
        z_t_h_public = z_t_h_public.reset_index()

        z_t_h_cars = read_s3_file(base_path + 'CH_solution.csv', type='csv')
        z_t_h_cars = z_t_h_cars.reset_index()

        z_t_z_cars = read_s3_file(base_path + 'CD_solution.csv', type='csv')
        z_t_z_cars = z_t_z_cars.reset_index()

        hubs = read_s3_file(base_path + 'Hub_solution.csv', type='csv')
        hubs = hubs.reset_index().reset_index()

        version_df_dict[version] = [h_t_z_bike, z_t_h_bike, h_t_z_public, z_t_h_public, z_t_h_cars, z_t_z_cars, hubs]
    
    return demand_gdf, parking_gdf, bicycle_gdf, current_hubs_gdf, bus_gdf, version_df_dict