from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Still keep CORS for other clients

latest_data = {
    "device_id": "smart-trash-001",
    "distance": 16.1,
    "bin_full": False,
    "trash_type": "plastic",
    "confidence": 87.5,
    "full_debounced": False,
    "measurement_id": 1072,
    "timestamp": 2292325,
    "last_update": "Never"
}

@app.route("/api/trash-data", methods=["POST", "GET", "OPTIONS"])
def trash_data():
    if request.method == "POST":
        try:
            data = request.get_json()
            latest_data.update(data)
            latest_data["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"📥 Received: {json.dumps(data, indent=2)}")
            return jsonify({"status": "success"})
        except:
            return jsonify({"status": "error"}), 400
    
    # GET request - Check if JSONP callback requested
    callback = request.args.get('callback')
    
    if callback:
        # JSONP response - wraps JSON in function call
        json_data = json.dumps(latest_data)
        response = f"{callback}({json_data})"
        resp = make_response(response)
        resp.headers['Content-Type'] = 'application/javascript'
        return resp
    else:
        # Regular JSON response
        return jsonify(latest_data)

@app.route("/")
def home():
    return """
    <html>
    <head><title>Trash API</title></head>
    <body>
        <h1>Trash Monitoring API</h1>
        <p>Supports JSONP for GitHub Pages</p>
        <p><a href="/api/trash-data">Regular JSON</a></p>
        <p><a href="/api/trash-data?callback=test">JSONP Example</a></p>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("🌐 Flask Server with JSONP Support")
    print("📍 Regular JSON: http://localhost:5000/api/trash-data")
    print("📍 JSONP Example: http://localhost:5000/api/trash-data?callback=myFunction")
    app.run(host="0.0.0.0", port=5000, debug=True)
