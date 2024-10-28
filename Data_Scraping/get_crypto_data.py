import requests
import pandas as pd
from datetime import datetime

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
    api_key = "af387748d6eaba1f35e3d283cad9dcaf8dc7504039d637dc71fbcd9874bcd630"
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

    # Historical High and Low prices over the last `variable1` days
    data[f'High_Last_{variable1}_Days'] = data['High'].rolling(window=variable1, min_periods=1).max()
    data[f'Low_Last_{variable1}_Days'] = data['Low'].rolling(window=variable1, min_periods=1).min()

    # Days since Historical High and Low
    data[f'Days_Since_High_Last_{variable1}_Days'] = data.apply(
        lambda row: (row['Date'] - data.loc[:row.name, 'Date'][data['High'][:row.name + 1] == row[f'High_Last_{variable1}_Days']].iloc[-1]).days
        if pd.notna(row[f'High_Last_{variable1}_Days']) else np.nan, axis=1
    )
    data[f'Days_Since_Low_Last_{variable1}_Days'] = data.apply(
        lambda row: (row['Date'] - data.loc[:row.name, 'Date'][data['Low'][:row.name + 1] == row[f'Low_Last_{variable1}_Days']].iloc[-1]).days
        if pd.notna(row[f'Low_Last_{variable1}_Days']) else np.nan, axis=1
    )

    # Percentage difference from Historical High and Low
    data[f'%_Diff_From_High_Last_{variable1}_Days'] = (data['Close'] - data[f'High_Last_{variable1}_Days']) / data[f'High_Last_{variable1}_Days'] * 100
    data[f'%_Diff_From_Low_Last_{variable1}_Days'] = (data['Close'] - data[f'Low_Last_{variable1}_Days']) / data[f'Low_Last_{variable1}_Days'] * 100

    # Future High and Low prices over the next `variable2` days
    data[f'High_Next_{variable2}_Days'] = data['High'].shift(-variable2).rolling(window=variable2, min_periods=1).max()
    data[f'Low_Next_{variable2}_Days'] = data['Low'].shift(-variable2).rolling(window=variable2, min_periods=1).min()

    # Percentage difference from Future High and Low
    data[f'%_Diff_From_High_Next_{variable2}_Days'] = (data['Close'] - data[f'High_Next_{variable2}_Days']) / data[f'High_Next_{variable2}_Days'] * 100
    data[f'%_Diff_From_Low_Next_{variable2}_Days'] = (data['Close'] - data[f'Low_Next_{variable2}_Days']) / data[f'Low_Next_{variable2}_Days'] * 100

    return data


def main():
    # fetch initial crypto data
    data = fetch_crypto_data("BTC/USD", "2024-01-01")
    #print(data)

    # Transform the data
    data['Date'] = pd.to_datetime(data['Date'])
    variable1, variable2 = 7, 5
    data = calculate_metrics(data, variable1, variable2)
    print(data)
    #data.to_csv("crypto_data1.csv", index=False)

if __name__ == "__main__":
    main()