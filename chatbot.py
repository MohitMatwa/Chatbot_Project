from langchain.llms import HuggingFaceHub
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from prompts import SYSTEM_PROMPT
from config import HUGGINGFACE_API_KEY
from utils import validate_email, validate_phone
import streamlit as st

class HiringChatbot:
    def __init__(self):
        self.llm = HuggingFaceHub(repo_id="mistralai/Mistral-7B-Instruct-v0.1", huggingfacehub_api_token=HUGGINGFACE_API_KEY)
        self.memory = ConversationBufferMemory()
        self.chain = LLMChain(llm=self.llm, memory=self.memory, prompt=PromptTemplate.from_template("{input}"))
        self.questions = [
            ("name", "What is your full name?"),
            ("email", "Please enter your email address."),
            ("phone", "What is your phone number?"),
            ("experience", "How many years of experience do you have?"),
            ("position", "What position are you applying for?"),
            ("location", "Where are you currently located?"),
            ("tech_stack", "Tell me about your technical skills, expertise, and the tools or technologies you are comfortable working with.")
        ]
    
    def get_next_question(self):
        awaiting_input = st.session_state.awaiting_input
        for field, question in self.questions:
            if awaiting_input == field:
                return question
        return "Thank you! We will process your application and get back to you soon."
    
    def process_response(self, user_input):
        exit_keywords = ["quit", "exit", "stop", "end", "bye"]  # List of exit words

        if user_input.lower() in exit_keywords:
            st.session_state.conversation_ended = True
            return "END_CONVERSATION"

        awaiting_input = st.session_state.awaiting_input
        collected_info = st.session_state.collected_info

        casual_responses = ["good work", "nice job", "thank you", "well done", "great", "awesome", "ok", "cool"]
    
        if user_input.lower() in casual_responses:
            return "I'm glad you found it helpful! Let me know if you have any questions or need more information."
        

        more_questions_requests = ["generate some more questions", "give me more questions", "more questions please", "ask me more questions"]

        if user_input.lower() in more_questions_requests:
            # Ensure there is a valid tech stack before generating additional questions
            tech_stack = collected_info.get("tech_stack", "")
            if not tech_stack:
                return "Could you specify which technical skills you'd like questions for?"
            return self.generate_technical_questions(tech_stack.split(","), follow_up=True)

        if awaiting_input == "email" and not validate_email(user_input):
            return "Invalid email format. Please enter a valid email."
        if awaiting_input == "phone" and not validate_phone(user_input):
            return "Invalid phone number. Please enter a valid number."
        if awaiting_input == "experience":
            if not user_input.isdigit():  # Ensures only numeric input
                return "Invalid input. Please enter your years of experience as a number (e.g., 3, 5, 10)."
            user_input = int(user_input)
        if awaiting_input in ["position", "location"]:
            if user_input.isdigit():
                return f"Invalid input. {awaiting_input.capitalize()} should be a text-based response, not a number."


        collected_info[awaiting_input] = user_input
        next_index = [i for i, (field, _) in enumerate(self.questions) if field == awaiting_input][0] + 1

        if next_index < len(self.questions):
            st.session_state.awaiting_input = self.questions[next_index][0]
            return self.get_next_question()
        else:
            return self.generate_technical_questions(collected_info.get("tech_stack", "").split(","))


    def generate_technical_questions(self, tech_stack, follow_up=False):
        formatted_tech_stack = ', '.join(tech_stack).strip()

        # Adjust introduction based on whether it's a follow-up
        if follow_up:
            intro = "Here are some additional technical questions to further evaluate your skills:\n"
        else:
            intro = (
                "Thank you for sharing your expertise. "
                "To assess your skills, problem-solving approach, and industry knowledge, "
                "here are some relevant questions tailored to your background:\n"
            )

        # Generate AI-based technical questions
        prompt = f"Generate 3-5 technical questions for a candidate proficient in {formatted_tech_stack}."
        raw_questions = self.chain.run(prompt)

        # Remove unnecessary system-generated instructions from the AI response
        clean_questions = raw_questions.strip()

        # Ensure no unwanted prompt text appears in the response
        if "Generate 3-5 technical questions" in clean_questions:
            clean_questions = clean_questions.split("\n", 1)[-1].strip()  # Remove the first line if it repeats the prompt

        return f"{intro}\n{clean_questions}"


