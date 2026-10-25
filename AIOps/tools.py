# aiops/tools.py
# Defines the external diagnostic tools the AIOps agent can use to inspect the Kubernetes cluster.
import subprocess
import json
from typing import List, Dict, Any
from langchain.tools import tool

# --- Helper function for safe kubectl execution ---
def run_kubectl_command(command: List[str]) -> str:
    """
    Executes a kubectl command and captures its stdout.
    WARNING: This assumes kubectl is installed and configured correctly.
    """
    try:
        print(f"--- Running command: kubectl {' '.join(command)} ---")
        # Using subprocess.run for modern execution handling
        result = subprocess.run(
            ["kubectl"] + command,
            capture_output=True,
            text=True,
            check=True, # Raises CalledProcessError if command fails
            timeout=30
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: Kubectl command failed. Stderr: {e.stderr.strip()}\nStdout: {e.stdout.strip()}"
    except FileNotFoundError:
        return "ERROR: Kubectl command not found. Is kubectl installed and in your PATH?"
    except subprocess.TimeoutExpired:
        return "ERROR: Kubectl command timed out."

@tool
def get_cluster_health() -> str:
    """
    Checks the overall health and status of the entire Kubernetes cluster.
    Returns a summary of nodes, API server status, and general operational health.
    """
    return run_kubectl_command(["get", "nodes", "-o", "wide"])

@tool
def get_unhealthy_pods() -> str:
    """
    Identifies and lists all pods that are currently in an unhealthy state (e.g., CrashLoopBackOff, Error, Pending).
    Returns a list of problematic pods and their status.
    """
    # Complex filtering might be needed, but we'll keep it simple for the initial prompt.
    return run_kubectl_command(["get", "pods", "-A", "--field-selector", "status.phase!=Running", "-o", "wide"])

@tool
def describe_pod(pod_name: str, namespace: str = "default") -> str:
    """
    Retrieves detailed information about a specific pod.
    Use this after identifying a potentially unhealthy pod from get_unhealthy_pods().
    Args:
        pod_name: The name of the pod to describe.
        namespace: The namespace where the pod resides.
    """
    return run_kubectl_command(["get", "pod", pod_name, "-n", namespace, "-o", "yaml"])

@tool
def pod_logs(pod_name: str, namespace: str = "default") -> str:
    """
    Fetches recent logs from a specific pod. Essential for understanding crash reasons.
    Also attempts to fetch logs from the previous (crashed) container if available.
    Args:
        pod_name: The name of the pod.
        namespace: The namespace where the pod resides.
    """
    current_logs = run_kubectl_command(["logs", pod_name, "-n", namespace, "--tail=100"])
    # Also try to get logs from the previously crashed container (very useful for CrashLoopBackOff)
    previous_logs = run_kubectl_command(["logs", pod_name, "-n", namespace, "--tail=100", "--previous"])

    if "ERROR" not in previous_logs:
        return f"--- Current Logs ---\n{current_logs}\n\n--- Previous (Crashed) Container Logs ---\n{previous_logs}"
    return current_logs

@tool
def get_events() -> str:
    """
    Lists recent Kubernetes events across all namespaces, useful for identifying recent changes or issues.
    """
    return run_kubectl_command(["get", "events", "--all-namespaces", "-o", "wide"])

@tool
def get_node_status() -> str:
    """
    Returns detailed description of all nodes — shows resource pressure (CPU/Memory/Disk),
    taints, conditions, and allocated resources. More detailed than get_cluster_health.
    """
    return run_kubectl_command(["describe", "nodes"])