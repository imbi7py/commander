# coding:utf-8
import json
import img_utils

class DataHandler():
    def __init__(self, rc):
        self.rc = rc

    def process_received_quickview(self, data):
        str_img = data['data']
        pil_img = img_utils.str_to_img(str_img)
        self.rc.main_window.set_image(pil_img)
        print ('[data handler]recv an img')

    def process_received_data(self, data):
        data = json.loads(data)
        if data['type'] == 'str':
            print ('[data handler]recv a str: %s' % data['data'])
        elif data['type'] == 'quickview':
            self.process_received_quickview(data)
        else:
            print ('[data handler]unknown type: %s' % data['type'])
            return 'unknown type'
        return '0'
