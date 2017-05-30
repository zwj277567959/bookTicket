# coding=utf-8
import urllib2
import re
import robotparser
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import sys

# city = sys.argv[0]
# fromDate = sys.argv[1]
# toDate = sys.argv[2]
# append = sys.argv[3]


def get_item(html):
    txt = ''
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div',attrs={'id':'jxContentPanel'})
    for tmp in table.find_all('div',attrs={'class':'b_result_box js_list_block b_result_commentbox'}):
        name = tmp.find('a',attrs={'class':'e_title js_list_name'}).get_text().strip()
        if tmp.find('p', attrs={'class': 'item_price js_hasprice'}) is not None:
            price = tmp.find('p',attrs={'class':'item_price js_hasprice'}).get_text().strip()
        else:
            price = tmp.find('div',attrs={'class':'hotel_price'}).get_text().strip()
        locate = tmp.find('span', attrs={'class': 'area_contair'}).get_text().strip()
        txt += name + ' ' + price + ' ' + locate + ' \n'
    return txt




driver = webdriver.Chrome()
driver.get('http://hotel.qunar.com')
driver.find_element_by_class_name('search-btn').click()
city = '上海'
append = '北邮'
# driver.find_element_by_id('fromDate').send_keys(fromDate.decode('utf-8'))
# driver.find_element_by_id('toDate').send_keys(toDate.decode('utf-8'))
driver.find_element_by_id('jxQ').send_keys(append.decode('utf-8'))
driver.find_element_by_tag_name('button').click()
for i in range(1,2,1):
    print get_item(driver.page_source)
    time.sleep(2)
    driver.find_element_by_class_name('next').click()