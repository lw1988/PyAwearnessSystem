# -*- coding:utf-8 -*-
# Author : woodsay
# Date   : 2019/4/15
# File   : SSHMonitor.py
# For    : 利用 os.popen 执行系统命令, 通过 lastb 获取 ssh 失败登录详情
import os
from json import dumps, loads

cmd = "lastb | grep ssh |awk '{print $3}' | sort | uniq -c"


def ssh_monitr():
    '''监控 ssh 的失败登录日志'''
    raw_lst = list()
    
    with open('./output/analyse/ssh_analyse', 'a+') as ssh_fp:
        raw_data = ssh_fp.readlines()    
        for i in raw_data:
           raw_lst.append(loads(i))

        # 执行统计命令
        stream = os.popen(cmd)
        # 获取执行结果
        output = stream.read().split()
        stream.close()
        length = len(output)
        if length % 2 == 0:
            for i in range(0, length, 2):
                cot = int(output[i])
                if cot > 50:
                    info = dict()
                    info['count'] = output[i]
                    info['srcIP'] = output[i + 1]
                    info['evilType'] = 107
                    for each_d in raw_lst:
                        if each_d == info:
                            print('eq')
                            continue
                        evillink = [info['srcIP'], '', 107]
                        # 以json格式写入文件
                        ssh_fp.write(dumps(info) + '\n')
                        with open('./output/evillink_status.log', 'a') as f:
                            f.write(dumps(evillink) + '\n')
