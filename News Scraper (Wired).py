# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 23:02:11 2021

@author: ryanp
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import OrderedDict
from bs4.element import Comment
import urllib.request

seed_urls = ['https://www.wired.com/category/business',
             'https://www.wired.com/category/backchannel',
             'https://www.wired.com/category/gear']

page = requests.get('https://www.wired.com/category/business/')
soup = BeautifulSoup(page.content, 'html.parser')
#%% Get all sub-links on page
articles = []
hold_heads = []
headlines = []
hold_sub = []
sub_articles = []
side_articles = []

for body in soup.find_all(class_="page-loader-component"): #scrape all URLs on main part of page
    for link in body.find_all("a"):
        articles.append(link.get('href'))

for story in articles: #get side articles
    if ".com/story" in story:
        side_articles.append(story)

for story in articles: #get rest of page articles
    if "story" in story:
        hold_sub.append(story)

for x in side_articles: #remove side articles from rest due to format
    hold_sub.remove(x)
    
sub_articles = list(OrderedDict.fromkeys(hold_sub)) #remove duplicates by creating dictionary then convert back to list; keeps order v set

for title in soup.find_all("h2"): #headlines
    hold_heads.append(title.get_text())
headlines = list(OrderedDict.fromkeys(hold_heads))

for i in range(len(sub_articles)): #add prefix to articles for use in function
    sub_articles[i] = 'https://www.wired.com' + sub_articles[i]
#%% Scrape sub-links content
def build_dataset (sub_articles):
    article_data = []
    for url in sub_articles:
        data = requests.get(url)
        soup = BeautifulSoup(data.content, 'html.parser')
        
        news_articles = [{'article_headline': soup.find('h1').string,
                          'article_contents': soup.find_all(class_='paywall')}]
        article_data.extend(news_articles)
        
    df = pd.DataFrame(article_data)
    df = df[['article_headline', 'article_contents']]
    return df

#%% run program
news_df = build_dataset(sub_articles)
news_df.head(10)

#%% trial of different method

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts) 
#%%

html = urllib.request.urlopen(sub_articles[1]).read()
print(text_from_html(html))
