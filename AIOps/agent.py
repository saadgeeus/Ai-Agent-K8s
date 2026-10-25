# aiops/agent.py
# Core orchestration logic: connecting the LLM (Gemma4 via Ollama) with the diagnostic tools.
from langchain_community.llms import Ollama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from typing import List, Dict, Any

# Import dependencies from local modules
from .tools import get_cluster_health, get_unhealthy_pods, describe_pod, pod_logs, get_events, get_node_status
from .prompts import SYSTEM_PROMPT, PROMPTS
from .config import MODEL_NAME, OLLAMA_BASE_URL  # Single source of truth

def initialize_tools() -> List[Tool]:
    """
    Creates a list of LangChain Tool objects from the diagnostic functions.
    """
    tools = [
        Tool(
            name="get_cluster_health",
            func=get_cluster_health,
            description="Use this tool to get a high-level overview of the cluster health (Nodes status, etc.). Use first for general health check."
        ),
        Tool(
            name="get_unhealthy_pods",
            func=get_unhealthy_pods,
            description="Use this tool to list all pods that are not running normally (CrashLoopBackOff, Error, Pending). Use this when scanning for issues."
        ),
        Tool(
            name="describe_pod",
            func=describe_pod,
            description="Use this tool to get detailed YAML information for a specific pod name and namespace. Use when a pod is flagged as unhealthy."
        ),
        Tool(
            name="pod_logs",
            func=pod_logs,
            description="Use this tool to retrieve the last 100 lines of logs for a specific pod. Use this to understand *why* a pod is failing."
        ),
        Tool(
            name="get_events",
            func=get_events,
            description="Use this tool to retrieve recent Kubernetes events, which often indicate recent configuration changes or system-wide issues."
        ),
        Tool(
            name="get_node_status",
            func=get_node_status,
            description="Use this tool to check the status of individual worker nodes, looking for resource pressure or node failures."
        ),
    ]
    return tools

def initialize_agent_executor() -> AgentExecutor:
    """
    Sets up and returns the complete ReAct Agent Executor for diagnosis.
    """
    tools = initialize_tools()

    # Initialize the Ollama LLM
    llm = Ollama(
        model=MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        temperature=0.1 # Keep temperature low for deterministic, diagnostic answers
    )

    # Use the RCA prompt as the core guide for the agent
    prompt = PROMPTS['rca']

    # Create the agent using the ReAct pattern
    agent = create_react_agent(llm, tools, prompt)

    # Create the executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True, # Set to True to see the agent's thought process (Actions/Observations)
        handle_parsing_errors=True
    )

    return agent_executor

def run_diagnosis(agent_executor: AgentExecutor, initial_query: str) -> str:
    """
    Runs the full diagnostic cycle using the agent.
    """
    print("🤖 Starting AIOps Diagnosis Cycle...")
    try:
        # The agent uses the initial query to decide which tools to call.
        result = agent_executor.invoke({"input": initial_query})
        return result["output"]
    except Exception as e:
        return f"❌ AIOps Diagnosis Failed: {e}"