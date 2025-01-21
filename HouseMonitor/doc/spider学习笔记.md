# Spider学习笔记

[TOC]



## 1.Scrapy一目了然

SCRAPPY(/ˈSkreɪpaɪ/)是一个应用程序框架，用于抓取网站和提取结构化数据，这些数据可用于广泛的有用应用程序，如数据挖掘、信息处理或历史存档。

## 2.安装指南

## 3.基本概念

本教程将指导您完成以下任务：

1. 创建新的Scrapy项目
2. 写一篇 [spider](https://www.osgeo.cn/scrapy/topics/spiders.html#topics-spiders) 对网站进行爬网并提取数据
3. 使用命令行导出抓取的数据
4. 将spider改为递归跟踪链接
5. 使用蜘蛛参数

#### 3.1 创建项目

在开始抓取之前，你必须建立一个新的零碎项目。输入要在其中存储代码并运行的目录：

```shell
scrapy startproject project_name
```

这将创建一个 `tutorial` 目录包含以下内容：

```
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
```

### 1.1 terminal shell

```bash
# 生成爬虫指令
scrapy genspider itcast "itcast.cn"

```

问：

1. ->

   ```python
   def __init__(self) -> None:
   ```

2. s

## XPath

### 1.HTML

服务器读取URL，了解用户请求，然后回复一个HTML文档。HTML本质是一个文本文件。

- 尖括号里的字符称作`标签`，例如\<html>或\<head>。\<html>是起始标签，\</html>是结束标签。标签总是成对出现。某些网页没有结束标签，例如只用\<p>标签分隔段落，浏览器对这种行为是容许的，会智能判断哪里该有结束标签\</p>。
- \<p>与\</p>之间的内容称作HTML的`元素`。元素之间可以嵌套元素，比如例子中的\<div>标签，和第二个\<p>标签，后者包含了一个\<a>标签。
- 例如\<a href="http://www.iana.org/domains/example">，带有URL的href部分称作`属性`。
- 许多标签元素包含有文本，例如\<h1>标签中的Example Domain。

### 2.用XPath选择HTML元素

在Chrome中使用XPath，在开发者工具中点击控制台标签，使用$x功能。输入\$x('//h1')，就可以移动到\<h1>元素。

|         |                      |                                               |
| ------- | -------------------- | --------------------------------------------- |
| //      | 访问到所有的同名元素 | //p可以选择所有的p元素，//a可以选择所有的链接 |
| /       | 嵌套于标签内的标签   | //div/a选择所有div元素中的a元素               |
| @       | 属性筛选             | //a/@href 选择a的所有链接                     |
| *       | 通配符               | //div/* 选择div下的所有元素                   |
| text()  | 提取文字             | //a/text() 选择a元素下的文字                  |
| [@属性] | 寻找特定属性         |                                               |
|         |                      |                                               |
|         |                      |                                               |



## 爬虫基础

1. UR²IM——基础抓取过程

   URL→Request→Response→Item→More Urls

2. 使用Scrapy Sheel打开网站

   ```bash
   scrapy shell -s USER_AGENT="Mozilla/5.0" <your url here  e.g. http://www.gumtree.com/p/studios-bedsits-rent/...>
   ```

   –pdb:调试

3. 

## Reference

1. [Scrapy 2.5 documentation — Scrapy 2.5.0 documentation](https://docs.scrapy.org/en/latest/)
2. [从原理到实战，一份详实的 Scrapy 爬虫教程_菜鸟学Python的博客-CSDN博客](https://blog.csdn.net/cainiao_python/article/details/119224134)
3. [Python Scrapy中文教程，Scrapy框架快速入门！ (biancheng.net)](http://c.biancheng.net/view/2027.html)
4. [Scrapy 入门教程 | 菜鸟教程 (runoob.com)](https://www.runoob.com/w3cnote/scrapy-detail.html)
4. [Scrapy 教程 — Scrapy 2.5.0 文档 (osgeo.cn)](https://www.osgeo.cn/scrapy/intro/tutorial.html)
4. [python中yield的用法详解——最简单，最清晰的解释_冯爽朗的博客-CSDN博客_python yield](https://blog.csdn.net/mieleizhi0522/article/details/82142856)
4. [Scrapy css 语法|极客教程 (geek-docs.com)](https://geek-docs.com/scrapy/scrapy-tutorials/scrapy-css-grammar.html)
4. [Scrapy爬虫——突破反爬虫最全策略解析 - 简书 (jianshu.com)](https://www.jianshu.com/p/a94d7de5560f)
4. [fake-useragent/fake-useragent: Up-to-date simple useragent faker with real world database (github.com)](https://github.com/fake-useragent/fake-useragent)
4. [Python JSON | 菜鸟教程 (runoob.com)](https://www.runoob.com/python/python-json.html)
4. [ python+selenium(14)---定位table并获取table中的数据，并删除某一行数据（如果每行后面提供删除按钮）_wjgccsdn的博客-CSDN博客](https://blog.csdn.net/wjgccsdn/article/details/114023032)
4. [python中format用法（最全汇总）_西部点心王的博客-CSDN博客_python format](https://blog.csdn.net/moqisaonianqiong/article/details/114674204)
4. [数据结构简介 | Pandas (pypandas.cn)](https://pypandas.cn/docs/getting_started/dsintro.html)
4. [datetime — Basic date and time types — Python 3.11.2 documentation](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)
4. [Python批量查询地点坐标基于腾讯地图 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/401853601)
4. [(1条消息) Python获取高德POI(关键词搜索法)_Giser@lin的博客-CSDN博客](https://blog.csdn.net/abcbbbd/article/details/123650789)
4. [利用 Python 进行数据分析 · 第 2 版 - 《利用 Python 进行数据分析 · 第 2 版》 - 书栈网 · BookStack](https://www.bookstack.cn/read/pyda-2e-zh/README.md)

selenium+scrapy

1. [最新Scrapy（CrawlSpider）+Selenium全站数据爬取（简书）_CodeBoy‍的博客-CSDN博客](https://blog.csdn.net/qq_45352972/article/details/108985542)
2. [[Python3网络爬虫开发实战\] 13.8–Scrapy 对接 Selenium | 静觅 (cuiqingcai.com)](https://cuiqingcai.com/8397.html)
3. [scrapy对接selenium原理超详细解读！！！！_scrapy selenium_独角兽小马的博客-CSDN博客](https://blog.csdn.net/weixin_44457673/article/details/120074707)
4. [使用 Scrapy + Selenium 爬取动态渲染的页面 - 腾讯云开发者社区-腾讯云 (tencent.com)](https://cloud.tencent.com/developer/article/2016732?shareByChannel=link)
