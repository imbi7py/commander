import sys
import socket, config

cfg = config.load_config()

def ___client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message.encode())
        #response = sock.recv(1024)
        #print ("Received: {}".format(response))
    finally:
        sock.close()

def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))
#
#def send_cmd(cmd_):
#    _client = socket_utils.ControlClient(
#        server_ip = cfg['data_server_ip'],
#        server_port = int(cfg['data_server_port'])
#    )
#    _rsp = _client.send(cmd_)
#    print (_rsp)
#
#def run():
#    while True:
#        sys.stdout.write('>>> controller_terminal >>> ')
#        _cmd = input()
#        if _cmd.startswith('exit'):
#            break
#        else:
#            send_cmd(_cmd)

def main():
    ip, port = cfg['data_server_ip'], int(cfg['data_server_port'])
    client(ip, port, "Hello World 1")
    client(ip, port, "Hello World 2")
    client(ip, port, "Hello World 3")
#    if 1 == len(sys.argv):
#        run()
#    else:
#        send_cmd(sys.argv[1])


if __name__ == '__main__':
    main()