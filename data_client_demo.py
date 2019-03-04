import sys
import socket, config

cfg = config.load_config()


def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

def main():
    ip, port = cfg['data_server_ip'], int(cfg['data_server_port'])
    client(ip, port, "Hello World 1")
    client(ip, port, "Hello World 2")
    client(ip, port, "Hello World 3")


if __name__ == '__main__':
    main()