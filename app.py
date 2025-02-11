import chainlit as cl
from agent import TimeTravelAgent
import os
from dotenv import load_dotenv

load_dotenv()

@cl.on_chat_start
async def setup_agent():
    agent = TimeTravelAgent()
    cl.user_session.set("agent", agent)
    instructions = (
        "Greetings Temporal Explorer! Here are your instructions:\n\n"
        "• **Historical Date Query:** Enter a date in the format `YYYY-MM-DD` to see historical events.\n"
        "• **Alternate History Query:** Start your query with 'what if' to explore alternate history scenarios.\n"
        "• **Story Mode:** Include 'story mode', 'first-person', or 'narrative' in your query for an immersive historical experience.\n\n"
        "Choose an option and begin your journey through time!"
    )
    await cl.Message(
        content=instructions,
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
