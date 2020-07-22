import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
from datetime import datetime
import os

def get_symbol_path(symbol, base_dir='data'):
	return os.path.join(base_dir, '{}.csv'.format(str(symbol)))

# get data from csv files given symbols and date_lookback in years
def get_data(symbols, date_lookback=3):

	# get end date (current date) and subtract by date_lookback
	# inefficient method of calculating dates
	if(date_lookback>0):
		end_date = datetime.today()
		start_date = datetime(end_date.year-date_lookback, end_date.month, end_date.day).strftime('%Y-%m-%d')
		end_date = end_date.strftime('%Y-%m-%d')
	else:
		print('Invalid Date Lookback Entered')

	dates = pd.date_range(start_date, end_date)
	df = pd.DataFrame(index=dates)

	if 'SPX' not in symbols:
		symbols.insert(0, 'SPX')

	for symbol in symbols:
		df_temp = pd.read_csv(get_symbol_path(symbol), index_col='Date',
			             parse_dates=True, usecols=['Date', 'Adj Close'], 
			             na_values=['Nan'])
		df_temp = df_temp.rename(columns={'Adj Close': symbol})
		df = df.join(df_temp)
		if symbol == 'SPX':
			df = df.dropna(subset=['SPX'])

	return df

def normalize_data(df):
	return df/df.loc[df.index[0]]

def plot_data(data, title="Portfolio Performance"):
	ax = plt.plot(data, title=title)
	ax.set_xlabel("Date")
	ax.set_ylabel("Price")
	
	plt.show()
 
