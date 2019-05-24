from pyecharts import GeoLines, Style
from pyecharts.datasets.coordinates import get_coordinate
from pyecharts_javascripthon.api import TRANSLATOR
from json import loads

style = Style(
    title_color="#fff",
    title_top=20,
    title_pos="center",
    width="auto",
    height="100%",
    background_color="rgba(0,0,0,0)"
)

style_geo = style.add(
    maptype='world',            # 地图类型
    geo_effect_period=4,        # 特效持续时间
    geo_effect_traillength=0.1,  # 特效尾长
    geo_effect_symbol="pin",    # 特效形状
    geo_effect_symbolsize=5,    # 特效尺寸
    is_geo_effect_show=True,    # 是否显示特效
    is_roam=True,               # 鼠标缩放与平移 True, move or scale
    is_label_show=True,         # 是否展示图形上的文本标签
    label_color=['#339900', '#339900', '#339900'],  # 图形的颜色, 多值循环取值
    label_pos="right",          # 标签位置
    label_text_color="#7BECFF",  # 标签字体颜色
    label_formatter="{b}",      # 标签格式
    line_curve=0.2,             # 路径的弧度
    line_opacity=0,             # 线的透明度
    line_width=0,               # 线的宽度
    line_type=None,             # 线的类型
    is_legend_show=False,       # 是否显示图例分类
    is_toolbox_show=False,      # 是否显示工具箱
    border_color="#6cb7c9",     # 国家边界颜色
    geo_normal_color="rgba(12,12,12,0.5)"  # 国家区域颜色
)


def world_status():
    world = GeoLines('', **style.init_style)
    # 添加国际城市地理坐标
    sange = get_coordinate('Los Angeles', '美国')
    world.add_coordinate("Los Angeles", sange[0], sange[1])
    road = [
        ['Los Angeles', 'Los Angeles']
    ]
    world.add('', road, **style_geo)
    return world


def reload_data(addrs, local, dataset, ip_from):
    local_coord = local[0]
    local_city = local[1]

    road = []
    # 实例化世界地图
    world = GeoLines('', **style.init_style)
    try:
        # 添加本机坐标
        world.add_coordinate(local_city, local_coord[0], local_coord[1])
    except:
        # 重复添加可能会出错？
        pass

    if addrs:
        for ips in addrs:
            ips = loads(ips)
            ip = list(ips.keys())[0]
            is_evil = list(ips.values())[0]
            try:
                info = dataset.city(ip)
                ip_city = info.city.name
                ip_country = info.country.name
                # 经纬度
                ip_coord = [info.location.longitude, info.location.latitude]
                if ip_city and ip_country:
                    world.add_coordinate(ip_city, ip_coord[0], ip_coord[1])
                    path = [ip_city, local_city]
                    road.append(path)
                    if ip_country not in ip_from:
                        ip_from[ip_country] = 1
                    else:
                        ip_from[ip_country] += 1
            except:
                pass
    else:
        road = [['Los Angeles', local_city]]

    world.add('', road, **style_geo)
    option = world.get_options()
    # options中存在 Tooltip 对象，无法直接使用 json.dumps 转换，需要理由 pyecharts 的 TRANSLATOR API函数
    option = TRANSLATOR.translate(option)
    option = option.as_snippet()

    return option, ip_from
