import requests
import json
import time

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def get_llm_response(prompt: str) -> str:
    """
    Connects to the local Ollama server to get a response.
    """
    try:
        payload = {
            "model": "llama3.1:70b",  # <-- THIS IS THE UPGRADE
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        
        if response.status_code == 200:
            response_data = response.json()
            full_response = response_data.get("response", "Sorry, I got an empty response from the model.")
            return full_response.strip()
        else:
            return f"Error: Could not connect to Ollama. Status code: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama. Please make sure it's running."
    except Exception as e:
        return f"An unexpected error occurred: {e}"