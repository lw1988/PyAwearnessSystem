# -*- coding:utf-8 -*-
# Author : woodsay
# Date   : 2019/5/2
# File   : config.py
# For    : 配置项

# SQL 注入攻击匹配规则
sqlrule = "'|--|update|extractvalue|union|select|substr|information_schema".split(
    '|')
# XSS 跨站攻击匹配规则
xssrule = "script|iframe|javascript|onerror|onmouseover|/>".split('|')
# 木马后门 匹配规则
backrule = "eval|assert|system|shell_exec|passthru".split('|')
# 暴力破解 匹配规则
brutecot = 50


# 攻击类型字典
attackType = {
    100: '无威胁',
    101: 'XSS跨站',
    102: 'SQL注入',
    103: '目录扫描',
    104: 'DoS攻击',
    105: '暴力破解',
    106: '木马后门',
    107: 'SSH爆破'
}

# 要监视是否正常运行的程序列表
process = ['apache', 'mysqld', 'vsftpd', 'sshd']

# 流量统计单位
stream_unit = 1024               # KB
# stream_unit = 1024 * 1024        # MB
# stream_unit = 1024 * 1024 * 1024 # GB

# 服务器IP 网卡名称 经纬度 城市名称
local_ip = '192.168.43.74'
local_adapter = 'wlp4s0'
local_coord = [-118.24368, 34.05223]
local_city = 'Los Angeles'


# Web日志路径
apache_log = '/var/log/apache2/access.log'

# 检查服务状态的时间间隔(s)
pcheck_time = 60

# 检查暴力破解与目录扫描的时间间隔
bcheck_time = 60

# 检查SSH爆破的时间间隔
scheck_time = 60

# 统计攻击类型间隔
acheck_time = 60
