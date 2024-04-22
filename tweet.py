from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time
import pymongo
import sys
sys.stdout.reconfigure(encoding='utf-8')

username = input("input username :")
password = input ("input password : ")

PriceList=[]
comment_set = {}
browser = webdriver.Chrome()

url="https://twitter.com/i/flow/login"


search_User = input("Search Product :")

browser.get(url)

browser.implicitly_wait(30)
SearchElement = browser.find_element(By.NAME, 'text')  
SearchElement.send_keys(username +  Keys.RETURN)

browser.implicitly_wait(30)
SearchElement1 = browser.find_element(By.NAME, 'password')  
SearchElement1.send_keys(password +  Keys.RETURN)

browser.implicitly_wait(10)
searchUser = browser.find_element(By.CLASS_NAME,'r-30o5oe')
searchUser.send_keys(search_User +  Keys.RETURN)
time.sleep(random.uniform(2,5))


browser.implicitly_wait(10)
FirstUserClick =  browser.find_element(By.CSS_SELECTOR, "[data-testid='UserCell']")  
FirstUserClick.click()
time.sleep(random.uniform(2,5))




browser.implicitly_wait(10)
clickPostComment =  browser.find_element(By.XPATH, "//div[@data-testid='tweetText']/span")   
clickPostComment.click()
time.sleep(random.uniform(2,5))

wait = WebDriverWait(browser,30)




for _ in range(10):  
    
    comment_elements = browser.find_elements(By.XPATH, "//div[@data-testid='tweetText']//span[@class='css-1qaijid r-bcqeeo r-qvutc0 r-poiln3']")
    
    for comment_element in comment_elements:
        PriceList.append({"comment": comment_element.text})
        if len(PriceList) == 100:
            break

    if len(comment_set) == 100:
            break   
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(1, 2)) 
    



print(f"Number of comments collected: {len(PriceList)}")

comments = [item["comment"] for item in PriceList]

comment_set = set(comments)

print(f"Number of comments collected: {len(comment_set)}")





print(PriceList)
   

try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['amazon_data']
    collection = db[search_User]
    for i in comment_set:
         collection.insert_one({"comments":  i})
    print(f"Inserted {len(comment_set)} records into the collection {search_User}")
except Exception as e:
    print("An error occurred while inserting data into MongoDB:", e)





browser.quit()
