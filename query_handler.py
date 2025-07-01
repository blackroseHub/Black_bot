from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)

def classify_query(query):
    system_prompt = """
You are a task classifier for an AI assistant.

Classify the user input into one of the following categories:
- 'informational': Asking about services or general information
- 'task:summarize': Request to summarize or explain document content
- 'task:email': Draft an email (without sending)
- 'task:send_email': Draft and send an email
- 'task:tech_support': Asking for help or reporting a problem
- 'task:log_ticket': Reporting an issue that should be logged
- 'task:contact': Asking to speak to someone or schedule a call
- 'task:chitchat': Casual conversation, greetings
- 'task:external_search': Requires knowledge not in internal docs

Rules:
- If the user says “send this email” or “email this to…” → classify as 'task:send_email'
- If the user says “open a ticket” or “report this issue” → classify as 'task:log_ticket'
- Stick to one label. Respond with only the label.
"""

    full_prompt = f"{system_prompt}\n\nUser: {query}"
    response = llm.invoke(full_prompt)
    return response.content.strip().lower() if hasattr(response, "content") else response.strip().lower()

def search_documents(query, retriever):
    return retriever.get_relevant_documents(query)
