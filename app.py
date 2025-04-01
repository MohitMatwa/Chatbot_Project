import streamlit as st
from chatbot import HiringChatbot

def main():
    st.title("TalentScout Hiring Assistant")
    chatbot = HiringChatbot()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "collected_info" not in st.session_state:
        st.session_state.collected_info = {}
    if "awaiting_input" not in st.session_state:
        st.session_state.awaiting_input = "name"
    if "conversation_ended" not in st.session_state:
        st.session_state.conversation_ended = False
    if "greeted" not in st.session_state:
        st.session_state.greeted = False

    # Display chat messages in order
    for message in st.session_state.messages:
        st.chat_message(message["role"]).write(message["content"])

    # Greeting and first question
    if not st.session_state.greeted:
        greeting_message = "Hello! I’m TalentScout, your hiring assistant. I will guide you through the application process. Let's begin!"
        st.session_state.messages.append({"role": "assistant", "content": greeting_message})
        st.chat_message("assistant").write(greeting_message)

        first_question = chatbot.get_next_question()  # Ask for name
        st.session_state.messages.append({"role": "assistant", "content": first_question})
        st.chat_message("assistant").write(first_question)

        st.session_state.greeted = True  # Mark greeting as done

    # Get user input
    if not st.session_state.conversation_ended:
        user_input = st.chat_input("Your response:")

        if user_input:
            # Append user's response
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)

            # Process chatbot's response
            response = chatbot.process_response(user_input)

            # Handle conversation end
            if response == "END_CONVERSATION":
                st.session_state.conversation_ended = True
                response = "Thank you for your time! We will review your application and get back to you soon."

            # Append chatbot's response
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)

if __name__ == "__main__":
    main()
