from django.urls import path
from . import views


app_name = 'history_weath'
urlpatterns = [
    path('', views.home, name='home'),						#history_weath这个app的主页
    path('temperature_year', views.temperature_year),		#url: DomainName/history_weath/temperature_year, 用于ajax（POST）请求citys,years的月平均气温
    path('temperature_month', views.temperature_month),		#url: DomainName/history_weath/temprature_month, 用于ajax（POST）请求citys,years,month日平均气温
    path('weath_year_ratio', views.weath_year_ratio),		#url: DomainName/history_weath/weath_year_ratio, 用于ajax（POST）请求city,year天气比率
    path('weath_month_ratio', views.weath_month_ratio),		#url: DomainName/history_weath/weath_month_ration, 用于ajax（POST）请求city,year,month天气比率
]