# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import datetime
import pymysql
import hashlib
from bttt.mysqlConfigs import mysql_config
import time


class SqlDb(object):
    def __init__(self, user, passwd, db, db_port=3306, host='127.0.0.1'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.db_port = db_port
        self.md5OfUrlList = []

        self.db_config = {
            'host': self.host,
            'user': self.user,
            'password': self.passwd,
            'db': self.db,  # 进入的数据库名. loacl_movie
            'charset': 'utf8',
            'port': self.db_port
        }
        self.conn = None
        self.cur = None

    def connect_mysql_db(self):
        self.conn = pymysql.connect(**self.db_config)
        self.cur = self.conn.cursor()
        #print("已连接和建立游标.")

    def insert_to_sheet(self, sheet_sql, column_info, value_sql_tuple):
        try:
            sql = f'INSERT INTO {sheet_sql} {column_info} VALUE {value_sql_tuple}'
            #print(sql)
            rv = self.cur.execute(sql)
            print(f"接收到{rv}行数据.")
            resp = self.cur.fetchall()

            self.cur.close()

        except Exception as e:
            print(e)
            self.conn.rollback()  # 相当于撤销, 如果失败就回滚.

        finally:
            self.conn.commit()  # 提交修改的数据.
            self.conn.close()  # 关闭conn.
            print("插入结束, 已断开连接.")

    def select_to_column(self, sheet_sql, column_sql="*"):
        try:
            sql = f'SELECT {column_sql} FROM {sheet_sql}'
            # print(sql)
            rv = self.cur.execute(sql)
            # print(f"查看到{rv}行数据.")
            resp = self.cur.fetchall()
            offset_none = 0
            offset_url = 0

            for entry in resp:
                if entry[0] is not None:
                    #print(''.join(entry).strip())
                    self.md5OfUrlList.append(hashlib.md5(''.join(entry).strip().encode()).hexdigest())
                    offset_url += 1
                else:
                    offset_none += 1
            #print(f"空数据{offset_none}")
            #print(f"有效数据{offset_url}")
            # print(f"md5{self.md5OfUrlList}")

        except Exception as e:
            print(e)
            self.conn.rollback()

        finally:
            self.conn.commit()  # 提交修改的数据.
            self.conn.close()  # 关闭conn.
            #print("查看结束, 已断开连接.")

    def update_to_sheet(self, second):
        title = second['title']
        year = second['year']
        country = second['country']
        lan = second['lan']
        douban_link = second['douban_link']
        introduce = second['introduce']
        main_actor = second['main_actor']
        download_url = second['download_url']
        img_url = second['img_url']
        tuple_data = (title, year, country, lan, douban_link, introduce, main_actor, download_url, img_url)
        column_info = "(title, year, country, lan, douban_link, introduce, main_actor, download_url, img_url)"
        # print(tuple_data)

        self.connect_mysql_db()
        self.insert_to_sheet(sheet_sql='t_movies', column_info=column_info, value_sql_tuple=tuple_data)


class SourcePipeline(object):
    def process_item(self, item, spider):
        item['source'] = spider.name
        item['utc_time'] = str(datetime.utcnow())
        return item


class BtttPipeline(object):
    def open_spider(self, spider):
        self.file = open("btt.json", 'w')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False)
        #content = dict(item)
        
        host = mysql_config['MYSQL_HOSTS']
        
        user = mysql_config['MYSQL_USER']
        passwd = mysql_config['MYSQL_PASSWORD']
        db = mysql_config['MYSQL_DB']
        db_port = mysql_config['MYSQL_PORT']
        
        #print(f"user:{user}, passwd:{passwd}")
        mysql = SqlDb(user, passwd, db, db_port, host)
        mysql.connect_mysql_db()
        mysql.select_to_column(sheet_sql='t_movies', column_sql='douban_link')

        #f = open(r"btt.json", 'rb')
        url_md5 = []
        data_list = []

        #while True:
        try:
            data = json.loads(content)
           # print(f"data:{data}")
            data_list.append(data)
            url_md5.append(hashlib.md5((data['douban_link']).encode()).hexdigest())

        except Exception as e:
            print(e)
        #print(f"data_list:{data_list}")
        #print(f"url_md5:{url_md5}")
        offset = 0
        data_offset = 0
        for j, second in zip(url_md5, data_list):
            data_offset = 0
            for i in mysql.md5OfUrlList:
                if j == i:
                    print("重复一个")
                    offset += 1
                    data_offset += 1
            if data_offset == 0:
                mysql.update_to_sheet(second)
        print(f"重复{offset}")

        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item

    def close_spider(self, spider):
        self.file.close()
