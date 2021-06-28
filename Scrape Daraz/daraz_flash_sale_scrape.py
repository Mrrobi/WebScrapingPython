from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("--headless")
  
#url of the page we want to scrape
url = "https://www.daraz.com.bd/wow/i/bd/landingpage/flash-sale?"
  
# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome('E:\Robiuddin-PC\PythonWorkbook\Web Scrapping Python\Scrape Daraz\driver\chromedriver.exe',options=options) 
driver.get(url) 
  
# this is just to ensure that the page is loaded
time.sleep(5) 
  
html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

unitContent = soup.find_all('div',{"class":"unit-content"})

print(len(unitContent))
productTitle = []
productPrice = []
productStatus = []



for unit in unitContent:
    product = unit.find_all('div',{"class":["sale-title","sale-price","pg-text"]})
    if(len(product)==3 and product[1].text != "৳? ? ?"):
        productTitle.append(product[0].text)
        productPrice.append(product[1].text)
        productStatus.append(product[2].text)
    elif(len(product)==2 and product[1].text != "৳? ? ?"):
        productTitle.append(product[0].text)
        productPrice.append(product[1].text)

details = ["Title", "Discounted Price", "Status"]
rows = []

for x in range(len(productTitle)):
    rows.append([])
    rows[x].append(productTitle[x])
    rows[x].append(productPrice[x])
    if(len(productStatus)>x):
        rows[x].append(productStatus[x])
    else:
        rows[x].append("None")

data = pd.DataFrame(rows)
data = pd.DataFrame(data.values,columns = details)


if(os.path.isfile("daraz-flash-sell-data.csv")):
    old_data = pd.read_csv('daraz-flash-sell-data.csv')
    new_data = pd.concat([data,old_data],axis=0)
    new_data = new_data.drop_duplicates()
    new_data.to_csv("daraz-flash-sell-data.csv",index=None)
else:
    data.to_csv("daraz-flash-sell-data.csv",index=None)