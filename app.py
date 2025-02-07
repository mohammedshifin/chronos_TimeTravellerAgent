import chainlit as cl
from agent import TimeTravelAgent
import os
from dotenv import load_dotenv

load_dotenv()

@cl.on_chat_start
async def setup_agent():
    # Initialize time travel agent
    agent = TimeTravelAgent(api_key=os.getenv("GOOGLE_API_KEY"))
    cl.user_session.set("agent", agent)
    
    # Welcome message with historical header
    header = """
    <div style="text-align: center; padding: 20px; background: #f0f0f0; border-radius: 10px;">
        <h1 style="color: #2c3e50;">🕰️ Chronos Temporal Interface</h1>
        <p>Your Gateway to Historical Exploration</p>
    </div>
    """
    await cl.Message(content=header, author="System").send()
    
    # Initial prompt
    await cl.Message(
        content="Greetings Temporal Explorer! What historical date shall we investigate today? (YYYY-MM-DD format)",
        author="Chronos",
        language="markdown"
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
        
        # Format with markdown
        formatted = f"""
        **Historical Analysis Complete**
        
        {response}
        
        ---
        _Which temporal dimension shall we explore next?_
        """
        
        # Remove loader
        await loader.remove()
        
        # Send final response
        await cl.Message(
            content=formatted,
            author="Chronos",
            language="markdown"
        ).send()
        
    except Exception as e:
        await cl.Message(
            content=f"⏳ Temporal Paradox Detected: {str(e)}",
            author="System Error"
        ).send()

@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="Historical Explorer",
            markdown_description="Basic time travel interface",
            icon="https://example.com/clock.png"
        ),
        cl.ChatProfile(
            name="Deep History Mode",
            markdown_description="Advanced historical analysis",
            icon="https://example.com/book.png"
        )
    ]