# -*- coding:utf-8 -*-
# Author : woodsay
# Date   : 2019/5/2
# File   : app.py
# For    : 主文件

from flask import Flask, render_template
from app import WorldMapChart, AttackStatusChart, ServiceStatusChart, RequestsStatusChart
from app import StreamStatusChart, EvilStatusChart
from app.module import MultiLinkDetect, NetworkCapture, ProcessMonitor, SSHMonitor
from threading import Thread, Timer
from geoip2 import database
from os import listdir
from collections import OrderedDict
import json
import config
from pathlib import Path

# 实例化flask
app = Flask(__name__)

# 读取国家城市数据库
dataset = database.Reader('./app/libs/GeoLite2-City.mmdb')

# 访问IP计数器
ip_from = dict()
ip_from_sort = dict()

# 配置本机地理位置
local_coord = config.local_coord
local_city = config.local_city
local_pos = [local_coord, local_city]

# 文件指针
seek = 0

# 流量抓取与分析, 以线程非阻塞形式放入后台
netcap = NetworkCapture.netCapture()
ncap = Thread(target=netcap.capture)
ncap.start()

# 服务监控, 根据配置每隔pcheck_time检查一次服务状态


def pcheck_func():
    ProcessMonitor.processStatus()
    pcheck_time = config.pcheck_time
    global pcheck
    pcheck = Timer(pcheck_time, pcheck_func)
    pcheck.start()


# 多次访问判断, 根据配置每隔bcheck_time检查一次Apache访问日志
def bcheck_func():
    MultiLinkDetect.link_count()
    bcheck_time = config.bcheck_time
    global bcheck
    bcheck = Timer(bcheck_time, bcheck_func)
    bcheck.start()


# SSH爆破判断，根据配置每隔scheck_time检查一次ssh登录日志
def scheck_func():
    SSHMonitor.ssh_monitr()
    scheck_time = config.scheck_time
    global scheck
    scheck = Timer(scheck_time, scheck_func)
    scheck.start()


# 统计攻击类型, 根据配置每隔acheck_time统计一次
def acheck_func():
    attack_class = dict()
    target_files = listdir('./output/analyse')
    for filename in target_files:
        with open('./output/analyse/{}'.format(filename), 'r') as f:
            con = f.readlines()
            if con:
                for line in con:
                    line = json.loads(line)
                    attack_t = config.attackType[line['evilType']]
                    if attack_t not in attack_class:
                        attack_class[attack_t] = 1
                    else:
                        attack_class[attack_t] += 1
    with open('./output/attack_status.log', 'w') as f:
        f.write(json.dumps(attack_class))
    acheck_time = config.acheck_time
    acheck = Timer(acheck_time, acheck_func)
    acheck.start()


@app.route('/', methods=['GET', 'POST'])
def index():
    """面板首页"""
    # 数据读取
    # 初始读取服务状态
    with open('./output/services_status.log', 'r') as fp:
        services = json.load(fp)
    # 读取流量统计
    with open('./output/stream_status.log', 'r') as fp:
        streams = json.load(fp)
    # 读取攻击记录
    with open('./output/attack_status.log', 'r') as fp:
        attacks = json.load(fp)
    # 读取请求记录
    if not Path('./output/requests_status.log').is_file():
        global ip_from_sort
        requests = ip_from_sort 
    else:
        with open('./output/requests_status.log', 'r') as fp:
            requests = json.load(fp)
            ip_from_sort = requests
    # 图表绘制
    world_chart = WorldMapChart.world_status()
    world_id = world_chart._chart_id
    stream_chart = StreamStatusChart.stream_status(streams)
    stream_id = stream_chart._chart_id
    attack_chart = AttackStatusChart.attack_status(attacks)
    attack_id = attack_chart._chart_id
    request_chart = RequestsStatusChart.requests_status(requests)
    request_id = request_chart._chart_id
    service_chart = ServiceStatusChart.service_status(services)
    service_id = service_chart._chart_id
    evillink_chart = EvilStatusChart.evillink_status()

    return render_template('base.html',
                           attack_chart=attack_chart.render_embed(),
                           attack_id=attack_id,
                           world_chart=world_chart.render_embed(),
                           world_id=world_id,
                           stream_chart=stream_chart.render_embed(),
                           stream_id=stream_id,
                           request_chart=request_chart.render_embed(),
                           request_id=request_id,
                           service_chart=service_chart.render_embed(),
                           service_id=service_id,
                           evillink_chart=evillink_chart.render_embed())


@app.route('/chart_reload', methods=['POST'])
def chart_reload():
    with open('./output/requests_ip.log', 'r') as fp:
        addrs = fp.readlines()
    with open('./output/requests_ip.log', 'w') as fp:
        fp.truncate()
    global ip_from, ip_from_sort
    data, ip_from = WorldMapChart.reload_data(
        addrs, local_pos, dataset, ip_from)
    # dict 排序
    ip_from_sort = OrderedDict(
        sorted(ip_from.items(), key=lambda x: x[1], reverse=True))

    with open('./output/requests_status.log', 'w') as fp:
        fp.write(json.dumps(ip_from_sort))
    return data


@app.route('/request_reload', methods=["POST"])
def request_reload():
    # 使用全局变量而不是IO, 防止同时读写异常
    # with open('./output/requests_status.log', 'w') as fp:
    global ip_from_sort
    data = RequestsStatusChart.requests_status(ip_from_sort, 1)
    return data


@app.route('/service_reload', methods=['POST'])
def service_reload():
    with open('./output/services_status.log', 'r') as fp:
        ser = json.load(fp)
    data = ServiceStatusChart.service_status(ser, 1)
    return data


@app.route('/stream_reload', methods=['POST'])
def stream_reload():
    with open('./output/stream_status.log', 'r') as fp:
        stre = json.load(fp)
    data = StreamStatusChart.stream_status(stre, 1)
    return data


@app.route('/attack_reload', methods=['POST'])
def attack_reload():
    with open('./output/attack_status.log', 'r') as fp:
        attk = json.load(fp)
    data = AttackStatusChart.attack_status(attk, 1)
    return data


@app.route('/evil_reload', methods=['POST'])
def evil_reload():
    global seek
    fp = open('./output/evillink_status.log', 'r')
    fp.seek(seek)
    data = fp.readlines()
    seek = fp.tell()
    fp.close()
    rdata = dict()
    for i in range(len(data)):
        if i % 2 == 0:
            etmp = json.loads(data[i])
            rdata[i] = [etmp[0], etmp[1], config.attackType[int(etmp[2])]]
    return json.dumps(rdata)


if __name__ == '__main__':
    pcheck_func()
    bcheck_func()
    scheck_func()
    acheck_func()
    app.run(host='0.0.0.0', port=5000, debug=True)
