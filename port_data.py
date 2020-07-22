import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import math 
import scipy.optimize as spo 

from util import get_data, plot_data, normalize_data

# get daily returns for each ticker
def get_daily_returns(df):
	daily_returns = df.copy() 
	# from row 1 onwards and all columns equalds 
	# each row divided by each row values - 1
	daily_returns[1:] = (df[1:]/df[:-1].values)-1
	# no data prior to row[0] so set it = 0
	daily_returns.loc[daily_returns.index[0]] = 0 
	return daily_returns

# Get cumulative returns of port
def get_cum_ret(total_port):
	return total_port.loc[total_port.index[-1]]/total_port.loc[df.index[0]] -1

# Get average daily returns
def get_avg_daily_ret(daily_ret):
	return daily_ret.mean()

# Get sharpe ratio (risk adjusted returns)
def get_sharpe(alloc, df, principal):
	# multiplier depends on the frequency of samples
	# calculations below are for daily samples

	# provide allocation between each symbol 
	# calculate the total portfolio value and daily pct change in port val
	pos_vals = normalize_data(df)*alloc*principal
	port_val = pos_vals.sum(axis=1)
	daily_port_ret, daily_port_ret.loc[daily_port_ret.index[0]] = port_val.pct_change(), 0
	return -math.sqrt(252)*(daily_port_ret.mean()/daily_port_ret.std())

def optimize(df, principal, symbols, alloc):
	# set bounds and constraints for minimizer
	# namely sum to 1.0 and each alloc <= 1.0 but >= 0.0
	bound = (0.0,1.0)
	bounds = tuple(bound for asset in range(len(symbols)))
	arg = (df, principal)
	constraint = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

	# minimize get_sharpe given bounds, arg, constraint
	optimum_alloc = spo.minimize(get_sharpe, alloc, args=arg, method='SLSQP', bounds=bounds, constraints=constraint, options={'disp':True})

	# create new dataframe for allocations
	# round up as a percentage as function returns too many sfs
	rounded_optimum_alloc = pd.DataFrame(optimum_alloc.x, index=df.columns, columns=['allocation'])
	rounded_optimum_alloc.loc[:, 'allocation'] = [round(i*100,2)for i in rounded_optimum_alloc.loc[:, 'allocation']]
	
	return rounded_optimum_alloc

def main():
	# choose tickers and allocation of each ticker respectively
	symbols = ['SPX', 'AAPL', 'MSFT', 'GLD', 'GOOG']
	alloc = [0.2, 0.2, 0.2, 0.2, 0.2]
	principal = 50000
	df = get_data(symbols, 2)

	print(optimize(df, principal, symbols, alloc))

	
	

if __name__ == '__main__':
	main()