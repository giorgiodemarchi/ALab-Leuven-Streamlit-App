import boto3
import pandas as pd
import geopandas as gpd
from io import StringIO



def read_s3_file(file_path):
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

    # Read the object (in CSV format) as a pandas DataFrame
    df = pd.read_csv(StringIO(response['Body'].read().decode('utf-8')), index_col=0)

    return df


def load_data(bicycle_path, parking_path, demand_path):
    """
    Load all data from S3 and return geopandas dataframes
    """
    # Demand data
    demand_df = read_s3_file(demand_path)
    demand_gdf = gpd.GeoDataFrame(demand_df)
    
    # Parking data
    df_parking = read_s3_file(parking_path)
    df_parking = df_parking[['label', 'latitude', 'longitude', 'number_of_spots']]
    parking_gdf = gpd.GeoDataFrame(df_parking, geometry=gpd.points_from_xy(df_parking.longitude, df_parking.latitude))
    
    # Bicycle data
    df_bicycle = read_s3_file(bicycle_path)
    df_bicycle = df_bicycle.sample(n=100, random_state=42)
    bicycle_gdf = gpd.GeoDataFrame(df_bicycle, geometry=gpd.points_from_xy(df_bicycle['longitude'], df_bicycle['latitude']))
    
    return demand_gdf, parking_gdf, bicycle_gdf