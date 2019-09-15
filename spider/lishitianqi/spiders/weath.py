# -*- coding: utf-8 -*-
import scrapy
from lishitianqi.items import LishitianqiItem

class WeathSpider(scrapy.Spider):
	name = 'weath'
	allowed_domains = ['lishi.tianqi.com']
	start_urls = ['http://lishi.tianqi.com/']

	def parse(self, response):
		#选择中国所有城市名及对应url
		citys = response.css(".bcity a[target='_blank']::text").getall()
		cityurls = response.css(".bcity a[target='_blank']::attr(href)").getall()

		#将url添加到爬虫中，
		for city,url in zip(citys,cityurls):
			yield scrapy.Request(response.urljoin(url), meta={'city':city}, callback=self.city)

	def city(self, response):
		#选择城市所有年月份及对应url
		months = response.css(".tqtongji1 a::text").getall()
		monthurls = response.css(".tqtongji1 a::attr(href)").getall()

		#将url添加到爬虫中
		for url in monthurls:
			yield scrapy.Request(response.urljoin(url), meta={'city':response.meta['city']}, callback=self.month)

	def month(self, response):
		data = []
		#选择该月份中每天
		for ul in response.css(".tqtongji2 ul[class!='t1']"):
			data.append([response.meta['city']] + [li.css("::text").get() for li in ul.css('li')])

		#创建item，将数据传递个pipeline
		item = LishitianqiItem()
		item['data'] = data
		yield item
