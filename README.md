# 📊 Employee Performance Evaluation System
### RAG + MCP (Model Context Protocol) Integration

> An intelligent HR evaluation platform that combines **Retrieval-Augmented Generation (RAG)** with **5 live MCP Tools** — including a real **GitHub MCP Tool** — to deliver comprehensive, AI-powered employee performance insights.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green?logo=langchain)
![Ollama](https://img.shields.io/badge/Ollama-llama3.2-orange)
![MCP](https://img.shields.io/badge/MCP-1.27-purple)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.5-teal)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [MCP Tools](#mcp-tools)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [How to Run](#how-to-run)
- [GitHub MCP Tool Setup](#github-mcp-tool-setup)
- [Workflow](#workflow)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)

---

## 🧠 Overview

This project is an **AI-powered Employee Performance Evaluation System** built for HR teams and technical managers. It uses:

- **RAG (Retrieval-Augmented Generation)** to answer questions from employee documents (PDFs)
- **MCP (Model Context Protocol)** as a standardized tool layer to fetch live employee data across 5 domains
- **Ollama (llama3.2)** as the local LLM for answer generation
- **ChromaDB** as the vector store for semantic document search
- **Streamlit** as the interactive web UI

The system is specifically designed for evaluating employees in technical roles such as **Data Science**, **AI Engineering**, and **Software Development** — with GitHub contribution data as a key performance indicator.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI (main.py)                   │
│                                                                  │
│  ┌──────────────┐  ┌──────────────────────────────────────────┐ │
│  │  Sidebar     │  │           6 Tabs                         │ │
│  │  - Employee  │  │  📅 Attendance  ✅ Tasks  👨 Feedback    │ │
│  │    ID        │  │  🎓 Training   🐙 GitHub  💬 AI Chat    │ │
│  │  - GitHub    │  └──────────────────────────────────────────┘ │
│  │    Username  │                                                │
│  │  - Token     │                                                │
│  └──────────────┘                                                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               │                               │
    ┌──────────▼──────────┐       ┌────────────▼────────────┐
    │   RAG Pipeline      │       │   MCP Client             │
    │                     │       │   (mcp_client.py)        │
    │  PyPDFLoader        │       │                          │
    │  → Text Splitter    │       │  Spawns mcp_server.py   │
    │  → nomic-embed-text │       │  via stdio transport     │
    │  → ChromaDB         │       └────────────┬────────────┘
    │  → llama3.2         │                    │
    └─────────────────────┘       ┌────────────▼────────────┐
                                  │   MCP Server             │
                                  │   (mcp_server.py)        │
                                  │                          │
                                  │  Tool 1: Attendance      │
                                  │  Tool 2: Task Mgmt       │
                                  │  Tool 3: Manager Feedback│
                                  │  Tool 4: Training & Certs│
                                  │  Tool 5: GitHub API ──── ┼──► GitHub REST API
                                  └──────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 **Document RAG** | Ask questions about employees from uploaded PDF files |
| 🔌 **5 MCP Tools** | Live data from Attendance, Tasks, Feedback, Training, and GitHub |
| 🐙 **Real GitHub Data** | Fetches actual commits, PRs, issues, and code reviews via GitHub API |
| 💬 **AI Chat Assistant** | LLM-powered QA with MCP data injected into context |
| ⚡ **Persistent Vector Store** | ChromaDB on disk — embeddings built once, loaded instantly |
| 🎯 **Session State** | MCP data cached in Streamlit session across interactions |
| 📊 **Rich Metrics UI** | Tabbed dashboard with live metrics and progress bars |

---

## 🔧 MCP Tools

### Tool 1 — 📅 Attendance Tool
- Days present / absent
- Late arrival count
- Attendance percentage
- Status: Excellent / Good / Average

### Tool 2 — ✅ Task Management Tool
- Tasks assigned, completed, pending
- On-time delivery rate
- Priority breakdown (High / Medium / Low)
- Performance grade (A / B / C)

### Tool 3 — 👨‍💼 Manager Feedback Tool
- Overall rating (out of 5.0)
- Category scores: Communication, Technical, Teamwork, Problem-solving, Initiative, Time Management
- Strengths & improvement areas
- Promotion recommendation

### Tool 4 — 🎓 Training & Certification Tool
- Professional certifications (AWS, Google, Azure, Kubernetes, etc.)
- Training courses with platform & hours
- Total learning hours
- Learning index score

### Tool 5 — 🐙 GitHub MCP Tool *(Real GitHub API)*
- ✅ Repository contributions & commit count
- ✅ Pull requests created & merged (merge rate %)
- ✅ Issues opened & resolved (resolution rate %)
- ✅ Code review participation
- ✅ Top programming languages
- ✅ Overall GitHub performance score & grade

> **Ideal for evaluating:** Data Scientists, AI Engineers, Software Developers, DevOps Engineers

---

## 📁 Project Structure

```
Employee-Performance-Evaluation/
│
├── main.py              # Streamlit app — UI, RAG, MCP integration
├── mcp_server.py        # FastMCP server — all 5 tools defined here
├── mcp_client.py        # Python MCP client — calls server via stdio
├── requirements.txt     # All Python dependencies
├── .env.example         # Template for GitHub token
├── employee_details.pdf # Source document for RAG (your HR PDF)
└── chroma_db/           # Auto-created — ChromaDB vector store (gitignored)
```

---

## ⚙️ Prerequisites

Make sure the following are installed on your system:

| Tool | Purpose | Install |
|---|---|---|
| **Python 3.10+** | Runtime | [python.org](https://python.org) |
| **Ollama** | Local LLM server | [ollama.com](https://ollama.com) |
| **llama3.2** | Chat LLM model | `ollama pull llama3.2` |
| **nomic-embed-text** | Embedding model | `ollama pull nomic-embed-text` |
| **Git** | Version control | [git-scm.com](https://git-scm.com) |

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/employee-performance-evaluation.git
cd employee-performance-evaluation
```

### 2. Create a Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pull Required Ollama Models

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 5. Configure GitHub Token (Optional but Recommended)

```bash
# Copy the example file
copy .env.example .env     # Windows
cp .env.example .env       # macOS / Linux

# Edit .env and add your token
# Generate at: GitHub → Settings → Developer Settings → Personal Access Tokens
GITHUB_TOKEN=ghp_your_token_here
```

---

## ▶️ How to Run

### Start the Application

```bash
streamlit run main.py
```

Then open your browser at: **http://localhost:8501**

> **First run only:** The app will embed the PDF and build the ChromaDB index. This takes ~30–60 seconds.  
> **All subsequent runs:** The DB is loaded from disk instantly. ✅

---

## 📖 Workflow

```
1. Start Streamlit App
        │
        ▼
2. PDF is loaded → Split → Embedded with nomic-embed-text → Saved to ChromaDB
        │
        ▼
3. Enter Employee ID + GitHub Username in Sidebar
        │
        ▼
4. Click "🚀 Fetch All MCP Data"
        │
        ├─► MCP Client spawns mcp_server.py (stdio)
        │
        ├─► Tool 1: get_attendance(employee_id, month)
        ├─► Tool 2: get_task_management(employee_id, quarter)
        ├─► Tool 3: get_manager_feedback(employee_id, quarter)
        ├─► Tool 4: get_training_certifications(employee_id)
        └─► Tool 5: get_github_performance(username, token)  ──► GitHub API
        │
        ▼
5. View results in 5 metric tabs
        │
        ▼
6. Ask questions in 💬 AI Assistant tab
        │
        ├─► RAG: Query → ChromaDB similarity search → relevant document chunks
        ├─► MCP: All fetched tool data injected into LLM context
        └─► llama3.2 generates a comprehensive answer
```

---

## 🐙 GitHub MCP Tool Setup

The GitHub MCP Tool uses the **real GitHub REST API** via `PyGithub`.

### Get a Personal Access Token (PAT)

1. Go to **GitHub → Settings → Developer Settings**
2. Click **Personal access tokens → Fine-grained tokens → Generate new token**
3. Set scopes:
   - `repo` — for private repositories
   - `public_repo` — for public repositories only
4. Copy the token and paste it into the Streamlit sidebar

### What Data Is Fetched

```
📦 Repository Contributions
   └── Commits per repo (last 90 days)
   └── List of repos contributed to
   └── Top programming languages

🔀 Pull Requests
   └── Total PRs created
   └── PRs merged + merge rate %

🐛 Issue Handling
   └── Open vs closed issues
   └── Resolution rate %

👁️ Code Review Participation
   └── PR comments/review activity

📊 Performance Scores
   └── Commit Score (0-100)
   └── Collaboration Score (0-100)
   └── Overall GitHub Score + Grade (A/B/C)
```

> **Without a token:** Works but limited to 60 requests/hour (GitHub rate limit).  
> **With a token:** 5,000 requests/hour.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **LLM** | Ollama — llama3.2:latest |
| **Embeddings** | Ollama — nomic-embed-text |
| **Vector Store** | ChromaDB (persistent) |
| **RAG Framework** | LangChain (langchain_community, langchain_chroma) |
| **MCP Protocol** | `mcp[cli]` v1.27 — FastMCP |
| **GitHub API** | PyGithub v2.9 |
| **PDF Loader** | pypdf + LangChain PyPDFLoader |
| **Text Splitter** | RecursiveCharacterTextSplitter |

---

## 🙈 .gitignore Recommendations

Add this `.gitignore` to avoid pushing sensitive/large files:

```gitignore
# Virtual environment
venv/

# ChromaDB (auto-generated)
chroma_db/

# Python cache
__pycache__/
*.pyc

# Environment variables (contains GitHub token)
.env

# PDF (optional — add if confidential)
# employee_details.pdf
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-mcp-tool`
3. Commit your changes: `git commit -m "Add: new MCP tool for salary prediction"`
4. Push to branch: `git push origin feature/new-mcp-tool`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 👨‍💻 Author

Built with ❤️ using Python, LangChain, Ollama, ChromaDB, and the MCP Protocol.

> ⭐ If you found this project useful, please give it a star on GitHub!
