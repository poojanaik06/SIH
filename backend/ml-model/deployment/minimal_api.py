#!/usr/bin/env python3
"""
Minimal working API for crop yield prediction
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify
from simple_predict import predict_yield

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "Crop Yield Prediction API"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        result = predict_yield(data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Minimal Crop Yield Prediction API...")
    print("📡 Listening on http://localhost:3000")
    print("📋 Endpoints:")
    print("   GET  /health   - Health check")
    print("   POST /predict  - Crop yield prediction")
    print()
    print("📝 Example curl command:")
    print("""curl -X POST http://localhost:3000/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "Area": "India",
    "Item": "Rice",
    "Year": 2024,
    "average_rain_fall_mm_per_year": 1200,
    "avg_temp": 26.0,
    "pesticides_tonnes": 100
  }'""")
    
    app.run(host='0.0.0.0', port=3000, debug=True)