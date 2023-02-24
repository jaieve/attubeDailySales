import json
import os
import time
import datetime

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
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation) # 모바일버전 설정
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 불필요한 에러 메시지 없애기
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # dr = webdriver.Chrome("C:/windows/chromedriver.exe")  # 크롬 드라이버를 실행하는 명령어를 dr로 지정
    driver.set_window_position(0, 0)
    driver.set_window_size(1500, 800)
    driver.get(data['url'])
    time.sleep(2)

    act = ActionChains(driver)  # 드라이버에 동작을 실행시키는 명령어를 act로 지정
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

    loginInfo['baemin']['date'] = getYesterday('-')
    loginInfo['baemin']['sum'] = dailySaleSum[1].text  + " 원"
    driver.quit()

    context = loginInfo
    template = loader.get_template('dailySale/index.html')
    return HttpResponse(template.render(context, request))

def yogiyo(request):
    data = loginInfo['yogiyo']
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) # 브라우저 꺼짐 방지
    mobile_emulation = {"deviceName": "iPhone X"}
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation) # 모바일버전 설정
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) # 불필요한 에러 메시지 없애기
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # dr = webdriver.Chrome("C:/windows/chromedriver.exe")  # 크롬 드라이버를 실행하는 명령어를 dr로 지정
    driver.set_window_position(0, 0)
    driver.set_window_size(1500, 800)
    driver.get(data['url'])
    time.sleep(2)
    act = ActionChains(driver)  # 드라이버에 동작을 실행시키는 명령어를 act로 지정
    elem_id = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[1]/td/input')
    elem_pw = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/table/tbody/tr[2]/td/input')
    btnLogin = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/button')
    act.send_keys_to_element(elem_id, data['id']).send_keys_to_element(elem_pw, data['password']).click(btnLogin).perform()
    time.sleep(5)

    # 날짜설정
    dateStart = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/table/tbody/tr/td[2]/div/div[1]/div/input")
    dateEnd = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div[2]/div[2]/table/tbody/tr/td[2]/div/div[2]/div/input")
    btnSearch = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[2]/button')

    yesterday = getYesterday("-")
    dateStart.send_keys('')
    dateStart.send_keys(yesterday)
    dateEnd.send_keys('')
    dateEnd.send_keys(yesterday)
    act.click(btnSearch).perform()
    time.sleep(4)
    dailySaleSum = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div[2]/div[4]/div[2]/div/div[2]/table/tbody/tr[2]/td[4]/span[1]')

    loginInfo['yogiyo']['date'] = yesterday
    loginInfo['yogiyo']['sum'] = dailySaleSum.text  + " 원"
    driver.quit()

    context = loginInfo
    template = loader.get_template('dailySale/index.html')
    return HttpResponse(template.render(context, request))


def deleteComma(price):
    price = price.replace('원','').strip()
    price = price.replace(',', '')
    price = int(price.replace(',', ''))
    return price

def addComma(price):
    pass

