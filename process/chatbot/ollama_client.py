import requests
import json

OLLAMA_API = "http://localhost:11434"
HEADERS = {"Content-Type": "application/json"}


def model_exists(model_name):
    """Check if model is already pulled."""
    try:
        res = requests.get(f"{OLLAMA_API}/api/tags")
        if res.status_code == 200:
            tags = res.json().get("models", [])
            return any(model_name in m['name'] for m in tags)
    except Exception as e:
        print("Tag check failed:", e)
    return False


def pull_model(model_name):
    """Pull model if not already available."""
    try:
        print(f"Pulling model: {model_name}")
        res = requests.post(
            f"{OLLAMA_API}/api/pull",
            headers=HEADERS,
            json={"name": model_name},
            stream=True
        )

        if res.status_code != 200:
            return f"❌ Failed to pull model: {res.text}"

        for line in res.iter_lines():
            if line:
                progress = json.loads(line.decode("utf-8"))
                status = progress.get("status", "")
                if status in ["success", "completed"]:
                    return "✅ Model pulled successfully"

        return "⚠️ Pull did not complete properly"

    except Exception as e:
        return f"❌ Error pulling model: {e}"


def chat_with_model(system_prompt, user_prompt, model_name):
    """Send chat message to Ollama API."""
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    }

    try:
        res = requests.post(f"{OLLAMA_API}/api/chat", headers=HEADERS, data=json.dumps(payload))
        if res.status_code == 200:
            result = res.json()
            return result["message"]["content"]
        else:
            return f"❌ Error {res.status_code}: {res.text}"
    except Exception as e:
        return f"❌ Exception occurred: {str(e)}"
