# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LishitianqiItem(scrapy.Item):
	# define the fields for your item here like:
	city = scrapy.Field()
	date = scrapy.Field()
	maxt = scrapy.Field()
	mint = scrapy.Field()
	weath = scrapy.Field()
	windd = scrapy.Field()
	windp = scrapy.Field()
	data = scrapy.Field()
