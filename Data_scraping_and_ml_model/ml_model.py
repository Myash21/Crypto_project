import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Set time-based variables for historical and future periods
variable1, variable2 = 7, 5

def train_model(data):
    """
    Trains a machine learning model to predict future price differences.

    Parameters:
    - data (DataFrame): The DataFrame containing calculated metrics and target variables.

    Returns:
    - model: The trained machine learning model.
    - metrics: A dictionary with model evaluation metrics (RMSE and R-squared).
    """
    # Define feature and target columns based on variable1 and variable2
    feature_cols = [
        f'Days_Since_High_Last_{variable1}_Days',
        f'%_Diff_From_High_Last_{variable1}_Days',
        f'Days_Since_Low_Last_{variable1}_Days',
        f'%_Diff_From_Low_Last_{variable1}_Days'
    ]
    target_cols = [
        f'%_Diff_From_High_Next_{variable2}_Days',
        f'%_Diff_From_Low_Next_{variable2}_Days'
    ]

    # Drop rows with NaN values in target columns
    data = data.dropna(subset=target_cols)

    # Separate features (X) and targets (y)
    X = data[feature_cols]
    y = data[target_cols]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = MultiOutputRegressor(LinearRegression())
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)

    # Save the model
    joblib.dump(model, 'trained_model.pkl')

    # Return the trained model and evaluation metrics
    metrics = {"RMSE": rmse, "R2_Score": r2}
    return model, metrics

def predict_outcomes(model, input_features):
    """
    Uses the trained model to predict future price differences.

    Parameters:
    - model: The trained machine learning model.
    - input_features (list or array): Input feature values for prediction.

    Returns:
    - predictions: A dictionary with predicted values for target variables.
    """
    # Make predictions
    prediction = model.predict([input_features])[0]
    predictions = {
        f'%_Diff_From_High_Next_{variable2}_Days': prediction[0],
        f'%_Diff_From_Low_Next_{variable2}_Days': prediction[1]
    }
    return predictions

def main():
    # Load dataset
    data = pd.read_csv('data/crypto_data1.csv')

    # Train the model
    model, metrics = train_model(data)
    print("Model Metrics:", metrics)

    # Load the trained model and make predictions on new data
    model = joblib.load('trained_model.pkl')
    new_data = [7, -3.2, 5, 2.5]  # Example input feature values
    predictions = predict_outcomes(model, new_data)
    print("Predicted Outcomes:", predictions)

if __name__ == "__main__":
    main()
