#-*- coding:utf-8 -*-
import requests
from pyquery import PyQuery
import time
import re
import os
from threading import Thread

url = 'http://news.baidu.com/'

def read_now():
    """ 查看新闻或保存新闻
    """
    yes_no = input('今天的新闻准备好了,是否现在查看(n/y): ')
    if yes_no in ['y', 'Y']:
        print('正在打开，请稍等...')
        time.sleep(3)
        os.startfile(str(date) + 'news.txt')
    else:
        print('新闻已帮您保存至本地，可以随时查看！')

def close_now():
    """提示'关闭'作用
    """
    print('\n')
    print('页面正在关闭...')
    time.sleep(3)

try:
    response1 = requests.get(url)
    if response1.status_code == 200:
        jpy = PyQuery(response1.text)
        news_lists = jpy('ul > li').items()
        # new = [] #list
        news = ''  # str
        for it in news_lists:  # 获取静态页面的新闻标题和对应链接
            new_content = it('a').text()
            new_link = it('a').attr('href')
            new1 = new_content + '   ' + str(new_link) + '\n'
            # new.append(new1)# 对应new = [],以list形式保存
            news += new1  # 对应new = ''，以str形式保存

        # 利用正则匹配去除多余的内容
        b = re.search(r'(热点要闻.*?javascript:;\s[\w\W\d\D\s\S]*)?(二维码.*?javascript:;)\s', news)

        # 获取当前时间
        code_time = int(time.time())
        timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(code_time))
        # 添加一些附加信息
        news_headers = '新闻来源：百度新闻' + '\n' + '获取时间：' + str(timenow) + '\n' \
                       + 'Authorization: 中原' + '\n'
        result_news = news_headers + b.group(1)

        date = time.strftime('%Y-%m-%d')
        with open(str(date) + 'news.txt', 'w', encoding='utf-8') as f:
            f.write(result_news)

        # 利用多线程在长时间无输入时自动退出
        thd = Thread(target=read_now)
        thd.daemon = True
        thd.start()

        time.sleep(10)
        close_now()
    else:
        print('页面请求出错了...')
        time.sleep(2)
except:
    print('似乎是断网了...')
    time.sleep(2)







