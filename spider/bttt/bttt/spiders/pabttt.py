# -*- coding: utf-8 -*-
import scrapy
from bttt.items import BtttItem
import re
import time
import urllib.request
from PIL import Image
from bttt.mysqlConfigs import mysql_config


class PabtttSpider(scrapy.Spider):
    name = 'pabttt'
    allowed_domains = ['douban.com', 'bttt.la']
    #start_urls = ['https://www.bttt.la/movie.php?/order/id/1/']
    login_url = "https://accounts.douban.com/login"
    start_urls = [login_url]
    front_url = "https://www.bttt.la"

    def parse(self, response):
        img_link = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
        user_name = input('user:')
        user_passwd = input('passwd:')

        if img_link is None:
            print("登陆时没有遇到验证码...")
            formdata = {
                "source": "index_nav",
                "redir": "https://www.douban.com",
                "form_email": user_name,
                "form_password": user_passwd,  # 密码
                "login": "登录",
            }

        else:
            print("登陆时遇到验证码...")
            # 图片存储路径
            img_path = mysql_config['img_path']
            # 第一个参数接受url，第二个参数接受存储路径
            urllib.request.urlretrieve(img_link, img_path)
            try:
                # 自动打开验证码图片
                im = Image.open(img_path)
                im.show()
            except:
                print("打开图片失败...")

            captcha_solution = input("请输入验证码:")

            formdata = {
                "source": "index_nav",
                "redir": "https://www.douban.com",
                "form_email": user_name,  # 密码
                "form_password": user_passwd,
                "login": "登录",
                "captcha-solution": captcha_solution,
                "captcha-id": captcha_id,
            }

        print("正在登陆中...")
        yield scrapy.FormRequest(url=self.login_url, formdata=formdata, callback=self.login_after)

    def login_after(self, response):
        r = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()
        if r is None:
            print("登陆失败！")
        else:
            print("登陆成功！当前账户为：%s" % r)
            yield scrapy.Request(url='https://www.bttt.la/movie.php?/order/id/1/', callback=self.bttt_parse)

    def bttt_parse(self, response):
        # 每一页的电影链接
        pgUrl_list = response.xpath("//div[@class='perone']/div[@class='litpic']/a/@href").extract()
        for title in pgUrl_list:
            url = self.front_url + title
            yield scrapy.Request(url=url, callback=self.bt_page_parse)
        # 下一页的url
        next_url = self.front_url + response.xpath("//ul[@class='pagelist']/li[last()-1]/a/@href").extract_first()
        yield scrapy.Request(url=next_url, callback=self.bttt_parse)

    def bt_page_parse(self, response):
        # bt详情页里面的豆瓣跳转页面
        redirect_url = self.front_url + response.xpath("//a[@rel='nofollow']/@href").extract_first()
        # bt详情页中的bt种子链接
        bt_url_list = response.xpath("//div[@class='tinfo']/a/@href").extract()
        if len(bt_url_list) != 0:
            # 请求跳转页面取豆瓣url.
            yield scrapy.Request(url=redirect_url, callback=self.get_douban, meta={'data': bt_url_list[0]})
        else:
            return

    def get_douban(self, response):
        # 匹配豆瓣url
        douban_url = re.findall(r'location\.href=(.*?);', response.body.decode(), re.S)[0].strip('"')
        douban_url = douban_url[0:4] + douban_url[4:-1] + '/'
        print(f"douban:{douban_url}")
        bt_url = response.meta['data']
        # 请求bt种子链接
        yield scrapy.Request(url=self.front_url + bt_url, callback=self.get_bt, meta={'data': douban_url})

    def get_bt(self, response):
        # 匹配种子链接中的磁力
        dLink = re.findall('<a href="(.*?)&.*?">', response.body.decode())[1]
        douban_url = response.meta['data']
        # 请求豆瓣详情页
        yield scrapy.Request(url=douban_url, callback=self.doubana, meta={'dLink': dLink})
        #time.sleep(1)

    def doubana(self, response):
        # 详情页
        try:
            item = BtttItem()
            item['title'] = response.xpath("//span[@property='v:itemreviewed']/text()").extract_first()
            item['year'] = response.xpath("//span[@class='year']/text()").extract_first().strip('()')
            div_id_info = response.xpath("string(//div[@id='info'])").extract_first()
            item['country'] = re.findall(r"制片国家/地区: (.*?)\n", div_id_info)[0]
            item['lan'] = ''.join(re.findall(r"语言: (a.*?)\n", div_id_info))
            item['douban_link'] = response.url
            div_class_indent = response.xpath("string(//div[@class='indent'])").extract_first()
            item['introduce'] = ''.join(re.findall(r"\u3000\u3000(.*?)\n", div_class_indent))
            item['main_actor'] = ''.join(re.findall(r"主演: (.*?)\n", div_id_info))
            item['download_url'] = response.meta['dLink']
            item['img_url'] = response.xpath("//a[@class='nbgnbg']/img/@src").extract_first()
            yield item
        except Exception as e:
            print(f"error:{e}")
