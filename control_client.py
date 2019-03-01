import sys
import socket_utils, config

cfg = config.load_config()

def send_cmd(cmd_):
    _client = socket_utils.ControlClient(
        server_ip = cfg['control_server_ip'],
        server_port = int(cfg['control_server_port'])
    )
    _rsp = _client.send(cmd_)
    print (_rsp)

def run():
    while True:
        sys.stdout.write('>>> controller_terminal >>> ')
        _cmd = input()
        if _cmd.startswith('exit'):
            break
        else:
            send_cmd(_cmd)

def main():
    if 1 == len(sys.argv):
        run()
    else:
        send_cmd(sys.argv[1])


if __name__ == '__main__':
    main()