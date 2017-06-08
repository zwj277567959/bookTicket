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
        txt = {}
        txt["name"] = tmp.find('a', attrs={'class': 'e_title js_list_name'}).get_text().strip()
        if tmp.find('p', attrs={'class': 'item_price js_hasprice'}) is not None:
            txt["price"] = tmp.find('p', attrs={'class': 'item_price js_hasprice'}).get_text().strip()
        else:
            txt["price"] = tmp.find('div', attrs={'class': 'hotel_price'}).get_text().strip()
        txt["locate"] = tmp.find('span', attrs={'class': 'area_contair'}).get_text().strip()
        txt1.append(txt)
    return txt1


@app.route('/bookHotel', methods=['GET'])
def bookhotel():
    city = request.args.get('city')
    append = request.args.get('append')
    fromDate = request.args.get('fromDate')
    toDate = request.args.get('toDate')

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
        driver.quit()
        display.stop()
        return jsonify({'status': 200, 'data': txt})
    except Exception, e:
        driver.quit()
        display.stop()
        return jsonify({'status': -1, 'error': e})

@app.route('/bookFlight', methods=['GET'])
def bookflight():
    isround = request.args.get('isround')
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
            print ("1111111")
            driver.find_element_by_id('radio_D').click()
            driver.find_element_by_id('ReturnDepartDate1TextBox').click()
            driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(toDate)
            driver.find_element_by_id('ReturnDepartDate1TextBox').send_keys(Keys.TAB)
        else:
            toDate = fromDate
        driver.find_element_by_id('DepartCity1TextBox').click()
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
            txt = {}
            txt["company"] = tmp.find_element_by_class_name('logo').text.replace("\n", " ")
            right = tmp.find_element_by_class_name('right').text.split("\n")
            txt["startime"] = right[0]
            txt["fromPlace"] = right[1]
            left = tmp.find_element_by_class_name('left').text.split("\n")
            txt["endtime"] = left[0]
            txt["toPlace"] = left[1]
            txt["unDelayRate"] = tmp.find_element_by_class_name('service').text.replace("\n", " ")
            txt["price"] = tmp.find_element_by_class_name('price').text.replace("\n", " ")
            list.append(txt)
        driver.quit()
        display.stop()
        print (list)
        return jsonify({'status': 200, 'data': list})
    except Exception, e:
        driver.quit()
        display.stop()
        return jsonify({'status': -1, 'error': e})

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
            txt = {}
            txt["train"] = tmp.find_element_by_class_name("train").text.replace("\n", " ")
            txt["fromPlace"] = tmp.find_element_by_class_name("start").text.replace("\n", " ")
            txt["toPlace"] = tmp.find_element_by_class_name("end").text.replace("\n", " ")
            txt["startime"] = tmp.find_element_by_class_name("startime").text.replace("\n", " ")
            txt["endtime"] = tmp.find_element_by_class_name("endtime").text.replace("\n", " ")
            txt["timelong"] = tmp.find_element_by_class_name("col6").text.replace("\n", " ")
            ticketType = tmp.find_element_by_class_name("col3").text.split("\n")
            ticketNum = tmp.find_element_by_class_name("col4").text.split("\n")
            txt["tickets"] =[]
            for i in range(len(ticketNum)):
                ticket ={}
                ticket["type"] = ticketType[i].split(" ")[0]
                ticket["price"] = ticketType[i].split(" ")[1]
                ticket["num"] = ticketNum[i]
                txt["tickets"].append(ticket)
            trainllist.append(txt)
        driver.quit()
        display.stop()

        return jsonify({'status': 200, 'data': trainllist})
    except Exception, e:
        driver.quit()
        display.stop()
        return jsonify({'status': -1, 'error': e})

@app.route('/')
def index():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
