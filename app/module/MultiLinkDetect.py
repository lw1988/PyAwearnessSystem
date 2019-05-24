# -*- coding:utf-8 -*-
# Author : woodsay
# Date   : 2019/5/5
# File   : MultiLinkDetect.py
# For    : 对同一IP多次连接请求的探测
from os import popen
from json import dumps
import config


def link_count():
    # 筛选IP/访问次数/访问时间
    cmd = "cat %s | awk -F' ' '{print $1}' | uniq -c | sort -n " % config.apache_log
    count_cmd = cmd + "| awk -F' ' '{print $1}' "
    ip_cmd = cmd + "| awk -F' ' '{print $2}' "

    count_result = popen(count_cmd)
    ip_result = popen(ip_cmd)

    counts = count_result.read().split()
    ips = ip_result.read().split()

    ip_result.close()
    count_result.close()

    fp = open('./output/analyse/brute_analyse', 'w')
    for i in range(len(ips)):
        cot = int(counts[i])
        # 筛选访问次数大于 100 的
        if cot > 100:
            addr = ips[i]
            cmd = "cat {} | grep {} | ".format(config.apache_log, addr)
            file_cmd = cmd + "awk '{print $7}'"
            time_cmd = cmd + "awk '{print $4}'"
            time_result = popen(time_cmd)
            file_result = popen(file_cmd)
            # 取最后50次访问的时间，判断是否是短时间内连续访问
            times = time_result.read().split()[-50:]
            # 取最后50次访问的文件，判断是否是短时间内请求同一文件
            files = file_result.read().split()[-50:]
            time_result.close()
            file_result.close()

            # Apache日志的标准时间格式为: 08/Apr/2019:17:35:07
            stime_h = int(times[0][-8:-6])
            stime_m = int(times[0][-5:-3])
            etime_h = int(times[-1][-8:-6])
            etime_m = int(times[-1][-5:-3])

            # 1分钟内请求超过一定次数
            if etime_h == stime_h and etime_m - stime_m < 1:

                info = {
                    'srcIP': addr,
                    'count': cot,
                    'evilType': None
                }
                # 如果是请求的都是同一文件则判断为暴力破解
                if files[-1] == files[-2] == files[-3] == files[-4]:
                    info['evilType'] = 105
                # 否则判断为目录扫描
                else:
                    info['evilType'] = 103
                evillink = [info['srcIP'], '', info['evilType']]
                fp.write(dumps(info) + '\n')
                with open('./output/evillink_status.log', 'a') as evf:
                    evf.write(dumps(evillink) + '\n')
            else:
                pass
    fp.close()
