# coding:utf-8
import sys, socket, config, json, os, time, random
import img_utils
import cv2
import numpy as np

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

def send_img(ip, port, pil_img, aircraft_type, sensor_type, monitor_type):
    data_ = json.dumps({
        'type': 'quickview',
        'data': img_utils.img_to_str(pil_img),
        'aircraft_type': aircraft_type,
        'sensor_type': sensor_type,
        'monitor_type':monitor_type
    })
    send_data_to_ip_port(ip, port, data_)
    print ('send img success')

def get_test_image_names(dir_):
    names_ = os.listdir(dir_)
    for i in range(len(names_)):
        names_[i] = dir_ + '/' + names_[i]
    return names_

def normalization(img_pil):
    from PIL import Image
    import numpy as np
    img_np = np.array(img_pil)
    min_ = np.min(img_np)
    max_ = np.max(img_np)
    img_np = np.array((img_np-min_)/max_*255, dtype=np.uint8)
    img_new = Image.fromarray(img_np)
    return img_new

def is_color_img(img_pil):
    import numpy as np
    img_np = np.array(img_pil)
    if len(img_np) == 3:
        return True
    else:
        return False



def main():
    from PIL import Image, ImageDraw, ImageFont
    ip, port = cfg['data_server_ip'], int(cfg['data_server_port'])
    send_string(ip, port, "Hello World 1")
    send_string(ip, port, "Hello World 2")
    #test_img_names = get_test_image_names('pics/长光所红外地面')
    while True:
        test_img_names = 'pics/realdata/双波段视频吊舱_可见光/长光可见飞行.mp4'
        aircraft_types = ['aircraft_type1', 'aircraft_type2', 'aircraft_type3']
        sensor_types = ['sensor_typea', 'sensor_typeb', 'sensor_typec']
        cap = cv2.VideoCapture(test_img_names)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        ret, img = cap.read()
        while (ret):
            '''
            for name_ in test_img_names:
                aircraft_type = aircraft_types[random.randint(0, 2)]
                sensor_type = sensor_types[random.randint(0, 2)]
                img = Image.open(name_)
                img = normalization(img)
                is_color_img(img)
                img = img.resize((500,500))
                draw = ImageDraw.Draw(img)
                text_ = 'aircrafttype: %s\nsensor_type: %s' % (aircraft_type, sensor_type)
                text_color = (255, 0, 0)
                if not is_color_img(img):
                    text_color = 255
                draw.text((00, 00), text_, fill = text_color)
                send_img(ip, port, img, aircraft_type, sensor_type)
                time.sleep(2)
            '''
            aircraft_type = aircraft_types[random.randint(0, 2)]
            sensor_type = sensor_types[random.randint(0, 2)]
            monitor_type = 'video'
            img = normalization(img)
            is_color_img(img)
            img = img.resize((100, 100))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("SansSerif_Italic.ttf", 16)
            text_ = '%s\n%s' % (aircraft_type, sensor_type)
            text_color = (255, 0, 0)
            if not is_color_img(img):
                text_color = 255
            draw.text((00, 00), text_, fill=text_color, font=font)
            send_img(ip, port, img, aircraft_type, sensor_type, monitor_type)
            ret, img = cap.read()
            # time.sleep(fps)





if __name__ == '__main__':
    main()
