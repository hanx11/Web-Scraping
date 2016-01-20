#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup


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
