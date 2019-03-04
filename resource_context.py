import controller, config, data_server, data_handler

class ResourceContext():
    def __init__(self):
        self.cfg = None
        self.control_socket_server = None
        self.controller = None
        self.main_window = None
        self.data_handler = None
    
    def init_resources(self, main_window):
        self.main_window = main_window
        self.cfg = config.load_config()
        self.controller = controller.Controller(self)
        self.data_socket_server = data_server.DataServer(self)
        self.data_handler = data_handler.DataHandler(self)