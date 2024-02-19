import requests
from OpenSSL import SSL
import numpy as np
import folium
from folium import plugins

# ##########################################全局变量#############################################################

# 绘制地图
def PlotLineOnMap(Lat1, Lon1):
    # 给出的坐标系为GCJ-02，如果需要测试google地图，需要进行坐标转换
    # 获取高德地图的路径规划点
    def get_route(start, end, mode, amap_key):
        #walking 这里的url中选择是步行，公交还是驾车路径，本文中driving?表示驾车，具体介绍见：https://lbs.amap.com/api/webservice/guide/api/direction
        url = f'https://restapi.amap.com/v3/direction/walking?origin={start}&destination={end}&strategy={mode}&key={amap_key}'
        response = requests.get(url)
        data = response.json()

        if data['status'] == '1':
            route = data['route']['paths'][0]['steps']
            return route
        else:
            print('请求失败，请检查输入参数。')
            return None
    location1=[31.024075697,121.43663227] #东下院
    location2=[31.0269309351,121.42602682] #霍体
    location3=[31.0252684663,121.4420986175] #电院
    # 起始点经纬度（格式：经度,纬度）
    location=[float(Lat1),float(Lon1)]
    source_location = str(Lon1)+','+str(Lat1)
    # 目标经纬度（格式：经度,纬度）
    target_location = '121.43348,31.01873'#校医院
    # 替换为你的高德API密钥,在高德开放平台里注册-》应用管理-》创建新应用-》服务平##台那里选择web服务-》记住生成的key，这里没有密钥的。后续填写到amap_key中
    amap_key = '951f8ee561869fcfe41c01259f8f0599'
# 路径规划策略，可以选择0~5的整数，具体含义可以参考高德API文档 具体介绍见：https://lbs.amap.com/api/webservice/guide/api/direction
# 本文用的是驾车路径，
# 0，速度优先，此路线不一定距离最短
# 1，费用优先，不走收费路段，且耗时最少的路线
# 2，距离优先，仅走距离最短的路线，但是可能存在穿越小路/小区的情况
# 3，速度优先，不走快速路，例如京通快速路（因为策略迭代，建议使用13）
# 4，躲避拥堵，但是可能会存在绕路的情况，耗时可能较长
# 5，多策略（同时使用速度优先、费用优先、距离优先三个策略计算路径）。
# 其中必须说明，就算使用三个策略算路，会根据路况不固定的返回一~三条路径规划信息。
# 6，速度优先，不走高速，但是不排除走其余收费路段
# 7，费用优先，不走高速且避免所有收费路段
# 8，躲避拥堵和收费，可能存在走高速的情况，并且考虑路况不走拥堵路线，但有可能存在绕路和时间较长
# 9，躲避拥堵和收费，不走高速
# #######################################################################################################
    strategy = 2
    list_latlon=[]
    Lon = []
    Lat = []
    guideline=""
    route = get_route(source_location,target_location, strategy, amap_key)
    if route:
        for i, step in enumerate(route):
            list_latlon.append(step["polyline"])
            instruction = step["instruction"]
            guide = f"步骤 {i+1}: {instruction}"
            guideline = guideline+guide+'\n'
    else:
        print('无法获取路线规划。')
    # 获取街道地图
    for item in list_latlon:
        points = item.split(';')
        for point in points:
            coords = point.split(',')
            Lon.append(float(coords[0]))
            Lat.append(float(coords[1]))
    tri = np.array(list(zip(Lat, Lon)))
    san_map = folium.Map(
        location=location1,
        zoom_start=16,#18
        # 高德街道图
        #tiles='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
        tiles='http://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}', # 高德卫星图
        attr='default')
    san_map.add_child(folium.LatLngPopup())
    #san_map.add_child(folium.ClickForMarker())
    folium.PolyLine(tri, color='#3388ff').add_to(san_map)
    marker_cluster = plugins.MarkerCluster().add_to(san_map)
    folium.Marker(location, color='red',popup="实时位置").add_to(marker_cluster)
    folium.Marker(location1, color='red',popup="1:东下院").add_to(marker_cluster)
    folium.Marker(location2, color='red',popup="2:霍体").add_to(marker_cluster)
    folium.Marker(location3, color='red',popup="3:电院").add_to(marker_cluster)
    san_map.save('./templates/choosepoint1.html')
    with open('./templates/choosepoint1.html', 'r') as file:
        file_content = file.read()
        start_index=file_content.find('<body>')#起点
        end_index=file_content.find("<div",start_index)#终点
        if end_index==-1 or start_index==-1:
            print('未找到待修改位置')
        a1 = "<div class='box' style='top:30px; left:100px; position: fixed; background-color:transparent; z-index: 999;'>\n"
        a2 = "<div class='tap'>\n"
        a3 = "<a href='/patientcenter/' style='border: 2px solid #040000; background-color:#FFFFFF;'>返回首页</a>\n"
        a4 = "</div>\n"
        a5 = "<form id='luxian' method='POST' action='/traffic/'>\n"
        a6 = "<div>\n"
        a7 = "{% csrf_token %}\n"
        a8 = "<input class='input_box' type='text' name='num' placeholder='位置序号' />\n"
        a9 = "<input class='input_box' type='text' name='lat' placeholder='纬度' />\n"
        a10 = "<input class='input_box' type='text' name='lon' placeholder='经度' />\n"
        a11 = "<input class='button_box' type='submit' value='确认' />\n"
        a12 = "</div>\n"
        a13 = "</form>\n"
        a14 = "<textarea cols='25' rows='5' style='width: 228px;'>\n"
        a15 = guideline
        a16 = "</textarea>\n"
        a17 = "</div>\n"
        ricean_factor= a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11+a12+a13+a14+a15+a16+a17
        update_content = file_content[:start_index]+"<body>"#获取这行代码之前的内容
        update_content += ricean_factor#修改这行代码
        update_content += file_content[end_index:]#获取这行代码之后的内容
        #写入文件
        if update_content!="":#如果修改内容不为空
            with open('./templates/choosepoint1.html', 'w') as file:#w表示覆盖写入，之前的内容都会被覆盖
                file.write(update_content)
#PlotLineOnMap('31.0224','121.4374')