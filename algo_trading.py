"""
This program will gather daily closing stock prices from the web API
Alphavantage. After gathering and appending new prices to the end of a
.csv file, three different trading strategies will be run for each stock
whose prices have been collected: simple moving average, mean reversion, and 
buy monday sell friday. The former two strategies will enable shorting. 
Results of each strategy will be saved to a json file. 
When applicable, a buy or sell signal will be reported for each stock for each
strategy on the last day of available data.
"""

import json #importing needed libraries
import requests
import time
import os
import datetime
import re


def get_data(ticker): #function to get/append data
    
    key1 = "Time Series (Daily)" #establish keys
    key2 = "4. close"
    
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=/"+ticker+"&outputsize=full&apikey=IL4XYW7MBBOAEL3S" #url w/ current ticker
    request = requests.get(url) #get data from url in json form
    time.sleep(12) #avoid too many requests to API
    rqst_dict = json.loads(request.text) #load json into dictionary
    
    if os.path.exists("/home/ubuntu/environment/final_project/data/"+ticker+".csv") == False: #if file does not exist...
        with open("/home/ubuntu/environment/final_project/data/"+ticker+".csv", "w") as file: #create new file
            file.write("Date," + ticker + " prices" + "\n") #header
            
            dates_prices = []
            for date in rqst_dict[key1]: #append dates and prices to list
                dates_prices.append(date + "," + rqst_dict[key1][date][key2] + "\n")
                
            dates_prices = dates_prices[::-1] #reverse list order
            file.writelines(dates_prices) #write list to file
    
    else: #if file exists, some data exists, so append new data
        with open("/home/ubuntu/environment/final_project/data/"+ticker+".csv", "r") as file:
            lines = file.readlines()
        last_date = lines[-1].split(",")[0] #get last date from file
        
        new_dates_prices = []
        for date in rqst_dict[key1]:
            if date == last_date: #add dates after latest date
                break
            new_dates_prices.append(date + "," + rqst_dict[key1][date][key2] + "\n")
            
               
        new_dates_prices = new_dates_prices[::-1] #reverse list
        with open("/home/ubuntu/environment/final_project/data/"+ticker+".csv", "a") as file:
            file.writelines(new_dates_prices) #write new dates to file
            
    
#defining simple moving average function

def simpleMovingAverageStrategy(prices):
    moving_avg = 0 #initializing variables
    total = 0
    first_buy = 0
    first_buy_tracker = 0
    buy = 0
    sell = 0
    trade_profit = 0
    total_profit = 0
    first_short = 0
    first_short_tracker = 0
    short_sell = 0
    short_buy = 0
    short_trade_profit = 0
    short_total_profit = 0
    short_position = 0
    
    for i in range(len(prices)):
        current_price = prices[i]
        if i >= 5:
            total += prices[i-1] #previous five days based on index values
            total += prices[i-2]
            total += prices[i-3]
            total += prices[i-4]
            total += prices[i-5]
            moving_avg = total/5
            total -= total #reset total for next iteration
            
            #logic for sma shorting
            
            if current_price < moving_avg and short_position == 0: #price going down, so short
                first_short_tracker += 1
                if first_short_tracker == 1: #track first short
                    first_short = current_price
                short_sell = current_price
                short_position = 1
                
                if i == len(prices) - 1: #check for last day
                    print("Short", ticker, "today for moving average shorting strategy.")
            
            elif current_price > moving_avg and short_position == 1: #price going up, so buy
                short_buy = current_price
                short_trade_profit = short_sell - short_buy
                short_total_profit += short_trade_profit
                short_position = 0
                
                if i == len(prices) - 1: #check for last day
                    print("Buy", ticker, "today for moving average shorting strategy.")
                
            #logic for normal sma trades
            
            if buy == 0: #if stock has not been purchased...
                if current_price > moving_avg: #if price is beginning up-trend...
                    first_buy_tracker += 1
                    
                    if first_buy_tracker == 1:#checking first buy and tracking it
                        first_buy = current_price
                    buy = current_price #track buy price
                    
                    if i == len(prices) - 1:
                        print("Buy", ticker, "today for moving average strategy.")
                        
                else: #if price is below 5-day average
                    pass
            
            elif current_price < moving_avg: #sell if price falls
                sell = current_price
                profit = sell - buy #find trade profit
                total_profit += profit #tracking total profit
                sell -= sell #resetting variables for next trade
                buy -= buy
                trade_profit -= profit
                
                if i == len(prices) - 1: #check for last day
                    print("Sell", ticker, "today for moving average strategy.")
                    
            else: #hold
                pass
            
    short_roi = round((short_total_profit/first_short) * 100, 2) #finding roi, formatting
    sma_roi = round((total_profit/first_buy) * 100, 2)
    short_total_profit = round(short_total_profit, 2)
    total_profit = round(total_profit, 2)
    return total_profit, sma_roi, short_total_profit, short_roi
    



