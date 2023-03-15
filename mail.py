from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from pymongo import MongoClient
from selenium.webdriver.chrome.service import Service
import time


def _parse_element(element, css_selector):
    result = WebDriverWait(element, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).text
    return result


def parse_email(element):
    item = {}

    item['from_name'] = _parse_element(
        element, 'span[class~="ns-view-message-head-sender-name"]')
    item['from_email'] = _parse_element(
        element, 'span[class~="mail-Message-Sender-Email"]')
    item['date'] = _parse_element(element,
                                  'div[class~="ns-view-message-head-date"]')
    item['subject'] = _parse_element(
        element, 'div[class~="mail-Message-Toolbar-Subject"]')
    item['text_messege'] = _parse_element(
        element, 'div.mail-Message-Body-Content')

    return item


MONGO_URI = 'mongodb://172.17.0.2:27017/'
MONGO_DATABASE = 'mail_db'

client = MongoClient(MONGO_URI)
mongo_base = client[MONGO_DATABASE]
collection = mongo_base['messeges']

#chrome_options = Options()
#chrome_options.add_argument("--headless")

driver = webdriver.Chrome()

url = 'https://mail.yandex.ru/'
title_site = 'Yandex'

driver.get(url)



try:
    mail_button = driver.find_element(By.XPATH,
    "//a[@class='Button2 Button2_type_link Button2_view_default Button2_size_m']"
    )
    mail_link = mail_button.get_attribute("href")
    driver.get(mail_link)

except exceptions.NoSuchElementException:
    print('Mail login not found')



if 'Авторизация' in driver.title:
   

    field_login = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'passp-field-login')))
    field_login.send_keys('Lyber777@yandex.ru')
    field_login.send_keys(Keys.ENTER)
    field_passwd = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'passp-field-passwd')))
    field_passwd.send_keys('*********')
    field_passwd.send_keys(Keys.ENTER)
    time.sleep(3)

    button_click = driver.find_element(By.XPATH, "//div[@data-t='challenge_sumbit_phone-confirmation']")
    button_click.click()


first_messege = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.CLASS_NAME, 'ns-view-messages-item-wrap')
    )
)
first_messege.click()

while True:
    try:
        collection.insert_one(parse_email(driver))

        button_next = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'след.')))
        button_next.click()
    except exceptions.TimeoutException:
        print('E-mails are over')
        break

driver.quit()