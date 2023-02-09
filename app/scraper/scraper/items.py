# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PostItem(scrapy.Item):
    username = scrapy.Field()
    source_id = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    media = scrapy.Field()
    source_created = scrapy.Field()
    
    