
这是一个用scrapy实现数据获取，用django实现web后端，用bootstrap，jqeruy等实现web前端，uwsgi+nainx部署的全栈项目。


项目的详细过程可以看https://www.cnblogs.com/plyonfly/p/11493115.html

我的个人云服务器已经部署了该项目http://pengliangyuan.club/history_weath/

有什么问题欢迎随时指出

项目运行方式：

1.下载代码

git clone https://github.com/pengliangyuan/Chinese-historical-weather-visualization-system.git



2.创建python虚拟环境

pip install virtualenv

pip install virtualenvwrapper

#创建目录用来存放虚拟环境

mkdir $HOME/.virtualenvs

#在~/.bashrc中添加行

export WORKON_HOME=$HOME/.virtualenvs

export VIRTUALENVWRAPPER_VIRTUALENV=/usr/local/python3/bin/virtualenv

source /usr/local/python3/bin/virtualenvwrapper.sh

#进入虚拟环境

workon django_env_py3



3.安装依赖

pip install -r requirements.txt　



4.修改数据库连接（有两处需要修改）

Chinese-historical-weather-visualization-system/spider/lishitianqi/pipelines.p

=====================================================

        def __init__(self):
                #连接数据库
                self.connect = pymysql.connect(
                        host='127.0.0.1',
                        port=8809,
                        db='lishitianqi',
                        user='root',
                        passwd='123',
                        charset='utf8',
                        use_unicode=True)
=======================================================


Chinese-historical-weather-visualization-system/webapps/webapps/settings.py

=====================================================

       DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lishitianqi',
        'USER': 'root',
        'PASSWORD':'123',
        'HOST':'127.0.0.1',
        'PORT':'8809',
    }

                      
=====================================================



5.创建数据库和数据表

cd Chinese-historical-weather-visualization-system/webapps

python manage.py makemigrations

python manage.py migrate

关于django使用mysql报错的问题可以看https://www.cnblogs.com/plyonfly/p/11493115.html#_label17


6.爬取数据

cd  Chinese-historical-weather-visualization-system/spider

scrapy crawl weath

#全国3100多个城市，数据优点多，大概需要8-9个小时

#数据修复, 由于网站数据有缺失，比如某个月少几天，某年少几个月，或某年份根本没数据，数据修复是从另一个网站抓取数据

scrapy crawl recovery

7.运行django

cd Chinese-historical-weather-visualization-system/webapps

python manage.py runserver

在浏览器访问localhost:8000
