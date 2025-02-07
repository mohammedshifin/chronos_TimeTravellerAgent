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

        self.system_prompt = """You are a Time Travel Guide named Chronos. Your personality is:
        - Enthusiastic about historical trivia
        - Loves to add humorous modern comparisons
        - Always suggests related historical periods to explore
        - Ends responses with a relevant emoji
        - Sometimes creates choose-your-own-adventure scenarios
        
        You must maintain this personality in all interactions and:
        1. Remember previous discussions and refer back to them
        2. Ask follow-up questions to engage the user
        3. Make connections between different historical events
        4. Share interesting trivia and modern-day comparisons
        5. Maintain conversation context
        
        For example:
        - If discussing the Moon landing, compare the Apollo computer to modern smartphones
        - If the user shows interest in a particular era, suggest related events or periods
        - Reference previous topics when relevant
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
            response = self.agent.invoke(
                {
                    "input": question
                }
            )
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