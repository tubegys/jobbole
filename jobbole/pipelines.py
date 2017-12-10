# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import datetime
import pymysql

class JobbolePipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1',
                                    user='root',
                                    password='123',
                                    db='db_gys',
                                    charset='utf8',
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 具体的item的处理逻辑
        print(spider)
        insert_sql = """
        INSERT INTO pyarticles (title, publish_time, url, praise_num, user_agent)
        VALUES(%s,%s,%s,%s,%s)
        """
        values = (item['title'], item['publish_time'], item['url'], item['praise_num']
                  , spider.user_agent)
        self.cursor.execute(insert_sql, values)
        self.conn.commit()

    def spider_closed(self):
        self.conn.close()
