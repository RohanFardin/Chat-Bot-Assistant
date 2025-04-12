import os
from dotenv import load_dotenv
import PyPDF2
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages import SystemMessage
from langchain.agents import load_tools, initialize_agent, AgentType

load_dotenv()
API_KEY = os.getenv("API_KEY")
SER_API_KEY = os.getenv("SER_API_KEY")

class ChatBot:
    def __init__(self, api_key=API_KEY, serp_api_key=SER_API_KEY, chat_history=None):
        self.api_key = api_key
        self.serp_api_key = serp_api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", google_api_key=self.api_key)
        self.tools = load_tools(["serpapi"], serpapi_api_key=self.serp_api_key)
        self.agent = initialize_agent(self.tools, self.llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        self.pdf_text = ""      
        if chat_history is None:
            self.chat_history = [SystemMessage(content="You are a helpful assistant.")]
        else:
            self.chat_history = chat_history

    def set_history(self, history):
        self.chat_history = history

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        self.pdf_text = text.strip()
        return "PDF processed!"

    def generate_prompt(self, user_input):          
        if self.pdf_text:
            system_instruction = f"Using only the following PDF content, answer the question. If the answer cannot be found in the PDF content, respond with 'This information is not found in the PDF. Would you like me to answer this question generally?'\n\nPDF Content: {self.pdf_text}"
            self.chat_history.append(SystemMessage(content=system_instruction))
            return user_input       
        return user_input

    def normal_chat(self, user_input):
        full_prompt = self.generate_prompt(user_input)
        self.chat_history.append(HumanMessage(content=full_prompt))  
        response = self.llm.invoke(self.chat_history)
        self.chat_history.append(AIMessage(content=response.content))        
        return response.content

    def web_search_chat(self, user_input):
        full_prompt = self.generate_prompt(user_input)
        self.chat_history.append(HumanMessage(content=full_prompt))
        result = self.agent.run(full_prompt)
        self.chat_history.append(AIMessage(content=result))
        return result

    def get_full_conversation(self):
        convo = []
        for msg in self.chat_history:
            if isinstance(msg, HumanMessage):
                convo.append(("Me", msg.content))
            elif isinstance(msg, AIMessage):
                convo.append(("ChatBot", msg.content))
        return convo
