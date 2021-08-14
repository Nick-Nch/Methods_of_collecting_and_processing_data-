
# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика.
# Cложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный).


import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support.ui import Select

def db_create():
    db_client = MongoClient('localhost', 27017)
    mongo_db = db_client['email_db']
    try:
        collection = mongo_db.create_collection('email')
    except BaseException:
        collection = mongo_db.email
    return collection

mail_user_name = input('Login: ')
mail_user_pass = input('Password: ')
url = 'https://mail.ru'

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get(url)

def look_mail(collection):
    login = driver.find_element_by_name('login')
    login.send_keys(mail_user_name)
    login.send_keys(Keys.ENTER)
    time.sleep(3)

    password = driver.find_element_by_name('password')
    password.send_keys(mail_user_pass)
    password.send_keys(Keys.ENTER)

    links = set()
    time.sleep(3)
    email_list = driver.find_elements_by_class_name(
        'js-tooltip-direction_letter-bottom')
    link_list = list(map(lambda el: el.get_attribute('href'), email_list))
    links = links.union(set(link_list))


    while True:
        actions = ActionChains(driver)
        actions.move_to_element(email_list[-1])
        actions.perform()
        email_list = driver.find_elements_by_class_name(
            'js-tooltip-direction_letter-bottom')
        link_list = list(map(lambda el: el.get_attribute('href'), email_list))

        if link_list[-1] not in links:
            links = links.union(set(link_list))
            continue
        else:
            break

    for href in list(links):
        driver.get(href)
        time.sleep(3)
        email_for_db = {
            'from': driver.find_element_by_class_name('letter-contact').get_attribute('title'),
            'title': driver.find_element_by_xpath('//h2').text,
            'body': driver.find_element_by_class_name('letter-body').text,
            'date': driver.find_element_by_class_name('letter__date').text}
        try:
            collection.insert_one(email_for_db)

        except BaseException:
            continue


start_time = time.time()
look_mail(db_create())
print("--- %s seconds ---" % round(( time.time() - start_time), 3))
print('---------EOF---------')














