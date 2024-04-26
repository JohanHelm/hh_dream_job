import time

from selenium import webdriver

from secrets.client_secrets import client_id

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument('--user-data-dir=/home/pp/.config/google-chrome/Default')
options_chrome.add_experimental_option('excludeSwitches', ['enable-automation'])

url = f"https://hh.ru/oauth/authorize?response_type=code&client_id={client_id}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"}

with webdriver.Chrome(options=options_chrome) as browser:
    browser.get(url)
    time.sleep(60)
