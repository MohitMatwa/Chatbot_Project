# Chatbot_Project

The TalentScout Hiring Assistant is an AI-powered chatbot designed to facilitate the hiring process by collecting applicant details, assessing technical skills, and guiding users through structured conversations. The chatbot is built using Streamlit for the interface, LangChain for AI-driven responses, and Hugging Face’s Mistral-7B-Instruct-v0.1 as the primary language model.
The chatbot is structured across multiple Python files, each handling a different aspect of its functionality. Below is a comprehensive breakdown of its execution flow, including every function and mechanism involved in its operation.

1. Application Entry Point (app.py)
Step-by-Step Execution Flow
When the chatbot is launched, execution begins in the app.py file, which serves as the main entry point. It initializes Streamlit, sets up session state variables, and starts the chatbot’s conversation logic.
1.1 Initializing Session State
Streamlit’s st.session_state is used to manage conversation history, track input progress, and ensure smooth execution.
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

1.2 Main Execution Flow
The chatbot execution follows these steps:
Instantiate the HiringChatbot class from chatbot.py.


Handle the greeting if it hasn’t been displayed yet.


Continuously process user input and generate responses.


Display chatbot responses in Streamlit’s interface.


def main():
    chatbot = HiringChatbot()
    if not st.session_state.greeted:
        chatbot.greet_user()
        st.session_state.greeted = True

    user_input = st.text_input("You:")
    if user_input:
        response = chatbot.handle_input(user_input)
        st.session_state.messages.append(("User", user_input))
        st.session_state.messages.append(("Bot", response))





2. Core Chatbot Logic (chatbot.py)
The HiringChatbot class is responsible for:
Managing conversation flow.


Asking questions and collecting responses.


Generating technical questions.


Handling conversation termination.


2.1 Greeting the User
The chatbot greets users when the conversation starts. The greeting message is only sent once per session.
def greet_user(self):
    greeting = "Hello! Welcome to TalentScout Hiring Assistant. Let's get started with your application."
    st.session_state.messages.append(("Bot", greeting))

2.2 Handling User Input
The handle_input() function processes user responses, validates input, and determines the next question to ask.
def handle_input(self, user_input):
    awaiting_input = st.session_state.awaiting_input
    
    if awaiting_input == "email" and not validate_email(user_input):
        return "Invalid email format. Please enter a valid email."
    if awaiting_input == "phone" and not validate_phone(user_input):
        return "Invalid phone number. Please enter a valid number."
    if awaiting_input == "experience" and not user_input.isdigit():
        return "Invalid input. Please enter your years of experience as a number."
    
    st.session_state.collected_info[awaiting_input] = user_input
    next_question = self.get_next_question()
    return next_question


3. Handling Question Flow in Depth
The chatbot follows a structured question sequence. get_next_question() determines the next question to ask.
3.1 Question Order and Logic
Each question is asked in a specific sequence to ensure logical progression. The chatbot checks which questions have already been answered and determines the next question dynamically.
def get_next_question(self):
    for field, question in self.questions:
        if field not in st.session_state.collected_info:
            st.session_state.awaiting_input = field
            return question
    st.session_state.awaiting_input = None
    return "Thank you! We will process your application and get back to you soon."

This function ensures that the chatbot:
Asks all necessary questions before concluding.


Does not repeat already answered questions.


Moves smoothly through the hiring process.



4. Generating Technical Questions (prompts.py) - Deep Dive
Once a candidate provides their technical skills (tech stack), the chatbot dynamically generates questions using an AI-powered model.
4.1 AI-Based Question Generation
The chatbot formulates questions based on the candidate’s skills using the generate_technical_questions() function.
def generate_technical_questions(self, tech_stack, follow_up=False):
    formatted_tech_stack = ', '.join(tech_stack).strip()
    prompt = f"Generate 3-5 technical questions for a candidate proficient in {formatted_tech_stack}."
    raw_questions = self.chain.run(prompt)
    clean_questions = raw_questions.strip()
    return f"Here are some technical questions:\n{clean_questions}"

This ensures that candidates receive tailored technical questions that are relevant to their expertise.


5. Handling Special Cases & Exit Conditions - Expanded
The chatbot detects specific inputs to handle special cases such as exits, requests for additional questions, or casual responses.
5.1 Recognizing Exit Commands
exit_keywords = ["quit", "exit", "stop", "end", "bye"]
if user_input.lower() in exit_keywords:
    st.session_state.conversation_ended = True
    return "END_CONVERSATION"

This allows users to exit the chat at any time by typing keywords like "quit" or "bye".
5.2 Handling Additional Questions Requests
If a candidate asks for more questions, the chatbot can generate follow-up questions dynamically:
if "more questions" in user_input.lower():
    return self.generate_technical_questions(st.session_state.collected_info["tech_stack"], follow_up=True)


6. Ending the Conversation - In-Depth Process
Once all required information is collected, the chatbot acknowledges the user’s input and ends the session.
6.1 Final Confirmation Message
def conclude_conversation(self):
    return "Thank you for your time! We will review your application and get back to you soon."

6.2 Setting End Flag
To ensure no further input is processed, the chatbot sets conversation_ended = True.
st.session_state.conversation_ended = True

This guarantees that once the interview process is complete, the chatbot does not prompt the user for more responses.

Conclusion
The TalentScout Hiring Assistant chatbot efficiently collects candidate details, validates responses, and dynamically generates relevant technical questions. Its AI-driven conversation flow ensures an engaging and structured interview experience. With exit handling, logical question flow, and AI-powered evaluation, it streamlines the hiring process for both recruiters and applicants.

