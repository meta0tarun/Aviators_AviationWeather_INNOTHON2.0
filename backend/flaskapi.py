from flask import Flask, request, jsonify
from flask_cors import CORS
from main import run_pipeline

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "✅ Flight Weather API is running"

@app.route("/favicon.ico")
def favicon():
    return "", 204

@app.route("/analyze-flight", methods=["POST"])
def analyze_flight():
    data = request.get_json()
    flight_number = data.get("flight_number")
    forecast_offset = data.get("forecast_offset", 0)  # Default to 0 if not provided
    
    if not flight_number:
        return jsonify({"error": "Missing flight number"}), 400
    
    try:
        result = run_pipeline(
            flight_number=flight_number,
            forecast_offset=forecast_offset,
            return_data=True
        )
        if not result:
            return jsonify({"error": "No data returned from pipeline"}), 500
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)