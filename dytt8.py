# -*- coding:utf-8 -*-

import urllib.request
import os
import time
import random
import mysql.connector
import re
import requests
from bs4 import BeautifulSoup


# 定义一个获取页面的方法
def open_url(url):
    
    try:
        print('正在打开网站：' + url)
        # 初始化Request对象
        req = urllib.request.Request(url)
        # 添加User-Agent
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
        # 打开url对应的对象
        response = urllib.request.urlopen(req)
        print('打开网站成功...')
        # 读取
        html = response.read()
        return html
    except Exception as e:
        print(e)
        return -1


"""
# 保存到文件
def save_file(dict_href):
    folder = './target'
    os.mkdir(folder)
    os.chdir(folder)
    for each in dict_href.items():
        # 保存文件
        with open('target.txt','a') as f:
            f.write(each[0] + ' ' + each[1] + '\n')
        #time.sleep(1)
"""

# 保存到数据库
def insert_data(datalist):   
    try:
        #创建数据库连接对象
        conn = mysql.connector.connect(host = 'localhost',user = 'root', password = 'root123', database = 'test')
    except Exception as e:
        print(e)
    else:
        print('数据库连接成功，准备插入数据...')
        #创建游标
        cursor = conn.cursor()
    #创建数据库表
    try:
        CREATE_TABLE_SQL = '''
            CREATE TABLE VIDEO_LIST(
             ID INT(10) NOT NULL PRIMARY KEY AUTO_INCREMENT
            ,TITLE1 VARCHAR(255),TITLE2 VARCHAR(255)
            ,VIDEO_NAME VARCHAR(1000),HREF VARCHAR(500)
            ,CREATE_TIME DATETIME,UPDATE_TIME DATETIME)
        '''
        cursor.execute(CREATE_TABLE_SQL)
    except Exception as e:
        pass

    #插入数据
    count = 0
    for each in datalist:
        count += 1
        sql = 'insert into VIDEO_LIST(TITLE1,TITLE2,VIDEO_NAME,href,Create_time,update_time) VALUES(%s,%s,%s,%s,%s,%s)'
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(sql,(each['title1'],each['title2'],str(each['video_name']),str(each['href']),now,now))
    print('数据插入完成，成功插入%s条记录'%count)

    cursor.close()
    conn.commit()
    conn.close()


# 主函数
def crawler():
    # 目标地址
    url = 'http://www.ygdy8.net/html/gndy/dyzz/'
    video_list = []
    for i in range(1,500):
        full_url=  url + 'list_23_' + str(i) + '.html' 
        html_page = open_url(full_url)
        if html_page == -1:
            print('打开网站失败...')
            return -1
        print('开始爬取第[' + str(i) + ']页')
        html_page = html_page.decode('gbk', errors='ignore')
        soup = BeautifulSoup(html_page,"html.parser")
        #links = soup.find_all('a','ulink')
        #links = soup.find_all(re.compile(r'list'))
        links = soup.select('b > a')
        domain = 'http://www.ygdy8.net'
        for link in links:
            dict_video = {}
            title1 = '最新电影'
            title2 = ''
            href = domain + link.get('href')
            video_name = link.string
            #link1 = link.find_previous('a')
            dict_video['title1'] = '最新电影'
            dict_video['title2'] = ''
            dict_video['video_name'] = video_name
            dict_video['href'] = href
            video_list.append(dict_video)
            
            print('栏目1：'+ title1 + ' 栏目2:' + title2 + ' 电影名:' + video_name + ' 链接：' + href)
        t = int(random.uniform(1, 5))
        if len(video_list) >= 100:
            insert_data(video_list)
            video_list = []
        print('第[' + str(i) + ']页爬取完成，将休眠[' + str(t) + ']秒')
        time.sleep(t)
    print('爬取结束！')

# 程序入口    
if __name__ == '__main__':
    crawler()
