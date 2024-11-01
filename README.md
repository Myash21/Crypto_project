# Crypto Data Analysis and Prediction Model
## Overview
This project performs historical crypto data analysis and predictions using machine learning. The tasks include API data retrieval, historical metric calculations, and training a multi-target prediction model. The main objective is to forecast future price changes for cryptocurrencies.

## Table of Contents
1. API Selection
2. Data Retrieval
3. Metric Calculations
4. Machine Learning Model
5. Usage
6. Challenges and Key Learnings
   
## API Selection
The CryptoCompare API was chosen for its extensive coverage of cryptocurrency pairs, availability of historical data (daily, hourly, minutely), and user-friendly documentation. It allows up to 100,000 free API calls per month, supporting comprehensive data requirements.

## Data Retrieval
The get_crypto_data function retrieves historical data for a specified crypto pair (e.g., BTC/USD) and start date, using the CryptoCompare API. Data includes:
1. Open, High, Low, Close prices
2. Fetched data is stored as a pandas DataFrame and saved to an Excel file.

## Metric Calculations
The calculate_metrics function generates metrics to understand past and predict future price movements:
1. Historical High/Low: Highest and lowest prices over a specified past period.
2. Days Since High/Low: Days since the last historical high/low.
3. Percentage Difference from High/Low: Calculates the percentage difference between the close price and the high/low.
4. Future High/Low Prediction: Forecasts max/min values for the next specified days.
5. These metrics enable deeper analysis and serve as features for the ML model.

## Machine Learning Model
Using multi-target linear regression, the model predicts future high and low price percentage differences based on historical data.

1. train_model(): Trains the model on BTC/USD data and evaluates it using RMSE and R² metrics.
2. predict_outcomes(): Provides predictions for new data based on trained model.

Model Performance
1. RMSE: 6.28
2. R² Score: 0.107
The linear regression model offers baseline accuracy, but further improvements could include more complex models for nonlinear patterns in financial data.

## Usage
Install Dependencies:

## Challenges and Key Learnings

1. Rolling Window Calculations: Used for historical high/low tracking.
2. Multi-Target Prediction: Employed MultiOutputRegressor to predict multiple outputs.
3. Model Limitations: Linear regression was chosen for simplicity, but nonlinear models may improve accuracy for financial data.
