# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserJobItem(scrapy.Item):
    
    name = scrapy.Field()
    _id = scrapy.Field()
    salary = scrapy.Field()
    vacancy_link = scrapy.Field()
    site_scraping = scrapy.Field()
    
