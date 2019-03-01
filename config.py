import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def load_config():
    res = {}
    for line in open('%s/global.config' % current_dir):
        line = line.strip().split(' ')
        res[line[0]] = line[1]
    return res