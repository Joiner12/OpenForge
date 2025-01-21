# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 17:34:23 2023

@author: W-H
"""

from scrapy.cmdline import execute

# execute(["scrapy", "crawl", "lianjia_qingyang", "-o", "items.json"])
execute(["scrapy", "crawl", "lianjia_test"])
