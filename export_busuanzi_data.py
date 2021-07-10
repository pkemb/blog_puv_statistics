#-*- coding: UTF-8 -*-

import sys
import time
import urllib2
from bs4 import BeautifulSoup
import json
import xml.dom.minidom
import uuid
import datetime
import random
import socket
import os

reload(sys)
sys.setdefaultencoding('utf8')

header={'Referer':'', 'cookie':''}
busuanzi_url='http://busuanzi.ibruce.info/busuanzi?jsonpCallback=BusuanziCallback_1046609647591'
stat_file="page_puv_statistics.json"

def get_page_puv(url):
    header['Referer'] = url
    time.sleep(random.randint(1,5))
    try:
        req = urllib2.Request(busuanzi_url, headers=header)
        url_connection = urllib2.urlopen(req)
        source_code = url_connection.read()
        url_connection.close()
        plain_text=str(source_code)
    except (urllib2.HTTPError, urllib2.URLError, socket.error), e:
        print e
        return

    soup = BeautifulSoup(plain_text, "lxml")
    jsonp_string = soup.find("p").string
    json_string = jsonp_string.replace(');}catch(e){}', '').replace('try{BusuanziCallback_1046609647591(', '')
    return json.loads(json_string)

def get_site_map(sitemap_url):
    url_list = []
    try:
        req = urllib2.Request(sitemap_url)
        source_code = urllib2.urlopen(req).read()
        plain_text=str(source_code)
    except (urllib2.HTTPError, urllib2.URLError), e:
        print e
        return url_list

    dom_tree = xml.dom.minidom.parseString(plain_text)
    urlset = dom_tree.documentElement
    xml_urls = urlset.getElementsByTagName("url")
    for xml_url in xml_urls:
        url_loc = xml_url.getElementsByTagName('loc')[0]
        page_url = url_loc.childNodes[0].data
        url_list.append(page_url)
        #print(page_url)
    return url_list

if __name__=='__main__':
    busuanziId       = "".join(str(uuid.uuid4()).split("-")).upper()
    header['cookie'] = 'busuanziId=' + busuanziId
    url_list         = get_site_map("https://pkemb.com/sitemap.xml")

    page_puv_array = []
    for url in url_list:
        print(url)
        page_puv = {}
        while not page_puv:
            time.sleep(random.randint(1,3))
            page_puv = get_page_puv(url)

        page_puv['url'] = url
        page_puv.pop('version')
        page_puv_array.append(page_puv)

    now = str(datetime.datetime.now())
    page_puv_statistics = {'time':now, 'page_puv':page_puv_array}
    #print(page_puv_statistics)

    # write json to file
    if not os.path.exists(stat_file):
        with open(stat_file, 'a+') as f:
            print("file " + stat_file + "create success!!!")

    with open("page_puv_statistics.json", "r+") as f:
        value=f.read()
        if not value:
            stat_array = []
        else:
            stat_array = json.loads(value)['page_puv_statistics']
        stat_array.append(page_puv_statistics)
        f.seek(0)
        f.truncate()
        json.dump({'page_puv_statistics':stat_array}, f)