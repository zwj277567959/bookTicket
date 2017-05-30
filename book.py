# coding=utf-8
from pyvirtualdisplay import Display
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

app = Flask(__name__)

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-setuid-sandbox")

def get_item(html):
    txt1 = []
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', attrs={'id': 'jxContentPanel'})
    for tmp in table.find_all('div', attrs={'class': 'b_result_box js_list_block b_result_commentbox'}):
        txt = ''
        name = tmp.find('a', attrs={'class': 'e_title js_list_name'}).get_text().strip()
        if tmp.find('p', attrs={'class': 'item_price js_hasprice'}) is not None:
            price = tmp.find('p', attrs={'class': 'item_price js_hasprice'}).get_text().strip()
        else:
            price = tmp.find('div', attrs={'class': 'hotel_price'}).get_text().strip()
        locate = tmp.find('span', attrs={'class': 'area_contair'}).get_text().strip()
        txt += name + ' ' + price + ' ' + locate
        txt1.append(txt)
    return txt1


@app.route('/bookHotel', methods=['GET'])
def bookhotel():
    city = request.args.get('city')
    append = request.args.get('append')
    fromDate = request.args.get('fromDate')
    toDate = request.args.get('toDate')
    print city
    print append

    try:
        display = Display(visible=0, size=(1024, 768))
        display.start()
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('http://hotel.qunar.com')
        driver.find_element_by_class_name('search-btn').click()
        driver.find_element_by_id('toCity').send_keys(city)
        driver.find_element_by_id('toCity').send_keys(Keys.TAB)
        driver.find_element_by_id('fromDate').send_keys(fromDate)
        driver.find_element_by_id('fromDate').send_keys(Keys.TAB)
        driver.find_element_by_id('toDate').send_keys(toDate)
        driver.find_element_by_id('toDate').send_keys(Keys.TAB)
        driver.find_element_by_id('jxQ').send_keys('  ' + append)
        driver.find_element_by_id('jxQ').send_keys(Keys.TAB)
        driver.find_element_by_tag_name('button').click()
        txt = get_item(driver.page_source)
        driver.find_element_by_class_name('next').click()
        driver.close()
        display.stop()
        return jsonify({'txt': txt})
    except Exception, e:
        driver.close()
        display.stop()
        return jsonify({'txt': e})

@app.route('/bookFlight', methods=['GET'])
def bookflight():
    isround = request.args.get('isround')
    print isround
    fromCity = request.args.get('fromCity')
    toCity = request.args.get('toCity')
    toDate = request.args.get('toDate')
    fromDate = request.args.get('fromDate')

    try:
        display = Display(visible=0, size=(1024, 768))
        display.start()
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('http://flights.ctrip.com/')
        if isround:
            driver.find_element_by_id('radio_D').click()
            driver.find_element_by_id('ReturnDepartDate1TextBox').click()
            driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(toDate)
            driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(Keys.TAB)
        driver.find_element_by_id("DepartCity1TextBox").send_keys("")
        driver.find_element_by_id("DepartCity1TextBox").send_keys(fromCity)
        driver.find_element_by_id("DepartCity1TextBox").send_keys(Keys.TAB)
        driver.find_element_by_id("ArriveCity1TextBox").click()
        driver.find_element_by_id("ArriveCity1TextBox").send_keys(toCity)
        driver.find_element_by_id("ArriveCity1TextBox").send_keys(Keys.TAB)
        driver.find_element_by_id("DepartDate1TextBox").click()
        driver.find_element_by_id("DepartDate1TextBox").send_keys(fromDate)
        driver.find_element_by_id("DepartDate1TextBox").send_keys(Keys.TAB)
        driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(toDate)
        driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(Keys.TAB)
        driver.find_element_by_class_name("search").click()
        sleep(2)
        list = []
        for tmp in driver.find_elements_by_class_name("search_box"):
            txt = ''
            txt += tmp.find_element_by_class_name('logo').text.replace("\n", " ") + " " \
                   + tmp.find_element_by_class_name('right').text.replace("\n", "(") + ")" + "-" \
                   + tmp.find_element_by_class_name('left').text.replace("\n", "(") + ")" + " " \
                   + tmp.find_element_by_class_name('service').text.replace("\n", " ") + " " \
                   + tmp.find_element_by_class_name('price').text.replace("\n", " ")
            list.append(txt)
        driver.close()
        display.stop()
        return jsonify({'txt': list})
    except Exception, e:
        driver.close()
        display.stop()
        return jsonify({'txt': e})

@app.route('/bookTrain', methods=['GET'])
def booktrain():
    fromCity = request.args.get('fromCity')
    toCity = request.args.get('toCity')
    fromDate = request.args.get('fromDate')

    try:
        display = Display(visible=0, size=(1024, 768))
        display.start()
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('http://train.qunar.com/')
        sleep(2)
        # driver.find_element_by_css_selector("input[name='fromStation']").click()
        driver.find_element_by_css_selector("input[name='fromStation']").send_keys(fromCity)
        driver.find_element_by_css_selector("input[name='fromStation']").send_keys(Keys.TAB)
        # driver.find_element_by_css_selector("input[name='toStation']").click()
        driver.find_element_by_css_selector("input[name='toStation']").send_keys(toCity)
        driver.find_element_by_css_selector("input[name='toStation']").send_keys(Keys.TAB)
        # driver.find_element_by_css_selector("input[name='date']").click()
        driver.find_element_by_css_selector("input[name='date']").send_keys(fromDate)
        driver.find_element_by_css_selector("input[name='date']").send_keys(Keys.TAB)
        driver.find_element_by_css_selector("button[name='stsSearch']").click()
        sleep(2)
        trainllist = []
        for tmp in driver.find_elements_by_class_name("js_listinfo"):
            txt = ''
            txt += tmp.find_element_by_class_name("col1").text.replace("\n", " ") + " " \
                   + tmp.find_element_by_class_name("col2").text.replace("\n", " ") + " " \
                   + tmp.find_element_by_class_name("startime").text.replace("\n", " ") + " " \
                   + tmp.find_element_by_class_name("endtime").text.replace("\n", " ") + " " \
                   + tmp.find_element_by_class_name("col6").text.replace("\n", " ") + " " \
                   + tmp.find_element_by_class_name("col3").text.replace("\n", " ") + " " \
                   + tmp.find_element_by_class_name("col4").text.replace("\n", " ")
            trainllist.append(txt)

        driver.close()
        display.stop()
        return jsonify({'txt': trainllist})
    except Exception, e:
        driver.close()
        display.stop()
        return jsonify({'txt': e})

@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
