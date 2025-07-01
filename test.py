from chat_handler import chatbot_response

if __name__ == "__main__":
    print("🤖 Chatbot Test Harness Started. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() == "exit":
            print("👋 Exiting. Bye!")
            break
        response = chatbot_response(user_input)
        print(f"Bot: {response}\n")
