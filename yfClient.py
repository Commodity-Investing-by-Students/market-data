# Created by Maximo Xavier DeLeon on 06/03/2021
import yfinance as yf
import pandas as pd

# input a list of tickers alongside a start & stop date
# a dictionary of nested dataframes will be returned
# index the the price data for a ticker by using the desired ticker as a dictionary key
def get_close_prices_yahoo(tickers, start_date, stop_date):
  '''
  get close prices for securities listed in asset_list
  :param asset_list:
  :return:
  '''
  asset_dict = {}
  for asset in tickers:
    df = pd.DataFrame()
    current_asset = yf.Ticker(asset)
    ohclv_bars = current_asset.history(start=start_date, end=stop_date)
    asset_dict[asset] = ohclv_bars
  return asset_dict
