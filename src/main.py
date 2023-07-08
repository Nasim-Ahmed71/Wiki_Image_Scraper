from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By


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
    fileinfo = bs.find('span', {'class' : 'fileInfo'}).text
    size = re.findall('file size:\s*.*\s*KB', fileinfo)[0]
    type_ = re.findall('MIME type:\s*image\/.*', fileinfo)[0]
    dim = re.findall('[0 - 9].*pixels', fileinfo)[0]
    url_ = bs.find('a', href = re.compile('^(https://upload)')).attrs['href']
    time_ = bs.find('time', {'class' : 'dtstart'}).text
  
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
for elem in elems:
  url = elem.get_attribute('href')
  html = gotourl(url)
  bs = BeautifulSoup(html, 'lxml')
  det = details(bs)
  if len(det['url']) > 2:
    counter = counter + 1
  #print(det)

print(len(elems))
print(counter)

driver.close()
