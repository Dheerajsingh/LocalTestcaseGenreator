
import requests
import json
import sys

def handshake_ollama(model="llama3.2"):
    print(f"Initiating Handshake with Ollama (Model: {model})...")
    
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": "Hello! Reply with 'Connection Established'.",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        print(f"Success! Response: {data.get('response')}")
        return True
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Is it running on port 11434?")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = handshake_ollama()
    if not success:
        sys.exit(1)
