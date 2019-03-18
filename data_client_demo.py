# coding:utf-8
import sys, socket, config, json
import img_utils

cfg = config.load_config()

def send_data_to_ip_port(ip, port, data_):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        data_ = data_.encode('utf8')
        sock.sendall(data_)
        response = str(sock.recv(1024), 'ascii')
        return response

def send_string(ip, port, message):
    data_ = json.dumps({'type': 'str', 'data': message})
    send_data_to_ip_port(ip, port, data_)
    print ('send string success')
    return 0

def send_img(ip, port, pil_img):
    data_ = json.dumps({'type': 'img', 'data': img_utils.img_to_str(pil_img)})
    send_data_to_ip_port(ip, port, data_)
    print ('send img success')


def main():
    from PIL import Image
    ip, port = cfg['data_server_ip'], int(cfg['data_server_port'])
    send_string(ip, port, "Hello World 1")
    send_string(ip, port, "Hello World 2")
    send_img(ip, port, Image.open('pics/emojis/0.png'))
    send_img(ip, port, Image.open('pics/emojis/1.png'))


if __name__ == '__main__':
    main()
