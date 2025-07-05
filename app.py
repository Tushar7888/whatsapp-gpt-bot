from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os

app = Flask(__name__)

# ✅ Get your OpenAI key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "")
    response = MessagingResponse()

    try:
        reply = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": incoming_msg}]
        )
        msg = reply.choices[0].message.content.strip()
    except Exception as e:
        msg = "Sorry, error occurred: " + str(e)

    response.message(msg)
    return str(response)

if __name__ == "__main__":
    # ✅ Required for Render.com deployment
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
