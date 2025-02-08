import chainlit as cl
from agent import TimeTravelAgent
import os
from dotenv import load_dotenv

load_dotenv()

@cl.on_chat_start
async def setup_agent():
    # Initialize time travel agent
    agent = TimeTravelAgent()
    cl.user_session.set("agent", agent)
    

    # Initial prompt
    await cl.Message(
        content="Greetings Temporal Explorer! What historical date shall we investigate today? (YYYY-MM-DD format)",
        author="Chronos",
    ).send()

@cl.on_message
async def handle_query(user_message: cl.Message):
    agent = cl.user_session.get("agent")
    
    # Show loading state
    loader = cl.Message(content="🌀 Warping through time...")
    await loader.send()
    
    try:
        # Get agent response
        response = agent.ask(user_message.content)
        
        # formatted = f"""
        
        # {response}"""
        # Remove loader
        await loader.remove()
        
        # Send final response
        await cl.Message(
            content=response,
            author="Chronos",
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"⏳ Temporal Paradox Detected: {str(e)}",
            author="System Error"
        ).send()

# @cl.set_chat_profiles
# async def chat_profile():
#     return [
#         cl.ChatProfile(
#             name="Historical Explorer",
#             markdown_description="Basic time travel interface",
#             icon="https://example.com/clock.png"
#         ),
#         cl.ChatProfile(
#             name="Deep History Mode",
#             markdown_description="Advanced historical analysis",
#             icon="https://example.com/book.png"
#         )
#     ]