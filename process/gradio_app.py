from chatbot.ollama_client import model_exists, pull_model, chat_with_model, reset_history
import gradio as gr


def generate_response(system_prompt, user_prompt, model_name):
    if not user_prompt:
        return "❗Please enter a user prompt."

    if not model_name:
        return "❗Model name is missing."

    model_name = str(model_name).strip()

    if not model_exists(model_name):
        pull_status = pull_model(model_name)
        if not pull_status.startswith("✅"):
            return pull_status

    return chat_with_model(system_prompt, user_prompt, model_name)


def reset_chat():
    reset_history()
    print("Chat history reset")  # Debug
    return "✅ Conversation history cleared."


with gr.Blocks() as demo:
    gr.Markdown("## 🦙 Local LLaMA Chatbot with Context + Reset")

    system_prompt = gr.Textbox(label="System Prompt", value="You are a helpful assistant.")
    user_prompt = gr.Textbox(label="User Prompt", placeholder="Type your message...")
    model_name = gr.Textbox(label="Model", value="llama3.2")

    output = gr.Textbox(label="Response", lines=6)
    reset_message = gr.Textbox(label="Reset Status", interactive=False)

    with gr.Row():
        submit_btn = gr.Button("Generate Response")
        reset_btn = gr.Button("Reset Context")

    submit_btn.click(
        fn=generate_response,
        inputs=[system_prompt, user_prompt, model_name],
        outputs=output
    )

    reset_btn.click(
        fn=reset_chat,
        inputs=[],
        outputs=reset_message
    )

demo.launch()


# if __name__ == "__main__":
#     app.run(debug=True)

