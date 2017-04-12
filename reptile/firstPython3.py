# coding: UTF-8
import requests
from requests.exceptions import RequestException
import re
import pymysql

def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'gbk'
#            print (response.text)
            return response.text
    except RequestException:
        print ("完了")
        
def parse_page(html):
#   正则表达式建立  
    pattern = re.compile(r'<a target="_blank" class="small-(.*?)" href="http://china.nba.com/.*?">(.*?)</a>' , re.S)
#    应用正则表达式 
    itms = re.findall(pattern, html)
    for item in itms:
        d = {
            'English_name': item[0],
            'Chinese_name': item[1]
        }
        #录入数据库
        #BD(d['Chinese_name'], d['English_name'])
        print(d)

def BD(C_name, E_name):
    # Connect to the database
    connection = pymysql.connect(host='localhost',user='root',password='sherlock',
                                 db='nba',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `team` (`C_name`, `E_name`) VALUES (%s, %s)"
            cursor.execute(sql, (C_name, E_name))
            connection.commit()
    finally:
        connection.close()

def select(C_name):
    # Connect to the database
    connection = pymysql.connect(host='localhost',user='root',password='sherlock',
                                 db='nba',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:            
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `C_name`, `E_name` FROM `team` WHERE `C_name`=%s"
            cursor.execute(sql, (C_name,))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()

def main():
    url = "http://china.nba.com/teamindex/"
    html = get_page(url)
    parse_page(html)
    select('开拓者')
    
if __name__ == '__main__':
    main()
    