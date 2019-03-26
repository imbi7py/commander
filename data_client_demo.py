# coding:utf-8
import sys, socket, config, json, os, time, random
import img_utils

cfg = config.get_config()


def split_data(data_, part_length=4096):
    while len(data_) > 0:
        send, data_ = data_[:part_length], data_[part_length:]
        yield send


def send_data_to_ip_port(ip, port, data_):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        data_ = data_.encode('utf8')
        for part in split_data(data_):
            sock.sendall(part)
            response = str(sock.recv(1024), 'utf8')
        sock.sendall('end'.encode('utf8'))
        response = str(sock.recv(1024), 'utf8')
        return response

def send_string(ip, port, message):
    data_ = json.dumps({'type': 'str', 'data': message})
    send_data_to_ip_port(ip, port, data_)
    print ('send string success')
    return 0

def send_img(ip, port, pil_img, aircraft_type, sensor_type):
    data_ = json.dumps({
        'type': 'quickview',
        'data': img_utils.img_to_str(pil_img),
        'aircraft_type': aircraft_type,
        'sensor_type': sensor_type,
    })
    send_data_to_ip_port(ip, port, data_)
    print ('send img success')

def get_test_image_names(dir_):
    names_ = os.listdir(dir_)
    for i in range(len(names_)):
        names_[i] = dir_ + '/' + names_[i]
    return names_

def main():
    from PIL import Image, ImageDraw
    ip, port = cfg['data_server_ip'], int(cfg['data_server_port'])
    send_string(ip, port, "Hello World 1")
    send_string(ip, port, "Hello World 2")
    test_img_names = get_test_image_names('pics/uav_img')
    aircraft_types = ['aircraft_type1', 'aircraft_type2', 'aircraft_type3']
    sensor_types = ['sensor_typea', 'sensor_typeb', 'sensor_typec']
    while True:
        for name_ in test_img_names:
            aircraft_type = aircraft_types[random.randint(0, 2)]
            sensor_type = sensor_types[random.randint(0, 2)]
            img = Image.open(name_)
            img = img.resize((50, 50))
            draw = ImageDraw.Draw(img)
            draw.text((00, 00), 'aircrafttype: %s\nsensor_type: %s' % (aircraft_type, sensor_type), fill = (255, 0 ,0))
            send_img(ip, port, img, aircraft_type, sensor_type)
            time.sleep(2)


if __name__ == '__main__':
    main()
