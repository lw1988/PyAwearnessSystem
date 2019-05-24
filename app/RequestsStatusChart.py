# -*- coding:utf-8 -*-
# Author : woodsay
# Date   : 2019/4/25
# File   : RequestsStatusChart.py
# For    :

from pyecharts import Bar
from pyecharts_javascripthon.api import TRANSLATOR

def requests_status(requests, is_reload=0):
	country = list(requests.keys())[:10]
	counts = list(requests.values())[:10]
	# country = ['美国', '中国', '英国', '俄罗斯', '法国', '印度', '韩国', '巴西', '澳大利亚'][::-1]
	# times = [120, 70, 60, 50, 43, 12, 2, 2, 1][::-1]
	request = Bar('    请求IP来源\n    --------------', width="100%", height="100%", title_color="#6cb7c9",
	              title_pos="left", title_top=10)
	request.add('', country, counts, is_convert=True, is_toolbox_show=False, is_yaxis_show=False, is_label_show=True,
	            label_pos="right", xaxis_line_color="#6cb7c9", label_color="#fff", is_legend_show=True)

	if is_reload:
		option = request.get_options()
		option = TRANSLATOR.translate(option)
		option = option.as_snippet()
		return option
	return request
