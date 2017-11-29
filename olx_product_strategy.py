"""
Created on Sun Nov 26 13:32:40 2017

@author: Agus Velazquez
"""
#%%%%% IMPORTS %%%%%%%%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os 

#%%%%% DATA PREPROCESSING %%%%%%%
os.chdir('D:\Sistema\Santiago\Desktop\OLX')
category = pd.read_csv('category_data.csv')
item = pd.read_csv('item_data.csv')
item['first_reply_date'] = pd.to_datetime(item['first_reply_date'])
item['last_reply_date'] = pd.to_datetime(item['last_reply_date'])
item['date_live_nk'] = pd.to_datetime(item['date_live_nk'])
categories_item = item['category_sk'].str.split('|',expand = True)
item = pd.concat([item,categories_item[3],categories_item[4]], axis = 1)
item = item.rename(columns = {3:'l1_category',4:'l2_category'})
item['l1_category'] = pd.to_numeric(item['l1_category'])
item['l2_category'] = pd.to_numeric(item['l2_category'])

l1_category = category['category_sk'].str.split('|',expand = True)[3]
l1_category = pd.to_numeric(l1_category)
l1_category = pd.concat([l1_category, category['category_l1_name_en']], axis = 1).drop_duplicates([3], keep = 'last')


l2_category = category['category_sk'].str.split('|',expand = True)[4].fillna(0)
l2_category = pd.to_numeric(l2_category)
l2_category = pd.concat([l2_category, category['category_l2_name_en']], axis = 1).drop_duplicates([4], keep = 'last')


item['user_sk_encrypted'].nunique()


#%%%%%%%% PLOTS %%%%%%%%%
    #%% Rate of replies given by the seller    
    item2 = item[item.first_reply_date < '2017-09-17'] #date considerer to give a margin to the seller
    
    p = item2['successful_replies'] / item2['replies']
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    p.plot(kind = 'hist')
    ax1.set_xlabel('Succesfull_replies/Replies')
    ax1.set_ylabel('Items')
    #plt.yticks(y,item['listing_sk'])
    #%% Items antique
    x1 = pd.to_datetime(item['date_live_nk']) 
    x2 =  pd.to_datetime(item['last_reply_date'][3]) #Last day of analysis 21-09-2017
    ia = (x2 - x1).dt.days
    
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    x.plot(kind = 'hist')
    ax2.set_xlabel('Item Antique (in days)')
    ax2.set_ylabel('Items')
    ax2.set_title('Histogram : Intem Antiquity')
    #%% Items per user
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    item['user_sk_encrypted'].value_counts().plot(kind = 'hist')
    ax3.set_xlabel('Number of items per user')
    ax3.set_ylabel('Items')
    ax3.set_title('Items per Seller') 
    #%% Conversation relevance
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(111)
    item['average_conversation_length'].plot(kind = 'hist')
    ax4.set_xlabel('Average conversation length')
    ax4.set_ylabel('Items')
    ax4.set_title('Histogram : Average consertaion length per item')   
    #%% Intensity of replies per item
    # i = replies / item antique
    i = item[item.date_live_nk < '2017-09-21']['replies'] / ia[ia > 0]
    fig5 = plt.figure()
    ax5 = fig5.add_subplot(111)
    i.plot(kind = 'hist', bins = 20)
    ax5.set_xlabel('intensity = replies / item antiquity')  
    ax5.set_ylabel('Items')
    ax5.set_title('Histogram : Intensity of replies per item')  
#%% Ranking in one category
#example in category 16
item_rank = item[item['l1_category'] == 16]
