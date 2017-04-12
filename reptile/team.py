# coding: UTF-8
#利用爬虫写入球队信息

import requests
from requests.exceptions import RequestException
import pymysql
import json
import mysql.connector
import sys

#获取所有球队名
def get_team():
    connection = pymysql.connect(host='localhost',user='root',password='sherlock',
                                 db='nba',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:            
        with connection.cursor() as cursor:
            # Read a single record
            sql = "select `E_name` from `team`"
            cursor.execute(sql)
            resulr = cursor.fetchall()
            return resulr
    finally:
        connection.close()

#获取URL
def get_one_url(result):
    url = 'http://china.nba.com/static/data/team/standing_'+result['E_name']+'.json'
    return url
    
#获取球队信息json
def get_one_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text#字符串形式
        return None
    except RequestException:
        print('索引出错')
        return None

# 获取球队信息
def get_one_massage(html):
    date = json.loads(html)
    massage = date.get('payload').get('team')
    coach = massage.get('coach').get('headCoach')
    city = massage.get('profile').get('city')
    displayConference = massage.get('profile').get('displayConference')
    division = massage.get('profile').get('division')
    massage = {'coach':coach, 'city':city, 'zone':displayConference, 'subarea':division}
    print(massage)
    return massage

# 改变数据
def BD(massage, name):

    connection = pymysql.connect(host='localhost',user='root',password='sherlock',
                                 db='nba',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "UPDATE team SET gymnasium=%s, zone=%s, subarea=%s, coach=%s, city=%s WHERE E_name=%s"
            cursor.execute(sql, ('123', massage['zone'], massage['subarea'], massage['coach'], massage['city'], name['E_name']))
            connection.commit()
    finally:
        connection.close()
        
def main():
    name = get_team()
    for n in name:
        print(n)
        url = get_one_url(n)
        html = get_one_json(url)
        massage = get_one_massage(html)
        BD(massage, n)
    
if __name__ == '__main__':
    main()