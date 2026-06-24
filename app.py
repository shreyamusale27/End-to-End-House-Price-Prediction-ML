from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model and scaler
try:
    model = joblib.load('models/rf_model.joblib')
    scaler = joblib.load('models/scaler.joblib')
except Exception as e:
    print("Model or scaler not found. Please run model.py first.")
    model = None
    scaler = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None:
        return jsonify({'error': 'Model not loaded.'}), 500
        
    try:
        data = request.json
        # Feature names expected by California Housing dataset:
        # ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
        features = [
            float(data['medinc']),
            float(data['houseage']),
            float(data['averooms']),
            float(data['avebedrms']),
            float(data['population']),
            float(data['aveoccup']),
            float(data['latitude']),
            float(data['longitude'])
        ]
        
        # Scale the features
        features_scaled = scaler.transform([features])
        
        # Predict
        prediction = model.predict(features_scaled)[0]
        
        # California housing Target is expressed in hundreds of thousands of dollars ($100,000)
        predicted_price = prediction * 100000
        
        return jsonify({'price': predicted_price})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
