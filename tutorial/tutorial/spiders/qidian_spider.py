# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
import time
import threading
from selenium.webdriver.chrome.options import Options


class DmozSpider(scrapy.spiders.Spider):
    name = "book"
    allowed_domains = ["qidian.com"]
    start_urls = [
        "https://www.qidian.com/"
    ]

    chrome_options = Options()

    chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错

    chrome_options.add_argument('window-size=800x600')  # 指定浏览器分辨率
    chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # chrome_options.add_argument('--headless')

    def parse(self, response):
        #拿到左侧分类列表
        for sel in response.xpath('//div[contains(@id, "classify-list")]/dl/dd'):
            href = sel.xpath('a/@href').extract_first()
            hr_in = href.lstrip('/')
            url = response.urljoin(hr_in)
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        #拿到分类下书的列表
        for sel in response.xpath('//div[contains(@class, "rec-list")]/ul/li/em'):
            url_book = "https:" + sel.xpath('a/@href').extract_first()
            return scrapy.Request(url_book, callback=self.parse_book_info)

    dict_all_book_zhangjie = {}

    #获取书的信息
    def parse_book_info(self, response):
        book_name = response.xpath('//div[contains(@class, "book-info")]/h1/em/text()').extract_first()
        href = "https:" + response.xpath('//div[contains(@class, "book-info")]/p/a[contains(@id, "readBtn")]/@href').extract_first()
        list_detail = []
        dict_this = {book_name: list_detail}
        self.dict_all_book_zhangjie.update(dict_this)

        #打开链接
        browser = webdriver.Chrome(options=self.chrome_options)
        browser.get(href)

        #尝试关闭指南弹窗
        try:
            zhinan_close_btn = browser.find_element_by_xpath('//a[contains(@class, "lbf-panel-close lbf-icon lbf-icon-close")]')
            zhinan_close_btn.click()
        except Exception, e:
            print "zhinan_close_btn failed"
            print repr(e)

        #尝试关闭福利广告弹窗
        try:
            fuli_close_btn = browser.find_element_by_xpath("//div[contains(@style, '/349573/75d219eb067fae4345538fb91edf0ad4/0')]")
            fuli_close_btn.click()
        except Exception, e:
            print "fuli_close_btn failed"
            print repr(e)

        #点击目录按钮
        mulu_btn = browser.find_element_by_xpath('//dd[contains(@id, "j_navCatalogBtn")]/a')
        mulu_btn.click()

        time.sleep(1)
        #获取点击目录按钮后动态创建的包含章节列表的网页内容
        page = browser.page_source
        browser.close()
        #将新的网页内容转换为HtmlResponse对象
        resp = HtmlResponse('', body=page, encoding='utf-8')
        type_ = 0
        queueLock = threading.Lock()
        #章节数
        all = resp.xpath('//div[contains(@class, "volume-list")]/ul/li').__len__()
        for sel in resp.xpath('//div[contains(@class, "volume-list")]/ul/li'):
            href = "https:" + sel.xpath('a/@href').extract_first()
            type_ += 1
            yield scrapy.Request(href, callback=self.parse_zhangjiedetail,
                                 meta={'type_': bytes(type_), 'name': book_name, 'lock': queueLock, 'all': all}, errback=self.parse_zhangjie_error)

    #获取章节信息
    #type_用于排序
    #name为书名
    #lock锁
    #all章节总数
    def parse_zhangjiedetail(self, response):
        type_ = int(response.meta['type_']) - 1
        name = response.meta['name']
        all = response.meta['all']

        #章节名
        zhangjie = response.xpath('//h3[contains(@class, "j_chapterName")]/text()').extract_first()
        #章节内容
        detail = response.xpath('//div[contains(@class, "read-content j_readContent")]/p/text()').extract()
        d = "\n" + zhangjie + "\n"
        for onepice in detail:
            d += onepice + "\n"
        lock = response.meta['lock']
        lock.acquire()
        list_detail = self.dict_all_book_zhangjie[name]
        tup = (type_, d)
        list_detail.append(tup)
        self.dict_all_book_zhangjie[name] = list_detail
        print len(list_detail)
        print all
        #判断已获取的章节数如果不等于章节总数-获取失败的章节数 - 跳过   如果相同 - 写入
        if len(list_detail) != all - self.error_nums:
            lock.release()
            return False

        list_detail = self.dict_all_book_zhangjie[name]
        # del self.dict_all_book_zhangjie[name] 此处会有问题  但是屏蔽之后容易内存溢出 考虑到文本内容容量小 暂时屏蔽
        lock.release()
        #按type_排序
        list_detail.sort(key=self.takeFirst)
        print "write"
        info = ""
        #写入文件 -- E盘qidian文件夹下
        filename = '%s.txt' % name
        filepath = 'E:\\qidian\\%s' % filename
        for i in list_detail:
            info += i[1].encode('utf-8')
        with open(filepath, 'w') as f:
            f.write(info)

    error_nums = 0

    def parse_zhangjie_error(self, response):
        self.error_nums += 1
        print self.error_nums

    def takeFirst(self, elem):
        return elem[0]
