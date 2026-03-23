import asyncio
import warnings
import os
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from toolbox_core import ToolboxSyncClient

# Suppress the GenAI Part warning for a cleaner console
warnings.filterwarnings("ignore", category=UserWarning, module="google_genai")

PROJECT_ID = "xxx"
# Set these before initializing your Runner
os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1" # or your preferred region
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

async def run_retention_logic(text_input):
    # 1. Setup Toolbox
    toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
    
    try:
        graph_tools = toolbox.load_toolset('my_graph_toolset')

        # Define the Intelligence Report template within the Agent instructions
        report_instruction = (
            "You are an expert retention strategist. Follow these steps for every query:\n"
            "1. Run 'check_retention_history' for the customer.\n"
            "2. IF a previous 'Churned' outcome is found for a discount, run 'get_policy_details' for 'POL-99'.\n"
            "3. Generate the report using the following format:\n\n"
            "==================================================\n"
            "🔍 CONTEXT GRAPH INTELLIGENCE REPORT\n"
            "==================================================\n"
            "⚠️ PRECEDENT FOUND: HIGH-RISK FAILURE\n"
            "   • Date: [Date from history]\n"
            "   • Action: [Action_Taken] ([Discount_Amount])\n"
            "   • Outcome: ❌ [Final_Result]\n\n"
            "🛡️ CORPORATE POLICY ENFORCEMENT:\n"
            "   • Policy: [Name from policy tool] ([policy_id])\n"
            "   • Rule: [rule_definition from policy tool]\n"
            "   • Status: [IF is_active=True, 'ACTIVE - BLOCKING REPETITIVE TACTIC']\n\n"
            "==================================================\n"
            "Final Agent Decision: [Synthesize the history and policy into a recommendation.]"
        )
        
        agent = Agent(
            name="retention_specialist",
            model="gemini-2.5-flash",
            instruction=report_instruction,
            tools=graph_tools
        )

        user_id="user_123"
        session_id="session_456"
        APP_NAME = "RetentionApp"

        await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )
        runner = Runner(app_name="RetentionApp", agent=agent, session_service=session_service)

        current_content = types.Content(role='user', parts=[types.Part(text=text_input)])

        # Single execution (no while True loop)
        async for event in runner.run_async(
            new_message=current_content,
            user_id=user_id, 
            session_id=session_id
        ):
            # Only print if there is actual text content (skips 'None' from function calls)
            if event.author and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text: # This filters out the 'None' lines
                    print(f"\n[{event.author}]: {text}")

    finally:
        # 2. Crucial: Close the toolbox to prevent 'Unclosed Session' errors
        toolbox.close() # If your version supports close, otherwise:
        #pass 

if __name__ == "__main__":
    session_service = InMemorySessionService()
    prompt = "Should I give CUST-001 a 50% discount?"
    try:
        asyncio.run(run_retention_logic(prompt))
    except KeyboardInterrupt:
        print("\nPipeline stopped by user.")
