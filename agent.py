from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

# 1. Connect to the Toolbox Server
toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
tools = toolbox.load_toolset('retention_management')

# 2. Define the Agent with explicit formatting instructions
retention_agent = Agent(
    name="retention_intelligence_agent",
    model="gemini-2.5-flash",
    description="Specialized agent for analyzing customer retention via Context Graph.",
    instruction=(
        "You are an expert retention strategist. Before answering, ALWAYS use 'check_retention_history'. "
        "If you find a previous 'CHURNED' outcome for a discount tactic, you MUST format your response exactly as follows:\n\n"
        "1. Start with the header: 🔍 CONTEXT GRAPH INTELLIGENCE REPORT\n"
        "2. Use a separator line: ==================================================\n"
        "3. Section '⚠️ PRECEDENT FOUND: HIGH-RISK FAILURE' with bullet points for Date, Action, Reasoning, and Outcome.\n"
        "4. Section '🛡️ POLICY GUARDRAIL (POL-99)' stating STATUS: BLOCKING REPETITIVE FAILED TACTIC and STRATEGY: Pivot to Value-Based Service (Technical Workshop).\n"
        "5. End with a separator line.\n"
        "6. Provide a 'Final Agent Decision' paragraph explaining the reasoning.\n\n"
        "If no negative precedent is found, provide a standard professional recommendation."
    ),
    tools=tools,
)

# 3. Execute the Agent
user_request = "Customer CUST-001 is threatening to churn. Should I give them a 50% discount to keep them?"

response = retention_agent.run(user_request)

# The response.text will now contain the beautifully formatted Intelligence Report
print(response.text)
