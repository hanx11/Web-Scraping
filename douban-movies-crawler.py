#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

topic = [
			{'topic_id':'60443', 'topic_name':'爱情'},
			{'topic_id':'62355', 'topic_name':'喜剧'},
			{'topic_id':'62356', 'topic_name':'动画'},
			{'topic_id':'62359', 'topic_name':'剧情'},
			{'topic_id':'60454', 'topic_name':'科幻'},
			{'topic_id':'62360', 'topic_name':'动作'},
			{'topic_id':'62358', 'topic_name':'经典'},
			{'topic_id':'60979', 'topic_name':'悬疑'},
			{'topic_id':'61527', 'topic_name':'青春'},
			{'topic_id':'62364', 'topic_name':'犯罪'},
			{'topic_id':'62363', 'topic_name':'惊悚'},
			{'topic_id':'60434', 'topic_name':'文艺'},
			{'topic_id':'60334', 'topic_name':'纪录片'},
			{'topic_id':'209', 'topic_name':'搞笑'},
			{'topic_id':'60521', 'topic_name':'励志'},
			{'topic_id':'62369', 'topic_name':'恐怖'},
			{'topic_id':'62371', 'topic_name':'战争'},
			{'topic_id':'62370', 'topic_name':'短片'},
			{'topic_id':'62372', 'topic_name':'魔幻'},
			{'topic_id':'61810', 'topic_name':'黑色幽默'},
			{'topic_id':'62376', 'topic_name':'传记'},
			{'topic_id':'62375', 'topic_name':'情色'},
			{'topic_id':'62374', 'topic_name':'动画短片'},
			{'topic_id':'62377', 'topic_name':'感人'},
			{'topic_id':'62378', 'topic_name':'暴力'},
			{'topic_id':'62383', 'topic_name':'浪漫'},
			{'topic_id':'61554', 'topic_name':'女性'},
			{'topic_id':'62381', 'topic_name':'同志'},
			{'topic_id':'62386', 'topic_name':'史诗'},
			{'topic_id':'62387', 'topic_name':'童话'},
			{'topic_id':'62388', 'topic_name':'烂片'},
			{'topic_id':'62389', 'topic_name':'cult'}
		]

		
def get_tags():
	# 获取豆瓣电影分类标签
	tagList = []
	url = "http://movie.douban.com/tag/"
	try:
		r = requests.get(url)
	except Exception as e:
		raise e
	else:
		bsObj = BeautifulSoup(r.content, 'html.parser')
		tabList = bsObj.findAll('table', {'class':'tagCol'})
		for tab in tabList:
			for td in tab.tbody.findAll('td'):
				tagList.append(td.a.text)
		return tagList


def get_movies(start, limit=10, topic_id, topic_name):
	# 获取某分类下的电影信息
	movieList = []
	url = "https://www.douban.com/j/tag/items"
	params = {'start':start, 'limit':limit, 'topic_id':topic_id, 'topic_name':topic_name, 'mod':'movie'}
	try:
		r = requests.get(url, params=params)
	except Exception as e:
		raise e
	else:
		obj = r.json()
		html = obj.get('html')
		bsObj = BeautifulSoup(html, 'html.parser')
		dList = bsObj.findAll('dl')
		for dl in dList:
			movieObj = {}
			movieObj['name'] = dl.dd.find('a', {'class':'title'}).text
			movieObj['link'] = dl.dd.find('a', {'class':'title'}).get('href')
			movieObj['desc'] = dl.dd.find('div', {'class':'desc'}).text
			movieObj['rating'] = dl.dd.find('span', {'class':'rating_nums'}).text
			movieObj['imgLink'] = dl.dt.find('img').get('src')
			movieList.append(movieObj)
		return movieList




def get_tag_table():
	# 获取豆瓣电影分类标签中的分类列表
	try:
		response = requests.get('https://movie.douban.com/tag/')
	except Exception as e:
		raise e
	else:
		bsObj = BeautifulSoup(response.content, 'html.parser')
		tableList =  bsObj.findAll('table', {'class':'tagCol'})
		return tableList


def get_tag_link_list(tableList):
	# 获取豆瓣电影分类标签页中的各分类列表中的链接url
	tag_link_list = set()
	for table in tableList:
		tmplist = table.tbody.findAll('a')
		for link in tmplist:
			tag_link_list.add(link.get('href'))
	return tag_link_list

# link_list = get_tag_link_list()
# for link in link_list:
# 	try:
# 		response = urlopen(link.encode('utf-8'))
# 	except HTTPError as e:
# 		raise e
# 	else:
# 		html = response.read()
# 		bsObj = BeautifulSoup(html, 'html.parser')
# 		print(bsObj.prettify())


def main():
	tableList = get_tag_table()
	linkList = get_tag_link_list(tableList)
	for link in linkList:
		print(link)

if __name__ == '__main__':
	main()
