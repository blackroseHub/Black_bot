from query_handler import classify_query, search_documents, llm
from embedder_store import load_vector_store
from agents import summarize, draft_email, support_response, chitchat_response

retriever = load_vector_store().as_retriever(search_type="mmr", search_kwargs={"k": 12})
conversation_context = {}

def chatbot_response(user_input, session_id="default"):
    try:
        if session_id not in conversation_context:
            conversation_context[session_id] = []

        conversation_context[session_id].append(f"User: {user_input}")
        history = "\n".join(conversation_context[session_id])
        recent = "\n".join(conversation_context[session_id][-3:])

        classification = classify_query(user_input)
        print(f"🧠 Classified as: {classification}")

        context_docs = search_documents(user_input, retriever)

        # 🗨️ ROUTING SECTION
        if classification == "task:chitchat":
            reply = chitchat_response(user_input, history=history)

        elif classification == "task:email":
            reply = draft_email(user_input)

        elif classification == "task:send_email":
            reply = draft_email(user_input, auto_send=True, send_to="client@example.com")

        elif classification == "task:log_ticket":
            reply = support_response(user_type="existing", issue_desc=user_input)

        elif classification in ["task:tech_support", "task:contact"]:
            support_prompt = f"""
Conversation History:
{recent}

User now says: "{user_input}"

Determine response based on whether they are an existing or new user.
"""
            reply = llm.invoke(support_prompt).content.strip()

        elif classification in ["informational", "task:summarize"]:
            reply = summarize(context_docs, user_input, recent_history=recent)

        elif classification == "task:external_search":
            if context_docs:
                context_text = "\n\n".join(doc.page_content for doc in context_docs)
                prompt = f"""
You are a helpful AI assistant.

User: "{user_input}"

Use this info:
{context_text}

Respond clearly, or ask for clarification if needed.
"""
                reply = llm.invoke(prompt).content.strip()
            else:
                fallback_prompt = f"""
User: "{user_input}"

No internal info matched. Ask for clarification.
"""
                reply = llm.invoke(fallback_prompt).content.strip()

        else:
            reply = "I'm not sure how to help with that."

        conversation_context[session_id].append(f"Bot: {reply}")
        return reply

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
