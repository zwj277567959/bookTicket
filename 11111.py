import urllib2
import re
import robotparser
import time
from bs4 import BeautifulSoup
from selenium import webdriver


def get_item(html):
    result = open('1111.txt', 'a+')
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div',attrs={'id':'jxContentPanel'})
    for tmp in table.find_all('div',attrs={'class':'b_result_box js_list_block b_result_commentbox'}):
        name = tmp.find('a',attrs={'class':'e_title js_list_name'}).get_text().strip()
        if tmp.find('p', attrs={'class': 'item_price js_hasprice'}) is not None:
            price = tmp.find('p',attrs={'class':'item_price js_hasprice'}).get_text().strip()
        else:
            price = tmp.find('div',attrs={'class':'hotel_price'}).get_text().strip()
        locate = tmp.find('span', attrs={'class': 'area_contair'}).get_text().strip()
        result.write(name.encode('utf-8') + '\t')
        result.write(price.encode('utf-8') + '\t')
        result.write(locate.encode('utf-8') + '\n')
    result.close()

driver = webdriver.Chrome()
driver.get('http://hotel.qunar.com')
driver.find_element_by_class_name('search-btn').click()
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
num = int(soup.find('li', attrs={'class': 'item'}).get_text().split('/')[1])
get_item(html)
for i in range(1,num,1):
    print i
    driver.find_element_by_class_name('next').click()
    get_item(driver.page_source)
    time.sleep(2)
