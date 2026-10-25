# 🤖 AIOps — Autonomous Kubernetes Diagnostic Agent

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-ReAct_Agent-1C3C3C?style=for-the-badge)
![Ollama](https://img.shields.io/badge/Ollama-Gemma4-FF6B35?style=for-the-badge)
![Kubernetes](https://img.shields.io/badge/Kubernetes-kubectl-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Ek local, AI-powered SRE assistant jo aapke Kubernetes cluster ki problems automatically diagnose, analyze aur document karta hai — poori tarah offline.**

</div>

---

## 📖 Yeh Project Kya Hai?

**AIOps** ek Python-based command-line tool hai jo aapke Kubernetes cluster ka **automatic doctor** ban jaata hai.

Yeh tool ek **locally running AI model (Gemma4 via Ollama)** ko use karta hai jo ek experienced Senior SRE Engineer ki tarah kaam karta hai. Jab aap command chalate ho, yeh agent:

1. Khud `kubectl` commands chalata hai cluster ka data gather karne ke liye
2. Us data ko analyze karta hai problems dhundhne ke liye
3. Root cause (asli wajah) identify karta hai
4. Fix karne ke steps suggest karta hai
5. Ek proper SOP document bana ke save kar deta hai

**Khaasooyat:** Koi cloud nahi, koi API key nahi, sab kuch aapke apne machine pe hota hai.

---

## 🏗️ Project Ka Structure

```
D:\Ai-Agent-K8s\
│
├── AIOps/                    ← Main Python Package
│   ├── __init__.py           ← Package ka initialization file
│   ├── __main__.py           ← Entry point (python -m AIOps se run hota hai)
│   │
│   ├── config.py             ← ⚙️ Model name aur Ollama URL yahan set karo
│   ├── cli.py                ← 🖥️ CLI commands (scan, analyze, document, fix)
│   ├── agent.py              ← 🧠 AI Agent ka brain — ReAct loop orchestrator
│   ├── tools.py              ← 🔧 kubectl wrappers (cluster data fetch karne ke tools)
│   ├── prompts.py            ← 📝 AI ko diye jaane wale instructions (SRE persona)
│   └── sop.py                ← 📄 RCA ko SOP document mein convert karta hai
│
├── docs/
│   └── sop_report.md         ← 📋 Auto-generated SOP yahan save hoti hai
│
├── requirements.txt          ← Python dependencies
└── README.md                 ← Yeh file
```

### Har File Kya Kaam Karti Hai?

| File | Role | Simple Explanation |
|------|------|-------------------|
| `config.py` | Configuration | Model name change karna ho to sirf yahan se badlo |
| `cli.py` | Interface | User jo commands type karta hai woh yahan handle hoti hain |
| `agent.py` | Orchestrator | AI aur tools ke beech coordinator — ReAct loop |
| `tools.py` | Data Gatherer | `kubectl` commands chalata hai cluster info lane ke liye |
| `prompts.py` | Persona | AI ko batata hai ke woh ek Senior SRE hai aur kya format follow kare |
| `sop.py` | Documenter | Final analysis ko proper SOP Markdown mein format karta hai |

---

## 🧠 Yeh Kaam Kaise Karta Hai? (ReAct Loop)

```
Aap command chalate ho
        │
        ▼
  [ cli.py ]
  Command parse karta hai
        │
        ▼
  [ agent.py ] ← Gemma4 LLM yahan connect hota hai
  ReAct Loop shuru:
  ┌─────────────────────────────────────────┐
  │  THINK:  "Mujhe nodes ka status dekhna  │
  │           chahiye pehle..."              │
  │     ↓                                   │
  │  ACT:    get_cluster_health() tool call  │
  │     ↓                                   │
  │  OBSERVE: kubectl output aata hai        │
  │     ↓                                   │
  │  THINK:  "Ek pod CrashLoop mein hai,    │
  │           logs dekhte hain..."           │
  │     ↓                                   │
  │  ACT:    pod_logs() tool call            │
  │     ↓                                   │
  │  OBSERVE: Error logs milti hain          │
  │     ↓                                   │
  │  FINAL:  RCA + Fix Steps generate        │
  └─────────────────────────────────────────┘
        │
        ▼
  [ sop.py ]
  SOP document save hoti hai docs/ mein
```

---

## ⚙️ Prerequisites (Zaruri Cheezein)

Yeh tools aapke system pe install hone chahiye pehle:

| Tool | Kahan Se Milega | Kyun Zaruri Hai |
|------|----------------|-----------------|
| **Python 3.10+** | [python.org](https://www.python.org/downloads/) | Project ka runtime |
| **Ollama** | [ollama.com](https://ollama.com/download) | Local LLM server |
| **Gemma4 model** | `ollama pull gemma4` | AI ka brain |
| **kubectl** | Niche install guide dekho | Cluster se baat karne ke liye |
| **Kind** | Niche install guide dekho | Local Kubernetes cluster |

---

## 🪟 Windows Pe Setup (Step by Step)

### Step 1: Python Install Karo

```powershell
# Python 3.10+ install karo python.org se, ya winget se:
winget install Python.Python.3.11

# Verify karo
python --version
```

### Step 2: Ollama Install Karo

```powershell
# Ollama Windows installer download karo:
# https://ollama.com/download/windows
# Ya winget se:
winget install Ollama.Ollama

# Ollama service start karo (ek baar install karo, automatically chalega)
ollama serve

# Gemma4 model download karo (ek baar, ~3-4 GB download hoga)
ollama pull gemma4

# Test karo ke model kaam kar raha hai
ollama run gemma4 "Hello, are you working?"
```

### Step 3: kubectl Install Karo (Windows)

```powershell
# Chocolatey se (agar installed hai):
choco install kubernetes-cli

# Ya winget se:
winget install Kubernetes.kubectl

# Ya manually — PowerShell mein chalao:
curl.exe -LO "https://dl.k8s.io/release/v1.31.0/bin/windows/amd64/kubectl.exe"
# kubectl.exe ko kisi PATH folder mein rakho (jaise C:\Windows\System32)

# Verify karo
kubectl version --client
```

### Step 4: Kind Install Karo (Windows)

**Kind = Kubernetes IN Docker** — Docker containers ke andar ek poora Kubernetes cluster chalata hai.

```powershell
# Pehle Docker Desktop install karo:
# https://www.docker.com/products/docker-desktop/
# Docker Desktop start karo aur running verify karo

# Kind install karo — PowerShell mein:
curl.exe -Lo kind.exe https://kind.sigs.k8s.io/dl/v0.24.0/kind-windows-amd64
Move-Item .\kind.exe C:\Windows\System32\kind.exe

# Verify karo
kind version
```

### Step 5: Kind Cluster Banao (Windows)

```powershell
# Ek nayi cluster banao
kind create cluster --name aiops-cluster

# Verify karo ke nodes ready hain
kubectl get nodes

# Expected output:
# NAME                          STATUS   ROLES           AGE
# aiops-cluster-control-plane   Ready    control-plane   1m
```

---

## 🐧 Ubuntu/Linux Pe Setup (Step by Step)

### Step 1: Python Install Karo

```bash
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv -y

# Verify karo
python3 --version
```

### Step 2: Ollama Install Karo (Ubuntu)

```bash
# Ek liner install script (official):
curl -fsSL https://ollama.com/install.sh | sh

# Ollama service shuru karo
sudo systemctl start ollama
sudo systemctl enable ollama  # Boot pe automatically start

# Gemma4 model pull karo (~3-4 GB)
ollama pull gemma4

# Test karo
ollama run gemma4 "Hello!"
```

### Step 3: kubectl Install Karo (Ubuntu)

```bash
# Official repo se install karo
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Verify karo
kubectl version --client
```

### Step 4: Docker Install Karo (Ubuntu — Kind ke liye zaruri)

```bash
# Docker install karo
sudo apt-get install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker

# Aapne user ko docker group mein add karo (restart ke baad lagega)
sudo usermod -aG docker $USER
newgrp docker

# Verify karo
docker --version
```

### Step 5: Kind Install Karo (Ubuntu)

```bash
# Kind binary download karo
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.24.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Verify karo
kind version
```

### Step 6: Kind Cluster Banao (Ubuntu)

```bash
# Cluster banao
kind create cluster --name aiops-cluster

# Nodes check karo
kubectl get nodes

# Expected output:
# NAME                          STATUS   ROLES           AGE
# aiops-cluster-control-plane   Ready    control-plane   1m
```

---

## 🚀 AIOps Project Install Karo

```bash
# 1. Project folder mein jao
cd D:\Ai-Agent-K8s          # Windows
# cd ~/Ai-Agent-K8s          # Ubuntu

# 2. (Optional lekin best practice) Virtual environment banao
python -m venv venv

# Windows mein activate karo:
venv\Scripts\activate
# Ubuntu mein activate karo:
# source venv/bin/activate

# 3. Dependencies install karo
pip install -r requirements.txt
```

---

## 🖥️ CLI Commands — Poori Reference

### Commands Ki List

```
python -m AIOps [COMMAND]
```

| Command | Kya Karta Hai | Options |
|---------|---------------|---------|
| `scan` | Cluster ka full health check karta hai, anomalies dhundhta hai | `--query` / `-q` |
| `analyze` | Diya hua data le ke detailed RCA generate karta hai | `REPORT_CONTENT` |
| `document` | RCA ko formal SOP document mein convert kar ke save karta hai | `RCA_OUTPUT` |
| `fix` | *(Planned)* kubectl remediation commands suggest karta hai | — |

---

## 💡 Real Examples — CLI Commands Kaise Chalayein

### 🔍 Example 1: Basic Cluster Scan

```bash
# Sab se pehla command — cluster ki general health check
python -m AIOps scan
```

**Kya hoga:** Agent khud decide karega kaunse tools use karne hain, cluster ka data gather karega aur ek full RCA report print karega.

---

### 🎯 Example 2: Focused Scan (Specific Problem Pe)

```bash
# Kisi specific pod ki problem investigate karo
python -m AIOps scan -q "nginx pod CrashLoopBackOff mein kyun hai?"

# Specific namespace check karo
python -m AIOps scan -q "kube-system namespace mein koi unhealthy pods hain?"

# Node ki memory pressure check karo
python -m AIOps scan -q "Kisi node pe memory ya CPU pressure toh nahi?"

# Recent events dekho koi change hua hai?
python -m AIOps scan -q "Last 1 ghante mein cluster mein kya unusual events aaye hain?"
```

---

### 🔬 Example 3: Analyze (Apna Data De Ke RCA Nikalo)

```bash
# Agar aapke paas koi error output hai, us pe RCA chalao
python -m AIOps analyze "pod/my-app-7d9f8b CrashLoopBackOff, Exit Code: 137, OOMKilled"

# kubectl output copy kar ke analyze karo
python -m AIOps analyze "Events: Warning OOMKilling Container my-app exceeded memory limit of 128Mi"
```

**Kya hoga:** Agent us text ko padh ke formal RCA report generate karega — root cause, severity, aur fix steps ke saath.

---

### 📜 Example 4: SOP Document Generate Karo

```bash
# scan ka output copy karo aur document command mein paste karo
python -m AIOps document "## RCA: OOMKilled — nginx container exceeded 128Mi memory limit. Root cause: memory leak in v2.1.0. Fix: kubectl set resources deployment/nginx --limits=memory=512Mi"
```

**Kya hoga:** Ek proper SOP Markdown file banega aur `docs/sop_report.md` mein save ho jaega.

---

### 🔄 Example 5: Poora Workflow Ek Saath

```bash
# Step 1: Pehle scan karo
python -m AIOps scan

# ---- Output aata hai ----
# "## RCA: CrashLoopBackOff in pod my-app..."
# --- Yeh output copy karo ---

# Step 2: Agar aur detail chahiye
python -m AIOps analyze "<copied output from scan>"

# Step 3: SOP document banao
python -m AIOps document "<final RCA output>"

# Step 4: SOP check karo
cat docs/sop_report.md       # Ubuntu
type docs\sop_report.md      # Windows
```

---

### ℹ️ Help Commands

```bash
# Saare commands ki list dekho
python -m AIOps --help

# Kisi specific command ka help dekho
python -m AIOps scan --help
python -m AIOps analyze --help
python -m AIOps document --help
```

---

## 🧪 Setup Test Karo — Sab Theek Hai Ya Nahi?

```bash
# 1. Ollama chal raha hai?
curl http://localhost:11434/api/tags
# Expected: JSON response with model list

# 2. Gemma4 available hai?
ollama list
# Expected: gemma4 ki entry dikhe

# 3. kubectl cluster se connected hai?
kubectl cluster-info
# Expected: Kubernetes master ka URL dikhe

# 4. Nodes ready hain?
kubectl get nodes
# Expected: STATUS = Ready

# 5. AIOps ka quick test
python -m AIOps --help
# Expected: Commands ki list dikhe bina koi error ke
```

---

## 🔧 Configuration

Model ya URL change karna ho to sirf [`AIOps/config.py`](AIOps/config.py) edit karo:

```python
# AIOps/config.py

MODEL_NAME = "gemma4"                      # ← Yahan model badlo (llama3, mistral, etc.)
OLLAMA_BASE_URL = "http://localhost:11434" # ← Agar Ollama kisi aur machine pe hai
```

---

## 🛠️ Troubleshooting — Common Problems

| Problem | Wajah | Solution |
|---------|-------|----------|
| `Connection refused 11434` | Ollama nahi chal raha | `ollama serve` chalao |
| `model gemma4 not found` | Model pull nahi hua | `ollama pull gemma4` chalao |
| `kubectl not found` | PATH mein nahi hai | kubectl install guide upar dekho |
| `No nodes found` | Cluster nahi bana | `kind create cluster` chalao |
| `Agent is unavailable` | Ollama ya model missing | Upar 2 solutions dekho |
| `--help slow hai` | (Fixed) Pehle ka bug | Ab fix ho gaya, fast hoga |

---

## 🗺️ Roadmap

| Feature | Status |
|---------|--------|
| Cluster health scan (`scan`) | ✅ Ready |
| Root Cause Analysis (`analyze`) | ✅ Ready |
| SOP document generation (`document`) | ✅ Ready |
| Custom query support (`--query`) | ✅ Ready |
| Crashed pod previous logs | ✅ Ready |
| Auto-fix with kubectl (`fix`) | 🔄 Planned |
| LangGraph stateful workflow | 🔄 Planned |
| Multi-cluster support | 🔄 Future |
| Web dashboard | 🔄 Future |
| Slack/Email alerting | 🔄 Future |

---

## 🤝 Naya Tool Add Karna Chahte Ho?

Sirf 2 steps:

1. [`AIOps/tools.py`](AIOps/tools.py) mein naya `@tool` function likho:
```python
@tool
def get_deployments() -> str:
    """Lists all deployments in the cluster."""
    return run_kubectl_command(["get", "deployments", "-A"])
```

2. [`AIOps/agent.py`](AIOps/agent.py) mein `initialize_tools()` function ke andar us tool ko add karo — ReAct agent automatically seekh jaega use karna.

---

## 📄 License

MIT License — freely use karo, improvements contribute karo!

---

<div align="center">

Made with ❤️ | LangChain + Ollama + Gemma4 + Kubernetes

</div>
