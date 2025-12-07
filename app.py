from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import json
import uuid
from datetime import datetime
import os
import sys

# Import the RAG engine
sys.path.append('.')
from rag_engine import RAGTeachingAssistant

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)  # Secure random key
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize RAG assistant
assistant = RAGTeachingAssistant()

# Store chat histories (in production, use a database)
chat_histories = {}

@app.route('/')
def home():
    # Generate a unique session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    
    # Initialize chat history for this session
    if session['session_id'] not in chat_histories:
        chat_histories[session['session_id']] = []
    
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        session_id = session.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Add user message to history
        if session_id not in chat_histories:
            chat_histories[session_id] = []
        
        chat_histories[session_id].append({
            'type': 'user',
            'message': user_message,
            'time': datetime.now().strftime('%H:%M:%S')
        })
        
        # Process the query
        try:
            # Get response from RAG engine
            response = assistant.process_query(user_message)
            
            # Add assistant response to history
            chat_histories[session_id].append({
                'type': 'assistant',
                'message': response,
                'time': datetime.now().strftime('%H:%M:%S')
            })
            
            return jsonify({
                'response': response,
                'history': chat_histories[session_id]
            })
            
        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}"
            chat_histories[session_id].append({
                'type': 'assistant',
                'message': error_msg,
                'time': datetime.now().strftime('%H:%M:%S')
            })
            return jsonify({
                'response': error_msg,
                'history': chat_histories[session_id]
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    session_id = session.get('session_id')
    if session_id and session_id in chat_histories:
        return jsonify({'history': chat_histories[session_id]})
    return jsonify({'history': []})

@app.route('/clear', methods=['POST'])
def clear_chat():
    session_id = session.get('session_id')
    if session_id and session_id in chat_histories:
        chat_histories[session_id] = []
    return jsonify({'status': 'cleared'})

if __name__ == '__main__':
    # Make sure the templates and static folders exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)