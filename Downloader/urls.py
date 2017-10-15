# -*- coding: utf-8 -*-
# @Author: Haut-Stone
# @Date:   2017-06-13 19:50:42
# @Last Modified by:   Haut-Stone
# @Last Modified time: 2017-10-15 10:27:10

from django.conf.urls import url
from .import views

app_name = 'Downloader'

urlpatterns = [
	url(r'^$', views.helloPage, name = 'helloPage'),
	url(r'^av(?P<number>[0-9]+)/$', views.resultPage, name = 'resultPage'),
	url(r'^load/$', views.loadPage, name = 'loadPage'),
	url(r'^ios/(?P<number>[0-9]+)/$', views.iosPage, name = 'iosPage'),
	url(r'^ios/upuser-keyword=(?P<up_name>\w+)/$', views.searchUpPage, name = 'searchUpPage'),
	url(r'^ios/article/(?P<cv_number>[0-9]+)/$', views.articleCover, name='articleCover'),
	url(r'^ios/vip/(?P<av_number>[0-9]+)/$', views.fuckBilibili, name='fuckBilibili'),
	url(r'^ios/test/(?P<number>[0-9]+)/$', views.i_test, name='i_test'),
]