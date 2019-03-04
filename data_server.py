import socketserver, logging, threading

class DataServer():
    _instance = None

    @staticmethod
    def get_instance():
        assert DataServer._instance is not None
        return DataServer._instance

    def __init__(self, rc):
        self.rc = rc
        DataServer._instance = self
        ip, port = rc.cfg['data_server_ip'], int(rc.cfg['data_server_port'])

        self._server = socketserver.ThreadingTCPServer((ip, port), DataServer.Handler_Class)
        self._server_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._server_thread.start()

    class Handler_Class(socketserver.StreamRequestHandler):
        def handle(self):
            data = str(self.request.recv(1024), 'ascii')
            response = DataServer.get_instance().handler_func(data)
            response = bytes(response, 'ascii')
            self.request.sendall(response)
    
    def handler_func(self, data):
        try:
            ret = self.rc.data_handler.process_received_data(data)
            return ret
        except Exception as e:
            logging.exception(e)
            return '1'