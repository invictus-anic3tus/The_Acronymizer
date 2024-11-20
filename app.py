from flask import Flask, request, render_template, jsonify, send_from_directory
from flask_cors import CORS
from g4f.client import Client

app = Flask(__name__)

@app.route('/')
def serve_html():
    return send_from_directory('', 'index.html')

prevmessages = [
    {"role": "system", "content": "You are a helpful AI assistant chatbot."}
]

def ai(message):

    client = Client()
    recent_messages = prevmessages[-3:]
    recent_messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=recent_messages,
        )
        assistant_response = response.choices[0].message.content
        prevmessages.append({"role": "assistant", "content": assistant_response})
        return assistant_response
    
    except Exception as e:
        print(f"Error in AI response: {e}")
        return "Sorry, there was an error processing your request."


@app.route('/submit', methods=['POST'])
def handle_submit():
    data = request.get_json()
    user_message = data.get('message', '')
    response_message = ai(user_message)

    return jsonify({"response": response_message})



@app.route('/customize', methods=['POST'])
def custom_prompt():
    data = request.get_json()

    user_message = data.get('message', '')

    print("Recieved Text:", user_message)
    return jsonify({"response": 'Recieved'})



if __name__ == '__main__':
    app.run(debug=True)
