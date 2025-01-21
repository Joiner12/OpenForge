#-*- coding:utf-8 -*-
import requests
import json
# from Coordin_transformlat import gcj02towgs84
"""
    https://lbs.amap.com/api/webservice/guide/api/search#text
"""


def Get_poi(api_key, key_words, **kwargs):
    # 设置header
    header = {
        'User-Agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
    }

    # 构建url
    # //restapi.amap.com/v3/place/text?key=您的key&keywords=北京大学&types=高等院校&city=北京&children=1&offset=20&page=1&extensions=all
    url_base = 'https://restapi.amap.com/v3/place/text?'
    url = '{}key={}&keywords={}&city=chengdu&offset=2&page=1&extensions=base'.format(
        url_base, api_key, key_words)

    # 用get函数请求数据
    r = requests.get(url, headers=header)
    # 设置数据的编码为'utf-8'
    r.encoding = 'utf-8'
    # 将请求得到的数据按照'utf-8'编码成字符串
    data = r.text
    return data


def GET_Single_POI(key_words, *wargs, **kwargs):
    lon_lat = (-1, -1)
    # 高德API key
    key = '3afe3a1c16e7e3afc8e01df0ed7ef138'
    result = Get_poi(key, key_words)
    # json.loads可以对获取回来JSON格式的数据进行解码
    content = json.loads(result)
    if content['status'] == '1':
        pois = content['pois']
        location = pois[0]['location']
        lon_lat[0] = str(location).split(",")[0]
        lon_lat[1] = str(location).split(",")[1]
    # (经,纬)
    return lon_lat


# 读取原始数据
with open(r'D:\Code\HouseMonitor\src\DataMining\Yaohao\test-1.txt', 'r') as f:
    file_data = f.readlines()
#
data_len = list()
for data_line in file_data[1:]:
    temp = data_line.split(",")
GET_Single_POI()