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

	json_obj = json.dumps(info, ensure_ascii=False, indent=2) 
	return HttpResponse(json_obj)

#从url直接跳转
def resultPage(request, number):
	av_number = "av" + number
	info = spider(av_number)

	if info['url']== "error":
		return render(request, 'Downloader/404Page.html')
	else:
		return render(request, 'Downloader/loadPage.html', info)

#爬取up主头像的iOS端API
def searchUpPage(request, up_name):
	video_url = 'https://search.bilibili.com/upuser?keyword=' + up_name
	headers = {'User-Agent' : 'Mozilla/5.0'}
	r = requests.get(video_url, headers = headers)
	bs = BeautifulSoup(r.text, 'html5lib')
	up_infos = {'sum':0,'upusers':[]}

	for up in bs.findAll(attrs={'class': 'up-item'}):
		upface = up.findAll('div')[0]
		name = upface.a['title']
		imgUrl = 'https:' + upface.a.img['data-src']
		upinfo = up.findAll('div')[1].findAll('div')[2].findAll('span')
		videoNum = re.findall("\d+",upinfo[0].get_text())[0]
		fansNum = re.findall("\d+",upinfo[1].get_text())[0]
		up_info = {
			'name':name,
			'video_num':videoNum,
			'fans_num':fansNum,
			'img_url':imgUrl,
		}
		up_infos['sum'] = up_infos['sum'] + 1
		up_infos['upusers'].append(up_info)

	json_obj = json.dumps(up_infos, ensure_ascii=False, indent=2) 
	return HttpResponse(json_obj)
	
# 爬取图片的爬虫代码
def spider(av_number):

	headers = {
		'User-Agent':'Mozilla/5.0',
	}
	video_url = "http://www.bilibili.com/video/" + av_number
	r = requests.get(video_url, headers = headers)
	bs = BeautifulSoup(r.text, 'html5lib')
	img_link = bs.findAll('img')[0].get('src')

	if img_link == None:
		msg = {'url':'error','title':'error','author':'error',}
	else:
		img_url = "http:" + img_link
		title = bs.findAll('h1')[0].get('title')
		contents = bs.findAll('meta')
		author = contents[3].get('content')
		msg = {'url':img_url,'title':title,'author':author}
	return msg

def fuckBilibili(request, av_number):

	url = 'http://www.bilibili.com/video/av' + str(av_number)
	headers = {'User-Agent':'Mozilla/5.0'}
	cookies = {
		'DedeUserID': '221013145',
		'DedeUserID__ckMd5': '0ada37d8e37bee1f',
		'SESSDATA': 'ddff3d5b%2C1508937653%2C5dc59211'
	}
	default = {'url':'error','title':'error','author':'error'}
	default_json = json.dumps(default, ensure_ascii=False, indent=2)
	try:
		r = requests.get(url, headers=headers, cookies=cookies, timeout=3)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
	except:
		return HttpResponse(default_json)
	bs = BeautifulSoup(r.text, 'html5lib')
	link = bs.find_all('img')[0].get('src')		
	if link == None:
		return HttpResponse(default_json)
	else:
		title = bs.find_all('h1')[0].get('title')
		contents = bs.find_all('meta')
		author = contents[3].get('content')
		info = {'url':'https:' + link, 'title':title, 'author':author,}
		info_json = json.dumps(info, ensure_ascii=False, indent=2)
		return HttpResponse(info_json)

def articleCover(request, cv_number):
	url = 'http://www.bilibili.com/read/cv' + str(cv_number)
	headers = {'User-Agent':'Mozilla/5.0'}
	default = {'url':'error','title':'error','author':'error'}
	default_json = json.dumps(default, ensure_ascii=False, indent=2) 

	try:
		r = requests.get(url, headers=headers)
		r.raise_for_status()
		r.encoding = r.apparent_encoding
	except:
		return HttpResponse(default_json)
	bs = BeautifulSoup(r.text, 'html5lib')
	error = bs.find_all('div', class_='error')
	if len(error) == 0:
		js = bs.find_all('script')[0].text
		if js == None:
			return HttpResponse(default_json)
		else:
			info = {
				'url':js.split('"')[7],
				'title':js.split('"')[11],
				'author':js.split('"')[3]
			}
			info_json = json.dumps(info, ensure_ascii=False, indent=2) 
			return HttpResponse(info_json)
	else:
		return HttpResponse(default_json)

def i_test(request, number):
	av_number = "av" + number
	headers = {'User-Agent':'Mozilla/5.0'}
	url = "http://www.bilibili.com/video/" + av_number
	try:
		r = requests.get(url, headers=headers)
		r.raise_for_status()
	except:
		error = {'error':'无法连接到这个网站'}
		error_json = json.dumps(error, ensure_ascii=False, indent=2)
		return HttpResponse(error_json)
	else:
		bs = BeautifulSoup(r.text, 'html5lib')
		img_link = bs.findAll('img')[0].get('src')
		if img_link is None:
			error = {
				'url':url,
				'r.headers':dict(r.headers),
				'error':'没有找到图片',
				'html':r.text,
				'r.status_code':r.status_code,
			}
			error_json = json.dumps(error, ensure_ascii=False)
			return HttpResponse(error_json)
		else:
			img_url = "http:" + img_link
			title = bs.findAll('h1')[0].get('title')
			contents = bs.findAll('meta')
			author = contents[3].get('content')
			info = {
				'r.headers':dict(r.headers),
				'html':r.text,
				'r.status_code':r.status_code,
				'url':img_url,
				'title':title,
				'author':author,
			}
			info_json = json.dumps(info, ensure_ascii=False, indent=2)
			return HttpResponse(info_json)