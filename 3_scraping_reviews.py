# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import requests
import re

"""
3e ETAPE : Scraping Reviews

15sec 10review
1500sec 1000rev
6000sec 4000rev  == 1h36
"""
"""
Logiquement faisable avec seulement beautifullsoup
seuf que pb de langue 
donc selenium
"""


def scraping_review_by_review_url(url_review,username,user_list,rate_list,review_list,title_list,url_hotel_list):
    review_div_class = "featured-review-container"
    title_class = "title"
    review_text_class = "entry"
    url_hotel_div_class = "altHeadInline"
    url_prefix = "https://www.tripadvisor.fr"
    
    driver.get(url_review)
    time.sleep(1)
    soup_ = BeautifulSoup(driver.page_source,'lxml')
    review_div= soup_.find('div',class_=review_div_class)
    title = review_div.find('h1',class_=title_class).text
    review_text = review_div.find('div',class_=review_text_class).text
    review_text = review_text.replace('\t', ' ').replace('\n', ' ')
    rate = int(review_div.find('span',class_="ui_bubble_rating")['class'][1].split('bubble_')[1])/10
    url_hotel = review_div.find('div',class_=url_hotel_div_class).find('a')['href']
    title_list.append(title)
    review_list.append(review_text)
    rate_list.append(rate)
    user_list.append(username)
    url_hotel_list.append(url_prefix+url_hotel)        
        
        

def create_csv_review(filename,user_list,url_hotel_list,rate_list,title_list,review_list):
    df = pd.DataFrame({"username":user_list,"rate":rate_list,"title":title_list,"review":review_list,"url_hotel":url_hotel_list})    
    df = df.drop_duplicates()
    df.to_csv(filename, index = False, header=True,encoding='utf-8-sig')




if __name__ == '__main__':
    
    driver = webdriver.Firefox()
    df_url_reviews = pd.read_csv('reviews_url.csv')
    rate_list, review_list, title_list, url_hotel_list,  user_list = [], [], [], [], []
    try:
        #for i in range(45,55):
        for i in range(df_url_reviews.shape[0]):
            username = df_url_reviews.username[i]
            url_review_to_scrap = df_url_reviews.url_review[i]
            print(str(i)+ " "+ url_review_to_scrap)
            try:
                scraping_review_by_review_url(url_review_to_scrap,username,user_list,rate_list,review_list,title_list,url_hotel_list)
            except:
                print("ERREUR durant le scraping de "+ url_review_to_scrap +"  DE  "+ username )
        create_csv_review("reviews3.csv",user_list,url_hotel_list,rate_list,title_list,review_list)
    except:
        print("\n\nInterruption manuelle ou autre problème rencontré..")
        print("REVIEW URL en cours de traitement :  ", url_review_to_scrap)
        create_csv_review("reviews2.csv",user_list,url_hotel_list,rate_list,title_list,review_list)
        
            


