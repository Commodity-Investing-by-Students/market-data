'''
Created by Maximo Xavier DeLeon on 06/03/2021
'''
import json
import requests
import pandas as pd
import datetime

# NOTE this is very basic right now. I havent been able to get the futures data working

def get_quote(ticker,apiKey):
    endpoint  = 'https://api.tdameritrade.com/v1/marketdata/'+str(ticker)+'/quotes?apikey='+apiKey # create endpoint
    page = requests.get(url=endpoint) # get request using endpoint
    content_dict = (json.loads(page.content))[ticker]
    return content_dict
# example returned data
# {'assetType': 'EQUITY', 'assetMainType': 'EQUITY', 'cusip': '037833100', 'symbol': 'AAPL', 'description': 'Apple Inc. - Common Stock', 'bidPrice': 123.44, 'bidSize': 1300, 'bidId': 'Q', 'askPrice': 123.45, 'askSize': 1700, 'askId': 'K', 'lastPrice': 123.45, 'lastSize': 100, 'lastId': 'D', 'openPrice': 124.68, 'highPrice': 124.85, 'lowPrice': 123.13, 'bidTick': ' ', 'closePrice': 125.06, 'netChange': -1.61, 'totalVolume': 44810245, 'quoteTimeInLong': 1622738247320, 'tradeTimeInLong': 1622738246560, 'mark': 123.45, 'exchange': 'q', 'exchangeName': 'NASD', 'marginable': True, 'shortable': True, 'volatility': 0.015, 'digits': 4, '52WkHigh': 145.09, '52WkLow': 79.7325, 'nAV': 0.0, 'peRatio': 27.8877, 'divAmount': 0.88, 'divYield': 0.7, 'divDate': '2021-05-07 00:00:00.000', 'securityStatus': 'Normal', 'regularMarketLastPrice': 123.45, 'regularMarketLastSize': 1, 'regularMarketNetChange': -1.61, 'regularMarketTradeTimeInLong': 1622738246560, 'netPercentChangeInDouble': -1.2874, 'markChangeInDouble': -1.61, 'markPercentChangeInDouble': -1.2874, 'regularMarketPercentChangeInDouble': -1.2874, 'delayed': True, 'realtimeEntitled': False}

def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0

  
  # Also I am plannign on figuing out how to set start and stop dates for more reasonable bars 
def get_historical(ticker,parameters,apiKey):
    valid_period_types = ['day','month','year','ytd']
    valid_frequency_types = ['minute','daily','weekly','monthly']
    valid_periods= {'day': [1, 2, 3, 4, 5, 10],'month': [1, 2, 3, 6],'year': [1 , 2, 3, 5, 10, 15, 20],'ytd': [1]}
    valid_frequencies = {'minute': [1, 5, 10, 15, 30],'daily': [1],'weekly': [1],'monthly': [1]}


    #end_date = str(unix_time_millis(parameters['end_date']))
    #start_date = str(unix_time_millis(parameters['start_date']))

    periodType = parameters['periodType'] if parameters['periodType'] in valid_period_types else None
    frequencyType = parameters['frequencyType'] if parameters['frequencyType'] in valid_frequency_types else None

    if periodType is not None and frequencyType is not None: # check if the input period frequency and period types are valid

        period = parameters['period'] if int(parameters['period']) in valid_periods[periodType] else None
        frequency = parameters['frequency'] if int(parameters['frequency']) in valid_frequencies[frequencyType] else None

        if period is not None and frequency is not None: # check if the input period frequencies and periods are valid
            endpoint = 'https://api.tdameritrade.com/v1/marketdata/'+ticker+'/pricehistory?apikey='+apiKey+'&periodType='+periodType+'&period='+period+'&frequencyType='+frequencyType+'&frequency='+frequency #+'&endDate='+end_date+'&startDate='+start_date
            page = requests.get(url=endpoint)
            try:
                content_list = json.loads(page.content)
                df = pd.DataFrame(data=content_list['candles'],columns=['datetime', 'open', 'high', 'close', 'low', 'volume'])
                df.index = pd.to_datetime(df['datetime'],unit='ms')
                df = df.drop(['datetime'],axis=1)
                return df

            except json.decoder.JSONDecodeError:
                print('Error fetching historical data!')



    else: print('invalid period type and or frequency type')


historical_parameter_template = {
    'periodType': 'year',
    'period': '1',
    'frequencyType': 'daily',
    'frequency': '1'
}




API_KEY = '------'
ticker = 'AAPL'

print('Quote Example',get_quote(ticker,apiKey=API_KEY))
df = get_historical(ticker,historical_parameter_template,API_KEY)

