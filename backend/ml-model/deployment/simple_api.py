#!/usr/bin/env python3
"""
Simple working API using the fixed simple_predict.py logic
"""

from flask import Flask, request, jsonify
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our working prediction function
from simple_predict import predict_yield

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "message": "Simple API is running"})

@app.route('/predict', methods=['POST'])
def predict():
    """Simple prediction endpoint using working simple_predict logic"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Use the working predict_yield function
        result = predict_yield(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🌾 Simple Crop Yield API")
    print("=" * 40)
    print("🚀 Starting on http://localhost:3000")
    print("📖 Endpoints:")
    print("   GET  /health  - Health check")
    print("   POST /predict - Crop yield prediction")
    print()
    print("📝 Example request:")
    print("""curl -X POST http://localhost:3000/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "Area": "India",
    "Item": "Rice",
    "Year": 2024,
    "average_rain_fall_mm_per_year": 1200,
    "avg_temp": 26.0,
    "pesticides_tonnes": 100,
    "nitrogen": 80,
    "phosphorus": 40,
    "potassium": 60,
    "soil_ph": 6.5,
    "humidity": 65,
    "ndvi_avg": 0.75
  }'""")
    
    app.run(host='0.0.0.0', port=3000, debug=True)