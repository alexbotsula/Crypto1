#%%

import os
import csv
import pytz
import pandas as pd
from datetime import datetime

#%%

from catalyst.api import record, symbol, symbols, get_orderbook
from catalyst.utils.run_algo import run_algorithm

#%%
def initialize(context):
    # Portfolio assets list
    context.asset = symbol('btc_usdt') # Bitcoin

    # Create an empty DataFrame to store results
    context.pricing_data = pd.DataFrame()

def handle_data(context, data):
    # Variables to record for a given asset: price and volume
    # Other options include 'open', 'high', 'open', 'close'
    # Please note that 'price' equals 'close'
    current = data.history(context.asset, ['volume', 'high', 'low', 'open', 'close'], 1, '1T')

    # Append the current information to the pricing_data DataFrame
    context.pricing_data = context.pricing_data.append(current)

def analyze(context=None, results=None):
    # Save pricing data to a CSV file
    filename = os.path.splitext(os.path.basename(__file__))[0]
    context.pricing_data.to_csv(filename + '.csv')

#%%
# year-month-day
start = datetime(2019, 2, 21, 0, 0, 0, 0, pytz.utc)
end = datetime(2020, 2, 22, 0, 0, 0, 0, pytz.utc)
results = run_algorithm(initialize=initialize,
                        handle_data=handle_data,
                        analyze=analyze,
                        start=start,
                        end=end,
                        exchange_name='binance',
                        data_frequency='minute',
                        quote_currency ='usdt',
                        capital_base=10000)

# %%
