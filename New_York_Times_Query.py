#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 21:29:38 2017

@author: caitlinshener
"""
#from nytimesarticle import articleAPI
import requests
import time
import csv


def parse_articles(articles):
    '''
    This function takes in a response to the NYT api and parses
    the articles into a list of dictionaries
    '''
    article_dicts = []
    for i in articles['response']['docs']:
        if(i['type_of_material'] != 'briefing'):
            temp_dict = {\
            'Source': 'New York Times', \
            'Date': i['pub_date'][0:10],\
            'Title':i['headline']['main'].encode('ascii', 'ignore'),\
            'Url': i['web_url'],\
            'Material_Type': i['type_of_material']} 
            article_dicts.append(temp_dict)
    return(article_dicts) 



#make a csv file 



#change this into a while loop and do it while the length of the response is 
#something 10? 
articles= []
i =0 
more= True
while(more): 
#for i in range(0,5): 
    
    address = "http://api.nytimes.com/svc/search/v2/articlesearch.json?q=sexual+harassment&begin_date=20171110&sort=oldest&api-key=<apikey>&page=" + str(i)
    r = requests.get(address)
    data = r.json()
   #if there are more articles to scrap 
    if (len(data["response"]["docs"]) >  0): 
        for p in parse_articles(data): 
             # add the dictionary to the list
            articles.append(p)
            time.sleep(2)
    #if there are not any more articles to scrape
    else: more = False 
    #this next line avoids rate limits - 100 pages 
    if(i>99): 
        print("rate exceeded")
        #if the rate is exceeded, I want to see the last one 
        print(articles[-1])
        more= False
    i+= 1
    

with open('sexualharrassment2.csv', 'w') as csvfile:
    fieldnames = ['Source', 'Date', 'Title', 'Url', 'Material_Type']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for a in articles: 
       writer.writerow(a)
        
    


