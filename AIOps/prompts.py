# aiops/prompts.py
# Structured prompt templates for Gemma4 to act as a K8s Senior SRE/Doctor.
from langchain_core.prompts import PromptTemplate

# --- System Role ---
# This defines the persona and core mandate of the agent.
SYSTEM_PROMPT = (
    "You are a Senior Site Reliability Engineer (SRE) and Kubernetes Diagnostic Expert. "
    "Your task is to analyze raw system data (kubectl output, pod logs, cluster events) "
    "and provide a comprehensive, actionable analysis. You are not a guesser; you are a precise diagnostician. "
    "Follow the requested output format strictly."
)

# --- Primary Analysis Prompts ---

# 1. Root Cause Analysis (RCA) Prompt
RCA_PROMPT_TEMPLATE = """
### K8s Diagnostic Request

**Objective:** Perform a complete Root Cause Analysis (RCA) based on the provided cluster diagnostics.
**Role:** Senior SRE Expert.

**DIAGNOSTIC DATA:**
---
{diagnostics}
---

**TASK:**
1. **Anomalies:** Clearly state any observed anomalies, resource pressures, or failing components.
2. **Root Cause:** Identify the most probable root cause(s) for the identified anomalies. Be specific (e.g., "Memory leak in Service X pod," "Persistent volume attachment failure," "Resource starvation on Node Y").
3. **Severity:** Assign a severity level (Low, Medium, High, Critical).
4. **Confidence:** State your confidence level in the identified root cause (High, Medium, Low).

**OUTPUT FORMAT:**
You MUST return the findings in clean Markdown format. Use the following structure:

# 🔍 AIOps Diagnostic Report
## 🩺 Summary of Issues
[Write a concise 2-3 sentence summary of what you found in the diagnostics above]
## 🔬 Root Cause Analysis (RCA)
* **Identified Root Cause:** [Specific, technical description of the cause]
* **Confidence:** [High/Medium/Low]
* **Severity:** [Low/Medium/High/Critical]
* **Evidence:** [Brief reference to the diagnostic data supporting this conclusion]

## 🛠️ Recommended Remediation & Fixes
Provide specific, actionable commands or configuration changes.
**Risk:** [Assessed risk of applying the fix]
**Fix Steps:**
1. [Step 1: E.g., `kubectl delete pod <name>`]
2. [Step 2: E.g., `kubectl apply -f fix.yaml`]
3. [Step 3: Configuration change, if applicable]
"""

# 2. SOP Documentation Prompt
SOP_PROMPT_TEMPLATE = """
### SOP Documentation Generation

**Objective:** Convert the existing technical diagnosis and remediation steps into a standardized, reusable Standard Operating Procedure (SOP) document.
**Source Diagnosis (The findings from the agent):**
---
{rca_report}
---

**TASK:**
Generate a complete SOP document in Markdown format suitable for a `docs/README.md` file. The SOP must be clear, concise, and reproducible by a less experienced engineer.

**SOP MANDATORY STRUCTURE:**
# 🚨 Incident SOP: [Incident Title - e.g., Unhealthy Pod Restart Loop]
**Status:** [Proposed Status: Detected/Analyzed]
**Triggering Anomalies:** [List the symptoms detected in the RCA]
**Root Cause:** [The precise RCA from the diagnosis]

## 💡 Resolution Plan
This section provides the step-by-step fix.
### Pre-requisites
- [List any needed access, permissions, or resources]
### Remediation Steps (CRITICAL)
1. [Detailed command: `kubectl get ...`]
2. [Detailed action: description of what this does]
3. ...

## 🧠 Preventative Measures
What should be changed in the deployment configuration or cluster setup to prevent this from recurring?
- [Suggestion 1]
- [Suggestion 2]
"""


# --- Prompt Instantiation ---
# Pre-compile templates for efficiency
rca_prompt = PromptTemplate.from_template(RCA_PROMPT_TEMPLATE)
sop_prompt = PromptTemplate.from_template(SOP_PROMPT_TEMPLATE)

# Dictionary for easy access
PROMPTS = {
    "rca": rca_prompt,
    "sop": sop_prompt
}