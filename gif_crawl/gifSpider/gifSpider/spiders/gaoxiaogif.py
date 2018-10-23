# -*- coding: utf-8 -*-
import re
from copy import deepcopy

import scrapy


class GaoxiaogifSpider(scrapy.Spider):
    name = 'gaoxiaogif'
    allowed_domains = ['gaoxiaogif.com']
    start_urls = [
        'http://m.gaoxiaogif.com/tag/neihandongtaitu/',
        'http://m.gaoxiaogif.com/tag/fuli/',
        # 'http://m.gaoxiaogif.com/tag/buzuosijiubuhuisi/',
        'http://m.gaoxiaogif.com/tag/niurenxilieGIF/',
        # 'http://m.gaoxiaogif.com/tag/zhongkouweiGIFtupian/',
        'http://m.gaoxiaogif.com/tag/zhangzishi/',
        # 'http://m.gaoxiaogif.com/tag/chehuoGIF/',
    ]

    def parse(self, response):
        if response.status != 404:
            ul_list = response.xpath('//ul[@id="tp_lists"]/li')
            for li in ul_list:
                item = {}
                url = li.xpath('.//a/@href').extract_first()
                url = 'http://m.gaoxiaogif.com' + url
                # print('--->',url)
                item['title_url'] = url
                title = li.xpath('.//h3/@title').extract_first()
                # print('--->',title)
                item['title'] = title
                yield scrapy.Request(
                    url,
                    callback=self.parse_detail,
                    meta={'item': deepcopy(item), 'curr_page': 1}
                )
        # 翻页
        if response.status != 404:
            print('***********', response.url)
            print('***********', response.meta.get('curr_page'))
            curr_page = response.meta.get('curr_page')
            if not curr_page:
                curr_page = 1
            # for i in range(SCRAPY_DEEPTH):
            next_url = '/'.join(response.url.split('/')[:-1])
            next_url += '/index_{}.html'.format(curr_page + 1)
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta={'curr_page': curr_page + 1}
            )

    def parse_detail(self, response):
        # res = re.findall(r'src="(.*?)">',response.text)
        item = response.meta.get('item')
        img_url = response.xpath('//*[@id="img-box"]/p[2]/img/@src').extract_first()
        # print(detail_url)
        item['img_url'] = img_url
        item['source'] = 'http://m.gaoxiaogif.com'
        # print(item)
        yield item
