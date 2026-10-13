import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Reads the secret key from Vercel environment variable
PROXY_SECRET_KEY = os.environ.get("PROXY_SECRET_KEY")

@app.before_request
def check_bearer_token():
    # Allow public ping for UptimeRobot health check
    if request.path == "/health":
        return None
        
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {PROXY_SECRET_KEY}":
        return jsonify({
            "error": "Unauthorized",
            "message": "Invalid or missing API key"
        }), 401

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "awake"}), 200
