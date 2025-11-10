from flask import Flask, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

@app.route("/", methods=["GET"])
def index():
    return "Server is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        req = request.get_json()
        if not req or "queryResult" not in req or "queryText" not in req["queryResult"]:
            return jsonify({"error": "Invalid request format"}), 400
        user_message = req["queryResult"]["queryText"]

        if not GROQ_API_KEY:
            return jsonify({"error": "GROQ_API_KEY not configured"}), 500

        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content
        return jsonify({"fulfillmentText": bot_reply})
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    # For local development
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)