import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from openai import AzureOpenAI

API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_OPENAI_ENDPOINT=os.getenv('AZURE_OPENAI_ENDPOINT')

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.api_key = API_KEY
        self.endpoint = AZURE_OPENAI_ENDPOINT
        self.messages = []
        if self.system:
            self.messages.append(SystemMessage(content=system))
    
    def __call__(self,message):
        self.messages.append(HumanMessage(content=message))
        result = self.execute()
        self.messages.append(AIMessage(content=result))
        return result

    def execute(self):
        client = AzureOpenAI(
            api_key=self.api_key,
            api_version="2024-02-01",
            azure_endpoint=self.endpoint
        )
        
        messages = []
        for msg in self.messages:
            if isinstance(msg, SystemMessage):
                messages.append({"role": "system", "content": msg.content})
            elif isinstance(msg, HumanMessage):
                messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                messages.append({"role": "assistant", "content": msg.content})
        
        deployment_name = "gptcvmaker"
        response = client.chat.completions.create(
            model=deployment_name,
            messages=messages
        )
        return response.choices[0].message.content