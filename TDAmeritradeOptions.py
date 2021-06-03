'''
                    -TD Ameritrade Data Api-
get option chain data and (soon) live quotes of underlying security
Created by Maximo Xavier DeLeon 02/07/2021

06/03/2021 - When I origionally made this I was bored. Give me some time to add comments and create better documentation for this file.
'''

import json
import requests
import pandas as pd
import ast

API_KEY = '<TD Ameritrade API key here>'
option_params = {'symbol' : 'AAPL',
                 'contractType' : 'CALL',
                 'strikeCount' : '5',
                 'includeQuotes' : 'TRUE',
                 'strategy' : 'ANALYTICAL',
                 'interval' : '',
                 'strikePrice' : '137',
                 'range' : 'ALL',
                 'fromDate' : '',
                 'toDate' : '',
                 'volatility' : '',
                 'underlyingPrice' : '',
                 'interestRate' : '',
                 'daysToExpiration' : '',
                 'expMonth': '',
                 'optionType': ''}



class option_feed(object):
    def __init__(self, api_key):
        self.api_key = api_key # get the api from the user when declaring the object
        self.profile_dict = {} 

    def add_company_profile(self, profile_name, profile):
        self.profile_dict[profile_name] = profile

    def get_chain_from_profile(self, profile_name):
        if profile_name in self.profile_dict:
            return self.get_chain(self.profile_dict[profile_name])
        else:
            print(str(profile_name) + ' does not exist')
            return None

    def get_chain(self, data_params):
        endpoint = 'https://api.tdameritrade.com/v1/marketdata/chains?apikey={key}'
        endpoint = endpoint.format(key=self.api_key)
        for keys in data_params:
            if len(data_params[keys]) > 0:
                endpoint = endpoint + '&' + keys + '=' + data_params[keys]
            else:
                pass

        print(endpoint)
        page = requests.get(url=endpoint)
        try:
            content_dict = json.loads(page.content) # pull the data
            chain = content_dict
            option_list = []
            for keys in chain['callExpDateMap']:
                for morekeys in chain['callExpDateMap'][keys]:
                    option_data = str(chain['callExpDateMap'][keys][morekeys]).replace('[', '').replace(']','').replace( '\'', '"')
                    option_data = ast.literal_eval(option_data)
                    # print(keys + ' ' + morekeys + ' -> ' + str(option_data))
                    option_list.append(option_data)

            header_list = []
            for keys in option_list[0]:
                header_list.append(keys)
            df = pd.DataFrame(columns=header_list)
            for i in range(len(option_list)):
                df = df.append(option_list[i], ignore_index=True)
            df.index = df['daysToExpiration']

            return df

        except json.decoder.JSONDecodeError:
            print('Error fetching chain!')




if __name__ == "__main__":
    option_droid = option_feed(api_key=API_KEY)
    option_droid.add_company_profile(profile_name='MainApple',profile=option_params)
    print(option_droid.profile_dict)
    chain_df = option_droid.get_chain_from_profile(profile_name='MainApple')
    print(chain_df)
