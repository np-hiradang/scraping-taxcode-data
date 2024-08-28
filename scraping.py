from selenium import webdriver
from selenium.webdriver.chrome.service import Service

DRIVER_PATH = 'chromedriver-mac-x64/chromedriver'
web = 'https://masothue.com'

service = Service(executable_path=DRIVER_PATH)
driver = webdriver.Chrome(service=service)

driver.get(web)