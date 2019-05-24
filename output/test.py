import json
import random
import time


def gen():
    ip = ''
    for i in range(3):
        ip += str(random.randint(1, 255)) + '.'
    ip += str(random.randint(1, 255))

    evil = random.randint(0, 1)
    return ip, evil


for i in range(10):
    ips = []
    fp = open('./requests_ip.log', 'w')
    for i in range(10):
        a, b = gen()
        tmp = {a: b}
        fp.write(json.dumps(tmp) + '\n')
    fp.close()
    time.sleep(4)
