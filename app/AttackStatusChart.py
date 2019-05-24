# -*- coding:utf-8 -*-
# Author : woodsay
# Date   : 2019/4/24
# File   : AttackStatusChart.py
from pyecharts import Pie
from pyecharts_javascripthon.api import TRANSLATOR


def attack_status(attacks, is_reload=0):
    attack_type = list(attacks.keys())
    attack_count = list(attacks.values())

    status = Pie('           攻击事件总览\n           -----------------', width="100%", height="100%", title_pos="left",
                 title_top=40, title_color="#6cb7c9")

    # attack_type = ['SQL注入', 'XSS跨站', '暴力破解', 'DoS', '木马后门']
    # attack_num = [90, 30, 102, ```3`0, `20]

    status.add("", attack_type, attack_count, radius=[30, 38], label_text_color=None,
               legend_orient='vertical', center=[50, 60], is_legend_show=False, is_toolbox_show=False,
               is_label_show=False)

    if is_reload:
        option = status.get_options()
        option = TRANSLATOR.translate(option)
        option = option.as_snippet()
        return option
    else:
        return status
