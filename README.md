# RAG-based-AI-Teaching-Assistant

A  Retrieval-Augmented Generation (RAG) based AI assistant built using Flask. This project retrieves context using embeddings and generates responses through a custom RAG pipeline.

## Features
- Flask backend API
- RAG engine for answering queries
- Embeddings stored using joblib
- Frontend built with HTML, CSS, and JavaScript
- Ready for Render deployment

## Project Structure
app.py  
rag_engine.py  
embeddings.joblib  
prompt.txt  
response.txt  
requirements.txt  
render.yaml  
static/  
  - script.js  
  - style.css  
templates/  
  - index.html  

## Run Locally
1. Install dependencies:
pip install -r requirements.txt

2. Start the server:
python app.py

3. Open in browser:
http://127.0.0.1:5000

## Deploy on Render
1. Push code to GitHub  
2. Create a Web Service on Render  
3. Use these commands:  
Build command: pip install -r requirements.txt  
Start command: gunicorn app:app  
4. Deploy and get your live URL.

