import os

current_dir = os.path.dirname(os.path.abspath(__file__))

config = {
    'data_server_ip': '127.0.0.1',
    'data_server_port': '9998',
    'quickview_filter_item_preload': {
        'uav_type': ['uav_type1', 'uav_type2'],
        'sensor_type': ['sensor_typea', 'sensor_typeb'],
    },
}

def load_config():
    return config