# defining mean reversion function
    
def meanReversionStrategy(prices): #define function for mr strategy
    moving_avg = 0 #initializing variables
    total = 0
    first_buy = 0
    first_buy_tracker = 0
    buy = 0
    sell = 0
    trade_profit = 0
    total_profit = 0
    first_short = 0
    first_short_tracker = 0
    short_sell = 0
    short_buy = 0
    short_trade_profit = 0
    short_total_profit = 0
    short_position = 0
    
    for i in range(len(prices)): #loop to find moving average
        current_price = prices[i]
        if i >= 5: #on and after fifth day
            total += prices[i-1] #previous five days based on index values
            total += prices[i-2]
            total += prices[i-3]
            total += prices[i-4]
            total += prices[i-5]
            moving_avg = total/5
            total -= total #reset total for next iteration
            
            #logic for mr shorting
            
            if current_price > moving_avg * 1.02 and short_position == 0: #overpriced, so short
                first_short_tracker += 1
                if first_short_tracker == 1:
                    first_short = current_price
                short_sell = current_price
                # print("Sell at:", current_price)
                short_position = 1
                
                if i == len(prices) - 1: #check for last day
                    print("Short", ticker, "today for mean reversion shorting strategy.")
            
            elif current_price < moving_avg * .98 and short_position == 1: #underpriced, so buy
                short_buy = current_price
                short_trade_profit = short_sell - short_buy
                short_total_profit += short_trade_profit
                short_position = 0
                
                if i == len(prices) - 1: #check for last day
                    print("Buy", ticker, "today for mean reversion shorting strategy.")
            
            #logic for normal mr trades
            
            if buy == 0: #if the stock has not been purchased...
                if current_price < moving_avg * .98: #buy if price drops
                    first_buy_tracker += 1
                    
                    if first_buy_tracker == 1: #check for first buy
                        first_buy = current_price
                    buy = current_price
                    
                    if i == len(prices) - 1: #check for last day
                        print("Buy", ticker, "today for mean reversion strategy.")
                else:
                    pass
                    
            elif current_price > moving_avg * 1.02: #sell if price rises
                sell = current_price
                profit = sell - buy #find trade profit
                total_profit += profit #tracking total profit
                sell -= sell #resetting variables for next trade
                buy -= buy
                trade_profit -= profit
                
                if i == len(prices) - 1: #check for last day
                    print("Sell", ticker, "today for mean reversion strategy.")
            else:
                pass
            
    short_roi = round((short_total_profit/first_short) * 100, 2) #finding roi, formatting
    mr_roi = round((total_profit/first_buy) * 100, 2)
    short_total_profit = round(short_total_profit, 2)
    total_profit = round(total_profit, 2)
    return total_profit, mr_roi, short_total_profit, short_roi
    
    
