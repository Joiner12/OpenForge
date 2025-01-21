#-*- coding:utf-8 -*-
"""
    Created on Wed Feb 15 17:37:11 2023

    @author: W-H
    
"""
################################################
# 获取摇号楼盘信息
################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os, re
from time import sleep
import random

# workspace
cmd = '''cd D:\Code\HouseMonitor\src\DataMining\Yaohao\src'''
os.system(cmd)
data_file = r'D:\Code\HouseMonitor\src\DataMining\Yaohao\test-1.txt'
data = list()
table_header = [
    "区域", "项目名称", "预售证号", "预售范围", "住房套数", "开发商咨询电话", "登记开始时间", "登记结束时间",
    "名单外人员资格已释放时间", "名单内人员资格已释放时间", "预审码取得截止时间", "项目报名状态", "联系地址"
]


class Yaohao():
    # 基链接
    base_url = ""
    browser = None

    def __init__(
            self,
            base_url=r'https://zw.cdzjryb.com/lottery/accept/index') -> None:
        self.base_url = base_url
        # 初始化浏览器驱动
        try:
            self.browser = webdriver.Edge(
                executable_path=
                r"D:\Code\HouseMonitor\src\DataMining\Yaohao\driver\msedgedriver.exe",
                capabilities={
                    "browserName": "MicrosoftEdge",
                    "version": "",
                    "platform": "WINDOWS",
                    "ms:edgeOptions": {
                        'extensions': [],
                        #'args': ['--headless']
                    }
                })
        except:
            # return
            pass
        # 主页面
        self.start_home_page()
        try:
            cur_page = 1
            while True:
                cur_page = self.get_cur_page_num()
                #cur_page_table = self.get_table_content()
                # cur_page_table = self.get_table_content_v1()
                #data.append(cur_page_table)
                sleep(2 + random.random())
                self.next_page()
                if cur_page >= 288:
                    break
        except:
            pass
        data_to_file(data)
        self.browser.close()

    # 跳转到信息页面
    def start_home_page(self):
        self.browser.get(self.base_url)
        x_path = '//*[@id="projectList"]'
        # x_path = "/html/body/div[3]/ul[2]/a[1]/li"
        self.browser.find_element(By.XPATH, x_path).click()

    # 下一页
    def next_page(self):
        x_path = '//div[@class="pages-box"]//a[8]'
        # x_path = '/html/body/div[2]/div[3]/a[8]'
        next_button = self.browser.find_element(By.XPATH, x_path)
        next_button.click()

    # 当前页数
    def get_cur_page_num(self):
        page_num = None
        try:
            page_num = self.browser.find_element(
                By.CSS_SELECTOR,
                "body > div.nav.nav-nobg > div.pages-box > a.on").text
        except:
            pass
        cut_str = "*" * 20 + "\r\n" + '|{: ^18}|\r\n'.format(
            int(page_num)) + "*" * 20
        print(cut_str)
        return int(page_num)

    # 读取表格
    def get_table_content_v1(self):
        x_path = '//table//tbody//tr'
        trs = self.browser.find_element(By.XPATH, x_path)
        for tr in trs:
            print(tr)

    # 读取表格
    def get_table_content(self, table_id="_projectInfo"):
        arr = list()
        arr_row = list()
        table = self.browser.find_element(By.ID, table_id)
        # 通过标签名获取表格的所有行
        table_tr_list = table.find_elements(By.TAG_NAME, "tr")
        # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
        for tr in table_tr_list:
            # 信息弹窗
            view_button = tr.find_element(By.CLASS_NAME, "view")
            view_button.click()
            # 文本内容
            WebDriverWait(self.browser, 2).until(
                expected_conditions.presence_of_all_elements_located(
                    (By.ID, "dialog-view")))
            sleep(2 + random.random())
            content_dia = self.browser.find_element(By.ID, "dialog-view").text
            house_location = re.findall("联系地址.*?\n", content_dia)
            # 关闭弹窗
            div_close = self.browser.find_element(By.CLASS_NAME,
                                                  "ui-dialog-buttonset")
            div_close.find_element(By.CLASS_NAME, "ui-button").click()
            #
            arr_row = (tr.text).split(" ")  # 以空格拆分成若干个(个数与列的个数相同)一维列表
            if len(house_location) > 0:
                loca_temp = house_location[0]
                loca_temp = loca_temp.replace("\n", "")
                loca_temp = loca_temp.replace("联系地址：", "")
            else:
                loca_temp = 'None'
            arr_row[-1] = loca_temp
            print(arr_row)
            arr.append(arr_row)  # 将表格数据组成二维的列表
        return arr


def data_to_file(data):
    with open(data_file, 'w') as f:
        temp = ",".join(table_header)
        f.writelines(temp + "\r\n")
    with open(data_file, 'a') as f:
        for data_table in data:
            for data_row in data_table:
                temp = ",".join(data_row)
                f.writelines(temp + "\r\n")


if __name__ == "__main__":
    yh = Yaohao()