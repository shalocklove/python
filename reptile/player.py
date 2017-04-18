# coding: UTF-8
'''
Created on 2017��4��12��

@author: Administrator
'''
import string
import pymysql
import requests
from requests.exceptions import RequestException
import json
from numpy import int0

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

def get_page(name):
    try:
        response = requests.get('http://china.nba.com/static/data/team/roster_'+ name['E_name']+'.json')
        print('http://china.nba.com/static/data/team/roster_'+ name['E_name']+'.json')
        if response.status_code == 200:
            response.encoding = 'utf-8'
            print(name['E_name'])
            return response.text
    except RequestException:
        print ("完了")
        return 0
        
def get_one_massage(html):
    l = []
    date = json.loads(html)
    massage = date.get('payload').get('players')
    for m in massage:
        profile = m.get('profile')
        id = profile.get('playerId')
        id = int(id)
        firstname = profile.get('firstName')
        lastname = profile.get('lastName')
        country = profile.get('country')
        weight = profile.get('weight').strip()[0:-2]
        firstW = weight[0:-3]
        secondW = weight[-2:-1]
        firstW = float(firstW)
        secondW = float(secondW)
        weight = firstW + 0.1 * secondW
        height = profile.get('height')
        firstH = height[0:1]
        secondH = height[2:]
        firstH = float(firstH)
        secondH = float(secondH)
        height = firstH + 0.01 * secondH
        position = profile.get('position')
        jerseyNo = profile.get('jerseyNo')
        experience = profile.get('experience')
        experience = int(experience)
        displayAffiliation = profile.get('displayAffiliation')
        ma = {
            'id': id,
            'firstname': firstname,
            'lastname': lastname,
            'country': country,
            'weight': weight,
            'height': height,
            'position': position,
            'jerseyNo': jerseyNo,
            'experience': experience,
            'displayAffiliation': displayAffiliation
            }
        l.append(ma)
    print(l)
    return l

def DB(date):
    connection = pymysql.connect(host='localhost',user='root',password='sherlock',
                                 db='nba',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `player` (`firstname`,`lastname`,`country`,`weight`,`height`,`positions`,`jerseyNo`,`experience`,`displayAffiliation`) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            for d in date:
                print(d['firstname'])
                print(type(d.get('firstname')),type(d.get('lastname')),type(d.get('country')),type(d.get('weight')),type(d.get('height')),type(d.get('position')),type(d.get('jerseyNo')),type(d.get('experience')),type(d.get('displayAffiliation')))
                cursor.execute(sql,(d['firstname'],d['lastname'],d['country'],str(d['weight']),str(d['height']),d['position'],d['jerseyNo'],str(d['experience']),d['displayAffiliation']))
                connection.commit()
    finally:
        connection.close()
        
def main():
    i = 1
    name = get_team()
    for n in name:
        html = get_page(n)
        print(i)
        i += 1
        date = get_one_massage(html)
        DB(date)
        
if __name__ == '__main__':
    main()
    