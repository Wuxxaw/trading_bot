# trading_bot
A bot that automatically buys and sells stocks and shares on Trading 212

## Project Aim

The aim of this project is to scrape live share price information from Trading 212, and build a bot to use this data to buy and sell shares - for a profit!

## How I will build this using Python!

The project code base will consist of 3(.5) core python packages

* BeautifulSoup - To scrape share price information on:
    * Share Price
    * Ticker
    * Company Name
* Selenium - To interact with a web browser
    * Log into Trading 212
    * Buy shares
    * Sell Shares
* Pandas & Numpy - To store, transform, and analyse the data

## Current algorithm for buying and selling shares

The maths is quite simple here, and follows a relatively straight forward algorithm with basic user input parameters.

parameters set by the user include:
* 'value' - the total value to be spent on each Buy
* 'pctDecChange' - what % decrease in price to automatically Buy at - this will be the BUY trigger
* 'pctIncChange' - what % increase in price to automatically Sell at - this will be the SELL trigger

For a single company:
1. Share Price information is scraped every 10 seconds, and held for 1 hour
2. Calculate difference between current share price and peak* share price value over the last 6 minutes
    * Peak = 90% of max share price + 10% of mean share price (over the last 6 minutes). This can be tuned in future
3. When difference between current and peak* share price is less than 'pctDecChange', BUY trigger will be activated
    * Once shares are bought, add ticker to a list of bought shares, and do not buy anymore of these until sold
4. When difference between current share price and the price it was bought at is greater than 'pctIncChange', SELL trigger will be activated
    * Once shares are sold, remove ticker from list of bought shares

## Chosen Shares

A user can feed a list of tickers into the script that will be tracked on T212. From testing, the ideal shares will be those with high volatility, as these are more likely to trigger the BUY and SELL functions. 

The current list only includes TSLA.


