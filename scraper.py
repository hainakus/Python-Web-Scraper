import time
import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import re

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Continente"]

dblist = client.list_database_names()
if "Continente" in dblist:
  print("The database exists.")

events_collection = db['products']
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(10)
cats = ['Mercearia', 'bio-saudavel']
for cat in cats:
    url_scrape = 'https://www.continente.pt/stores/continente/pt-pt/public/Pages/category.aspx?cat=' + cat + '(eCsf_WebProductCatalog_MegastoreContinenteOnline_Continente_EUR_Colombo_PT)'
    driver.get(url_scrape)
    elem = driver.find_element_by_css_selector('div.categoryContent.collapse-expand.collapse-expand-item')
    html = driver.execute_script("return arguments[0].innerHTML;", elem)
        #pass the HTML to Beautifulsoup.
    soup = BeautifulSoup(html,'html.parser')
        #get the HTML of the table called site Table where all the links are displayed
    cards = soup.find_all('div', {'class': 'productBoxTop'})
    for card in cards:
        if card:
            image = card.img.get('src')
            title = card.select_one('div.title a.ecsf_QuerySuggestions').text
            brand = card.select_one('div.type').text
            description = card.select_one('div.containerDescription div.subTitle').text
            price = card.select_one('div.standardPriceContainer-selector div.priceFirstRow').text
            unity_price = card.select_one('div.standardPriceContainer-selector div.priceSecondRow').text
            x = events_collection.insert_one({'image': image, 'title':title, 'brand': brand, 'description': description, 'price': price, 'unity_price': unity_price})

            #print list of the _id values of the inserted documents:
        print(x.inserted_id)
    clickable = driver.find_element_by_css_selector('.next')
    driver.execute_script("arguments[0].scrollIntoView();", clickable)
    clickable.click()
    for x in range(84):
        
        
        elem = driver.find_element_by_css_selector('div.categoryContent.collapse-expand.collapse-expand-item')
        html = driver.execute_script("return arguments[0].innerHTML;", elem)
        #pass the HTML to Beautifulsoup.
        soup = BeautifulSoup(html,'html.parser')
        #get the HTML of the table called site Table where all the links are displayed
        cards = soup.find_all('div', {'class': 'productBoxTop'})
        for card in cards:
            if card:
                image = card.img.get('src')
                title = card.select_one('div.title a.ecsf_QuerySuggestions').text
                brand = card.select_one('div.type').text
                description = card.select_one('div.containerDescription div.subTitle').text
                price = card.select_one('div.standardPriceContainer-selector div.priceFirstRow').text
                unity_price = card.select_one('div.standardPriceContainer-selector div.priceSecondRow').text
                x = events_collection.insert_one({'category': cat ,'image': image, 'title':title, 'brand': brand, 'description': description, 'price': price, 'unity_price': unity_price})

                #print list of the _id values of the inserted documents:
            print(x.inserted_id)
        clickable = driver.find_element_by_css_selector('.next')
        driver.execute_script("arguments[0].scrollIntoView();", clickable)
        time.sleep(1)    
        clickable.click()
driver.quit()