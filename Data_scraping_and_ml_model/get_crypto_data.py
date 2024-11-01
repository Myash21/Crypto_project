import requests
import pandas as pd
from datetime import datetime
import numpy as np  # Import numpy for handling NaN values
import os

def fetch_crypto_data(crypto_pair, start_date):
    """
    Fetches daily historical data for a specified cryptocurrency pair from the CryptoCompare API.

    Parameters:
    - crypto_pair (str): Cryptocurrency pair in the format "BTC/USD".
    - start_date (str): Start date in "YYYY-MM-DD" format.

    Returns:
    - DataFrame: Contains Date, Open, High, Low, and Close prices.
    """
    # Convert start_date to UNIX timestamp
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
    # Parse crypto_pair into individual symbols (e.g., BTC/USD to BTC and USD)
    fsym, tsym = crypto_pair.split('/')

    # Define API endpoint and parameters
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        'fsym': fsym,
        'tsym': tsym,
        'limit': 2000, # max limit defined by cryptocompare api is 2000
        'toTs': start_timestamp
    }

    # Define the headers with your API key
    api_key = os.getenv("CRYPTO_API_KEY")
    headers = {'authorization': f'Apikey {api_key}'}

    # Send request to CryptoCompare API
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Check for errors in the API response
    if data['Response'] != 'Success':
        raise Exception("Error fetching data from CryptoCompare:", data['Message'])

    # Extract historical data and convert to DataFrame
    historical_data = data['Data']['Data']
    df = pd.DataFrame(historical_data)

    # Convert UNIX timestamp to datetime for readability
    df['time'] = pd.to_datetime(df['time'], unit='s')
    # Rename columns to match the desired format
    df.rename(columns={'time': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, inplace=True)
    # Select and order columns
    df = df[['Date', 'Open', 'High', 'Low', 'Close']]

    return df

def calculate_metrics(data, variable1, variable2):
    """
    Calculates historical and future metrics for a given DataFrame with cryptocurrency data.

    Parameters:
    - data (DataFrame): The historical cryptocurrency data containing 'Date', 'Open', 'High', 'Low', 'Close' columns.
    - variable1 (int): The look-back period for historical high and low metrics.
    - variable2 (int): The look-forward period for future high and low metrics.

    Returns:
    - DataFrame: The input DataFrame with added metric columns.
    """

    # Calculate historical high and low prices over the last `variable1` days
    data[f'High_Last_{variable1}_Days'] = data['High'].rolling(window=variable1, min_periods=1).max()
    data[f'Low_Last_{variable1}_Days'] = data['Low'].rolling(window=variable1, min_periods=1).min()

    # Calculate days since historical high and low
    data[f'Days_Since_High_Last_{variable1}_Days'] = data.apply(
        lambda row: (row['Date'] - data.loc[:row.name, 'Date'][data['High'][:row.name + 1] == row[f'High_Last_{variable1}_Days']].iloc[-1]).days
        if pd.notna(row[f'High_Last_{variable1}_Days']) else np.nan, axis=1
    )
    data[f'Days_Since_Low_Last_{variable1}_Days'] = data.apply(
        lambda row: (row['Date'] - data.loc[:row.name, 'Date'][data['Low'][:row.name + 1] == row[f'Low_Last_{variable1}_Days']].iloc[-1]).days
        if pd.notna(row[f'Low_Last_{variable1}_Days']) else np.nan, axis=1
    )

    # Calculate percentage difference from historical high and low
    data[f'%_Diff_From_High_Last_{variable1}_Days'] = (data['Close'] - data[f'High_Last_{variable1}_Days']) / data[f'High_Last_{variable1}_Days'] * 100
    data[f'%_Diff_From_Low_Last_{variable1}_Days'] = (data['Close'] - data[f'Low_Last_{variable1}_Days']) / data[f'Low_Last_{variable1}_Days'] * 100

    # Calculate future high and low prices over the next `variable2` days
    data[f'High_Next_{variable2}_Days'] = data['High'].shift(-variable2).rolling(window=variable2, min_periods=1).max()
    data[f'Low_Next_{variable2}_Days'] = data['Low'].shift(-variable2).rolling(window=variable2, min_periods=1).min()

    # Calculate percentage difference from future high and low
    data[f'%_Diff_From_High_Next_{variable2}_Days'] = (data['Close'] - data[f'High_Next_{variable2}_Days']) / data[f'High_Next_{variable2}_Days'] * 100
    data[f'%_Diff_From_Low_Next_{variable2}_Days'] = (data['Close'] - data[f'Low_Next_{variable2}_Days']) / data[f'Low_Next_{variable2}_Days'] * 100

    return data

def main():
    # Fetch initial cryptocurrency data
    data = fetch_crypto_data("BTC/USD", "2024-01-01")

    # Transform data: set date to datetime and calculate metrics
    data['Date'] = pd.to_datetime(data['Date'])
    variable1, variable2 = 7, 5  # Look-back and look-forward periods
    data = calculate_metrics(data, variable1, variable2)

    # Output transformed data
    print(data)
    # Optionally save data to CSV
    # data.to_csv("crypto_data1.csv", index=False)

if __name__ == "__main__":
    main()
