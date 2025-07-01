# agents.py

from query_handler import llm

def summarize(context_docs, user_input, recent_history=""):
    context_text = "\n\n".join(doc.page_content for doc in context_docs) if context_docs else ""

    prompt = f"""
You are a helpful AI assistant. Use the provided context to answer the user's question clearly and accurately.

Earlier chat context:
{recent_history}

User question:
"{user_input}"

Relevant info:
{context_text}

If the context doesn’t answer the question directly, reason it out or ask a clarifying question.
"""
    return llm.invoke(prompt).content.strip()

def draft_email(user_input):
    prompt = f"""
You are an AI assistant. Draft a professional email based on the user's request:

Request: {user_input}

Email:
"""
    return llm.invoke(prompt).content.strip()

def support_response(user_type):
    if user_type == "existing":
        return "Please contact our support team at support@example.com"
    else:
        return "You can reach our onboarding team at onboarding@example.com"

def chitchat_response(user_input, history=""):
    prompt = f"""
You are a friendly AI assistant having a casual conversation.

Recent chat:
{history}

User said: "{user_input}"

Reply naturally.
"""
    return llm.invoke(prompt).content.strip()
