# AIOps CLI Agent

A lightweight, open-source CLI agent designed to provide Autonomous AIOps capabilities for local Kubernetes clusters running on Kind.

This tool leverages a local Large Language Model (Gemma4 via Ollama) to function as an expert Senior SRE/Doctor, autonomously detecting anomalies, generating root cause analysis (RCA), proposing remediation steps, and automatically generating standardized Standard Operating Procedures (SOPs).

## ⚙️ Architecture Overview

The system is structured as a modular Python package:

- **`tools.py`**: Contains wrappers for `kubectl` commands, allowing the agent to inspect the cluster state.
- **`prompts.py`**: Houses the specialized System Prompts that guide Gemma4 to act as a domain expert (Senior SRE).
- **`agent.py`**: The core orchestrator, using LangChain/LangGraph patterns to connect the LLM with the diagnostic tools (ReAct Agent).
- **`cli.py`**: The user-facing interface, allowing commands like `aiops doctor scan` and `aiops doctor fix`.
- **`sop.py`**: Responsible for formatting the final diagnosis into human-readable documentation (SOPs).

## 🚀 Getting Started

1. **Prerequisites:**
   - Python 3.10+
   - Ollama installed and running with the Gemma4 model available (`ollama run gemma4`).
   - `kubectl` configured to point to your local Kind cluster.

2. **Installation:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Usage:**
   ```bash
   aiops doctor scan  # Initial health check and anomaly detection
   aiops doctor analyze # Deep dive on identified issues (RCA generation)
   aiops doctor fix     # Generate and suggest remediation commands
   aiops doctor document # Generate and save SOPs (README.md)
   ```

## 🧭 Usage Flow

The intended flow is iterative:
1. **`scan`**: Collects raw data via `tools.py`.
2. **`analyze`**: Passes raw data to the `agent.py` to generate RCA via `prompts.py`.
3. **`fix`**: Takes RCA/Remediation suggestions and validates them.
4. **`document`**: Uses `sop.py` to compile the findings into a structured `docs/README.md` SOP.