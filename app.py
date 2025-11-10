from flask import Flask, request, jsonifyfrom flask import Flask, request, jsonify

from groq import Groqfrom groq import Groq

import osimport os

from dotenv import load_dotenvfrom dotenv import load_dotenv



# Load environment variables from .env file# Load environment variables from .env file

load_dotenv()load_dotenv()



app = Flask(__name__)app = Flask(__name__)



GROQ_API_KEY = os.getenv("GROQ_API_KEY")GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)client = Groq(api_key=GROQ_API_KEY)



@app.route("/", methods=["GET"])@app.route("/", methods=["GET"])

def index():def index():

    return "Server is running!"    return "Server is running!"



@app.route("/webhook", methods=["GET", "POST"])@app.route("/webhook", methods=["GET", "POST"])  # Adding GET for testing

def webhook():def webhook():

    try:    try:

        req = request.get_json()        req = request.get_json()

        if not req or "queryResult" not in req or "queryText" not in req["queryResult"]:        if not req or "queryResult" not in req or "queryText" not in req["queryResult"]:

            return jsonify({"error": "Invalid request format"}), 400            return jsonify({"error": "Invalid request format"}), 400

        user_message = req["queryResult"]["queryText"]        user_message = req["queryResult"]["queryText"]

    except Exception as e:    except Exception as e:

        return jsonify({"error": f"Error processing request: {str(e)}"}), 500        return jsonify({"error": f"Error processing request: {str(e)}"}), 500



    try:    try:

        if not GROQ_API_KEY:        if not GROQ_API_KEY:

            return jsonify({"error": "GROQ_API_KEY not configured"}), 500            return jsonify({"error": "GROQ_API_KEY not configured"}), 500



        response = client.chat.completions.create(        response = client.chat.completions.create(

            model="llama3-70b-8192",            model="llama3-70b-8192",

            messages=[            messages=[

                {"role": "system", "content": "You are a helpful chatbot."},                {"role": "system", "content": "You are a helpful chatbot."},

                {"role": "user", "content": user_message}                {"role": "user", "content": user_message}

            ]            ]

        )        )



        bot_reply = response.choices[0].message.content        bot_reply = response.choices[0].message.content

        return jsonify({"fulfillmentText": bot_reply})        return jsonify({"fulfillmentText": bot_reply})

    except Exception as e:    except Exception as e:

        return jsonify({"error": f"Error calling Groq API: {str(e)}"}), 500        return jsonify({"error": f"Error calling Groq API: {str(e)}"}), 500



if __name__ == "__main__":if __name__ == "__main__":

    # Use this for local development    # Use this for local development

    app.run(host="0.0.0.0", port=10000, debug=True)    app.run(host="0.0.0.0", port=10000, debug=True)