def coupang(request):
    data = loginInfo['coupangEats']
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # 브라우저 꺼짐 방지
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # mobile_emulation = {"deviceName": "iPhone X"}
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation) # 모바일버전 설정
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 불필요한 에러 메시지 없애기
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # dr = webdriver.Chrome("C:/windows/chromedriver.exe")  # 크롬 드라이버를 실행하는 명령어를 dr로 지정
    driver.set_window_position(0, 0)
    driver.set_window_size(1500, 800)
    driver.get(data['url'])
    time.sleep(2)
    act = ActionChains(driver)  # 드라이버에 동작을 실행시키는 명령어를 act로 지정
    elem_id = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/form/div[1]/input')
    elem_pw = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/form/div[2]/input')
    btnLogin = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div/form/button')
    act.send_keys_to_element(elem_id, data['id']).send_keys_to_element(elem_pw, data['password']).click(btnLogin).perform()
    time.sleep(4)

    btnModalClose = driver.find_element(By.XPATH,'/html/body/div[2]/div/div/div/button')
    driver.implicitly_wait(5)
    btnModalClose.click()

    driver.find_element(By.XPATH, '/html/body/div/div/nav/div[2]/ul/li[2]/a').click()
    driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div/div[1]').click()
    time.sleep(2)

    yesterday = getYesterday(".")
    nextPage = True
    sum = 0;
    beforeSum = 0;
    for current in range(4):
        if nextPage:
            print(current + 1, "번째 페이지")
            lis = driver.find_elements(By.CSS_SELECTOR,'#merchant-management > div > div > div.management-scroll > div.management-page.p-2.p-md-4.p-lg-5.d-flex.flex-column > div > div > div > div.col-12.col-xl-9 > div:nth-child(5) > div > ul.order-search-result-content.row > li')
            for i in lis:
                date = i.find_element(By.CSS_SELECTOR,'section.order-item.row.text-nowrap > div.order-date.col-3.d-none.d-md-block > span:nth-child(1)').text.strip()
                if date == yesterday:
                    # section.order-item.row.text-nowrap > div.order-price.col-4.col-md-3.text-right > button > i
                    btnArrow = i.find_element(By.CSS_SELECTOR,'section.order-item.row.text-nowrap > div.order-price.col-4.col-md-3.text-right > button > i')
                    btnArrow.click()
                    beforeCalculate = i.find_element(By.CSS_SELECTOR,'section.container.order-details.initial-order-detail > div.row.order-summary > div.col-12.col-md-9.order-summary-detail > ul > li:nth-child(1) > div.col-4.text-right').text.strip()
                    beforeCalculate = deleteComma(beforeCalculate)
                    beforeSum = beforeSum + beforeCalculate
                    price = i.find_element(By.CSS_SELECTOR,'section.container.order-details.initial-order-detail > div.row.order-summary > div.col-12.col-md-9.order-summary-detail > ul > li.row.row-no-padding.row-border-top > div.col-4.text-right').text.strip()
                    price = deleteComma(price)
                    sum = sum + price
                    print('same', date, "매출액", beforeCalculate, "정산액", price, sum)
                    if lis.index(i)+1 == len(lis):
                        nextPageBtn = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[1]/div/div/div/div[1]/div[5]/div/div/div/div/ul/li['+str(current+4)+']/button')
                        nextPageBtn.click()
                        current = current + 1
                else:
                    print('another day')
                    if lis.index(i)+1 == len(lis):
                        nextPage = False
        else:
            break

    loginInfo['coupangEats']['date'] = getYesterday("-")
    loginInfo['coupangEats']['beforeSum'] = format(beforeSum, ',') + " 원"
    loginInfo['coupangEats']['sum'] = format(sum, ',') + " 원"
    driver.quit()

    context = loginInfo
    template = loader.get_template('dailySale/index.html')
    return HttpResponse(template.render(context, request))

def ttanggyeo(request):
    data = loginInfo['ttanggyeo']
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # 브라우저 꺼짐 방지
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # mobile_emulation = {"deviceName": "iPhone X"}
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation) # 모바일버전 설정
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 불필요한 에러 메시지 없애기
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # dr = webdriver.Chrome("C:/windows/chromedriver.exe")  # 크롬 드라이버를 실행하는 명령어를 dr로 지정
    driver.set_window_position(0, 0)
    driver.set_window_size(1500, 800)
    driver.get(data['url'])
    time.sleep(2)
    # 로그인
    act = ActionChains(driver)  # 드라이버에 동작을 실행시키는 명령어를 act로 지정
    elem_id = driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[1]/div[2]/div/input')
    elem_pw = driver.find_element(By.XPATH, '/html/body/div/div[2]/ul/li[2]/div[2]/div/input')
    btnLogin = driver.find_element(By.XPATH, '/html/body/div/div[3]/input')
    act.send_keys_to_element(elem_id, data['id']).send_keys_to_element(elem_pw, data['password']).click(
        btnLogin).perform()
    time.sleep(4)
    # 정산내역 화면 띄우기
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/nav/ul/li/ul[4]/li[3]/a').click()



    context = loginInfo
    template = loader.get_template('dailySale/index.html')
    return HttpResponse(template.render(context, request))


def index(request):
    template = loader.get_template('dailySale/index.html')
    context = loginInfo
    return HttpResponse(template.render(context, request))

def getYesterday(joinStr):
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days=-1)
    return yesterday.strftime("%Y"+joinStr+"%m"+ joinStr +"%d")