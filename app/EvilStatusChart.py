# -*- coding:utf-8 -*-
# Author : woodsay
# Date   : 2019/4/25
# File   : EvilStatusChart.py

from pyecharts import Line, Grid

def evillink_status():
	attack = Line('    恶意攻击监测\n    -------------', title_pos="left", title_top=10, title_color="#6cb7c9", width="100%", height="100%")
	attack.add('',[],[],is_toolbox_show=False, is_legend_show=False, is_xaxis_show=False, is_yaxis_show=False)
	return attack

