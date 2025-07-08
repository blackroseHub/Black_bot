# 🧠 BLACK BOT — Developer Tutorial & RAG Chatbot Guide

> **Created by: ALAN JYOTHIS THOMAS**  
> [🌙 GitHub: blackroseHub](https://github.com/blackroseHub)

Welcome to **BLACK BOT** — a modular Retrieval-Augmented Generation (RAG) chatbot template powered by LangChain + OpenAI.  
This guide is your go-to cheatcode for understanding, customizing, and deploying BLACK BOT.  
Whether you're a student, dev, or tech rebel, this bot’s built to help you rule your data and automate smart conversations.

> ⚡️ By default, BLACK BOT runs on OpenAI API — but it's fully adaptable. You can plug in other LLM APIs like Cohere, Anthropic, or run **Ollama** locally for offline RAG. [👉 Click here to jump to Ollama integration »](#-bonus-switch-from-openai-to-ollama-or-other-apis)

---

## 🚦 BLACK BOT Data Flow — How It Works

> Think of it like a pipeline: ✍️ Input → 🧠 Classify → ⚙️ Agent → 🪄 Generate → 🎯 Return

1. **User enters a message** in the UI.
2. Message goes to `chat_handler.py`, which manages the flow.
3. It’s passed to `query_handler.py`, where a prompt-based LLM classifies it — is it a `task:summarize`, `task:email`, `task:log_ticket`?
4. The **LLM returns a one-word classification**, like `task:summarize`.
5. `chat_handler.py` uses that label to call the corresponding agent function from `agents.py`.
6. The **agent does its job** (e.g., summarize using RAG, draft email, log issue).
7. Optionally, the **output is polished or reviewed by the LLM again** before being returned to the user.

---

### 🧭 Workflow 

> [🔎 Jump to query_handler.py »](#query_handlerpy) — [🎯 Jump to agents.py »](#agentspy) — [🎨 Jump to UI editing »](#-ui-customization-with-swagger-gradio-style)

---



## 📚 Index

1. [🚀 Getting Started](#-getting-started)
2. [💡 What is RAG?](#-what-is-rag-retrieval-augmented-generation)
3. [🗂️ File Structure & Core Roles](#-project-file-map--with-live-descriptions)
4. [🤹 Multi-Agent Architecture](#-multi-agent-architecture)
5. [🎯 Prompt Engineering](#-prompt-engineering-with-real-examples)
6. [🛡️ What to Change vs Not Touch](#-what-to-change--what-not-to-touch)
7. [🧠 Script Logic Breakdown](#-core-script-logic--described)
8. [🎨 UI Customization](#-ui-customization-with-swagger-gradio-style)
9. [🔁 Ollama & Other LLM Integrations](#-bonus-switch-from-openai-to-ollama-or-other-apis)

---

## 🚀 Getting Started

### 1. Create a Virtual Environment

**Windows:**
```bat
python -m venv chatbot-env
chatbot-env\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv chatbot-env
source chatbot-env/bin/activate
```

### 2. Clone the Repo

```bash
git clone https://github.com/blackroseHub/Black_bot.git
cd black-bot
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Drop Your Data

Put your PDFs or text files into the `/data/` directory.

### 5. Create Embeddings

```bash
python prepare_embeddings.py
```

### 6. Run the Chatbot UI

```bash
python chatbotUI_blackbot.py
```

---

## 💡 What is RAG (Retrieval-Augmented Generation)?

RAG is like giving your LLM a smart library card 📚.  
When a user asks a question, the system **searches your own docs** for the best answers, combines it with the power of the LLM (like OpenAI or Ollama), and gives a grounded, fact-aware response.

### **Simple Example**

- You: *“What is the refund policy?”*
- Bot: (searches your documents for "refund policy," finds the right paragraph, then summarizes or answers using that exact info.)

**Why RAG?**
- No need to retrain your model for every update.
- Super easy to keep docs fresh: just add new PDFs, re-embed, and done.
- More secure: your private knowledge base never leaves your system.

### **In This Template**

- Your data lives in `/data/`.
- Embeddings are stored locally in ChromaDB.
- LLM (OpenAI/Ollama/etc.) is only used for reasoning, not as the source of facts.

### **Who Should Use This?**
- Anyone building an internal chatbot
- Teams needing private, explainable, up-to-date bots
- Students who want to learn RAG hands-on

---

## 🗂️ Project File Map 

| File | Role |
|------|------|
| `config.py` | Your OpenAI key & vector DB setup |
| `prepare_embeddings.py` | Feed data to the AI brain |
| `loader_splitter.py` | Read + split your docs |
| `embedder_store.py` | Create/load vector embeddings |
| `query_handler.py` | Classify what the user wants |
| `chat_handler.py` | Orchestrates the response flow |
| `agents.py` | Defines what to say or do (email, ticket, summary, etc.) |
| `test_harness.py` | CLI test harness |
| `chatbotUI_blackbot.py` | Gradio-based UI frontend |

---

### **Main Script Logic — Where the Magic Happens**

#### [`chat_handler.py`](#chat_handlerpy)
- Controls conversation state, memory, and what agent to use
- Takes the classified intent and routes it to the correct function

#### [`query_handler.py`](#query_handlerpy)
- Sends user prompts to the LLM for classification (e.g., "Is this a support request?")
- Returns a single label for what the user wants

#### [`agents.py`](#agentspy)
- Houses each "agent": summarizer, email drafter, support ticket logger, etc.
- Each agent can call real APIs (send mail, log tickets) or just generate text

#### [`chatbotUI_blackbot.py`](#-ui-customization-with-swagger-gradio-style)
- Gradio-powered, full-featured chat interface
- Easily change branding, avatar, and layout

---

## 🤹 Multi-Agent Architecture

BLACK BOT isn’t just a chatbot.  
It’s a **multi-agent system** where each "agent" does one job super well:

- Summarizer Agent — turns docs into TL;DRs
- Email Agent — writes or sends emails
- Support Agent — logs support tickets
- ChitChat Agent — small talk, onboarding, etc.
- (Add your own: Invoice Agent, Search Agent, Web Scraper...)

**To add a new agent:**
1. Write a new function in `agents.py`.
2. Add a classification label in `query_handler.py`.
3. Map that label to the agent in `chat_handler.py`.

> 💡 **Pro tip:** You can trigger external APIs, webhooks, or anything Python can do!

---

## 🎯 Prompt Engineering — With Real Examples

Getting the right output = writing the right prompts.  
This template puts prompts in code (not magic).  
Tweak these to suit your company, style, or product.

**Example from `query_handler.py`:**

```python
system_prompt = """
Classify the user input into one of the following categories:
'informational', 'task:summarize', 'task:email', 'task:send_email', ...
"""
```
**Want a new task? Add a label and describe it here!**

**Example from `agents.py`:**

```python
def summarize(context_docs, user_input, recent_history=""):
    prompt = f"""
You are a helpful AI assistant. Use the provided docs and chat history to answer:
Chat History: {recent_history}
Docs: {context_docs}
User: {user_input}
"""
    return llm.invoke(prompt).content.strip()
```

**Tips for Prompt Engineering:**
- Be direct and clear (don't over-engineer).
- Add your own style ("Keep it funny", "Be formal", "Short answers", etc).
- Test and iterate!

---

## 🛡️ What to Change / What Not to Touch

| Safe to Change                  | Use Caution                 | Advanced Only                       |
|---------------------------------|-----------------------------|-------------------------------------|
| Prompts in code                 | Routing logic in handlers   | ChromaDB files                      |
| Add/edit agents (`agents.py`)   | Session/context tweaks      | Deep LangChain class changes        |
| Branding, UI/CSS, Gradio theme  | Classification rules        | VectorDB internal code              |
| File structure/docs in `/data`  |                            |                                     |

---

## 🧠 Core Script Logic — Described

- `chat_handler.py`: Manages state, memory, main router
- `query_handler.py`: Intent classification via LLM prompt
- `agents.py`: All agent actions (summarize, email, support, etc)
- `prepare_embeddings.py`: Ingest and vectorize your knowledge base
- `chatbotUI_blackbot.py`: Gradio-powered, fully brandable UI

---

## 🎨 UI Customization — With Swagger Gradio Style

BLACK BOT’s UI is all Gradio + a sprinkle of CSS rizz.

**To change the title/branding:**
```python
gr.HTML("""
<div style="text-align: center; background: black; color: #00FF99; ...">
    🤖 BLACK BOT · AI Chat Assistant
</div>
""")
```
**To change avatars:**
- Swap out the image URLs in `render_chat()` for your own PNGs.

**Want dark mode or neon?**
- Edit the CSS in `demo.css` (see `chatbotUI_blackbot.py`)

**Example:**

```css
.bubble.bot {
    background: #1f1f1f;
    color: #00FF99;
    margin-right: auto;
    box-shadow: 0 0 12px rgba(0,255,153,0.2);
}
```

**Pro Tip:**  
Try making the input box pulse or the chat bubbles animate — Gradio CSS is super hackable.

---


---
## 🔁 BONUS: Switch From OpenAI to Ollama or Other APIs

BLACK BOT runs on OpenAI out of the box, but here’s how to upgrade it:

### ✅ Ollama Local LLM Integration (e.g., Mistral, LLaMA2)

1. **Install Ollama (One-Time Setup)**
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
2. **Pull a model**
    ```bash
    ollama run mistral
    ```
3. **Update config.py**
    ```python
    USE_LOCAL_MODEL = True
    LOCAL_MODEL_NAME = "mistral"
    ```
4. **Modify query_handler.py**
    ```python
    from config import USE_LOCAL_MODEL, LOCAL_MODEL_NAME

    if USE_LOCAL_MODEL:
        from langchain_community.llms import Ollama
        llm = Ollama(model=LOCAL_MODEL_NAME)
    else:
        from langchain_openai import ChatOpenAI
        from config import OPENAI_API_KEY
        llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
    ```
5. **Do the same in agents.py**
    Everywhere you see `from query_handler import llm`, it will automatically use the one defined above.

You are now fully on local AI. 💪 Works offline. Runs fast. Privacy mode: engaged.

## 🧩 Further Reading & Troubleshooting

- [LangChain Docs](https://python.langchain.com/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Gradio Docs](https://gradio.app/docs/)
- [Ollama Docs](https://ollama.com/docs)
- Want more of this? Ping your project maintainer or  
  [🌙 Alan Jyothis Thomas on GitHub](https://github.com/blackroseHub)

---

Built by **Alan Jyothis Thomas** — [github.com/blackroseHub](https://github.com/blackroseHub)  
You now have everything you need to **run, hack, and extend BLACK BOT**.  
Go build something epic! 🚀
