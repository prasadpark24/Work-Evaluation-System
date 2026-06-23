# 🚀 Quick Start Guide

Get the Employee Performance Evaluation System up and running in 5 minutes!

## Prerequisites

- Python 3.9+
- Ollama installed ([Download](https://ollama.ai))
- `employee_details.pdf` file (for RAG features)

## Quick Setup (5 minutes)

### Step 1: Install Dependencies (2 min)

```bash
pip install -r requirements.txt
```

### Step 2: Setup Environment (1 min)

```bash
cp .env.example .env
```

### Step 3: Start Ollama (1 min)

In a new terminal:

```bash
ollama serve
```

Then in another terminal, download models:

```bash
ollama pull llama3.2:latest
ollama pull nomic-embed-text
```

### Step 4: Run Health Check (30 sec)

```bash
python health_check.py
```

### Step 5: Launch App (30 sec)

**Windows:**
```bash
run_app.bat
```

**Linux/Mac:**
```bash
./run_app.sh
```

Or manually:
```bash
streamlit run main.py
```

---

## What's Inside?

- **📊 8 Dashboard Tabs** - Attendance, Tasks, Feedback, Training, GitHub, Performance Summary, Survey, AI Chat
- **7 MCP Tools** - Live data from multiple sources
- **🤖 AI Assistant** - RAG-powered Q&A with access to all metrics
- **📈 Performance Summary** - Aggregated employee scores
- **😊 Employee Survey** - Engagement metrics and NPS

---

## 🔑 Key Features

| Feature | Purpose |
|---------|---------|
| **Configuration Management** | `.env` file for easy deployment |
| **Logging** | Automatic logs to `logs/app.log` |
| **Error Handling** | Graceful failures with helpful messages |
| **Health Check** | Verify setup before running |
| **Cache Control** | Clear cache from sidebar |

---

## 💡 Common Tasks

### Use GitHub Performance Tool

1. Go to GitHub → Settings → Developer Settings → Personal Access Tokens
2. Create a token with `repo` and `read:user` scopes
3. In sidebar, enter your GitHub username and token
4. Click "Fetch All MCP Data"

### Customize LLM Model

Edit `.env`:

```env
LLM_MODEL=mistral:7b      # or any other Ollama model
EMBED_MODEL=llama2:7b     # for embeddings
```

Then restart the app.

### Change Logging Level

For more detailed logs during debugging:

```env
LOG_LEVEL=DEBUG
```

Logs appear in `logs/app.log`

### Reduce Memory Usage

For systems with limited RAM, reduce chunk sizes in `.env`:

```env
CHUNK_SIZE=2000
CHUNK_OVERLAP=500
RAG_TOP_K=1
```

---

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `main.py` | Streamlit UI (8 tabs + AI chat) |
| `mcp_server.py` | MCP server with 10 tools |
| `mcp_client.py` | Client to call MCP tools |
| `config.py` | Configuration management |
| `logger_setup.py` | Logging configuration |
| `health_check.py` | Startup verification |
| `.env` | Environment variables |
| `PRODUCTION_SETUP.md` | Detailed setup guide |

---

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Ollama service not accessible" | Run `ollama serve` in another terminal |
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` |
| "PDF file not found" | Place `employee_details.pdf` in project root |
| "Empty knowledge base" | Check that `employee_details.pdf` has content |

---

## 🎯 Next Steps

1. **Customize** - Edit `.env` for your environment
2. **Test** - Use sample employee IDs (EMP001, EMP002, etc.)
3. **Integrate** - Connect with your HR systems
4. **Monitor** - Check `logs/app.log` for issues

---

## 📞 Need Help?

- Read `PRODUCTION_SETUP.md` for detailed configuration
- Check `logs/app.log` for error details
- Run `python health_check.py` to diagnose issues

---

**Ready? Run `run_app.bat` (Windows) or `./run_app.sh` (Linux/Mac)** ✨
