# coding:utf-8
import json
class DataHandler():
    def __init__(self, rc):
        self.rc = rc

    def process_received_data(self, data):
        data = json.loads(data)
        #self.rc.main_window.add_item_to_list(data)
        print ('[data handler]recv a  %s' % data['type'])
        return '0'
