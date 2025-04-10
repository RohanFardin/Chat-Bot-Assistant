import os
from dotenv import load_dotenv
import PyPDF2
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import HumanMessage, AIMessage
from langchain_core.messages import SystemMessage
from langchain.utilities import SerpAPIWrapper
from langchain.agents import load_tools, initialize_agent, AgentType

load_dotenv()
API_KEY = os.getenv("API_KEY")
SER_API_KEY = os.getenv("SER_API_KEY")

class ChatBot:
    def __init__(self, api_key=API_KEY, serp_api_key=SER_API_KEY):
        self.api_key = api_key
        self.serp_api_key = serp_api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", google_api_key=self.api_key)
        self.pdf_text = ""
        self.tools = load_tools(["serpapi"], serpapi_api_key=self.serp_api_key)
        self.agent = initialize_agent(self.tools, self.llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        self.chat_history = [SystemMessage(content="You are a helpful assistant.")]
        

    def normal_chat(self, user_input):
        self.chat_history.append(HumanMessage(content=user_input))
        response = self.llm.invoke(self.chat_history) 
        self.chat_history.append(AIMessage(content=response.content))
        return response.content
     
    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        self.pdf_text = text  
        return "PDF text extracted successfully!"

    def answer_from_pdf(self, user_input):
        self.chat_history.append(HumanMessage(content=f"Answer based on the PDF: {self.pdf_text}"))
        self.chat_history.append(HumanMessage(content=user_input))
        response = self.llm.invoke(self.chat_history)
        self.chat_history.append(AIMessage(content=response.content))
        return response.content

    def web_search_chat(self, user_input):
        self.chat_history.append(HumanMessage(content=user_input))
        return self.agent.run(user_input)
   
        
   