# -*- coding:utf-8 -*-
# Author : woodsay
# Date   : 2019/4/14
# File   : NetworkCapture.py
# For    : 理由 psutil 模块获取进程列表

import psutil
import config
import json


def processStatus():
    pros_status = {}
    pros = config.process
    for p in pros:
        pros_status[p] = 0
    pros_all = set()
    pros_run = psutil.process_iter()
    for p in pros_run:
        try:
            pros_all.add(p)
        except:
            pass
    for p in pros_all:
        try:
            for sp in pros:
                if sp.lower() in p.name().lower():
                    pros_status[sp] = 1
        except:
            pass

    with open('./output/services_status.log', 'w') as f:
        f.write(json.dumps(pros_status))
