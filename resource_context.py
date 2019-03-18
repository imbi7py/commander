import config, data_server, data_handler, quickview_store

class ResourceContext():
    def __init__(self):
        self.cfg = None
        self.data_socket_server = None
        self.main_window = None
        self.data_handler = None

    def init_resources(self, main_window):
        self.main_window = main_window
        self.cfg = config.load_config()
        self.data_socket_server = data_server.DataServer(self)
        self.data_handler = data_handler.DataHandler(self)
        self.quickview_store = quickview_store.QuickviewStore(self)
