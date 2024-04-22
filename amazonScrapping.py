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


PriceList=[]
browser = webdriver.Chrome()

url="https://www.amazon.in/"
search = input("Search Product :")
browser.get(url)

browser.implicitly_wait(30)
SearchElement = browser.find_element(By.NAME, 'field-keywords')  # Find the search box
SearchElement.send_keys(search + Keys.RETURN)

browser.implicitly_wait(10)
FirstProduct = browser.find_element(By.CLASS_NAME,'s-product-image-container')
FirstProduct.click()
time.sleep(random.uniform(2,5))


browser.switch_to.window(browser.window_handles[1]) 


browser.implicitly_wait(10)
see_more_reviews_link = browser.find_element(By.XPATH, "//a[contains(text(),'See more reviews')]")
see_more_reviews_link.click()
time.sleep(random.uniform(2,5))


wait = WebDriverWait(browser,30)
comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"review-text")))
ratings = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,'review-rating')))


for comment, rating in zip(comments, ratings):
            PriceList.append({"comments": comment.text, "rating": rating.get_attribute('textContent')})


  

for _ in range(20):
    try:
        nextPage = browser.find_element(By.CLASS_NAME, "a-last")
        nextPage.click()
        time.sleep(random.uniform(2, 5))

        comments = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "review-text")))
        ratings = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'review-rating')))
        
        for comment, rating in zip(comments, ratings):
            PriceList.append({"comments": comment.text, "rating": rating.get_attribute('textContent')})
    except Exception as e:
        print("An error occurred:", e)
        break






print(PriceList)
try:
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client['amazon_data']
    collection = db[search]
    collection.insert_many(PriceList)
    print(f"Inserted {len(PriceList)} records into the collection '{search}'")
except Exception as e:
    print("An error occurred while inserting data into MongoDB:", e)



browser.quit()