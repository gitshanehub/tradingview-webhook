from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Server is live", 200

@app.route("/tv-webhook", methods=["GET", "POST"])
def tv_webhook():
    print("=== WEBHOOK HIT ===", flush=True)

    data = request.get_json(silent=True)

    if data is None:
        raw_text = request.get_data(as_text=True)
        print("Type: text", flush=True)
        print(f"Body: {raw_text}", flush=True)
        return jsonify({
            "status": "received",
            "type": "text",
            "body": raw_text
        }), 200

    print("Type: json", flush=True)
    print(f"Body: {data}", flush=True)

    return jsonify({
        "status": "received",
        "type": "json",
        "body": data
    }), 200
