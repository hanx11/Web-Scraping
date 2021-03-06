#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                            user='root',
                            password='hanfeng',
                            db='douban_db',
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        sql = '''create table douban_movies (
                        name varchar(128),
                        link varchar(512),
                        movie_desc varchar(512),
                        rating varchar(4),
                        imglink varchar(128)
                    );
               '''
        cursor.execute(sql)
    connection.commit()
except Exception as e:
    raise e
finally:
    connection.close()
