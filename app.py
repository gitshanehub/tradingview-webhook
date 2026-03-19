import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


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

    symbol = data.get("symbol")
    price = data.get("price")
    interval = data.get("interval")
    alert_time = data.get("time")

    prompt = f"""
Analyze this trading alert:

Symbol: {symbol}
Price: {price}
Interval: {interval}
Time: {alert_time}

Give:
- Bias (bullish/bearish/neutral)
- Quick reasoning
- Risk
- Suggested action
Keep it short.
"""

    try:
        response = client.responses.create(
            model="gpt-5.4-mini",
            input=prompt
        )

        analysis = response.output_text

        print("=== AI ANALYSIS ===", flush=True)
        print(analysis, flush=True)

        return jsonify({
            "status": "received",
            "body": data,
            "analysis": analysis
        }), 200

    except Exception as e:
        print("OPENAI ERROR:", str(e), flush=True)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 200
