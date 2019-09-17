from django import views
from django.http import HttpResponse
from django.shortcuts import render, redirect,reverse
from .models import Lishitianqi, Citys
import django.utils.timezone as timezone
from xpinyin import Pinyin
import string
import json
from django.http import Http404
from django.db.models import Avg


#将DomainName重定向到DomainName/history_weath
def index(request):
	return redirect(reverse("history_weath:home"))

#history_weath这个app的主页
def home(request):
	hot_citys =	Citys.objects.filter(hot=1)
	
	#汉字转换拼音
	pin = Pinyin()

	#生成{'A':[], 'B':[], 'C':[] ...}, 为什么用[[] for i in range(26)]而不用[] * 26, 因为前者是浅拷贝，后者是引用
	citys = dict(zip(list(string.ascii_uppercase),[[] for i in range(26)])) 
	
	#将城市名转换为拼音，提取首字母，按不同首字母插入到citys中
	for item in Citys.objects.all():
		city = item.city
		first_letter = pin.get_pinyin(city)[:1].upper()
		citys[first_letter].append(city)
	
	#生成2011至今的年份列表
	years = [year for year in range(2011,timezone.now().year + 1)]
	context = {
		'hot_citys':hot_citys,
		'citys':citys,
		'years':years
	} 

	#将这些数据放入到django模板渲染后显示给用户
	return render(request, 'history_weath/home.html', {'context':context})
	

#url: DomainName/history_weath/temperature_year, 用于ajax（POST）请求citys,years的月平均气温
def temperature_year(request):
	post_data = json.loads(request.body)
	citys = post_data.get('citys',[])
	years = post_data.get('years',[])
	print("REQUEST:",citys,years)
	if citys == [] or years == []:
		raise Http404("Question does not exist")
	else:
		result = []
		for city in citys:
			for year in years:
				city_data = {'name':'%s(%s年)'%(city,year), 'data':[]}
				for month in range(1,13):
					#分别计算一个月的每天最高温度平均温度，一个月的每天最低温度平均温度
					month_avg = Lishitianqi.objects.filter(city=city,date__year=year,date__month=month).aggregate(Avg('maxt'),Avg('mint'))
					#在将一个月的每天最高温度平均温度，一个月的每天最低温度平均温度求平均
					mavg = round((month_avg['maxt__avg'] + month_avg['mint__avg'])/2) if month_avg['maxt__avg'] is not None else 0
					city_data['data'].append(mavg)
				result.append(city_data)

		#该曲线图参考https://jshare.com.cn/demos/hhhhxu，其中series.data即为ajax请求返回的数据
		print("RESPONSE:",result)
		return HttpResponse(json.dumps(result))

#url: DomainName/history_weath/temprature_month, 用于ajax（POST）请求citys,years,month日平均气温
def temperature_month(request):
	post_data = json.loads(request.body)
	citys = post_data.get('citys',[])
	years = post_data.get('years',[])
	month = post_data.get('month',"")
	print("REQUEST",citys, years, month)
	if citys == [] or years == [] or month == "":
		raise Http404("Question does not exist")
	else:
		result = []
		for city in citys:
			for year in years:
				month_obj = Lishitianqi.objects.filter(city=city,date__year=year,date__month=month)
				#在这里，日平均温度 = 日最高温度 + 日最低温度 / 2
				month_data = [round((day.maxt + day.mint)/2,1) for day in month_obj]
				city_data = {'name':'%s(%s年%s月)'%(city,year,month), 'data':month_data}
				result.append(city_data)
		
		#该曲线图参考https://jshare.com.cn/demos/hhhhxu，其中series.data即为ajax请求返回的数据
		print("RESPONSE",result)
		return HttpResponse(json.dumps(result))

#url: DomainName/history_weath/weath_year_ratio, 用于ajax（POST）请求city,year天气比率
def weath_year_ratio(request):
	post_data = json.loads(request.body)
	city = post_data.get('city',"")
	year = post_data.get('year',"")
	print("REQUEST",city, year)
	if city == "" or year == "":
		raise Http404("Question does not exist")
	else:
		
		weath_year = Lishitianqi.objects.filter(city=city,date__year=year)
		weath_cnts = [d.weath for d in weath_year]
		weath_mods = set(weath_cnts)
		data=[]
		for wd in weath_mods:
			cnt = weath_cnts.count(wd)
			data.append({
				'name':wd,						#天气类型，如晴，多云，多云转晴，小雨
				'y': cnt / len(weath_cnts)		#该类天气在一年天气中所占比例
				})
		
		#按天气比例排序
		data.sort(key=lambda x:x['y'])

		#将比例最高天气从饼中切出
		data[-1]['sliced'] = 1
		#选择比例最高的天气
		data[-1]['selected'] = 1

		#该饼图参考https://jshare.com.cn/demos/hhhhDX，其中series.data即为ajax请求返回的数据
		result = {'name':'%s(%s年)'%(city,year), 'data':data}
		print("RESPONSE",result)
		return HttpResponse(json.dumps(result))

#url: DomainName/history_weath/weath_month_ration, 用于ajax（POST）请求city,year,month天气比率
def weath_month_ratio(request):
	post_data = json.loads(request.body)
	city = post_data.get('city',"")
	year = post_data.get('year',"")
	month = post_data.get('month',"")
	print("REQUEST",city, year,month)
	if city == "" or year == "" or month == "":
		raise Http404("Question does not exist")
	else:
		
		weath_year = Lishitianqi.objects.filter(city=city,date__year=year,date__month=month)
		weath_cnts = [d.weath for d in weath_year]
		weath_mods = set(weath_cnts)
		data=[]
		for wd in weath_mods:
			cnt = weath_cnts.count(wd)
			data.append({
				'name':wd,					#天气类型，如晴，多云，多云转晴，小雨
				'y': cnt / len(weath_cnts)	#该类天气在一个月天气中所占比例
				})

		#按天气比例排序
		data.sort(key=lambda x:x['y'])

		#将比例最高天气从饼中切出
		data[-1]['sliced'] = 1
		#选择比例最高的天气
		data[-1]['selected'] = 1

		#该饼图参考https://jshare.com.cn/demos/hhhhDX，其中series.data即为ajax请求返回的数据
		result = {'name':'%s(%s年%s月)'%(city,year,month), 'data':data}
		print("RESPONSE",result)
		return HttpResponse(json.dumps(result))

#url: DomainName/history_weath/like_city, 用于ajax（POST）请求匹配city前缀名的所有城市
def like_city(request):
	post_data = json.loads(request.body)
	city = post_data.get('city',"")
	print("REQUEST",city)
	if city == "":
		raise Http404("Question does not exist")
	else:
		citys = Citys.objects.filter(city__startswith=city)
		result = [city.city for city in citys]
		print("RESPONSE",result)
		return HttpResponse(json.dumps(result))
