# coding=utf-8
import urllib2
import re
import robotparser
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep


isround = False;
fromCity = '天津';
toCity = ' 上海';
toDate ='2017-05-28';
fromDate = '2017-05-25'

driver = webdriver.Chrome()
driver.get('http://flights.ctrip.com/')
if isround:
    driver.find_element_by_id('radio_D').click()
    driver.find_element_by_id('ReturnDepartDate1TextBox').click()
    driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(toDate.decode('utf-8'))
    driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(Keys.TAB)
else:
    driver.find_element_by_id("DepartCity1TextBox").send_keys("")
    driver.find_element_by_id("DepartCity1TextBox").send_keys(fromCity.decode('utf-8'))
    driver.find_element_by_id("DepartCity1TextBox").send_keys(Keys.TAB)
    driver.find_element_by_id("ArriveCity1TextBox").click()
    driver.find_element_by_id("ArriveCity1TextBox").send_keys(toCity.decode('utf-8'))
    driver.find_element_by_id("ArriveCity1TextBox").send_keys(Keys.TAB)
    driver.find_element_by_id("DepartDate1TextBox").click()
    driver.find_element_by_id("DepartDate1TextBox").send_keys(fromDate.decode('utf-8'))
    driver.find_element_by_id("DepartDate1TextBox").send_keys(Keys.TAB)
    driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(toDate.decode('utf-8'))
    driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(Keys.TAB)
driver.find_element_by_class_name("search").click()
sleep(3)
for tmp in driver.find_elements_by_class_name("search_table_header"):
    txt = ""
    txt += tmp.find_element_by_class_name('logo').text.replace("\n", " ")+" "\
         + tmp.find_element_by_class_name('right').text.replace("\n", "(")+")"+"-"\
         + tmp.find_element_by_class_name('left').text.replace("\n", "(")+")"+" "\
         + tmp.find_element_by_class_name('service').text.replace("\n", " ")+" "\
         + tmp.find_element_by_class_name('price').text.replace("\n", " ")
    print txt