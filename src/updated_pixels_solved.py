from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By
import json


def gotourl(url):
  htmlpage = None
  try:
    htmlpage = requests.get(url).text
  except:
    htmlpage = None
  return htmlpage

def details(bs):
  det = {}
  det['url'] = ''
  det['dimension'] = ''
  det['size'] = ''
  det['time'] = ''
  det['type'] = ''

  fileinfo = ''
  size = ''
  type_ = ''
  dim = ''
  url_ = ''
  time_ = ''

  try:
    try:
      fileinfo = bs.find('span', {'class' : 'fileInfo'}).text
    except:
      a = 6
    try:
      size = re.findall('file size:\s*.*\s*KB', fileinfo)[0]
    except:
      a = 7
    try:
      type_ = re.findall('MIME type:\s*image\/.*', fileinfo)[0]
    except:
      a = 6
    try:
      dim = re.findall('[0-9].*,*[0 - 9].*pixels', fileinfo)[0]
    except:
      a = 7
    try:
      url_ = bs.find('a', href = re.compile('^(https://upload)')).attrs['href']
    except:
      a = 8
    try:
      time_ = bs.find('time', {'class' : 'dtstart'}).text
    except:
      a = 8
  
    if size.count('file size:') > 0:
      size = size.replace('file size:', '')
  except:
    a = 5

  
  det['url'] = url_
  det['size'] = size
  det['type'] = type_
  det['dimension'] = dim
  det['time'] = time_

  return det





#print(html)





driver = webdriver.Chrome()
url = 'https://commons.wikimedia.org/w/index.php?search=Elvis+Presley&title=Special:MediaSearch&type=image'
driver.get(url)
time.sleep(5)
elems = driver.find_elements(By.CLASS_NAME, 'sdms-image-result')


counter = 0



urls = set()



for elem in elems:
  url = elem.get_attribute('href')
  html = gotourl(url)
  bs = BeautifulSoup(html, 'lxml')
  det = details(bs)
  if len(det['url']) > 2:
    if det['url'] not in urls:
      urls.add(det['url'])
      print(det)

print(len(urls))
#print(counter)

driver.close()
