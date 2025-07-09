import gradio as gr
from ollama_client import model_exists, pull_model, stream_chat_with_model, reset_history

# Configuration
MODEL_NAME = "llama3.2"
SYSTEM_PROMPT = "You are a helpful assistant."


def chat(message, history):
    # history is a list of [user, assistant] message pairs
    flat_history = []
    for user_msg, assistant_msg in history:
        if user_msg:
            flat_history.append({"role": "user", "content": user_msg})
        if assistant_msg:
            flat_history.append({"role": "assistant", "content": assistant_msg})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + flat_history + [{"role": "user", "content": message}]

    # print("History is:")
    # print(flat_history)
    # print("And messages is:")
    # print(messages)

    if not model_exists(MODEL_NAME):
        pull_status = pull_model(MODEL_NAME)
        if not pull_status.startswith("✅"):
            yield pull_status
            return

    # Streaming generator
    for response_chunk in stream_chat_with_model(MODEL_NAME, messages):
        yield response_chunk


demo = gr.ChatInterface(fn=chat, title="🦙 Local LLaMA Chatbot", submit_btn="Send")

demo.launch()
