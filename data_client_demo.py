# coding:utf-8
import sys, socket, config, json, os, time, random, threading, cv2, img_utils
import numpy as np
from PIL import Image, ImageDraw, ImageFont

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

def send_img(ip, port, pil_img, aircraft_type, sensor_type,monitor_type):
    data_ = json.dumps({
        'type': 'quickview',
        'data': img_utils.img_to_str(pil_img),
        'aircraft_type': aircraft_type,
        'sensor_type': sensor_type,
        'monitor_type': monitor_type
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

def quickview_send(ip, port, folder,aircraft_type,sensor_type):
    while True:
        test_img_names=get_test_image_names(folder)
        for name_ in test_img_names:
            monitor_type='quickview'
            img = Image.open(name_)
            img = normalization(img)
            is_color_img(img)
            img = img.resize((500,500))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("SansSerif_Italic.ttf",35)
            text_ = 'aircrafttype: %s\nsensor_type: %s' % (aircraft_type, sensor_type)
            text_color = (255, 0, 0)
            if not is_color_img(img):
                text_color = 255
            draw.text((00, 00), text_, fill = text_color, font=font)
            send_img(ip, port, img, aircraft_type, sensor_type,monitor_type)
            time.sleep(2)

def video_send(ip, port,folder,aircraft_type,sensor_type):
    while True:
        files = get_test_image_names(folder)
        for file in files:
            cap = cv2.VideoCapture(file)
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            ret, img = cap.read()
            while (ret):
                monitor_type = 'video'
                img = normalization(img)
                is_color_img(img)
                img = img.resize((100, 100))
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("SansSerif_Italic.ttf", 12)
                text_ = '%s\n%s' % (aircraft_type, sensor_type)
                text_color = (255, 0, 0)
                if not is_color_img(img):
                    text_color = 255
                draw.text((00, 00), text_, fill=text_color, font=font)
                send_img(ip, port, img, aircraft_type, sensor_type, monitor_type)
                ret, img = cap.read()
                # time.sleep(fps)


def main():
    ip, port = cfg['data_server_ip'], int(cfg['data_server_port'])
    #quickview_send(ip, port, 'pics/realdata/多光谱', 'aircraft_type1', 'sensor_typea')
    #video_send(ip, port, 'pics/realdata/双波段视频吊舱_可见光', 'aircraft_type1', 'sensor_typea')
    threads = []
    t = threading.Thread(target=quickview_send, args=(ip, port, 'pics/realdata/可见光', '北航猛牛', '可见光',))
    threads.append(t)
    t = threading.Thread(target=quickview_send, args=(ip, port, 'pics/realdata/minisar', '北航猛牛', 'minisar',))
    threads.append(t)
    t = threading.Thread(target=quickview_send, args=(ip, port, 'pics/realdata/多光谱', '大疆', '多光谱',))
    threads.append(t)
    t = threading.Thread(target=video_send, args=(ip, port, 'pics/realdata/双波段视频吊舱_可见光', '地理所xxx', '双波段视频吊舱_可见光',))
    threads.append(t)
    t = threading.Thread(target=video_send, args=(ip, port, 'pics/realdata/双波段视频吊舱_红外', '北航猛牛2', '双波段视频吊舱_红外',))
    threads.append(t)
    for t in threads:
        t.setDaemon(True)
        t.start()

    t.join()



if __name__ == '__main__':
    main()
