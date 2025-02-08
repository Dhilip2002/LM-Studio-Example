import requests
import json

def verify_server():
    try:
        response = requests.get("http://localhost:1234/v1/models")
        response.raise_for_status()
        return True
    except:
        return False

def send_request(message):
    url = "http://localhost:1234/v1/chat/completions"
    
    payload = {
        "messages": [
            {"role": "system", "content": "Always answer only the technical questions"},
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": 100,
        "stream": False
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def format_response(response):
    if "error" in response:
        return response["error"]
    try:
        return response["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError):
        return "Error: Unexpected response format"

def main():
    if not verify_server():
        print("Error: Cannot connect to LM Studio server")
        return
        
    print("Welcome to the Chatbot! Type 'quit' to exit.")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            break
            
        response = send_request(user_input)
        print("Bot:", format_response(response))

if __name__ == "__main__":
    main()
