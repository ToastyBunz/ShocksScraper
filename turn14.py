from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv(override=True)                    #for python-dotenv method

import requests
import json
import os 
access_token = ''
options = Options()
options.add_argument('ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
s = requests.Session()
firstRun = True
def login() :
    # Login with the user session
    global access_token

    loginRequest = driver.get("https://turn14.com/index.php")
    try :
        username = driver.find_element(by=By.NAME, value='username')
    except NoSuchElementException as e:
        print("Cannot find username input for Turn14!")
        return {'error': 'Login failed, login page malformed'}
    username.send_keys(os.environ.get("TURN14_USER"))
    try :
        password = driver.find_element(by=By.NAME, value='password')
    except NoSuchElementException as e:
        print("Cannot find password input for Turn14!")
        return {'error': 'Login failed, login page malformed'}
    
    password.send_keys(os.environ.get("TURN14_PASS")+'\n')
    cookies = driver.get_cookies()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    loginCheckRequest = s.get('https://turn14.com/search/index.php')
    if (loginCheckRequest.status_code != 200) :
        return {'error': 'Login failed, check credentials'}
      
    apiTokenReturnVal = _updateAPIToken()
    if ("error" in apiTokenReturnVal.keys()) :
            return apiTokenReturnVal
    return {}
    



def _updateAPIToken() :
    tokenRequestBody = {
        "grant_type": "client_credentials",
        "client_id": os.environ.get("TURN14_CLIENT_ID"),
        "client_secret": os.environ.get("TURN14_CLIENT_SECRET")
    }
    tokenRequest = s.post("https://api.turn14.com/v1/token", tokenRequestBody);
    if(tokenRequest.status_code == 400) :
        return {'error':"Invalid Turn14 API credentials"}
    access_token = tokenRequest.json().get("access_token")
    #print(tokenRequest.json().get("access_token"))
    s.headers.update({'Authorization': "Bearer " + access_token})
    return {}

def refreshToken(r, *args, **kwargs):
    if r.status_code == 401:
        print("Fetching new token as the previous token expired")
        tokenUpdateResult = _updateAPIToken()
        if ("error" in tokenUpdateResult.keys()) :
            print(tokenUpdateResult)
        return s.send(r.request, verify=False)
    return r

def search(partNumber):
    global firstRun
    if(firstRun) : 
        loginReturnVal = login()
        if ("error" not in loginReturnVal.keys()):
            firstRun = False
        else:
            return loginReturnVal
    print(
        "Searching Turn14 for " + partNumber
    )
    searchRequest = s.get('https://turn14.com/ajax_scripts/vmm_autocomplete.php?action=partnumber&term=' + partNumber)
    if(searchRequest.status_code != 200) :
        return error("Part number search request failed, error " + str(searchRequest.status_code))
    print("search request text:", searchRequest.text)
    search = searchRequest.json()
    #search should be a array
    #TODO check size
    print("search", search)
    if ((not isinstance(search, list)) or len(search) == 0) :
        return error("No results")
    print(search[0])
    part = search[0].get("label")
    itemcode=search[0].get("itemcode")


    priceRequest = refreshToken(s.get("https://api.turn14.com/v1/pricing/"+itemcode))
    if(priceRequest.status_code != 200) :
        return error("Price Request Failed, error " + priceRequest.status_code);
    print(priceRequest.json())
    price = ''
    priceInfo = priceRequest.json()
    if("data" in priceInfo.keys()) :
        priceData = priceInfo.get("data")
        if ("attributes" in priceData.keys()) :
            priceAttributes = priceData.get("attributes")
            if ("purchase_cost" in priceAttributes.keys()) :
                price = str(priceAttributes.get("purchase_cost"))


    stockRequest = refreshToken(s.get("https://api.turn14.com/v1/inventory/"+itemcode))
    if(stockRequest.status_code != 200) :
        return error("Stock Request Failed, error " + stockRequest.status_code);
    print(stockRequest.json())
    stock = ''
    stockInfo = stockRequest.json()
    if("data" in stockInfo.keys()) :
        stockData = stockInfo.get("data")
        if ((not isinstance(stockData, list)) or len(stockData) == 0) :
            return error("No items returned in inventory check")

        if ("attributes" in stockData[0].keys()) :
            stockAttributes = stockData[0].get("attributes")
            if ("inventory" in stockAttributes.keys()) :
                inventory = stockAttributes.get("inventory")
                total = 0
                for location in inventory.keys() :
                    total += int(inventory[location])
                stock = str(total)

    # stock = driver.find_element(by=By.XPATH, value='//div[@data-itemcode="'+itemcode+'"]/div[2]/span[contains(@class,"stock-line")]')
    # stockline = stock.text #1457 In Stock (305 PA | 0 TX | 1152 NV)
    # price = driver.find_element(by=By.XPATH, value='//div[@data-itemcode="'+itemcode+'"]//span[contains(@class,"amount")]')
    # priceline = price.text[1:]
    return {
        'distributor': "Turn14",
        'price': price,
        'stock': stock,
        'link': 'https://turn14.com/search/index.php?vmmPart='+part
    }
def error(message) :
    print("Turn14 Error:", message)
    return {"error": message}
def cleanup() :
    driver.quit()
bs_1 = '24-238304'
bs_2 = '24-186728'
bs_3 = '47-310971'

ks_1 = '25001-397A'
fs_1 = '883-06-132'
#loginTurn14()
#searchTurn14(bs_1)
# searchTurn14(bs_2)
# searchTurn14(bs_3)
# searchTurn14(ks_1)
# searchTurn14(fs_1)


