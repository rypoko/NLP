### bbc.com article scraper
### runs in Spyder 4.2.5; Python 3.8.8

import sys

#path of wherever the chromedriver is located
sys.path.insert(0, r'C:\Users\ryanp\OneDrive\Documents\NIU\MST 691 Data Science Tools and Techniques\Code\chromedriver.exe')

import requests
import selenium.webdriver as webdriver
from bs4 import BeautifulSoup
import pandas as pd
from collections import OrderedDict
from bs4.element import Comment
import urllib.request
import time
from selenium.webdriver.chrome.options import Options

import os

#how to run using multiple URLs
#seed_urls = ['https://www.wired.com/category/business',
#             'https://www.wired.com/category/backchannel',
#             'https://www.wired.com/category/gear']

#pull webpage and make a soup object
page = requests.get('https://www.bbc.com/')
soup = BeautifulSoup(page.content, 'html.parser')

#%% Get all sub-links on page
#empty lists for using below
articles = []
hold_heads = []
headlines = []
hold_sub = []
sub_articles = []

#scrape all URLs on main part of page
for body in soup.find_all(class_="content"): 
    for link in body.find_all("a"):
        articles.append(link.get('href'))

#pull out only the article URLs, leaving the advertisment
#and other non-pertinent links
for story in articles: 
    if "news" in story:
        hold_sub.append(story)

#remove duplicates by creating dictionary then 
#convert back to list; keeps order v set limitations
sub_articles = list(OrderedDict.fromkeys(hold_sub)) 

#grabbing all the headlines
for title in soup.find_all("h3"): 
    hold_heads.append(title.get_text().strip('\n'))
headlines = list(OrderedDict.fromkeys(hold_heads))

#add prefix to articles for use in later function using concatenation
for i in range(len(sub_articles)): 
    if "bbc.com" in sub_articles[i]:
        continue
    else:    
        sub_articles[i] = 'https://www.bbc.com' + sub_articles[i]

#%% headless browser and scrolling function
def get_html_scroll(url):
    
    options = Options()
    options.headless = True
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    chrome_driver = r'C:\Users\ryanp\OneDrive\Documents\NIU\MST 691 Data Science Tools and Techniques\Code\chromedriver.exe'
    browser = webdriver.Chrome(chrome_driver, options = options)
    browser.get(url)
    
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(4)
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            time.sleep(4)
            match=True
    post_elms = browser.page_source
    return post_elms

#%% Scrape sub-links content
def build_dataset (sub_articles):
    article_data = []
    
    for url in sub_articles:
        data = get_html_scroll(url)        
        soup = BeautifulSoup(data, 'html.parser')
        text = []
        for paragraph in soup.find_all('p'):
            text.append(paragraph.get_text())
        
        news_articles = [{'article_headline': soup.find('h1').string,
                          'article_contents': text}]
        article_data.extend(news_articles)
    df = pd.DataFrame(article_data)
    df = df[['article_headline', 'article_contents']]
    return df

#%% run program
news_df = build_dataset(sub_articles[:5])
news_df.head(3)







