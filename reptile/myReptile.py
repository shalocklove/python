# coding: UTF-8
import requests
from requests.exceptions import RequestException
import re
import json

def get_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
#            print (response.text)
            return response.text
        else:
            return {
                'url': url,
                'status_code': response.status_code     
                    }
    except RequestException:
        print ("爬虫失败："+url)
        
def get_json(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
    except RequestException:
        print ("爬虫失败："+url)
        
def get_one_massage(html):
    date = json.loads(html)
    return date
        