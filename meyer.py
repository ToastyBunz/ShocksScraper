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

URL = "https://cart.bilsteinus.com/details?id=300287396269458499"
HEADERS = {}
options = Options()
options.headless=False
#options.add_argument('--headless=false')
options.add_argument("--window-size=1920,1200")
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
s = requests.Session()
def loginMeyer() :
    # Login with the user session
    global HEADERS
    driver.get("https://online.meyerdistributing.com/public/login")
    username = driver.find_element(by=By.XPATH, value='//*[@id="username"]/input')
    username.send_keys(os.environ.get("MEYER_USER"))
    password = driver.find_element(by=By.XPATH, value='//*[@id="password"]/input')
    password.send_keys(os.environ.get("MEYER_PASS")+'\n')
    password.submit()
    loginCheckRequest = driver.wait_for_request("/api/user/v3/logged-in/")
    #print(loginCheckRequest.headers)
    HEADERS = loginCheckRequest.headers
    #print(HEADERS)
    # Create a request interceptor
    def interceptor(request):
        del request.headers['Authorization']  # Delete the header first
        request.headers['Authorization'] = HEADERS["Authorization"]

    # Set the interceptor on the driver
    driver.request_interceptor = interceptor
    cookies = driver.get_cookies()
    
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])

'''
    
    password = driver.find_element(by=By.ID, value='dnn_ctr_Login_Login_DNN_txtPassword')
    password.send_keys(os.environ.get("BILSTEIN_PASS"))
    loginButton = driver.find_element(by=By.ID, value='dnn_ctr_Login_Login_DNN_cmdLogin')
    loginButton.click()
    expectedUrl = "https://cart.bilsteinus.com"
    # TODO wait for redirect?
'''

def searchMeyer(partNumber):
    print(
        "Searching Meyer for " + partNumber
    )
    print(HEADERS['Authorization'])
    searchRequest = s.get('https://online.meyerdistributing.com/api/search/autocomplete/all?search=' + partNumber, headers=HEADERS)
    if(searchRequest.status_code != 200) :
        return {"error": "Part number search request failed"}
    search = searchRequest.json()
    #search should be a array
    #TODO check size
    print(search[0])
    bestMatch=search[0]
    urlValue = bestMatch.get("urlValue")

    partRequest = s.get('https://online.meyerdistributing.com/api/part/inquiry/'+ urlValue, headers=HEADERS)

    partDetails = partRequest.json().get("details")
    price = partDetails.get("customerPrice")
    stock = partDetails.get("totalStock")

    return {
        'distributor': "Meyer",
        'price': price,
        'stock': stock,
        'link': 'https://online.meyerdistributing.com/parts/details/' + partNumber
    }

    #driver.get('https://online.meyerdistributing.com/parts/search;search=' + partNumber)
       # TODO status code check
    '''
    products = json.loads(r.json()).get("Products")
    if(not "Product" in products.keys()) :
        print("No results found for "+partNumber)
        return
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
    # TODO status code check
    prices = json.loads(r.json()).get("Prices").get("PriceList")
    if(len(prices)!= 1) :
        print("No price reported")
        return
    customerPrice = prices[0].get("CustomerPrice")
    print("Bilstein")
    print(customerPrice)
    inventory = product.get("Inventory")
    available = '0'
    if(len(inventory) == 0) :
        available = 'Unavailable'
    else :
        available = inventory[0].get("Available")
    print(available)
    link = "https://cart.bilsteinus.com/details?id="+itemId
    print(link)
    print()
    return {
        'distributor': "Bilstein",
        'price': customerPrice,
        'status': available,
        'link': link
    }'''

loginMeyer()
#searchMeyer("123")
#searchBilstein("CC-11125")

