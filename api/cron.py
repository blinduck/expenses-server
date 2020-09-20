import time
from datetime import datetime
from pprint import pprint

import arrow
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

login_page = "https://thewaterside.com.sg/account/login"
squash_booking_page = 'https://thewaterside.com.sg/facilities/booking/1036'



def write_to_file(text):
    f = open("weblog.txt", "a")
    f.write(text)
    f.close()


def do_booking(driver, username, password, court):
    driver.get(login_page)
    username_el = driver.find_element_by_id("Username")
    pprint(username_el)
    username_el.clear()
    username_el.send_keys(username)
    password_el = driver.find_element_by_id("Password")
    password_el.clear()
    password_el.send_keys(password)
    time.sleep(1)
    form_el = driver.find_element_by_id('login-form')
    form_el.submit()

    driver.get(squash_booking_page)
    time.sleep(1)
    date_id = get_next_wednesday_id()
    driver.find_element_by_id('d' + date_id).click()
    time.sleep(0.5)
    prefix = 't80' if court is 1 else 't81'
    print('prefix is ', prefix)
    driver.find_element_by_id(prefix + '_1900_2000_' + date_id).click()
    driver.find_element_by_id(prefix + '_2000_2100_' + date_id).click()

    time.sleep(0.5)

    driver.find_element_by_id('cmd-bk-book').click()



def test_selenium():
    chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox") # linux only
    chrome_options.add_argument("--headless")

    # driver = webdriver.Chrome('/usr/local/bin/chromedriver',  options=chrome_options)
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    do_booking(driver, "Chewycowz@gmail.com", "ChewY13!", 1)
    time.sleep(3000)
    # driver.close()



def get_next_wednesday_id():
    return '2020-09-24'

    #  assuming it's running on tuesday in UTC
    start = arrow.get(datetime(2020, 9, 29), 'UTC')
    next_wed = start.shift(days=+8)
    return next_wed.format('YYYY-MM-DD')

def test_timing():
    time = arrow.utcnow()
    write_to_file(time.format() + " " +  time.to("Asia/Singapore").format() + '\n')

