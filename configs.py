def kepler_config(target_variable, display_target_variable, clean_variable, selected_options, parking_label, parking_spots, selected_columns):
    """
    Define Kepler maps configs
    """
    if display_target_variable == True:
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
                            'strokeColor': [210, 210, 210],
                            'colorRange': {
                                'name': 'Global Warming',  
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
    else:
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
                        'opacity': 0,  # Set fill opacity to 0 to make it transparent
                        'strokeOpacity': 1,  # Set stroke opacity to 1 for full visibility
                        'thickness': 0.4,  # Set the thickness of the border to be thinner
                        'strokeColor': [210, 210, 210],  # Set the border color to a light grey for uniform color
                        'stroked': True,
                        'filled': False,  # Set to False to not fill the multipolygons
                        'enable3d': False,
                        'wireframe': False
                    },
                    # Remove colorField, sizeField, and sizeScale if they are not needed
                },
                # Remove the visualChannels block if you are not using it for uniform color
            }
        ]

    if 'Parking' in selected_options:
        parking_layer = {
            'id': 'parking-layer',
            'type': 'point',  # Use 'point' for point data
            'config': {
                'dataId': 'parking_data',
                'label': parking_label,
                'columns': {
                    'latitude': 'latitude',  # Your DataFrame's latitude column name
                    'longitude': 'longitude',  # Your DataFrame's longitude column name
                },
                'isVisible': True,
                'visConfig': {
                    'opacity': 0.8,
                    'strokeOpacity': 0.8,
                    'radius': 10,
                    'stroked': True,
                    'filled': True,
                    'color': [255, 0, 0],  # Red color for parking places
                },
                'textLabel': [{
                    'field': parking_label,
                    'color': [255, 255, 255],
                    'size': 5,
                    'offset': [0, 0],
                    'anchor': 'middle',
                    'alignment': 'center'
                }]
            }
        }
        layers.append(parking_layer)

    if 'Bicycle' in selected_options:
        bicycle_layer = {
            "id": "bicycle-layer",
            "type": "geojson",
            "config": {
                "dataId": "bicycle_data",
                "label": "Bicycle",
                "columns": {
                    "lat0": "latitude",       # Source Latitude
                    "lng0": "longitude"
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

    if 'Multimodal Hubs' in selected_options:
        multimodal_layer = {
            'id': 'multimodal-layer',  # Unique identifier for the multimodal hubs layer
            'type': 'point',  # Assuming multimodal hubs are points
            'config': {
                'dataId': 'multimodal_data',  # Must match the name used in add_data for multimodal hubs data
                'label': 'Multimodal Hubs',
                'columns': {
                    'latitude': 'latitude',  # Your DataFrame's latitude column name for multimodal hubs
                    'longitude': 'longitude',  # Your DataFrame's longitude column name for multimodal hubs
                },
                'isVisible': True,
                'visConfig': {
                    'opacity': 1,
                    'strokeOpacity': 1,
                    'radius': 10,
                    'stroked': True,
                    'filled': True,
                    'color': [0, 153, 255],  # Choose a color for multimodal hubs, e.g., blue
                },
                'textLabel': [{
                    'field': None,  # Replace with a field name if you want to show labels
                    'color': [255, 255, 255],
                    'size': 12,
                    'offset': [0, 0],
                    'anchor': 'start',
                    'alignment': 'center'
                }]
            }
        }
        layers.append(multimodal_layer)


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
