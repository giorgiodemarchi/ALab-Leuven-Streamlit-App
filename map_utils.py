import folium

def get_color(demand_value):
    if demand_value < 40:
        return 'rgb(237, 235, 112)'
    if demand_value < 150:
        return 'rgb(245, 229, 40)'
    elif demand_value < 300:
        return 'rgb(255, 171, 66)'
    elif demand_value < 600:
        return 'rgb(245, 75, 8)'
    else:
        return 'rgb(254, 19, 20)'
    
def radius_scale(number_of_spots):
    scale_factor = 0.3
    scale = scale_factor * (number_of_spots ** 0.5)
    return max(1, scale)



def create_map(gdf, time_of_day,parking_gdf, parkings_selected, hubs_df, hubs_selected, bicycle_gdf, bike_network, public_network):

    target_demand = f"{time_of_day} Demand"


    # Initialize your map with a central point (adjust these coordinates)
    m = folium.Map(location=[50.878933, 4.702433], zoom_start=11, pitch=45)

    # Add multipolygons from the GeoDataFrame
    for _, row in gdf.iterrows():
        # Create a feature with properties
        feature = folium.GeoJson(
            data={
                'type': 'Feature',
                'properties': {
                    'Zone': row['Zone'],
                    'Demand': row[target_demand]
                },
                'geometry': row['geometry'].__geo_interface__
            },
            style_function=lambda feature: {
                'fillColor': get_color(feature['properties']['Demand']),
                'color': get_color(feature['properties']['Demand']),
                'weight': 1,
                'fillOpacity': 0.6
            },
            tooltip=f"Zone: {row['Zone']}, Demand: {row[target_demand]}"
        )
        feature.add_to(m)

    if parkings_selected:
        for _, row in parking_gdf.iterrows():
            folium.CircleMarker(
                location=[row['geometry'].y, row['geometry'].x],
                radius=radius_scale(row['number_of_spots']),  # Scale the radius
                popup=f"Number of Spots: {row['number_of_spots']}",
                fill=True,
                fill_opacity=1,
            ).add_to(m)

    if hubs_selected:
        for _, row in hubs_df.iterrows():
            folium.CircleMarker(
                location=[row['geometry'].y, row['geometry'].x],
                radius=5,
                fill=True,
                fill_opacity=1,
                fill_color='green',
                color='green',
            ).add_to(m)

    if bike_network:
        for i, row in bicycle_gdf.iterrows():
            # Extract the coordinates from the LINESTRING geometry
            line_coords = [(coord[1], coord[0]) for coord in row['geometry'].coords]

            if i in [1,4,10,20]:
                print(line_coords)
            # Create a line and add it to the map
            folium.PolyLine(
                line_coords,
                color='blue',
                weight=10,
                opacity=0.8
            ).add_to(m)

    return m