def weekdayStrat(days_of_week, prices): #define monday friday strat
    total = 0
    first_buy = 0
    first_buy_tracker = 0
    buy = 0
    sell = 0
    trade_profit = 0
    total_profit = 0
    
    for i in range(len(prices)):
        current_price = prices[i]
        current_date = days_of_week[i]
        if current_date == 0 and buy == 0: #if weekday = monday and stock was sold last friday...
            first_buy_tracker += 1
            buy = current_price 
            
            if first_buy_tracker == 1: #check for first buy
                first_buy = current_price
                
            if i == len(prices) - 1: #check for last day
                print("Buy", ticker, "today for weekday strategy.")
            
            else:
                pass
                    
        elif current_date == 4 and buy != 0: #if weekday = friday and market was open monday...
            sell = current_price
            profit = sell - buy #find trade profit
            total_profit += profit #tracking total profit
            sell -= sell #resetting variables for next trade
            buy -= buy
            trade_profit -= profit
            
            if i == len(prices) - 1: #check for last day
                print("Sell", ticker, "today for weekday strategy.")
        else:
            pass
            
    roi = round((total_profit/first_buy) * 100, 2) #find percent return
    total_profit = round(total_profit, 2) #round total_profit for json file
    return total_profit, roi
        

def saveResults(results): #define function to save dictionary to json
    json.dump(results, open("/home/ubuntu/environment/final_project/results.json", "w"), indent=4) #save results to json w/ formatting


tickers = ["AAPL", "JPM", "PEP", "WMT", "MRNA", "RSG", "PG", "ZM", "NKE", "BA"] #list of tickers
results = {} #initialize results dictionary

for ticker in tickers:
    get_data(ticker) #get data for ticker
    with open("/home/ubuntu/environment/final_project/data/"+ticker+".csv", "r") as file:
        lines = file.readlines()
    prices = []
    days_of_week = []
    for line in lines:
        price = line.split(",")[1] #seperate prices
        date = line.split(",")[0] #seperate dates
        try: #error handling for headers
            prices.append(float(price)) #add prices to list
            day_of_week = datetime.datetime.strptime(date, '%Y-%m-%d').weekday() #convert strings to dates, find weekday
            days_of_week.append(day_of_week) #add dates to list
        except:
            pass
    
    smaResults = simpleMovingAverageStrategy(prices) #sma for current ticker
    results["%s_sma_profit" % (ticker)] = smaResults[0] #save profit to dictionary from tuple
    results["%s_sma_returns" % (ticker)] = smaResults[1] #save roi to dictionary from tuple
    results["%s_sma_shorting_profit" % (ticker)] = smaResults[2] #shorting profits/returns to dict
    results["%s_sma_shorting_returns" % (ticker)] = smaResults[3]
    
    mrResults = meanReversionStrategy(prices) #mr for current ticker
    results["%s_mr_profit" % (ticker)] = mrResults[0] #save profit to dictionary from tuple
    results["%s_mr_returns" % (ticker)] = mrResults[1] #save roi to dictionary from tuple
    results["%s_mr_shorting_profit" % (ticker)] = mrResults[2] #shorting profits/returns to dict
    results["%s_mr_shorting_returns" % (ticker)] = mrResults[3]
    
    weekdayResults = weekdayStrat(days_of_week, prices) #weekday for current ticker
    results["%s_weekdays_profit" % (ticker)] = weekdayResults[0] #save profit to dictionary from tuple
    results["%s_weekdays_returns" % (ticker)] = weekdayResults[1] #save roi to dictionary from tuple
    print()

high_profit = 0 #initialize vars to track high profit/roi
high_strat = 0
high_returns = 0
high_strat_returns = 0

for key in results:
    if re.search(".+profit", key): #search for "profit" in key
        if results[key] > high_profit:
            high_profit = results[key]
            high_strat = key
            
    else: #search for "returns" in key
        if results[key] > high_returns: 
            high_returns = results[key]
            high_strat_returns = key
   
print("Stock and strategy with highest profit: ", high_strat,", ", "${:,.2f}".format(high_profit), sep="") #report highest $ profit
print("Stock and strategy with highest roi: ", high_strat_returns,", ", high_returns, "%", sep="") #report highest % return

saveResults(results) #save results dict to json



