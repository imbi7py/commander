import os

current_dir = os.path.dirname(os.path.abspath(__file__))

config = {
    'data_server_ip': '127.0.0.1',
    'data_server_port': '9998',
    'quickview_filter_item_preload': {
        'aircraft_type': ['aircraft_type1', 'aircraft_type2'],
        'sensor_type': ['sensor_typea', 'sensor_typeb'],
    },
}

def get_config():
    return config
