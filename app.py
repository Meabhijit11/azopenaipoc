import os
import logging
from flask import Flask, request, jsonify, send_from_directory
from openai import AzureOpenAI
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/query', methods=['POST'])
def query_openai():
    data = request.json
    user_query = data.get("query")

    if not user_query:
        logging.error("No query provided")
        return jsonify({"error": "No query provided"}), 400

    try:
        response = client.chat.completions.create(
            model="abazopenaipoc",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_query}
            ]
        )
        logging.info(f"Query: {user_query} | Response: {response.choices[0].message.content}")
        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)