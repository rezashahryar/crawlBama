from number.items import NumberItem
import scrapy
import json


class CrawlNumberSpider(scrapy.Spider):
    name = 'crawlBama'

    def start_requests(self):
        global header
        header = {
        'content-type': "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'referer': 'https://bama.ir/'
        }
        for i in range(1, 1100):
            url = f'https://bama.ir/cad/api/search?pageIndex={i}'
            yield scrapy.Request(url=url, headers=header, method='GET', callback=self.parse)


    def parse(self, response, **kwargs):
        api_phone = 'https://bama.ir/cad/api/detail/{token}/phone'
        data = json.loads(response.body)
        for url in data['data']['ads']:
            if url['type'] == 'ad':
                url = url['metadata']['canonical']

        for code in data['data']['ads']:
            if code['type'] == 'ad':
                code = code['detail']['code']
                print(code)
                yield scrapy.Request(url=api_phone.format(token=code), method='GET', callback=self.get_info)

    def get_info(self, response):
        items = NumberItem()
        data = json.loads(response.body)
        if data['data']['phone'] is not None:
            for phone in data['data']['phone']:
                items['phone'] = data['data']['phone']
        if data['data']['mobile'] is not None:
            items['mobile'] = data['data']['mobile']

        yield items