# -*- coding:utf-8-*-
"""
搜索给定位置周边环境
"""
from requests import get


class APISearch():
    UrlPart = {
        "urlhead":
        "https://restapi.amap.com/v3/place/around?key=6de2b5a95a0e35fc03782b55d455d8c4",
        "key": "&key=6de2b5a95a0e35fc03782b55d455d8c4",
        "keywords": "&keywords=学校",
        "location": "&location=103.968104,30.672837",
        "radius": "&=1000"
    }

    def __init__(self):
        super().__init__()
        # 验证网站链接是否正确
        if True:
            TestUrl = self.UrlPart["urlhead"] + self.UrlPart[
                "location"] + self.UrlPart["radius"] + self.UrlPart["keywords"]
        else:
            TestUrl = "https://restapi.amap.com/v3/place/around?key=6de2b5a95a0e35fc03782b55d455d8c4&location=116.473168,39.993015&radius=10000&types=011100"
        html = get(TestUrl).json()
        if not html['info'] == "OK":
            self.html = html['info']
            print(html['info'])
            return
        else:
            print("url test succeed")
            self.html = html
    # 搜索周边的学校

    def School(self):
        pois = self.html['pois']
        for k in pois:
            print(k['pname'] + k['cityname']+k['adname'] +
                  k['address'] + "\n"+k['name']+k['location']+"\n")


if __name__ == "__main__":
    aps = APISearch()
    aps.School()
