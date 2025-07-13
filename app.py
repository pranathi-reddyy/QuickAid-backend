from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

app = Flask(__name__)
CORS(app)

# ✅ Use environment variable instead of hardcoding
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/medicine-info', methods=['POST'])
def get_medicine_info():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({'result': 'No input provided'}), 400

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "user", "content": f"What is the medical use or purpose of the tablet '{query}'?"}
            ],
            max_tokens=150
        )
        result = response['choices'][0]['message']['content']
        return jsonify({'result': result})
    
    except Exception as e:
        print("OpenAI Error:", e)
        return jsonify({'result': 'Error retrieving medicine info'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
