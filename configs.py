def kepler_config(target_variable, clean_variable, selected_options, parking_label, parking_spots, selected_columns):
    """
    Define Kepler maps configs
    """
    layers = [
        {
                'id': 'your-layer-id',  # Unique identifier for the layer
                'type': 'geojson',
                'config': {
                    'dataId': 'data_1',  # Must match the name used in add_data
                    'label': clean_variable,
                    'columns': {
                        'geojson': 'geometry'  # Your geometry column
                    },
                    'isVisible': True,
                    'visConfig': {
                        'opacity': 0.6,
                        'strokeOpacity': 0.6,
                        'thickness': 0,
                        'strokeColor': [255, 255, 255],
                        'colorRange': {
                            'name': 'Global Warming',  # This is an example color range
                            'type': 'sequential',
                            'category': 'Uber',
                            'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                        },
                        'strokeColorRange': {
                            'name': 'Global Warming',
                            'type': 'sequential',
                            'category': 'Uber',
                            'colors': ['#5A1846', '#900C3F', '#C70039', '#E3611C', '#F1920E', '#FFC300']
                        },
                        'radius': 10,
                        'sizeRange': [0, 10],
                        'radiusRange': [0, 50],
                        'heightRange': [0, 500],
                        'elevationScale': 5,
                        'stroked': True,
                        'filled': True,
                        'enable3d': False,
                        'wireframe': False
                    },
                    'colorField': {
                        'name': target_variable,  # Field from your data to use for coloring
                        'type': 'integer'
                    },
                    'sizeField': {
                        'name': target_variable,
                        'type': 'integer'
                    },
                    'sizeScale': 'linear'
                },
                'visualChannels': {
                    'colorField': {
                        'name': target_variable,
                        'type': 'integer'
                    },
                    'colorScale': 'quantile',
                    'sizeField': {
                        'name': target_variable,
                        'type': 'integer'
                    },
                    'sizeScale': 'linear',
                    'strokeColorField': {
                        'name': target_variable,
                        'type': 'integer'
                    },
                    'strokeColorScale': 'quantile',
                    'heightField': {
                        'name': target_variable,
                        'type': 'integer'
                    },
                    'heightScale': 'linear',
                    'radiusField': {
                        'name': target_variable,
                        'type': 'integer'
                    },
                    'radiusScale': 'linear'
                }
            
            }
        ]
    if 'Parking' in  selected_options:
        parking_layer = {
            'id': 'parking-layer',  # Unique identifier for the parking layer
            'type': 'geojson',
            'config': {
                'dataId': 'parking_data',  # Must match the name used in add_data for parking data
                'label': 'Parking',
                'columns': {
                    'geojson': 'geometry'  # Your geometry column in parking data
                },
                'isVisible': True,
                'visConfig': {
                    'opacity': 0.8,
                    'strokeOpacity': 0.8,
                    'thickness': 2,
                    'strokeColor': [255, 255, 255],  # Red color for parking places
                    'colorRange': {
                        'name': 'Global Warming',  # This is an example color range
                        'type': 'sequential',
                        'category': 'Uber',
                        'colors': [255, 255, 255]  # Red color for parking places
                    },
                    'strokeColorRange': {
                            'name': 'Global Warming',
                            'type': 'sequential',
                            'category': 'Uber',
                            'colors': [255, 255, 255]
                    },
                    'radius': 10,
                    'sizeRange': [0, 10],
                    'radiusRange': [0, 50],
                    'heightRange': [0, 500],
                    'elevationScale': 5,
                    'stroked': True,
                    'filled': True,
                    'enable3d': True,
                    'wireframe': False
                },
                'textLabel': [
                    {
                        'field': parking_label,  # Column name in parking_df containing labels
                        'color': [255, 255, 255],
                        'size': 5,
                        'offset': [0, 0],
                        'anchor': 'middle',
                        'alignment': 'center'
                    }
                ]
            }
        }
        layers.append(parking_layer)

    if 'Bicycle' in selected_columns:
        bicycle_layer = {
            "id": "bicycle-layer",
            "type": "geojson",
            "config": {
                "dataId": "bicycle_data",
                "label": "Bicycle",
                "columns": {
                    "lat0": "latitude",       # Source Latitude
                    "lng0": "longitude",      # Source Longitude
                    "lat1": "zone_lat",       # Target Latitude
                    "lng1": "zone_lon",       # Target Longitude
                },
                "isVisible": True,
                "visConfig": {
                    "opacity": 0.8,
                    "thickness": 1.5,          # Stroke thickness
                    "colorRange": {
                        "name": "Global Warming",
                        "type": "sequential",
                        "category": "Uber",
                        "colors": ["#5A1846", "#900C3F", "#C70039", "#E3611C", "#F1920E", "#FFD301"]
                    }
                }
            }
        }
        layers.append(bicycle_layer)

    config = {
    'version': 'v1',
    'config': {
        'mapState': {
            'latitude': 50.878933, 
            'longitude': 4.702433,
            'zoom': 11,
            'pitch': 45
        },
        'visState': {
            'layers': layers,  # This should be the only 'layers' definition
            'interactionConfig': {
                'tooltip': {
                    'fieldsToShow': {
                        'data_1': [target_variable],
                        'parking_data': [parking_label, parking_spots],
                        'bicycle_data': ['distance_km']
                    }
                }
            },
            "blendMode": "additive" 
        }
    }
}
    return config
