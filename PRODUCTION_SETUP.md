# 🚀 Production Setup Guide

## Overview

This Employee Performance Evaluation System is now **production-ready** with the following features:

- ✅ **Configuration Management** - Environment-based configuration via `.env`
- ✅ **Comprehensive Logging** - Structured logging to console and file
- ✅ **Error Handling** - Graceful error handling across all modules
- ✅ **Health Checks** - Startup verification of dependencies
- ✅ **7 MCP Tools** - Including 2 new production tools (Performance Summary, Employee Survey)
- ✅ **Enhanced RAG** - Better error handling in vectorstore operations
- ✅ **Cache Management** - Clear cache button in sidebar

---

## 📁 Project Structure

```
Work-Evaluation-System/
├── main.py                    # Streamlit application (updated with error handling)
├── mcp_client.py              # MCP client (with 2 new tools)
├── mcp_server.py              # MCP server (with 10 tools total)
├── config.py                  # ⭐ NEW: Centralized configuration
├── logger_setup.py            # ⭐ NEW: Production logging setup
├── health_check.py            # ⭐ NEW: Startup verification script
├── run_app.bat                # ⭐ NEW: Windows startup script
├── run_app.sh                 # ⭐ NEW: Unix/Mac startup script
├── requirements.txt           # Dependencies (updated)
├── .env                       # Environment variables (create from .env.example)
├── .env.example               # Example environment variables
├── README.md                  # Project documentation
├── PRODUCTION_SETUP.md        # This file
└── logs/                      # ⭐ NEW: Automatically created log directory
```

---

## 🔧 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and update as needed:

```bash
cp .env.example .env
```

**Available Configuration Options:**

```env
# LLM & Embedding Models
EMBED_MODEL=nomic-embed-text      # Ollama embedding model
LLM_MODEL=llama3.2:latest         # Ollama LLM model
OLLAMA_BASE_URL=http://localhost:11434

# RAG Settings
CHUNK_SIZE=5000                   # PDF chunk size
CHUNK_OVERLAP=1500                # Overlap between chunks
RAG_TOP_K=3                        # Number of top-k results to retrieve

# Logging
LOG_LEVEL=INFO                    # Options: DEBUG, INFO, WARNING, ERROR

# GitHub
GITHUB_DEFAULT_DAYS=90            # Days to analyze for GitHub metrics

# Cache
CACHE_TTL_SECONDS=3600            # Cache time-to-live in seconds
```

### 3. Prepare Required Files

**PDF for RAG:**
Place an `employee_details.pdf` file in the project root for RAG to work.

```
Work-Evaluation-System/
├── employee_details.pdf   ⬅️ Add your PDF here
├── main.py
└── ...
```

### 4. Start Ollama Service

Before running the app, ensure Ollama is running:

```bash
ollama serve
```

In another terminal, verify Ollama has the required models:

```bash
ollama pull llama3.2:latest
ollama pull nomic-embed-text
```

### 5. Run Health Check

Verify all dependencies and services are ready:

```bash
python health_check.py
```

Expected output:
```
✓ langchain installed
✓ streamlit installed
✓ Ollama service is running
✓ PDF file found
✓ Health check complete! Ready to start the app.
```

### 6. Start the Application

**Windows:**
```bash
run_app.bat
```

**Linux/Mac:**
```bash
chmod +x run_app.sh
./run_app.sh
```

**Manual:**
```bash
streamlit run main.py
```

---

## 📊 New Production Features

### Configuration Management (`config.py`)

Centralized configuration with environment variable support:

```python
from config import EMBED_MODEL, LLM_MODEL, CHROMA_DB_DIR, LOG_LEVEL
```

Benefits:
- No hardcoded values in source code
- Easy deployment across environments
- Secure sensitive configuration

### Logging Setup (`logger_setup.py`)

Production-grade logging to console and file:

```python
from logger_setup import get_logger
logger = get_logger()
logger.info("Event logged to console and logs/app.log")
```

Log files are stored in `logs/app.log` with rotation support.

### Health Checks (`health_check.py`)

Automatic verification before app start:
- ✅ Checks all required packages
- ✅ Verifies Ollama service connectivity
- ✅ Validates PDF file presence
- ✅ Provides actionable error messages

