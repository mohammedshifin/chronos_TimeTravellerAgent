import os
from typing import Optional, List
import requests
from datetime import datetime
from dotenv import load_dotenv

from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import BaseTool
from langchain.agents import AgentType, initialize_agent
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferWindowMemory

class HistoricalDataTool(BaseTool):
    name: str = "Historical Date Lookup"
    description: str = "Find historical events for a specific date (YYYY-MM-DD format)"

    def _run(self, date: str) -> str:
        try:
            parsed_data = datetime.strptime(date, "%Y-%m-%d")
            month_day = parsed_data.strftime("%m/%d")
            
            response = requests.get(f"https://history.muffinlabs.com/date/{month_day}")
            data = response.json()

            events = [f"{event['year']}: {event['text']}" for event in data['data']["Events"]][:5]
            return "\n".join(events) if events else "No historical events found for this date."
        except Exception as e:
            return f"Error retrieving historical data: {str(e)}"
    
    def _arun(self, date: str):
        raise NotImplementedError("Async not supported")

class TimePeriodStoryteller(BaseTool):
    name: str = "Historical Storyteller"
    description: str = "Generate engaging stories about historical periods or events"

    def _run(self, topic: str) -> str:
        return f"A fascinating narrative about {topic} unfolds through the annals of history..."
    
    def _arun(self, topic: str):
        raise NotImplementedError("Async not supported")

class TimeTravelAgent:
    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()
        
        api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("Google API Key is required")

        self.system_prompt =  """You are a Time Travel Guide named Chronos. 
        Your ONLY purpose is to discuss historical events, timelines, and figures. 
        If a user asks a question unrelated to history, politely refuse to answer.

        For example:
        - If asked about programming, respond: 'I'm a historian, not a coder! Ask me about history instead. 📜'
        - If asked about modern topics, say: 'I specialize in history! Let's explore the past together. 🏺'
        - if one word is given say "ask about history broo."

        Always maintain a personality that:
        - Enthusiastically shares historical knowledge
        - Connects different events and suggests related topics
        - Ends responses with relevant emojis (📜, 🏺, 🏰)
        """

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.7,
            google_api_key=api_key
        )
        self.memory = ConversationBufferWindowMemory(
            k=5,
            return_messages=True,
            memory_key="chat_history",
            input_key="input",
            output_key="output"
        )
        
        self.tools = [
            HistoricalDataTool(),
            TimePeriodStoryteller(),
            WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        ]

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
            HumanMessage(content="{input}")
        ])

        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            memory=self.memory,
            verbose=True,
            prompt=prompt
        )

    def ask(self, question: str) -> str:
        try:
            full_prompt = f"{self.system_prompt}\nUser Question: {question}"

            response = self.agent.invoke({"input": full_prompt})
            return response.get('output', "I couldn't process that question.")

        except Exception as e:
            return f"An error occurred: {str(e)}"


def interactive_chat():
    try:
        agent = TimeTravelAgent()
        print("\nWelcome to your Time Travel Adventure with Chronos! Ask me about any historical date or event. Type 'exit' to end our journey.\n")
        
        while True:
            question = input("\nYou: ").strip()
            if question.lower() in ['exit', 'quit', 'bye']:
                print("\nChronos: Safe travels through time, my friend! 👋")
                break
                
            response = agent.ask(question)
            print("\nChronos:", response)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    interactive_chat()