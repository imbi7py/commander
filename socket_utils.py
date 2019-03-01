import socket, threading, time, logging

class BaseSocketServer():
    def __init__(self, rc, ip, port, recv_length=4096):
        self.rc = rc
        self.ip, self.port, self.recv_length = ip, port, recv_length
        self.sk = socket.socket()
        self.sk.bind((self.ip, self.port))
        self.sk.listen(5)
    
    def run(self):
        while True:
            self._get_info()

    def _get_info(self):
        raise 'Pure virtual function'


class ControlServer(BaseSocketServer, threading.Thread):
    def __init__(self, rc, recv_length=4096):
        ip, port = rc.cfg['control_server_ip'], int(rc.cfg['control_server_port'])
        BaseSocketServer.__init__(self, rc, ip, port, recv_length)
        threading.Thread.__init__(self, target=self.run, args=tuple(), daemon=True)
        self.start()

    def _get_info(self):
        conn, address = self.sk.accept()
        _cmd = conn.recv(self.recv_length).decode()
        logging.info('[%s] got cmd: %s' % (time.asctime(time.localtime(time.time())), _cmd))
        _rsp = self.rc.controller.execute_command(_cmd, address)
        conn.sendall(_rsp.encode())
        conn.close()
        return

class BaseClient():
    def __init__(self, server_ip, server_port, recv_length=4096):
        self.server_ip, self.server_port, self.recv_length = server_ip, int(server_port), recv_length
        self.s = socket.socket()

class ControlClient(BaseClient):
    def __init__(self, server_ip, server_port):
        BaseClient.__init__(self, server_ip, server_port)
    
    def send(self, cmd):
        self.s.connect((self.server_ip, self.server_port))
        self.s.sendall(cmd.encode())
        _rsp = self.s.recv(self.recv_length).decode()
        self.s.close()
        return _rsp