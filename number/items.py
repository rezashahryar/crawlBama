# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose

def to_delete(dict):
    result = {}
    for i in dict:
        if i not in result:
            result['mobile'] = i
    
    return result

class NumberItem(scrapy.Item):
    # phone = scrapy.Field(input_processor=MapCompose(to_delete))
    mobile = scrapy.Field(input_processor=MapCompose(to_delete))