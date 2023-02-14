from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from json.decoder import JSONDecodeError
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv(override=True)                    #for python-dotenv method

import requests
import json
import os 

URL = "https://cart.bilsteinus.com/details?id=300287396269458499"
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1200")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
s = requests.Session()
loggedin = False
firstRun = True

def login() :
    global loggedin
    global driver
    if (loggedin) :
        return
    # Login with the user session

    driver.get("https://cart.bilsteinus.com/Login")

    username = driver.find_element(by=By.ID, value='dnn_ctr_Login_Login_DNN_txtUsername')
    username.send_keys(os.environ.get("BILSTEIN_USER"))
    password = driver.find_element(by=By.ID, value='dnn_ctr_Login_Login_DNN_txtPassword')
    password.send_keys(os.environ.get("BILSTEIN_PASS"))
    loginButton = driver.find_element(by=By.ID, value='dnn_ctr_Login_Login_DNN_cmdLogin')
    loginButton.click()
    expectedUrl = "https://cart.bilsteinus.com"
    actualUrl = driver.current_url
    if (expectedUrl == actualUrl) :
        loggedin = True
    # TODO wait for redirect?
    cookies = driver.get_cookies()
    
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    loginCheck = s.get("https://cart.bilsteinus.com/Account/Customer-Price", allow_redirects=False)
    if (loginCheck.status_code != 200):
        loggedin = False
        return {'error': 'Login failed, check credentials'}
    return {}

def search(partNumber):
    global firstRun
    if(firstRun) : 
        loginReturnVal = login()
        if ("error" not in loginReturnVal.keys()):
            firstRun = False
        else:
            return loginReturnVal
    print(
        "Searching Bilstein for " + partNumber
    )
    print()
    r = s.post('https://cart.bilsteinus.com/API/Exchange/ProductService/GetProductsByPartNumber?partNumber=' + partNumber,
            data='{"ItemNumber":"'+partNumber+'"}',
            )
    print(r.status_code)
    # TODO status code check
    if (r.status_code != 200):
        print("Bilstein server error {}".format(r.status_code))
        return {'error': 'Server error {} on part search'.format(r.status_code)}
    try:
        print(r.json())
        products = json.loads(r.json()).get("Products")
    except JSONDecodeError as e:
        return {'error': 'Invalid part number'}
    if(not "Product" in products.keys()) :
        print("No results found for "+partNumber)
        return {'error': 'No results'}
    productList = products.get("Product")
    if(len(productList) > 1) :
        print("Duplicate products for this part number")
        return {
            'error': "Duplicate products for this part number"
        }
    product = productList[0]
    itemId = product.get("ItemId")

    r = s.post('https://cart.bilsteinus.com/API/Exchange/UserService/ProductPriceLookupByRole',
            data='{"ItemId":"'+itemId+'"}',
            )
    if (r.status_code != 200) :
        return {'error': "Price search error {}".format(r.status_code)}
    # TODO status code check
    print(r.json())
    prices = json.loads(r.json()).get("Prices").get("PriceList")
    if(len(prices)!= 1) :
        print("No price reported")
        return {'error': "Price list did not have exactly one element"}
    customerPrice = prices[0].get("CustomerPrice")
    print("Bilstein")
    print(customerPrice)
    inventory = product.get("Inventory")
    available = '0'
    if(len(inventory) == 0) :
        available = 'Unavailable'
    else :
        inventoryTotal = 0
        for warehouse in inventory :
            
            available = warehouse.get("Available")
            try:
                count = int(available)
                inventoryTotal += count
            except ValueError:
                continue
        #TODO add all warehouses
    print(available)
    link = "https://cart.bilsteinus.com/details?id="+itemId
    print(link)
    print()
    return {
        'distributor': "Bilstein",
        'price': str(customerPrice),
        'stock': str(available),
        'link': link
    }
def cleanup() :
    driver.quit()
#loginBilstein()
#searchBilstein("BIL33-225487")
#searchBilstein("CC-11125")

