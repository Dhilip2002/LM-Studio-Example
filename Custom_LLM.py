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
        "model": "phi-3.1-mini-128k-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.7,
        "max_tokens": 800,
        "top_p": 0.95,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def format_response(response):
    if "error" in response:
        return f"Error: {response['error']}"
    try:
        return response["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        return f"Error parsing response: {str(e)}\nFull response: {json.dumps(response, indent=2)}"

def main():
    if not verify_server():
        print("Error: Cannot connect to LM Studio server. Please ensure:")
        print("1. LM Studio is running")
        print("2. Server is started")
        print("3. Model is loaded")
        return
        
    print("Chat started. Type 'quit' to exit.")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            break
            
        response = send_request(user_input)
        print("\nBot:", format_response(response))

if __name__ == "__main__":
    main()
