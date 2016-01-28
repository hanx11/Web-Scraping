#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import requests
import pymysql.cursors
from bs4 import BeautifulSoup
import pdb

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

# Connect to the database
connection = pymysql.connect(host='localhost',
                            user='root',
                            password='hanfeng',
                            db='douban_db',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)


def add_movie_record(movie):
	# 将电影信息添加到数据表中
	try:
		name = movie['name'].strip(' ')
		link = movie['link'].strip(' ')
		movie_desc = movie['desc'].strip(' ')
		rating = movie['rating'].strip(' ')
		imglink = movie['imgLink'].strip(' ')
		with connection.cursor() as cursor:
			sql = "INSERT INTO douban_movies VALUES (%s, %s, %s, %s, %s);"
			cursor.execute(sql, (name, link, movie_desc, rating, imglink))
		connection.commit()
	except Exception as e:
		raise e

def is_existed(movie):
	# 判断该部电影是否已存在于数据库中
	try:
		with connection.cursor() as cursor:
			sql = "SELECT name FROM douban_movies WHERE name=%s;"
			cursor.execute(sql, movie['name'])
			result = cursor.fetchone()
			if result is None:
				return True
			else:
				return False
	except Exception as e:
		raise e

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

def get_movies(params):
	# 根据参数获取豆瓣电影信息
	movieList = []
	url = "https://www.douban.com/j/tag/items"
	# params = {'start':start, 'limit':limit, 'topic_id':topic_id, 'topic_name':topic_name, 'mod':'movie'}
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
			try:
				movieObj = {}
				movieObj['name'] = dl.dd.find('a', {'class':'title'}).text
				movieObj['link'] = dl.dd.find('a', {'class':'title'}).get('href')
				movieObj['desc'] = dl.dd.find('div', {'class':'desc'}).text
				movieObj['rating'] = dl.dd.find('span', {'class':'rating_nums'}).text
				movieObj['imgLink'] = dl.dt.find('img').get('src')
				movieList.append(movieObj)
			except Exception as e:
				continue
		return movieList


def main():
	for t in topic:
		topic_id = t['topic_id']
		topic_name = t['topic_name']
		for s in range(0, 1000, 10):
			# pdb.set_trace()
			params = {'start':s, 'limit':10, 'topic_id':topic_id, 'topic_name':topic_name, 'mod':'movie' }
			movies = get_movies(params)
			for m in movies:
				if is_existed(m):
					add_movie_record(m)
					print(m)
				else:
					continue


if __name__ == '__main__':
	main()

