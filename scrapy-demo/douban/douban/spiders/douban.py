# coding=utf-8
from scrapy.spiders import Spider
import re
from scrapy import Request
from ..items import DoubanImgsItem


class Douban(Spider):
    name = 'douban'

    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cookie': 'll="118282"; bid=UptK4kDEzj0; ue="cnhacker459@163.com"; gr_user_id=72bc77c5-d8e3-400e-abd3-5833aae9f885; ap=1; _vwo_uuid_v2=F7FF3E3B4FF64E68D5236A13BA96204A|4dfe5cca086f3d59f4b36a85ed3a90b7; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1488266010%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D_DuWJ5rsiaxCIdv1pj1hT7ytR63fdl15ChB0apCmpGvCevamdZ5Ws3V2tBVh_tiI%26wd%3D%26eqid%3Dd372c3980001d16800000006589b21d9%22%5D; _pk_id.100001.8cb4=e321643b0837abd0.1480306554.80.1488266010.1487570926.; _pk_ses.100001.8cb4=*',
        'Host': 'www.douban.com',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    def __init__(self, url='72064682', *args, **kwargs):
        self.allowed_domains = ['douban.com']
        self.start_urls = [
            'https://www.douban.com/photos/album/%s/' % (url)]
        self.url = url
        super(Douban, self).__init__(*args, **kwargs)

    def start_requests(self):
        # start_urls是一个列表 里面包含了url  循环这个列表
        for url in self.start_urls:
            # callback代表回调函数 这里指定了下面的parse函数
            yield Request(url=url, headers=self.default_headers, callback=self.parse)

    def parse(self, response, **kwargs):
        # 循环该页面
        list_imgs = response.xpath('//div[@class="photolst clearfix"]//img/@src').extract()

        if not list_imgs:
            # 如果没有就返回
            return

        # 有照片
        for url in list_imgs:
            # 创建一个图片对象 然后 yield
            item = DoubanImgsItem()
            item['image_urls'] = [url]
            yield item

        next = response.xpath('//*[@id="content"]/div[2]/div[1]/div[6]/span[3]/a')
        if next:
            path = next[0].xpath('@href')[0].extract()
            yield Request(url=path, headers=self.default_headers, callback=self.parse)
