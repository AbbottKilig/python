# -*- coding:utf-8 -*-
#!/usr/bin/python

import os
import re
from io import BytesIO

import requests
from PIL import Image
from bs4 import BeautifulSoup


def request_picture_url(url):
    req = requests.get(url)
    bf = BeautifulSoup(req.content)
    pictures = bf.find_all('img', class_="size-full")
    picture_urls = []
    for picture in pictures:
        picture_urls.append(picture['src'])
    return picture_urls

def request_url(url):
    picture_urls = []
    picture_urls.extend(request_picture_url(url))
    req = requests.get(url)
    bf = BeautifulSoup(req.content)
    pages = bf.find_all('a', href=re.compile(url+ "/"))
    for page in pages:
        picture_urls.extend(request_picture_url(page['href']))
    return bf.title.string, picture_urls

def save_picture(path, urls):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        for i in range(len(urls)):
            print(urls[i])
            image = Image.open(BytesIO(requests.get(urls[i]).content))
            image.save(path + "/" + str(i) + ".jpg")

# path, urls = request_url(url)
# save_picture(path, urls)

if __name__ == '__main__':

    jar = requests.cookies.RequestsCookieJar()
    i = 1
    while(True):
        url = "http://www.iprshe.vip/#/page/" + str(i)
        r = requests.get(url, cookies=jar)
        jar = r.cookies
        soup = BeautifulSoup(r.content)
        refers = soup.find_all('a', class_="thumbnail")
        for refer in refers:
            print(refer['href'])
            path, urls = request_url(refer['href'])
            save_picture(path, urls)
        i =  i + 1







