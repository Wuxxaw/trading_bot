# -*- coding: utf-8 -*-
"""
Created on Wed May 27 20:16:36 2020

@author: wilso
"""


import hiddenInfo
import bs4
import requests
from bs4 import BeautifulSoup
import time, datetime
import pandas as pd #create dataframe
import numpy as np #arrays plus analysis
import matplotlib.pyplot as plt #data visualisation
import seaborn as sns #statistical data visualisation
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#%matplotlib inline

starttime=time.time()

sym=["TSLA"]#, "TSLA", "AV.L", "PTON", "ROKU"]
amount = 10

#Initiate web instance
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://demo.trading212.com")

username = driver.find_element_by_id("username-real")
password = driver.find_element_by_id("pass-real")
login = driver.find_element_by_xpath("/html/body/div[1]/section[2]/div/div[2]/div/form/input[4]")

username.clear()
sleep(0.2)
password.clear()
sleep(0.2)

username.send_keys(hiddenInfo.email)
sleep(0.5)
password.send_keys(hiddenInfo.pwd)
sleep(2)

login.click()
sleep(5)


#r=requests.get('https://uk.finance.yahoo.com/quote/')
#soup=bs4.BeautifulSoup(r.text,features="html.parser")
#price=soup.find_all('div',{'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
#return price

page_source = driver.page_source

soup = BeautifulSoup(page_source,features="html.parser")

#Extract first company name in watchlist
soup.find_all('div', {'class': 'tradebox-header'})[0].find('div', {'class': 'instrument-name'}).text

j = 0

while True:
    try:
        soup.find_all('div', {'class': 'tradebox-header'})[j].find('div', {'class': 'instrument-name'}).text
        j += 1
    except IndexError:
        print("Watchlist check, there are "+str(j)+" listings")
        break



#buy shares
#this needs changing to accommodate for Euro and GBP transactions
def buyShare(ticker):
    driver.find_element_by_xpath("//div[@class='invest-tradebox _focusable pretty-name-shown' and contains(@data-code, '" + ticker + "')]//*[@class='buy-button']").click()
    sleep(0.5)
    
    investOption = driver.find_element_by_xpath("//*[contains(@class, 'invest-by-content')]")
    investOption.click()
    sleep(0.5)
    
    investValue = driver.find_element_by_xpath("//*[contains(@class, 'item item-invest-by-items-value')]")
    investValue.click()
    sleep(0.5)
    
    clearZero = driver.find_element_by_xpath("//*[contains(@class, 'visible-input')]/input")
    clearZero.clear()
    sleep(0.5)
    
    enterValue = driver.find_element_by_xpath("//*[contains(@class, 'visible-input')]/input")
    enterValue.send_keys(str(value))
    sleep(0.5)
    
    reviewOrder = driver.find_element_by_xpath("//*[contains(@id,'uniqName') and contains(@class, 'custom-button review-order-button')]")
    reviewOrder.click()                                         
    sleep(1)
    buyOrder = driver.find_element_by_xpath("//*[contains(@id,'uniqName') and contains(@class, 'custom-button send-order-button')]")
    buyOrder.click()
    sleep(1)
    
    checkBought.loc[checkBought.Ticker == ticker, 'Bought'] = float(latestData['Price'][i])




#sell shares
def sellShare(ticker):
    driver.find_element_by_xpath("//div[@class='invest-tradebox _focusable pretty-name-shown' and contains(@data-code, '" + ticker + "')]//*[@class='sell-button']").click()
    sleep(0.5)
    
    investOption = driver.find_element_by_xpath("//*[contains(@class, 'invest-by-content')]")
    investOption.click()
    sleep(0.5)
    
    investValue = driver.find_element_by_xpath("//*[contains(@class, 'item item-invest-by-items-value')]")
    investValue.click()
    sleep(0.5)
    
    clearZero = driver.find_element_by_xpath("//*[contains(@class, 'visible-input')]/input")
    clearZero.clear()
    sleep(0.5)
    
    enterValue = driver.find_element_by_xpath("//*[contains(@class, 'visible-input')]/input")
    enterValue.send_keys(str(sellValue))
    sleep(0.5)
    
    reviewOrder = driver.find_element_by_xpath("//*[contains(@id,'uniqName') and contains(@class, 'custom-button review-order-button')]")
    reviewOrder.click()                                         
    sleep(1)
    sellOrder = driver.find_element_by_xpath("//*[contains(@id,'uniqName') and contains(@class, 'custom-button send-order-button')]")
    sellOrder.click()
    sleep(1)

    checkBought.loc[checkBought.Ticker == ticker, 'Bought'] = np.nan



#Extract first company share price in watchlist
#soup.find_all('div', {'class': 'tradebox-header'})[0].find('div', {'class': 'instrument-price'}).find_all('span')[2].text+soup.find_all('div', {'class': 'tradebox-header'})[0].find('div', {'class': 'instrument-price'}).find_all('span')[3].text


cols = ['Ticker', 'CompanyName', 'DateTime', 'Price']
df = pd.DataFrame(columns = cols)
latestData = pd.DataFrame(columns = cols)
dfBought = pd.DataFrame(columns = cols)
dfSold = pd.DataFrame(columns = cols)