### Error Handling

All critical functions now have try-except blocks:

```python
try:
    vectorstore = load_vectorstore()
except Exception as e:
    logger.error(f"Error loading vectorstore: {e}")
    st.error(f"Error loading knowledge base: {str(e)}")
```

---

## 🆕 New MCP Tools

The system now includes **10 MCP tools** (up from 5):

### Existing Tools (5)
1. **Attendance Tool** - Monthly attendance records
2. **Task Management Tool** - Task completion metrics
3. **Manager Feedback Tool** - Performance ratings
4. **Training & Certifications Tool** - Learning records
5. **GitHub Performance Tool** - Real GitHub API data

### New Tools (2) ⭐
6. **Performance Summary Tool** - Overall performance aggregation
7. **Employee Survey Tool** - Engagement & satisfaction metrics

### Existing Tools Continued (3)
8. **Peer Review Tool** - Peer evaluation scores
9. **Wellness Tool** - Stress, sleep, activity metrics
10. **Compensation Tool** - Salary & benefits data

---

## 📝 Usage Examples

### Basic Usage

```python
from mcp_client import EmployeeMCPClient

client = EmployeeMCPClient()

# Fetch individual metrics
attendance = client.get_attendance("EMP001", month="2024-04")
summary = client.get_performance_summary("EMP001", quarter="Q1-2024")
survey = client.get_employee_survey("EMP001", year="2024")

# Get GitHub data (requires GitHub username)
github = client.get_github_performance("torvalds", github_token="ghp_...")
```

### With Error Handling

```python
from logger_setup import get_logger

logger = get_logger()

try:
    data = client.get_performance_summary("EMP001")
    logger.info(f"Fetched data: {data}")
except Exception as e:
    logger.error(f"Failed to fetch data: {e}")
    # Handle gracefully
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` to version control**
   ```bash
   # Add to .gitignore
   .env
   ```

2. **Use GitHub PAT with minimum scopes**
   - Only enable `repo` and `read:user` scopes

3. **Rotate credentials regularly**
   - Update `.env` with new tokens periodically

4. **Secure log files**
   - Logs in `logs/` may contain sensitive data
   - Restrict file permissions: `chmod 600 logs/app.log`

---

## 📈 Performance Optimization

### Caching

The application uses Streamlit's `@st.cache_resource` decorator:

```python
@st.cache_resource(show_spinner="Setting up knowledge base...")
def load_vectorstore():
    # Expensive operation - cached
    return vectorstore
```

Users can clear cache from the sidebar ("Clear Cache" button).

### Logging Levels

For production, use `INFO` level to avoid excessive logging:

```env
LOG_LEVEL=INFO
```

For debugging, temporarily set to `DEBUG`:

```env
LOG_LEVEL=DEBUG
```

---

## 🐛 Troubleshooting

### Ollama Service Not Running

```
Error: Ollama service not accessible
```

**Solution:**
```bash
ollama serve
```

### Missing Dependencies

```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution:**
```bash
pip install -r requirements.txt
```

### PDF File Not Found

```
PDF file not found: employee_details.pdf
```

**Solution:**
Place `employee_details.pdf` in the project root directory.

### Low Memory During RAG

Reduce chunk size in `.env`:

```env
CHUNK_SIZE=2000
CHUNK_OVERLAP=500
```

---

## 📋 Deployment Checklist

- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] `.env` file created and configured
- [ ] Ollama service running and models downloaded
- [ ] `employee_details.pdf` placed in project root
- [ ] Health check passes: `python health_check.py`
- [ ] Log directory writable: `logs/` exists and has permissions
- [ ] GitHub PAT (if using GitHub tool) has correct scopes
- [ ] Tested locally: `streamlit run main.py`

---

## 📞 Support

For issues or questions:
1. Check logs in `logs/app.log`
2. Run health check: `python health_check.py`
3. Review error messages in Streamlit UI
4. Check configuration in `.env` and `config.py`

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [LangChain Documentation](https://docs.langchain.com)
- [Ollama Documentation](https://ollama.ai)
- [MCP Protocol Documentation](https://modelcontextprotocol.io)

---

**Last Updated:** 2026-06-23  
**Version:** 1.0-Production
