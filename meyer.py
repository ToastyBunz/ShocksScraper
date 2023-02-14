from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv(override=True)                    #for python-dotenv method

import requests
import json
import os 

HEADERS = {}
options = Options()
options.headless=False
# options.add_argument('--headless')
options.add_argument("--window-size=1920,1200")
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
s = requests.Session()
firstRun = True
def login() :
    # Login with the user session
    global HEADERS
    driver.get("https://online.meyerdistributing.com/public/login")
    username = driver.find_element(by=By.XPATH, value='//*[@id="username"]/input')
    username.send_keys(os.environ.get("MEYER_USER"))
    password = driver.find_element(by=By.XPATH, value='//*[@id="password"]/input')
    password.send_keys(os.environ.get("MEYER_PASS")+'\n')
    password.submit()
    # WebDriverWait(driver, 5)
    # driver.get("https://online.meyerdistributing.com/contact-us")
    loginCheckRequest = driver.wait_for_request("/api/user/v3/logged-in/")
    # if (loginCheckRequest.response.status_code != 200) :
    #     return {'error': 'Login failed, check credentials'}
    #print(loginCheckRequest.headers)
    HEADERS = loginCheckRequest.headers
    
    # Create a request interceptor
    def interceptor(request):
        del request.headers['Authorization']  # Delete the header first
        request.headers['Authorization'] = HEADERS["Authorization"]

    # Set the interceptor on the driver
    driver.request_interceptor = interceptor
    cookies = driver.get_cookies()
    
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    return {}

'''
    
    password = driver.find_element(by=By.ID, value='dnn_ctr_Login_Login_DNN_txtPassword')
    password.send_keys(os.environ.get("BILSTEIN_PASS"))
    loginButton = driver.find_element(by=By.ID, value='dnn_ctr_Login_Login_DNN_cmdLogin')
    loginButton.click()
    expectedUrl = "https://cart.bilsteinus.com"
    # TODO wait for redirect?
'''

def search(partNumber):
    global firstRun
    if(firstRun) : 
        loginReturnVal = login()
        if ("error" not in loginReturnVal.keys()):
            firstRun = False
        else:
            return loginReturnVal
    print(
        "Searching Meyer for " + partNumber
    )
    print(HEADERS['Authorization'])
    searchRequest = s.get('https://online.meyerdistributing.com/api/search/autocomplete/parts?search=' + partNumber, headers=HEADERS)
    if(searchRequest.status_code != 200) :
        print(searchRequest.status_code)
        return {"error": "{}: Part number search request failed".format(searchRequest.status_code)}
    search = searchRequest.json()
    print(search)
    if ((not isinstance(search, list)) or len(search) == 0) :
        return error("No results")
    #search should be a array
    #TODO check size
    # if (len(search) == 0) :
        
    print(search[0])
    bestMatch=search[0]
    urlValue = bestMatch.get("urlValue")

    partRequest = s.get('https://online.meyerdistributing.com/api/part/inquiry/'+ urlValue, headers=HEADERS)

    partDetails = partRequest.json().get("details")
    price = partDetails.get("customerPrice")
    stock = partDetails.get("totalStock")

    return {
        'distributor': "Meyer",
        'price': str(price),
        'stock': str(stock),
        'link': 'https://online.meyerdistributing.com/parts/details/' + urlValue
    }
def error(message) :
    print("Meyer Error:", message)
    return {"error": message, 'distributor': "Meyer"}
def cleanup() :
    driver.quit()
#loginMeyer()
#searchMeyer("123")
#searchBilstein("CC-11125")

