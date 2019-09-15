"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from history_weath.views import index 


urlpatterns = [
    path('', index),											#将DomainName重定向到DomainName/history_weath，见history_weath/views.py中的index函数
	path('history_weath/', include('history_weath.urls')),		#引用history_weath/urls.py，访问url = 引用url + 被引用url 
    path('admin/', admin.site.urls),
]
