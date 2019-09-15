# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors

#用于获取某年某月有多少天， 
import calendar

#用于获取汉字的拼音， pip install xpinyin
from xpinyin import Pinyin


class LishitianqiPipeline(object):

	def __init__(self):
		#连接数据库
		self.connect = pymysql.connect(
			host='127.0.0.1',
			port=8809,
			db='lishitianqi',
			user='root',
			passwd='p1994l08y04',
			charset='utf8',
			use_unicode=True)

		#通过cursor执行增删该查
		self.cursor = self.connect.cursor()

	def process_item(self, item, spider):

		#插入天气数据
		self.cursor.executemany(
			"""insert ignore into lishitianqi(city, date, maxt, mint, weath, windd, windp)
			values (%s, %s, %s, %s, %s, %s, %s)""", item['data'])

		#提交sql语句
		self.connect.commit()

		#必须实现返回
		return item

	#在爬虫运行前执行这个函数
	def open_spider(self, spider):

		if spider.name == 'recovery' and True:
			#读取https://lishi.tianqi.com/和http://www.tianqihoubao.com/lishi/支持查询的所有城市列表存, eval将字符串变为python语句, 转换为set用于取交集
			citys_primary = set(eval(open("citys_primary.txt","r",encoding="utf-8").read()))
			citys_backup = set(eval(open("citys_backup.txt","r",encoding="utf-8").read()))
			startyear = 2011
			endyear = 2019
			endmonth = 9
			pin = Pinyin()

			def check_or_appendurl(city,year,month):
				#计算year年month月有多少天
				stmr = calendar.monthrange(year, month)[1]
				#通过sql获取city城市year年month月有多少天
				sql = "select count(city) from lishitianqi where city='%s' and date like '%d-%02d%%'" % (city,year,month)
				self.cursor.execute(sql)
				apmr = self.cursor.fetchall()[0][0]

				#若数据库中某城市某月的天数不等于该月的实际天数，说明这个城市这个月的数据有丢失，需要构造url到备用网站获取天气数据
				if stmr != apmr:
					url = "http://www.tianqihoubao.com/lishi/%s/month/%d%02d.html" % (pin.get_pinyin(city, ''),year,month)
					print(stmr,apmr,'append url: %s' % url)
					spider.start_urls.append(url)

			#citys_primary为在https://lishi.tianqi.com/支持查询的所有城市列表存，citys_backup为http://www.tianqihoubao.com/lishi/支持查询的所有城市列表
			#理想情况下爬虫https://lishi.tianqi.com/就能获取到所有需要的数据，但是从网站抓取来的数据并非可靠，有可能某个月的某几天数据丢失，
			#所有需要到备用网站将数据库缺失数据补齐
			#备用网站数据集与主用网站数据集不重合，所以在做数据修复的时候要取交集
			for city in citys_primary & citys_backup:
				for year in range(startyear,endyear):
					for month in range(1,13):
						check_or_appendurl(city,year,month)

				for month in range(1,endmonth):
					check_or_appendurl(city,endyear,month)


	def close_spider(self, spider):
		pass
