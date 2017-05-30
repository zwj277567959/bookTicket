# coding=utf-8
import urllib2
import re
import robotparser
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


fromCity = '天津';
toCity = ' 上海';
toDate ='2017-05-28';
fromDate = '2017-05-25'

driver = webdriver.Chrome()
driver.get('http://train.qunar.com/')
sleep(2)
# driver.find_element_by_css_selector("input[name='fromStation']").click()
driver.find_element_by_css_selector("input[name='fromStation']").send_keys(fromCity.decode('utf-8'))
driver.find_element_by_css_selector("input[name='fromStation']").send_keys(Keys.TAB)
# driver.find_element_by_css_selector("input[name='toStation']").click()
driver.find_element_by_css_selector("input[name='toStation']").send_keys(toCity.decode('utf-8'))
driver.find_element_by_css_selector("input[name='toStation']").send_keys(Keys.TAB)
# driver.find_element_by_css_selector("input[name='date']").click()
driver.find_element_by_css_selector("input[name='date']").send_keys(fromDate.decode('utf-8'))
driver.find_element_by_css_selector("input[name='date']").send_keys(Keys.TAB)
driver.find_element_by_css_selector("button[name='stsSearch']").click()
sleep(3)
txt = ''
for tmp in driver.find_elements_by_class_name("js_listinfo"):
    txt+= tmp.find_element_by_class_name("col1").text.replace("\n", " ") + " " \
        + tmp.find_element_by_class_name("col2").text.replace("\n", " ") + " " \
        + tmp.find_element_by_class_name("startime").text.replace("\n", " ") + " " \
        + tmp.find_element_by_class_name("endtime").text.replace("\n", " ") + " " \
        + tmp.find_element_by_class_name("col6").text.replace("\n", " ") + " " \
        + tmp.find_element_by_class_name("col3").text.replace("\n", " ") + " "\
        + tmp.find_element_by_class_name("col4").text.replace("\n", " ") + "/n"