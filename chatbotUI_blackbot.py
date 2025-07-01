import gradio as gr
from chat_handler import chatbot_response

# 🧠 Initial Messages
initial_messages = [
    ("bot", "🦾 Welcome to BLACK BOT."),
    ("bot", "I'm your AI wingman. Ask me anything. ⚡")
]

# 🗨️ Response Logic
def chatbot_reply(message, history):
    history.append(("user", message))
    bot_reply = chatbot_response(message)
    history.append(("bot", bot_reply))
    return history, ""

# 🖼️ Render Chat UI
def render_chat(history):
    chat_html = ""
    for sender, msg in history:
        if sender == "bot":
            chat_html += f"""
            <div class='chat-row left'>
                <img src='https://cdn-icons-png.flaticon.com/512/4712/4712107.png' class='avatar'>
                <div class='bubble bot'>{msg}</div>
            </div>
            """
        else:
            chat_html += f"""
            <div class='chat-row right'>
                <div class='bubble user'>{msg}</div>
                <img src='https://cdn-icons-png.flaticon.com/512/1144/1144760.png' class='avatar'>
            </div>
            """
    return chat_html

# ⚙️ Gradio UI Block
with gr.Blocks(theme=gr.themes.Soft(), css=".container { max-width: 100% !important; }") as demo:
    gr.HTML("""
    <div style="text-align: center; background: black; color: #00FF99; padding: 24px; border-radius: 0 0 12px 12px; font-size: 26px; font-family: monospace;">
        🤖 BLACK BOT · AI Chat Assistant
    </div>
    """)

    chat_display = gr.HTML(elem_id="chat_area")
    state = gr.State(initial_messages)

    with gr.Row():
        msg = gr.Textbox(
            placeholder="Ask me something smart…",
            container=False,
            scale=9,
            show_label=False,
            lines=1
        )
        send = gr.Button("➤", scale=1)

    msg.submit(fn=chatbot_reply, inputs=[msg, state], outputs=[state, msg]) \
       .then(fn=render_chat, inputs=state, outputs=chat_display)
    send.click(fn=chatbot_reply, inputs=[msg, state], outputs=[state, msg]) \
        .then(fn=render_chat, inputs=state, outputs=chat_display)

    demo.load(fn=render_chat, inputs=state, outputs=chat_display)

# 🧑‍🎨 Custom CSS
demo.css = """
html, body {
    margin: 0;
    padding: 0;
    height: 100%;
    background: #111;
    font-family: 'Segoe UI', sans-serif;
}
#chat_area {
    height: calc(100vh - 180px);
    overflow-y: auto;
    padding: 24px;
    background: #000;
}

.chat-row {
    display: flex;
    align-items: flex-end;
    margin-bottom: 12px;
}
.chat-row.left {
    justify-content: flex-start;
}
.chat-row.right {
    justify-content: flex-end;
}
.avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    margin: 0 10px;
    box-shadow: 0 2px 12px rgba(0,255,153,0.4);
}
.bubble {
    padding: 14px 18px;
    border-radius: 16px;
    max-width: 70%;
    font-size: 15.5px;
    line-height: 1.4;
}
.bubble.bot {
    background: #1f1f1f;
    color: #00FF99;
    margin-right: auto;
    box-shadow: 0 0 12px rgba(0,255,153,0.2);
}
.bubble.user {
    background: #2d2d2d;
    color: #fff;
    margin-left: auto;
    box-shadow: 0 0 8px rgba(255,255,255,0.1);
}
.gr-button {
    background: linear-gradient(135deg, #00FF99, #00CC88);
    color: black;
    border-radius: 50px !important;
    font-size: 20px;
    width: 42px;
    height: 42px;
}
.gr-button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0,255,153,0.3);
}
.gr-textbox textarea {
    border-radius: 30px !important;
    font-size: 16px;
    padding: 12px 16px;
    background: #1a1a1a;
    color: #00FF99;
}
"""

demo.launch()
