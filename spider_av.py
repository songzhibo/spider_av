
import urllib
import urllib.request
import html.parser
import requests
from random import choice
import base64
import subprocess
import re
import os
from requests.exceptions import HTTPError
from socket import error as SocketError
from http.cookiejar import CookieJar

PATH = './video/'
main_url = 'https://www.406v.com/'
#type_url = 'https://www.264q.com/Html/88/'
type_url = 'https://www.264q.com/Html/%s/'

#每个类型最多下载几页视频
TYPE_MAX_NUM = 99
def create_headers():
     headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36' }
     return headers

thunder_path = 'D:\Program Files (x86)\Thunder Network\Thunder\Program\Thunder.exe'
def Url2Thunder(url):
	url='AA'+url+'ZZ'
	url = base64.b64encode(url.encode('ascii'))
	url = b'thunder://' + url
	thunder_url = url.decode()
	return thunder_url

def download_with_thunder(file_url):
	thunder_url = Url2Thunder(file_url)
	subprocess.call([thunder_path, thunder_url])

def load_video(video_url, file_path, video_name):
    # use pyhton download video
    # if not os.path.isdir(file_path):
    #     os.makedirs(file_path)
    #
    # path = file_path + video_name + '.mp4'
    # if os.path.exists(path):
    #     print(video_name+" is existed  return true")
    #     return
    #
    # request = urllib.request.Request(video_url, headers=create_headers())
    # response = urllib.request.urlopen(request)
    # data = response.read()
    # picture = open(path, "wb")
    # picture.write(data)
    #
    # response.close()

    #use thunder download
    print('start use thunder...')
    download_with_thunder(video_url)
    print('end use thunder...')

def spider_video_page(video_page_url):
#    proxiesInfo = {'http': '125.112.207.173:20376'}
    proxiesInfo = {'HTTPS': '115.203.69.181:808'}
#    proxiesInfo = {'http':'119.5.0.119:808'}
    proxies = urllib.request.ProxyHandler(proxiesInfo)

    opener = urllib.request.build_opener(proxies)
    urllib.request.install_opener(opener)

    request = urllib.request.Request(video_page_url, headers=create_headers())
    response = urllib.request.urlopen(request)

    # request = urllib.request.Request(video_page_url, None, create_headers())
    # response = urllib.request.urlopen(request)

    content = response.read().decode('utf-8')
    pattern = re.compile(
        '<ul class=.*?downurl.*?>.*?<a href="(.*?)".*?</ul>', re.S)
    items = re.findall(pattern, content)

    pattern = re.compile(
    '<dd class=.*?film_title.*?>.*?<h1>(.*?)</h1>', re.S)
    names = re.findall(pattern, content)

    response.close()

    if len(names) == 1 & len(items)==1 :
        return names[0], items[0]
    else:
        print("get name and item error")
        return 'false', 'false'

def get_conten(url):
    request = urllib.request.Request(url, None, create_headers())
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(request)
    content = response.read().decode('utf8')

    response.close()
    return content

#爬去每一页的12个视频
def spider_video_list_page(url):
    content = get_conten(url)
    pattern = re.compile(
    '<li><a href="(.*?)".*?</li>',re.S)
    items = re.findall(pattern, content)

    print ('')
    print('page list url = ', url)
    print("page list length = ", len(items))
    for item in items:
        video_page_url = main_url + item
        video_name,  video_url = spider_video_page(video_page_url)
        if video_name == 'false':
            continue

        print(video_page_url)
        print (video_name)
        print (video_url)
        file_path = PATH
        load_video(video_url, file_path, video_name)

#爬去一个类型的所有视频
def spider_atype(type_url):
    #获取类型名字
    content = get_conten(type_url)
    pat = re.compile(
    '<div class="box cat_pos clearfix">.*?<span class="cat_pos_l">'
    '.*?<a href.*?<a href.*?>(.*?)</a>',re.S)
    type_names = re.findall(pat, content)
    print('spider ' + type_names[0] + ' : ' + type_url)

    #先爬去总页数
    pattern = re.compile(
    '<strong>.*?/(.*?)</strong>',re.S)
    items = re.findall(pattern, content)
    if len(items) == 0:
        print("error 页数为0 return")
        return

    page_length = int(items[0])
    print('总共 %s 页'%page_length)

    # 创建url， 第一个就是原始的url，其他的都是加上 index-2.html
    for i in range(page_length):
        if i >= TYPE_MAX_NUM :
            break

        page_url = type_url
        if i != 0:
            page_num_str = str(i+1)
            page_url = type_url + 'index-%s.html'%page_num_str

  #      print (page_url)
        spider_video_list_page(page_url)

def main():
    for i in range(7):
        num = 87 + i
        a_type_url = type_url%str(num)
        spider_atype(a_type_url)

main()
#spider_atype('https://www.264q.com/Html/88/')
# video_page_url = 'https://www.406v.com//Html/88/19675.html'
# spider_video_page(video_page_url)
