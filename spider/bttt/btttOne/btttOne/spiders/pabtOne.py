# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from btttOne.items import BtttoneItem
import urllib.request
from PIL import Image
from btttOne import settings
import time
import traceback


class PabtoneSpider(CrawlSpider):
    name = 'pabtOne'
    allowed_domains = ['bttt.la', 'douban.com']
    login_url = "https://accounts.douban.com/login"
    bt_one_url = 'https://www.bttt.la/movie.php?/order/id/1/'
    start_urls = [login_url, bt_one_url]
    front_url = "https://www.bttt.la"

    rules = (
        Rule(LinkExtractor(allow=r'/movie\.php\?/order/id/\d+/'), callback='parse_item', follow=True),
    )

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_douban)
        time.sleep(2)

    def parse_douban(self, response):
        img_link = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
        user_name = settings.douban_user
        user_passwd = settings.douban_passwd

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
            img_path = settings.img_path
            # 第一个参数接受url，第二个参数接受存储路径
            urllib.request.urlretrieve(img_link, img_path)

            try:
                # 自动打开验证码图片
                im = Image.open(img_path)
                im.show()

            except Exception as e:
                print(f"打开图片失败...{e}")

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
        resp = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()

        if resp is None:
            print("登陆失败！")

        else:
            print(f"登陆成功！当前账户为:{resp}")
            yield scrapy.Request(url=self.start_urls[1], callback=self.parse)

    def parse_item(self, response):
        movie_url_list = response.xpath("//div[@class='perone']/div[@class='litpic']/a/@href").extract()

        for title_url in movie_url_list:
            url = self.front_url + title_url
            yield scrapy.Request(url=url, callback=self.movie_page_parse)

    def movie_page_parse(self, response):
        # bt网站中的详情页面url.
        bt_movie_url = response.url
        # bt详情页里面的豆瓣跳转页面.
        redirect_url = self.front_url + response.xpath("//a[@rel='nofollow']/@href").extract_first()
        # 请求跳转页面取豆瓣url.
        yield scrapy.Request(url=redirect_url, callback=self.crawl_douban_url,
                             meta={'movie_url': bt_movie_url})

    def crawl_douban_url(self, response):
        # 匹配豆瓣
        douban_url = re.findall(r'location\.href=(.*?);', response.body.decode())   # , re.S

        if len(douban_url) != 0:
            douban_link = douban_url[0].strip('"')
            print(f"douban_url:{douban_link}")
            yield scrapy.Request(url=douban_link, callback=self.parse_detail_douban,
                                 meta={'movie_url': response.meta['movie_url']})

        else:
            return

    def parse_detail_douban(self, response):
        # 详情页
        try:
            douban_link = response.url
            if douban_link[4] == 's':
                douban_link = douban_link[0:4] + douban_link[5:-1] + '/'

            item = BtttoneItem()
            item['title'] = response.xpath("//span[@property='v:itemreviewed']/text()").extract_first()
            item['year'] = response.xpath("//span[@class='year']/text()").extract_first().strip('()')

            div_id_info = response.xpath("string(//div[@id='info'])").extract_first()
            item['director'] = ''.join(re.findall(r"导演: (.*?)\n", div_id_info))
            item['screenwriter'] = ''.join(re.findall(r"编剧: (.*?)\n", div_id_info))
            item['main_actor'] = ''.join(re.findall(r"主演: (.*?)\n", div_id_info))
            item['country'] = ''.join(re.findall(r"制片国家/地区: (.*?)\n", div_id_info))
            item['lan'] = ''.join(re.findall(r"语言: (.*?)\n", div_id_info))
            item['types'] = ''.join(re.findall(r"类型: (.*?)\n", div_id_info))
            item['duration'] = ''.join(re.findall(r"片长: (.*?)\n", div_id_info))
            item['douban_link'] = douban_link

            div_class_indent = response.xpath("string(//div[@class='indent'])").extract_first()
            item['introduce'] = ''.join(re.findall(r"\u3000\u3000(.*?)\n", div_class_indent))

            item['img_url'] = response.xpath("//a[@class='nbgnbg']/img/@src").extract_first()
            yield item

        except:
            traceback.print_exc()

        # except Exception as e:
        #     print(f"详情页发生错误:{e}")


