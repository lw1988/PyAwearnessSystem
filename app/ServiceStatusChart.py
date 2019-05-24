# -*- coding:utf-8 -*-
# Author : woodsay
# Date   : 2019/4/25
# File   : ServiceStatusChart.py

from pyecharts import EffectScatter, Grid
from pyecharts_javascripthon.api import TRANSLATOR


def service_status(services, is_reload=0):
    symbol = "roundRect"
    symbol_size = 10

    apache_pos = [10]
    mysql_pos = [10]
    ssh_pos = [10]
    ftp_pos = [10]

    grid = Grid(width="100%", height="100%")

    service = EffectScatter(" 服务运行状态\n -----------------", width="100%", height="100%", title_color="#6cb7c9",
                            title_top=10)

    down = "#F52E44"  # 红灯宕机
    up = "#01A901"    # 绿灯正常
    colors = [down] * 4
    if services['apache']:
        colors[0] = up
    if services['mysqld']:
        colors[1] = up
    if services['sshd']:
        colors[2] = up
    if services['vsftpd']:
        colors[3] = up
    service.add("apache", apache_pos, [16], symbol_size=symbol_size, effect_scale=3.5,
                effect_period=2, symbol=symbol, label_color=colors)
    service.add("mysql", mysql_pos, [12], symbol_size=symbol_size, effect_scale=3.5,
                effect_period=2, symbol=symbol, label_color=colors)
    service.add("ssh", ssh_pos, [8], symbol_size=symbol_size, effect_scale=3.5,
                effect_period=2, symbol=symbol, label_color=colors)
    service.add("ftp", ftp_pos, [4], symbol_size=symbol_size, effect_scale=3.5,
                effect_period=2, symbol=symbol, label_color=colors, is_toolbox_show=False,
                is_label_show=False, is_xaxis_show=False, is_yaxis_show=False, is_legend_show=False)

    grid.add(service, grid_right="75vh", grid_top="90vh", grid_bottom="20vh")
    if is_reload:
        option = grid.get_options()
        option = TRANSLATOR.translate(option)
        option = option.as_snippet()
        return option
    else:
        return grid
