import os, time, logging
import socket_utils
import resource_context, controller, config
import load_qgis_qt


class Main_Server():
    def __init__(self):
        self.rc = resource_context.ResourceContext()
        self.init_resource()
    
    def init_resource(self):
        self.rc.main_server = self
        self.rc.cfg = config.load_config()
        self.rc.controller = controller.Controller(self.rc)
        self.rc.control_socket_server = socket_utils.ControlServer(self.rc)

    def run(self):
        while not self.stopflag:
            logging.info('[%s] main server is running' % time.asctime(time.localtime(time.time())))
            time.sleep(30)
    
    def stop(self):
        logging.info('stopped')
        exit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    Main_Server().run()