from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

import requests
import json
import os 

HEADERS = {}
options = Options()
options.headless=False
#options.add_argument('--headless=false')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
s = requests.Session()
def loginTurn14() :
    # Login with the user session
    global HEADERS
    driver.get("https://turn14.com/index.php")
    username = driver.find_element(by=By.NAME, value='username')
    username.send_keys(os.environ.get("TURN14_USER"))
    password = driver.find_element(by=By.NAME, value='password')
    password.send_keys(os.environ.get("TURN14_PASS")+'\n')
    cookies = driver.get_cookies()
    
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    

def searchTurn14(partNumber):
    print(
        "Searching Meyer for " + partNumber
    )
    searchRequest = s.get('https://turn14.com/ajax_scripts/vmm_autocomplete.php?action=partnumber&term=' + partNumber)
    if(searchRequest.status_code != 200) :
        return {"error": "Part number search request failed"}
    search = searchRequest.json()
    #search should be a array
    #TODO check size
    print(search[0])
    part = search[0].get("label")
    itemcode=search[0].get("itemcode")
    parturl = 'https://turn14.com/search/index.php?vmmPart='+part
    driver.get(parturl)

    stock = driver.find_element(by=By.XPATH, value='//div[@data-itemcode="'+itemcode+'"]/div[2]/span[contains(@class,"stock-line")]')
    stockline = stock.text #1457 In Stock (305 PA | 0 TX | 1152 NV)
    price = driver.find_element(by=By.XPATH, value='//div[@data-itemcode="'+itemcode+'"]//span[contains(@class,"amount")]')
    priceline = price.text
    return {
        'distributor': "Turn14",
        'price': priceline,
        'stock': stockline,
        'link': parturl
    }

loginTurn14()
searchTurn14("24-238304")
#searchBilstein("CC-11125")

