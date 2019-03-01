import os, time
import socket_utils
import resource_context, controller, config

class Main_Server():
    def __init__(self):
        self.rc = resource_context.ResourceContext()
        self.init_resource()
        self.stopflag = False
    
    def init_resource(self):
        self.rc.main_server = self
        self.rc.cfg = config.load_config()
        self.rc.controller = controller.Controller(self.rc)
        self.rc.control_socket_server = socket_utils.ControlServer(self.rc)

    def run(self):
        while not self.stopflag:
            print ('[%s] main server is running' % time.asctime(time.localtime(time.time())))
            time.sleep(30)
    
    def stop(self):
        print ('stopped')
        exit()


if __name__ == '__main__':
    Main_Server().run()