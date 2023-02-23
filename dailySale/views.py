import json
import os
import time
from datetime import date, datetime

import requests
import selenium
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common import keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# Create your views here.
# def getJson():
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logininfo.json")
file = open(json_path, 'rt', encoding='utf-8-sig')
loginInfo = json.load(file);

def baemin(request):
    data = loginInfo['baemin']

    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) # 브라우저 꺼짐 방지
    mobile_emulation = {"deviceName": "iPhone X"}
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation) # 모바일버전 설정
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 불필요한 에러 메시지 없애기

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # dr = webdriver.Chrome("C:/windows/chromedriver.exe")  # 크롬 드라이버를 실행하는 명령어를 dr로 지정
    driver.set_window_position(0, 0)
    driver.set_window_size(1500, 800)
    driver.get(data['url'])
    time.sleep(2)

    act = ActionChains(driver)  # 드라이버에 동작을 실행시키는 명령어를 act로 지정
    # elem_id = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/form/div[1]/span/input')
    # elem_pw = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/form/div[2]/span/input')
    # btnLogin = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/form/button')
    elem_id = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/form/div[1]/span/input')
    elem_pw = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/form/div[2]/span/input')
    btnLogin = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/form/button')
    act.send_keys_to_element(elem_id, data['id']).send_keys_to_element(elem_pw, data['password']).click(btnLogin).perform()
    time.sleep(2)

    # 주문내역 url로 바로 이동
    orderUrl = 'https://ceo.baemin.com/self-service/orders/history'
    driver.execute_script('window.open("https://ceo.baemin.com/self-service/orders/history");')
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(4)

    # 날짜설정
    openPopUp = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div[3]/div[1]/div/div[1]/button[1]')
    openPopUp.click()
    btnDaily = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/form/div[2]/div/div/div[1]/label[1]/div')
    btnDaily.click()
    rdaioDaily = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/form/div[2]/div/div/div[2]/div/div/div[2]/label/input')
    rdaioDaily.click()
    btnApply = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[4]/div[1]/form/div[3]/button')
    btnApply.click();
    time.sleep(3)

    date = driver.find_element(By.CLASS_NAME, 'FilterContainer-module__k3Id')
    dailySaleSum = driver.find_elements(By.CLASS_NAME, 'Contents-module__GDe2')
    print(date.text, dailySaleSum[1].text)
    loginInfo['baemin']['date'] = date.text
    loginInfo['baemin']['sum'] = dailySaleSum[1].text
    context = loginInfo
    template = loader.get_template('dailySale/index.html')
    return HttpResponse(template.render(context, request))

def index(request):
    template = loader.get_template('dailySale/index.html')
    context = loginInfo
    return HttpResponse(template.render(context, request))