#set values for loop
i = 0
value = 100 #spending on each trade, GBP
sellValue = 1000000 
pctDecChange = 99 #check for when the price decreases
pctIncChange = 101 #check for when the price increases
buyPrice = "" 


##Load dataframe first from pickle, then check if has any rows/columns?
##If below code is run from scratch, it will not know wheter any shares have currently been bought
#if checkBought is not None:
#    print("Already exists")
#else:
tickerList = []

now=datetime.datetime.now()
page_source = driver.page_source
soup = BeautifulSoup(page_source,features="html.parser")

for i in range(j):
    tickerListItem = soup.find_all('div', {'class': 'instrument-type-market'})[i].find_all('span')[0].text
    tickerList.append(tickerListItem)
    company = soup.find_all('div', {'class': 'tradebox-header'})[i].find('div', {'class': 'instrument-name'}).text
    price = soup.find_all('div', {'class': 'tradebox-header'})[i].find('div', {'class': 'instrument-price'}).find_all('span')[2].text.replace("\xa0","")+soup.find_all('div', {'class': 'tradebox-header'})[i].find('div', {'class': 'instrument-price'}).find_all('span')[3].text
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    ticker = soup.find_all('div', {'class': 'instrument-type-market'})[i].find_all('span')[0].text
    df = df.append({'Ticker': ticker, 'CompanyName': company, 'DateTime': time, 'Price': float(price)},ignore_index=True)
checkBought = pd.DataFrame({'Ticker' : tickerList, 'Bought' : np.nan})

while True:
    #i = 0
    now=datetime.datetime.now()
    page_source = driver.page_source
    soup = BeautifulSoup(page_source,features="html.parser")
    latestData = latestData.iloc[0:0]
    for i in range(j):
        company = soup.find_all('div', {'class': 'tradebox-header'})[i].find('div', {'class': 'instrument-name'}).text
        price = soup.find_all('div', {'class': 'tradebox-header'})[i].find('div', {'class': 'instrument-price'}).find_all('span')[2].text.replace("\xa0","")+soup.find_all('div', {'class': 'tradebox-header'})[i].find('div', {'class': 'instrument-price'}).find_all('span')[3].text
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        ticker = soup.find_all('div', {'class': 'instrument-type-market'})[i].find_all('span')[0].text
        df = df.append({'Ticker': ticker, 'CompanyName': company, 'DateTime': time, 'Price': float(price)},ignore_index=True)
        dfWeighted = ((df.tail(360*j).groupby('Ticker')[('Price')].max()*0.9).loc[tickerList]+(df.tail(360*j).groupby('Ticker')[('Price')].mean()*0.1).loc[tickerList]).to_frame(name = 'Price').reset_index()
        latestData = latestData.append({'Ticker': ticker, 'CompanyName': company, 'DateTime': time, 'Price': float(price)},ignore_index=True)
        pctDiff = latestData.loc[:,'Price':].div(dfWeighted.loc[:,'Price':]).mul(100)
        print(str(ticker)+": "+str(company)+" share price is "+price+ " at "+time)
        #if statement to check if buyShare function should be executed
        if pctDiff['Price'].iloc[i] < pctDecChange and np.isnan(checkBought['Bought'].iloc[i]):
            print("Buy Shares in " + ticker)
            buyShare(ticker)
            dfBought = dfBought.append({'Ticker': ticker, 'CompanyName': company, 'DateTime': time, 'Price': float(price)},ignore_index=True)
            #set checkBought as bought price for that ticker
        #else if value is not null
        elif ~np.isnan(checkBought['Bought'].iloc[i]):
            print("  Already holding shares in "+ticker)
        #else continue with while loop
        else:
            None
        
        if latestData['Price'][i] > checkBought['Bought'][i]*(pctIncChange/100) and ~np.isnan(checkBought['Bought'].iloc[i]):
            print("Sell Shares in " + ticker)
            sellShare(ticker)
            dfSold = dfSold.append({'Ticker': ticker, 'CompanyName': company, 'DateTime': time, 'Price': float(price)},ignore_index=True)
        #else if value is not null
        elif pctDiff['Price'].iloc[i] > pctIncChange and np.isnan(checkBought['Bought'].iloc[i]):
            None
            #print("  Not yet holding shares in "+ticker)
        #else continue with while loop
        else:
            None
        
    sleep(8)







##Check this code - make price float earlier on so it doesn't need to be changed every iteration
#df['Price'] = pd.to_numeric(df['Price'])
#df.groupby('Ticker')[('Price')].mean()


##added to code
#dfWeighted2 = ((df.tail(360*j).groupby('Ticker')[('Price')].max()*0.9)+(df.tail(360*j).groupby('Ticker')[('Price')].mean()*0.1)).to_frame(name = 'Price').reset_index()
#dfWeighted2 = dfWeighted2.set_index('Ticker')
#latestData['Price'] = pd.to_numeric(latestData['Price']) 
#latestData.loc[:,'Price':].div(dfWeighted2.loc[:,'Price':]).mul(100)

##use this code as a way to buy shares
##recreate buy and sell shares code
#driver.find_element_by_xpath("//div[@class='invest-tradebox _focusable pretty-name-shown' and contains(@data-code, '" + df['Ticker'].iloc[0] + "')]//*[@class='buy-button']").click()
    