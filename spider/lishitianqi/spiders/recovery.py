# -*- coding: utf-8 -*-
import scrapy
import re
from lishitianqi.items import LishitianqiItem

class RecoverySpider(scrapy.Spider):
	name = 'recovery'
	allowed_domains = ['tianqihoubao.com']

	def parse(self, response):
		tableTitle = response.css(".wdetail h1::text").get()
		#获取城市名，为了防止出现空列表导致KeyError故用join，''.join([]) == ''
		city = ''.join(re.findall("([\u4E00-\u9FA5]+)历史天气预报",tableTitle))

		data = []
		for tr in response.css(".wdetail table tr")[1:]:
			tds = tr.css("td")
			#获取日期
			date = tds[0].css("a::text").get()
			dl = re.findall("(\d{4})年(\d{2})月(\d{2})日",date)
			date = '-'.join(dl[0])  if dl!= [] else '1990-00-00'

			#获取天气
			weath = tds[1].css("::text").get()
			wl = re.findall("[\u4E00-\u9FA5]+", weath)
			weath = '~'.join(wl) if len(wl) == 2 else '未知~未知'

			#获取最低、最高气温
			tem = tds[2].css("::text").get()
			tl = re.findall("(\d+|-\d+)℃", tem)
			maxt,mint = tl if len(tl) == 2 else [0,0]

			#获取风向，风速度
			win = tds[3].css("::text").get()
			wil = re.findall("[\u4E00-\u9FA50-9-\u2265\u2264]+", win)
			wil = [re.sub('[≤]','小于等于', w) for w in wil]
			wil = [re.sub('[≥]','大于等于', w) for w in wil]
			windd,windp = ('~'.join(wil[0::2]),'~'.join(wil[1::2])) if len(wil) == 4 else ("未知","未知")

			data.append([city, date, maxt, mint, weath, windd, windp])

		#创建item，将数据传递个pipeline
		item = LishitianqiItem()
		item['data'] = data
		yield item