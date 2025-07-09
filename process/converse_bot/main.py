import gradio as gr
from ollama_client import model_exists, pull_model, stream_chat_with_model


def build_chat_interface():
    with gr.Blocks() as demo:
        gr.Markdown("## 🦙 Local OLLAMA Chatbot - Configurable")

        # Input controls
        with gr.Row():
            system_prompt_input = gr.Textbox(label="System Prompt", value="You are a helpful assistant.", lines=2)
            model_name_input = gr.Textbox(label="Model Name", value="llama3.2")

        config_status = gr.Textbox(label="Status", interactive=False)

        # Shared state object for config
        state = gr.State({"model": "llama3.2", "system": "You are a helpful assistant."})

        # Update state dynamically and return it
        def set_config(system_prompt, model_name, state):
            system_prompt = system_prompt.strip()
            model_name = model_name.strip()

            if not system_prompt or not model_name:
                return "❗ Both model and prompt are required.", state

            state["model"] = model_name
            print(model_name)
            state["system"] = system_prompt
            return f"✅ Config set: Model = {model_name}, Prompt = '{system_prompt[:30]}...'", state

        gr.Button("Set Configuration").click(
            fn=set_config,
            inputs=[system_prompt_input, model_name_input, state],
            outputs=[config_status, state]
        )

        gr.Markdown("---")

        # Chat handler that receives updated state
        def chat(message, history, state):
            model = state["model"]
            system_prompt = state["system"]

            flat_history = []
            for user_msg, assistant_msg in history:
                if user_msg:
                    flat_history.append({"role": "user", "content": user_msg})
                if assistant_msg:
                    flat_history.append({"role": "assistant", "content": assistant_msg})

            messages = [{"role": "system", "content": system_prompt}] + flat_history + [{"role": "user", "content": message}]

            if not model_exists(model):
                pull_status = pull_model(model)
                if not pull_status.startswith("✅"):
                    yield pull_status
                    return

            for response_chunk in stream_chat_with_model(model, messages):
                yield response_chunk

        # Single chat interface
        with gr.Column():
            gr.ChatInterface(fn=chat, additional_inputs=[state])

    return demo

demo = build_chat_interface()
demo.launch()
