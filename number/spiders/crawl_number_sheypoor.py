import scrapy
import json
import time


class CrawlNumberSheypoor(scrapy.Spider):
    name = 'crawlNumbeerSheypoor'

    header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://www.sheypoor.com/api/v10.0.0/auth/send'
        body = "{'username': '09050236353'}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Referer": "https://www.sheypoor.com/session?return=https://www.sheypoor.com/session/myListings/active",
        }

        yield scrapy.Request(url=url, method='POST', body=body, callback=self.send_password, headers=headers)

    def send_password(self, response):
        data = json.loads(response.body)
        url = 'https://www.sheypoor.com/api/v10.0.0/auth/verify'
        token = data['data']['verify']['token']
        code = str(input("please enter your code:"))
        body = '{"verification_code": code, "verify_token": token}'

        yield scrapy.Request(url=url, method='POST', dont_filter=True, body=body, callback=self.parse)


    def parse(self, response):
        url = 'https://www.sheypoor.com/api/v10.0.0/listings/{id}/number'
        data = json.loads(response.body)
        
        for item in data['data']:
            idd = item['id']
            yield scrapy.Request(url.format(id=idd), method='GET', callback=self.get_info)
            time.sleep(10)

    def get_info(self, response):
        data = json.loads(response.body)
        phoneNumber = data['data']['attributes']['phoneNumber']
        print("*" * 90)
        print(phoneNumber)

        yield {
            "num": phoneNumber
        }