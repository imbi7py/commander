import os

def bin_to_hex(input_file, output_file, block_size=256):
    num_system_conversion(input_file, output_file,blocksize=block_size)

def hex_to_bin(input_file, output_file, block_size=256):
    num_system_conversion(input_file, output_file, turn='hex_to_bin', blocksize=block_size)

def num_system_conversion(input_file, output_file, turn='bin_to_hex', blocksize=256):
    if not(os.path.exists(input_file)):
        raise Exception('input_file is not exist')
    if (os.path.exists(output_file)):
        raise Exception('output_file is exist')
    try:
        with open(output_file,'w') as w_file:
            with open(input_file,'r') as r_file:
                text=r_file.read()
                text_split = text.split()
                output_text=''
                for element in text_split:
                    if turn=='bin_to_hex':
                        elem = hex(int(element, 2))[2:].upper()
                        elem ='0'*(2-len(elem))+elem
                        output_text = output_text + elem+ ' '
                    elif turn=='hex_to_bin':
                        elem = bin(int(element, 16))[2:]
                        elem = '0'*(8-len(elem))+elem
                        output_text = output_text + elem + ' '
                    else:
                        pass
                print(output_text)
                w_file.write(output_text)
    except IOError:
        print('output_file write error')

#bin_to_hex('F:/lab505/commander/aircraft/status2.txt','F:/lab505/commander/aircraft/status3.txt')
def get_fly_location(input_file):
    fly_location=[]
    if not(os.path.exists(input_file)):
        raise Exception('input_file is not exist')
    try:
        with open(input_file, 'r') as f:
            text = f.read().split()
            text_len=len(text)
            if(text_len<=105):
                return fly_location
            now=0
            while(text[now]!='11101011'or text[now+1]!='10010000'):
                now=now+1
                if(now+105>=text_len):
                    break
            while(now+105<text_len):
                lon=text[now+57]+text[now+58]+text[now+59]+text[now+60]
                lat=text[now+61]+text[now+62]+text[now+63]+text[now+64]
                height=text[now+65]+text[now+66]
                height=height[0]+'0'*8+height[1:]
                lon=float(int(lon,2))/1000000
                lat=float(int(lat,2))/1000000
                height=float(int(height,2))
                fly_location.append((lon,lat,height))
                now=now+105
                while (text[now] != '11101011' or text[now + 1] != '10010000'):
                    now = now + 1
                    if (now + 105 >= text_len):
                        break
            return fly_location

    except IOError:
        print('input_file read error')

#hex_to_bin('F:/lab505/commander/aircraft/status1.txt','F:/lab505/commander/aircraft/status2.txt')
fly_location=get_fly_location('aircraft/status2.txt')
print(fly_location)
print(len(fly_location))