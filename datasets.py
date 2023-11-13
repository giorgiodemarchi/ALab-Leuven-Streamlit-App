import boto3
import pandas as pd
import geopandas as gpd
from io import StringIO, BytesIO
import streamlit as st

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
        df = gpd.read_file(BytesIO(response['Body'].read()))
    
    if type == 'gpkg':
        # Read the object (in GPKG format) as a GeoPandas GeoDataFrame
        df = gpd.read_file(BytesIO(response['Body'].read()), driver='GPKG')

    return df


def load_data(bicycle_path, parking_path, demand_path, current_hubs_path):
    """
    Load all data from S3 and return geopandas dataframes
    """
    # Demand data
    demand_gdf = read_s3_file(demand_path, type='geojson')
    demand_gdf = demand_gdf.set_crs(epsg=3857, allow_override=True)

    # Parking data
    df_parking = read_s3_file(parking_path, type='csv')
    parking_gdf = gpd.GeoDataFrame(df_parking, geometry=gpd.points_from_xy(df_parking.longitude, df_parking.latitude))
    parking_gdf = parking_gdf[['geometry', 'number_of_spots']]
    parking_gdf = parking_gdf.set_crs(epsg=3857, allow_override=True)

    # Bicycle data
    bicycle_gdf = read_s3_file(bicycle_path, type='gpkg')
    bicycle_gdf = bicycle_gdf[['geometry']].reset_index()
    bicycle_gdf = bicycle_gdf.set_crs(epsg=3857, allow_override=True)
    bicycle_gdf.columns = ['id','geometry']

    # Mutli-modal hub
    df_current_hubs = read_s3_file(current_hubs_path, type='csv')
    df_current_hubs = df_current_hubs[['latitude', 'longitude']]
    current_hubs_gdf = gpd.GeoDataFrame(df_current_hubs, geometry=gpd.points_from_xy(df_current_hubs['longitude'], df_current_hubs['latitude']))
    current_hubs_gdf = current_hubs_gdf.set_crs(epsg=3857, allow_override=True)


    # MODEL OUTPUT dataframes
    h_t_z_bike = read_s3_file('ModelOutput/hub-to-zone-bikes.csv', type='csv')
    h_t_z_public = read_s3_file('ModelOutput/hub-to-zone-public.csv', type='csv')
    hubs = read_s3_file('ModelOutput/hubs.csv', type='csv')
    z_t_h_cars = read_s3_file('ModelOutput/zone-to-hub-cars.csv', type='csv')
    z_t_z_cars = read_s3_file('ModelOutput/zone-to-zone-cars.csv', type='csv')


    return demand_gdf, parking_gdf, bicycle_gdf, current_hubs_gdf, [h_t_z_bike, h_t_z_public, hubs, z_t_h_cars, z_t_z_cars]