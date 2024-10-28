import requests
import pandas as pd
from datetime import datetime
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
    # Convert start_date to timestamp
    start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())

    # Parse crypto_pair into individual symbols
    fsym, tsym = crypto_pair.split('/')

    # Define API endpoint and parameters
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        'fsym': fsym,            # From symbol
        'tsym': tsym,            # To symbol
        'limit': 2000,           # Max days to fetch in one request
        'toTs': start_timestamp  # End timestamp (fetches data from start date onward)
    }

    # API Key (register at CryptoCompare to get one if required)
    api_key = os.getenv("CRYPTO_API_KEY")
    headers = {
        'authorization': f'Apikey {api_key}'
    }

    # Send request
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Check for errors in response
    if data['Response'] != 'Success':
        raise Exception("Error fetching data from CryptoCompare:", data['Message'])

    # Extract data
    historical_data = data['Data']['Data']
    # Convert to DataFrame
    df = pd.DataFrame(historical_data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={'time': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close'}, inplace=True)
    df = df[['Date', 'Open', 'High', 'Low', 'Close']]

    return df

def main():
    print(fetch_crypto_data("BTC/USD", "2024-10-29"))

if __name__ == "__main__":
    main()