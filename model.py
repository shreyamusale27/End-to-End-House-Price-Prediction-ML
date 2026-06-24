import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def run_ml_pipeline():
    # 1. Setup directories
    os.makedirs('static', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    print("Fetching dataset...")
    # 2. Data Collection
    housing = fetch_california_housing()
    df = pd.DataFrame(housing.data, columns=housing.feature_names)
    df['Target'] = housing.target
    
    # 3. Exploratory Data Analysis
    print("Generating EDA visualizations...")
    sns.set_theme(style="whitegrid")
    
    # Target distribution
    plt.figure(figsize=(8, 5))
    sns.histplot(df['Target'], bins=50, kde=True, color='teal')
    plt.title('Distribution of House Prices')
    plt.xlabel('House Price (in $100,000s)')
    plt.tight_layout()
    plt.savefig('static/target_dist.png')
    plt.close()
    
    # Correlation heatmap
    plt.figure(figsize=(10, 8))
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    plt.savefig('static/corr_heatmap.png')
    plt.close()
    
    # 4. Data Preprocessing
    print("Preprocessing data...")
    X = df.drop('Target', axis=1)
    y = df['Target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler
    joblib.dump(scaler, 'models/scaler.joblib')
    
    # 5. Model Training
    print("Training the Random Forest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train_scaled, y_train)
    
    # 6. Evaluation
    print("Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"R-squared: {r2:.4f}")
    
    # Save evaluation metrics
    with open('models/metrics.txt', 'w') as f:
        f.write(f"MSE: {mse:.4f}\n")
        f.write(f"R2: {r2:.4f}\n")
        
    # Save the model
    joblib.dump(model, 'models/rf_model.joblib')
    print("Pipeline completed successfully! Model and artifacts saved.")

if __name__ == '__main__':
    run_ml_pipeline()
