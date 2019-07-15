"""自动登录163邮箱-deprecated

网易邮箱的登录框iframe的id会每次加载时会自动变换
通过BeautifulSoup解析网页自动获取该id
然后使得浏览器定位到该登录框

"""

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

browser = webdriver.Chrome()
browser.get('https://mail.163.com')

sleep(5)
soup = BeautifulSoup(browser.page_source, 'lxml')
browser.switch_to.frame(soup.find('iframe')['id'])
browser.find_element_by_name('email').send_keys('your_account')
browser.find_element_by_name('password').send_keys('your_password')
browser.find_element_by_id("dologin").click()
