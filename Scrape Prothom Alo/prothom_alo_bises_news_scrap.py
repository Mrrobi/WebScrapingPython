from requests.api import head
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import os

res = requests.get("https://www.prothomalo.com/topic/%E0%A6%AC%E0%A6%BF%E0%A6%B6%E0%A7%87%E0%A6%B7-%E0%A6%B8%E0%A6%82%E0%A6%AC%E0%A6%BE%E0%A6%A6")

soup = BeautifulSoup(res.text, 'lxml')

listDiv = soup.find_all('div',{"class":"customStoryCard9-m__story-data__2qgWb"})
print(len(listDiv))
heading = []
link = []
shortDet = []
for l in listDiv:
    heading.append(l.h2.text)
    link.append(l.a['href'])
    if(l.span):
        shortDet.append(l.span.text)
    else:
        shortDet.append("")

details = ["Link", "Heading", "Short Details"]
rows = []

for x in range(len(heading)):
    rows.append([])
    rows[x].append(link[x])
    rows[x].append(heading[x])
    rows[x].append(shortDet[x])

data = pd.DataFrame(rows)
data = pd.DataFrame(data.values,columns = details)


if(os.path.isfile("prothom-alo-bises-news-data.csv")):
    old_data = pd.read_csv('prothom-alo-bises-news-data.csv')
    new_data = pd.concat([data,old_data],axis=0)
    new_data = new_data.drop_duplicates()
    new_data.to_csv("prothom-alo-bises-news-data.csv",index=None)
else:
    data.to_csv("prothom-alo-bises-news-data.csv",index=None)
