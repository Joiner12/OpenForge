import scrapy
import time
from scrapy.http import Request
from Lianjia.items import LianjiaItem
import random


class LianjiaTestSpider(scrapy.Spider):
    name = "lianjia_test"
    allowed_domains = ["cd.fang.lianjia.com"]
    start_urls = ["http://cd.fang.lianjia.com/"]

    def __init__(self):
        self.url_num = 0
        self.apartment_num = 0
        self.done_num = 0

    def parse(self, response):
        if False:
            # 获取各个区的url
            regions = response.css(
                '#filter > ul:nth-child(2) > li.filter__item--level2 > a')
            for region in regions[1:]:
                url = 'https://cd.lianjia.com' + region.attrib['href']
                yield Request(url, callback=self.parse_region)
        else:
            url = 'https://cd.fang.lianjia.com/loupan/qingyang/'
            yield Request(url, callback=self.parse_region)

    # 遍历所有页
    def parse_region(self, response):
        house_num = int(
            response.xpath(
                '/html/body/div[3]/div[2]/div/span[2]/text()').get())  # 房子数量
        page_num = min(house_num // 30 + 1, 100)  # 每页展示30条
        print('house number:', house_num)
        for i in range(1, page_num + 1):
            time.sleep(random.randint(1, 3) / 10)
            time.sleep(0.1)
            url = response.url + 'pg{}'.format(i)
            print("获取单页数据")
            yield Request(url, callback=self.parse_overview)

    # 爬取房屋概况信息
    def parse_overview(self, response):
        infos = response.css('.resblock-list')

        for info in infos:
            suburl = info.css('a::attr(href)').get()
            print("楼盘链接")
            resblock_name = infos[0].css('.resblock-name>a::text').get()
            resblock_type = infos[0].css('.resblock-name>span::text').getall()
            resblock_location = infos[0].css(
                '.resblock-location>span::text').getall()
            resblock_location_link = infos[0].css(
                '.resblock-name>a::attr(href)').get()
            resblock_tag = infos[0].css('.resblock-tag span::text').getall()
            resblock_price = infos[0].css('.resblock-price *::text').getall()
            """
            1.['\n                        ','55000', '\xa0元/㎡(均价)', '总价480(万/套)']
            2.['\n                        ', '价格待定']
            """
            url = 'https://cd.lianjia.com' + suburl
            print(url)
            # if 'zufang' in suburl:
            #     if False:
            #         item = LianjiaItem()
            #         item['title'] = info.css(
            #             '.content__list--item--aside').attrib['title']
            #         item['location'] = '-'.join(
            #             info.css('.content__list--item--des a::text').getall())
            #         des = info.css('.content__list--item--des::text').getall()
            #         item['house_type'] = des[-2].strip()
            #     else:
            #         des = info.css('.content__list--item--des::text').getall()
            #         print(des)
            #     url = 'https://cd.lianjia.com' + suburl
            #     print(url)
            #     self.url_num += 1
            #     if True:
            #         print('url_num: ', self.url_num)
            #     else:
            #         yield Request(url,
            #                       meta={'item': item},
            #                       callback=self.parse_info)
            #     # yield item
            # else:
            #     self.apartment_num += 1
            #     # print('apartment_num: ', self.apartment_num)

    # 爬取房屋详细信息
    def parse_info(self, response):
        resblock_name = response.css('.title-wrap>div>h2::text').get()
        resblock_name_second_name = response.css(
            '.title-wrap>.other-name::text').get()
        # ['参考均价', '16000', '元/平(单价) ', '95', '(万/套)(总价)', '参考均价', '16000', ' 元/平']
        reblock_price = response.css('.price span::text').getall()
        # ['商业类', '环线房', '近主干道', '配套齐全']
        reblock_tag = response.css('.resblock-tag>.item span::text').getall()
        reblock_location_content = response.css(
            '.info-list .content::text').get()
        reblock_location_map = response.css(
            '.info-list .map a::attr(href)').get()
        try:
            item = response.meta['item']

            # res = response.css('i.gov_title::text').getall()
            # print('res:',res)
            item['house_code'] = response.css(
                'i.gov_title::text').getall()[1].split('：')[1].strip()
            # print('house_code:', item['house_code'])

            item['price'] = response.css('div.content__aside--title span::text').get() + \
                            response.css('div.content__aside--title::text').getall()[1].strip()
            # print('price:', item['price'])

            item['tags'] = ','.join(
                response.css('p.content__aside--tags i::text').getall())
            # print('tags:', item['tags'])

            item['lease'] = response.css(
                '#aside > ul > li:nth-child(1)::text').get()
            # print('lease:', item['lease'])

            item['area'] = response.css(
                '#info > ul:nth-child(2) > li:nth-child(2)::text').get().split(
                    '：')[1]
            # print('area:', item['area'])

            item['orientation'] = response.css(
                '#info > ul:nth-child(2) > li:nth-child(3)::text').get().split(
                    '：')[1]
            # print('orientation:', item['orientation'])

            item['floor'] = response.css(
                '#info > ul:nth-child(2) > li:nth-child(8)::text').get().split(
                    '：')[1]
            # print('floor:', item['floor'])

            item['elevator'] = response.css(
                '#info > ul:nth-child(2) > li:nth-child(9)::text').get().split(
                    '：')[1]
            # print('elevator:', item['elevator'])

            item['stall'] = response.css(
                '#info > ul:nth-child(2) > li:nth-child(11)::text').get(
                ).split('：')[1]
            # print('stall:', item['stall'])

            item['water'] = response.css(
                '#info > ul:nth-child(2) > li:nth-child(12)::text').get(
                ).split('：')[1]
            # print('water:', item['water'])

            item['electricity'] = response.css(
                '#info > ul:nth-child(2) > li:nth-child(14)::text').get(
                ).split('：')[1]
            # print('electricity:', item['electricity'])

            item['fuel_gas'] = response.css(
                '#info > ul:nth-child(2) > li:nth-child(15)::text').get(
                ).split('：')[1]
            # print('fuel_gas:', item['fuel_gas'])

            item['heating'] = response.css(
                '#info > ul:nth-child(2) > li:nth-child(17)::text').get(
                ).split('：')[1]
            # print('heating:', item['heating'])

            # item['stall'] = response.css('#info > ul:nth-child(2) > li:nth-child(11)::text').get().split('：')[1]
            facilities = response.css(
                'body > div.wrapper > div:nth-child(2) > div.content.clear.w1150 > div.content__detail > div.content__article.fl > ul > li'
            )
            facility_list = []
            for facility in facilities[1:]:
                if 'no' not in facility.attrib['class']:
                    facility_list.append(
                        facility.css('::text').getall()[-1].strip())
            item['facility'] = ','.join(facility_list)
            # print('facility:', item['facility'])
            #
            item['description'] = ''.join([
                x.strip()
                for x in response.css('#desc > p:nth-child(3)::text').getall()
            ])
            # print('#' * 60)

            self.done_num += 1
            print(
                'url_num:', self.url_num, 'apartment_num:', self.apartment_num,
                'done_num:', self.done_num, "finishing rate:{:.2f}-%".format(
                    self.done_num / self.url_num * 100))
            # print(item)
            # print("#"*60)
            yield item  # 返回数据
        except AttributeError as e:
            print(e)
            time.sleep(5)
