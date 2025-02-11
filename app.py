import chainlit as cl
from agent import TimeTravelAgent
import os
from dotenv import load_dotenv

load_dotenv()

@cl.on_chat_start
async def setup_agent():
    agent = TimeTravelAgent()
    cl.user_session.set("agent", agent)
    
    await cl.Message(
        content="Greetings Temporal Explorer! What historical date shall we investigate today? (YYYY-MM-DD format) Or ask 'what if' questions for alternate history scenarios!",
        author="Chronos",
    ).send()

@cl.on_message
async def handle_query(user_message: cl.Message):
    agent = cl.user_session.get("agent")
    
    try:
        user_query = user_message.content.lower()

        if "what if" in user_query:
            response = agent.ask(f"Alternate History: {user_message.content}")
        elif "story mode" in user_query or "first-person" in user_query or "narrative" in user_query:
            response = agent.ask(f"Sory Mode: {user_message.content}") 
        else:
            response = agent.ask(user_message.content)
        await cl.Message(
            content=response,
            author="Chronos",
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"⏳ Temporal Paradox Detected: {str(e)}",
            author="System Error"
        ).send()
