class DataHandler():
    def __init__(self, rc):
        self.rc = rc
    
    def process_received_data(self, data):
        self.rc.main_window.add_item_to_list(data)
        print ('[data handler]recv  %s' % data)
        return '0'