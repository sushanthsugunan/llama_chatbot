import dash
from dash import html, dcc, Input, Output, State
from chatbot.ollama_client import model_exists, pull_model, chat_with_model, reset_history

app = dash.Dash(__name__)
app.title = "LLaMA Chat Interface"

app.layout = html.Div([
    html.H1("🦙 My Personal Assistant", style={"textAlign": "center"}),

    html.Label("🖥️ System Prompt:"),
    dcc.Textarea(id='system-prompt', value="You are a helpful assistant.", style={'width': '100%', 'height': 80}),

    html.Label("웃 User Prompt:"),
    dcc.Textarea(id='user-prompt', placeholder="Type your question here...", style={'width': '100%', 'height': 100}),

    html.Label("✪✪ Model Name:"),
    dcc.Input(id='model-name', type='text', value='llama3.2', style={'width': '50%'}),

    html.Br(), html.Br(),

    html.Div([
        html.Button("Generate Response", id='submit-btn', n_clicks=0),
        html.Button("Reset Context", id='reset-btn', n_clicks=0, style={"marginLeft": "20px"})
    ]),

    html.Br(), html.Br(),
    html.Div(id='response-output', style={'whiteSpace': 'pre-wrap', 'background': '#f4f4f4', 'padding': '10px'}),
    html.Div(id='reset-output', style={'color': 'green', 'marginTop': '10px'})
])


@app.callback(
    Output('response-output', 'children'),
    Input('submit-btn', 'n_clicks'),
    State('system-prompt', 'value'),
    State('user-prompt', 'value'),
    State('model-name', 'value')
)
def generate_response(n_clicks, system_prompt, user_prompt, model_name):
    if n_clicks == 0 or not user_prompt:
        return ""

    if not model_exists(model_name):
        pull_status = pull_model(model_name)
        if not pull_status.startswith("✅"):
            return pull_status

    return chat_with_model(system_prompt, user_prompt, model_name)


@app.callback(
    Output('reset-output', 'children'),
    Input('reset-btn', 'n_clicks')
)
def reset_chat(n_clicks):
    if n_clicks > 0:
        reset_history()
        return "✅ Conversation history cleared."
    return ""


if __name__ == "__main__":
    app.run(debug=True)
