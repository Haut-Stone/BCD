from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import re, requests, sys
from bs4 import BeautifulSoup
import json


#手工输入跳转
def helloPage(request):
	return render(request ,'Downloader/helloPage.html')

#图片结果界面
def loadPage(request):
	av_number = request.POST['target']
	info = spider(av_number)

	if info['url'] == "error":
		return render(request, 'Downloader/404Page.html')
	else:
		return render(request, 'Downloader/loadPage.html', info)

# ios端的API
def iosPage(request, number):
	av_number = "av" + number
	info = spider(av_number)

	filename = "msg.json"
	try:
		with open(filename, 'w') as f:
			json.dump(info, f, ensure_ascii=False, indent=2)
	except IOError:
		print("The file doesn't exit.")
	else:
		with open(filename) as f:
			return HttpResponse(f)

#从url直接跳转
def resultPage(request, number):
	av_number = "av" + number
	info = spider(av_number)

	if info['url']== "error":
		return render(request, 'Downloader/404Page.html')
	else:
		return render(request, 'Downloader/loadPage.html', info)

# 爬取图片的爬虫代码
def spider(av_number):

	headers = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Cookie':'sid=ao8p7v84; UM_distinctid=15b7180b90f66-0f075e064d05ab-396c7807-1fa400-15b7180b91285; pgv_pvi=3513811968; fts=1492257914; finger=14bc3c4e; buvid3=835A244A-230C-4CF5-8FB3-E8C675EE8EA115577infoc; purl_token=bilibili_1497336042; pgv_si=s4574550016; CNZZDATA2724999=cnzz_eid%3D108963144-1492253091-%26ntime%3D1497334496',
		'Host':'www.bilibili.com',
		'Referer':'http://space.bilibili.com/3098214',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
	}

	video_url = "http://www.bilibili.com/video/" + av_number
	r = requests.get(video_url, headers = headers)
	bs = BeautifulSoup(r.text, 'html5lib')
	img_link = bs.findAll('img')[0].get('src')

	if img_link == None:
		msg = {
			'url':'error',
			'title':'error',
			'author':'error',
		}
	else:
		img_url = "http:" + img_link
		title = bs.findAll('h1')[0].get('title')
		contents = bs.findAll('meta')
		author = contents[3].get('content')

		msg = {
			'url':img_url,
			'title':title,
			'author':author,
		}

		print("videoUrl: " + video_url)
		print("imgUrl: " + img_url)
		print("Title: " + title)
		print("Author: " + author)
	return  msg

