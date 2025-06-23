from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from openai import OpenAI

app = Flask(__name__)

# ✅ Load OpenAI key securely from environment variable
client = OpenAI()

@app.route("/bot", methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    print(f"User said: {incoming_msg}")

    # Generate GPT reply
    reply = generate_reply(incoming_msg)

    # Send reply back to WhatsApp via Twilio
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)
    return str(resp)

def generate_reply(user_msg):
    try:
        prompt = f"You are a helpful assistant helping someone reply to a customer care message. Message: \"{user_msg}\". What is the best way to respond?"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7,
        )

        reply = response.choices[0].message.content.strip()
        return reply

    except Exception as e:
        print("Error with GPT:", e)
        return f"Sorry, GPT failed: {str(e)}"

if __name__ == "__main__":
    app.run(port=5000)
