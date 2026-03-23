This README is specifically tailored for the MCP (Model Context Protocol) version of your project. It highlights the modularity of the "Agentic Stack," showing how Spanner Graph becomes a plug-and-play "Wisdom Provider" for any MCP-compliant client.

🌐 Context Graph on Spanner (MCP Edition)
Modern AI agents often perform unreliably because they lack "Institutional Memory"—the ability to recollect which organizational decisions led to success and which led to costly mistakes.

This repository demonstrates the professional Agentic Stack on Google Cloud, using the Model Context Protocol (MCP) to bridge Spanner Graph with the Google ADK. This architecture allows for a decoupled, secure, and globally consistent "System of Intelligence".

🏗️ The Architecture: Decoupled Intelligence
Unlike the standalone version, this implementation uses the MCP Toolbox to expose Spanner Graph as a standardized set of tools.

Foundation: Google Cloud Spanner Graph — Storing the State, Event, and Policy clocks.

The Bridge: MCP Toolbox — A secure "handshake" that turns SQL/GQL queries into executable AI tools.

The Brain: Google ADK (Agent Development Kit) — Orchestrating the reasoning loop and enforcing governance.

📂 Repository Structure
agent.py: The ADK Agent that connects to the MCP Toolbox server to execute its "Institutional Memory" lookups.

tools.yaml: The configuration file defining the MCP tools, including check_retention_history and get_policy_details.

ContextGraph.sql: DDL/DML for Spanner Graph Nodes (Customers, Policies, Decisions, Outcomes) and Edges.

🚀 Getting Started
1. Initialize Spanner Graph
Apply the schema in ContextGraph.sql to your Spanner instance to seed your "Institutional Memory".

2. Start the MCP Toolbox
Launch the toolbox server to expose your Spanner tools over HTTP:

Bash
./toolbox --tools-file "tools.yaml"
Wait for the log: INFO: Initialized 2 tools: check_retention_history, get_policy_details.

3. Run the Agent
In a separate terminal, execute the ADK Agent:

Bash
python3 agent.py
🛡️ Why use the MCP Toolbox?
Security & Discovery: The toolbox handles the authentication and discovery of Spanner tools automatically.

Model Agnostic: Because it uses the Model Context Protocol, you can swap the ADK Agent for other MCP-compliant clients without rewriting your Spanner logic.

Dynamic Updates: Update your tools.yaml or your Spanner Policies table, and the Agent inherits the new "Wisdom" instantly without a code deploy.

💡 Key Takeaways
The State Clock: Spanner provides the real-time "Truth".

The Event Clock: The Graph provides the historical "Wisdom".

The Policy Guardrail: The ADK provides the necessary "Governance".
