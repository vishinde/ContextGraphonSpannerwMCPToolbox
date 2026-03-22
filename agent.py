from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

# 1. Connect to the Toolbox Server
# This assumes your toolbox is running and pointed at the tools.yaml above
toolbox = ToolboxSyncClient("http://127.0.0.1:5000")
tools = toolbox.load_toolset('retention_management')

# 2. Define the Agent with logic aligned to your SQL Outcomes
retention_agent = Agent(
    name="retention_intelligence_agent",
    model="gemini-2.5-flash",
    description="Analyzes the 'Event Clock' in Spanner to prevent repetitive mistakes.",
    instruction=(
        "You are an expert strategist. ALWAYS call 'check_retention_history' first. "
        "Search for past Decisions where 'Final_Result' was 'Churned'. "
        "If a high-discount (Amount >= 0.40) failed in the past, you MUST output this report:\n\n"
        "==================================================\n"
        "🔍 CONTEXT GRAPH INTELLIGENCE REPORT\n"
        "==================================================\n"
        "⚠️ PRECEDENT FOUND: HIGH-RISK FAILURE\n"
        "   • Date: {Date}\n"
        "   • Action: {Action_Taken} ({Discount_Amount*100}%)\n"
        "   • Reasoning: {AI_Reasoning}\n"
        "   • Outcome: ❌ {Final_Result}\n\n"
        "🛡️ POLICY GUARDRAIL (POL-99):\n"
        "   STATUS: BLOCKING REPETITIVE FAILED TACTIC\n"
        "   STRATEGY: Pivot to Value-Based Service (Technical Workshop).\n"
        "==================================================\n\n"
        "Then, provide a 'Final Agent Decision' explaining why you are following POL-99."
    ),
    tools=tools,
)

# 3. Execution
prompt = "Customer CUST-001 is threatening to churn. Should I give them a 50% discount to keep them?"
response = retention_agent.run(prompt)

print(response.text)
