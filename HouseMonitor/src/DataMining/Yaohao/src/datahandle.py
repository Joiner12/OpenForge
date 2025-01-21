#-*- coding:utf-8 -*-
import numpy as np
import pandas as pd
from datetime import datetime

data = pd.DataFrame(columns=[
    "区域", "项目名称", "预售证号", "预售范围", "住房套数", "开发商咨询电话", "登记开始时间", "登记结束时间",
    "名单外人员资格已释放时间", "名单内人员资格已释放时间", "预审码取得截止时间", "项目报名状态", "联系地址"
])

with open(r'D:\Code\HouseMonitor\src\DataMining\Yaohao\test-1.txt', 'r') as f:
    file_data = f.readlines()
#
data_len = list()
for data_line in file_data[1:]:
    temp = data_line.split(",")
    #
    if len(temp) == 18:
        data.iat[len(data) + 1, 0] = temp[0]
        data.iat[len(data) + 1, 1] = temp[1]
        data.iat[len(data) + 1, 2] = temp[2]
        data.iat[len(data) + 1, 3] = temp[3]
        data.iat[len(data) + 1, 4] = temp[4]
        data.iat[len(data) + 1, 5] = temp[5]
        dt = datetime.strptime("{} {}".format(temp[6], temp[7]),
                               '%Y-%m-%d %H:%M:%S')
        data.iat[len(data) + 1, 6] = dt
        dt = datetime.strptime("{} {}".format(temp[8], temp[9]),
                               '%Y-%m-%d %H:%M:%S')
        data.iat[len(data) + 1, 7] = dt
        dt = datetime.strptime("{} {}".format(temp[10], temp[11]),
                               '%Y-%m-%d %H:%M:%S')
        data.iat[len(data) + 1, 8] = dt
        dt = datetime.strptime("{} {}".format(temp[12], temp[13]),
                               '%Y-%m-%d %H:%M:%S')
        data.iat[len(data) + 1, 9] = dt
        dt = datetime.strptime("{} {}".format(temp[14], temp[15]),
                               '%Y-%m-%d %H:%M:%S')
        data.iat[len(data) + 1, 10] = dt
        data.iat[len(data) + 1, 11] = temp[16]
        data.iat[len(data) + 1, 12] = temp[17]
        data.iat[len(data) + 1, 13] = (0.0, 0.0)
    else:
        data.iat[len(data) + 1, 0] = temp[0]
        data.iat[len(data) + 1, 1] = temp[1]
        data.iat[len(data) + 1, 2] = temp[2]
        data.iat[len(data) + 1, 3] = temp[3]
        data.iat[len(data) + 1, 4] = temp[4]
        data.iat[len(data) + 1, 5] = temp[5]
        dt = datetime.strptime("{} {}".format(temp[6], temp[7]),
                               '%Y-%m-%d %H:%M:%S')
        data.iat[len(data) + 1, 6] = dt
        data.iat[len(data) + 1, -2] = temp[-1]
        data.iat[len(data) + 1, -1] = (0.0, 0.0)