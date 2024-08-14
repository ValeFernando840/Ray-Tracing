import numpy as np
import pandas as pd 

def get_dates(year):
  dates = pd.date_range(start = f'{year}-01-01', end = f'{year}-12-31')
  dates_str = dates.strftime('%d-%m-%Y').to_numpy()
  return dates_str

def save_dates(dates,year_save):
  year_save = str(year_save)
  df = pd.DataFrame(dates,columns=['Date'])
  name_csv ='dates'+ year_save + '.csv'
  df.to_csv('dataset/'+name_csv,index=False)
  return 0
data = save_dates(get_dates(2011),2011)



