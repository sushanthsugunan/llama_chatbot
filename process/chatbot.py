import argparse
import requests
import json

OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}

def chat_with_ollama(system_prompt, user_prompt, model_name="llama3.2"):
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False  # set True if you want streaming responses
    }

    response = requests.post(OLLAMA_API, headers=HEADERS, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()
        return result['message']['content']
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

def main():
    parser = argparse.ArgumentParser(description="Chat with LLaMA 3.2 via Ollama")
    parser.add_argument('--system', type=str, required=True, help="System prompt")
    parser.add_argument('--user', type=str, required=True, help="User prompt")
    parser.add_argument('--model', type=str, default="llama3.2", help="Model name (default: llama3.2)")
    args = parser.parse_args()

    print("Sending request to Ollama...")
    try:
        reply = chat_with_ollama(args.system, args.user, args.model)
        print("\n=== Response ===")
        print(reply)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
