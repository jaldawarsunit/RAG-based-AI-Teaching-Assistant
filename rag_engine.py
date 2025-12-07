import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests
import json
import time

def create_embedding(text_list):
    try:
        r = requests.post("http://localhost:11434/api/embed", json={
            "model": "bge-m3",
            "input": text_list
        })
        r.raise_for_status()
        embedding = r.json()['embeddings']
        return embedding
    except Exception as e:
        print(f"Error in creating embedding: {e}")
        return None

def inference(prompt):
    try:
        r = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        })
        r.raise_for_status()
        response = r.json()
        return response
    except Exception as e:
        print(f"Error in inference: {e}")
        return {"response": f"Error: {str(e)}"}

class RAGTeachingAssistant:
    def __init__(self):
        self.df = None
        self.load_embeddings()
    
    def load_embeddings(self):
        """Load embeddings from file"""
        try:
            self.df = joblib.load("embeddings.joblib")
            print("Embeddings loaded successfully")
        except Exception as e:
            print(f"Error loading embeddings: {e}")
            self.df = pd.DataFrame()
    
    def process_query(self, incoming_query):
        """Main function to process user query"""
        try:
            # Step 1: Create embedding for the question
            print("Creating embedding for query...")
            question_embedding = create_embedding([incoming_query])
            if question_embedding is None:
                return "Error: Could not create embedding"
            
            question_embedding = question_embedding[0]
            
            # Step 2: Find similarities
            print("Finding similar content...")
            similarities = cosine_similarity(
                np.vstack(self.df['embedding']), 
                [question_embedding]
            ).flatten()
            
            # Get top 3 results
            top_results = 3
            max_indx = similarities.argsort()[::-1][0:top_results]
            new_df = self.df.iloc[max_indx]
            
            # Step 3: Create prompt
            print("Creating prompt...")
            prompt = f'''I am teaching python using one shot taught by code with harry youtuber. Here are video subtitle chunks containing video title, video number, start time in seconds, end time in seconds, the text at that time:

{new_df[["title", "number", "start", "end", "text"]].to_json(orient="records")}
--------------------------------
"{incoming_query}"
User asked this question related to the video chunks, you have to answer in a human way (don't mention the above format, it's just for you) where and how much content is taught in which video (in which video and at what timestamp) and guide the user to go to that particular video. If user asked unrelated question, tell him that you can only answer questions related to the course.'''

            # Save prompt for debugging
            with open("prompt.txt", "w") as f:
                f.write(prompt)
            
            # Step 4: Get response from LLM
            print("Getting response from LLM...")
            response = inference(prompt)
            
            if "response" in response:
                result = response["response"]
            else:
                result = str(response)
            
            # Step 5: Save response
            with open("response.txt", "w") as f:
                f.write(result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            print(error_msg)
            return error_msg

# For command line use
if __name__ == "__main__":
    assistant = RAGTeachingAssistant()
    incoming_query = input("Ask a Question: ")
    response = assistant.process_query(incoming_query)
    print("\n" + "="*50)
    print("RESPONSE:")
    print(response)