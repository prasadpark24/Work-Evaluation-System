import os
os.environ.setdefault('STREAMLIT_LOGGER_LEVEL', 'debug')

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from ollama import chat
from mcp_client import EmployeeMCPClient
import streamlit as st
import json

from config import (
    CHROMA_DB_DIR, EMBED_MODEL, LLM_MODEL, CHUNK_SIZE, CHUNK_OVERLAP,
    RAG_TOP_K, PDF_FILE, DEFAULT_EMPLOYEE_ID, DEFAULT_MONTH, 
    DEFAULT_QUARTER, DEFAULT_YEAR
)
from logger_setup import get_logger

logger = get_logger()


st.set_page_config(
    page_title="Employee Performance Evaluation",
    page_icon="📊",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# RAG — cached vectorstore
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Setting up knowledge base...")
def load_vectorstore():
    try:
        embeddings = OllamaEmbeddings(model=EMBED_MODEL)
        if CHROMA_DB_DIR.exists() and list(CHROMA_DB_DIR.glob("*")):
            logger.info("Loading existing vectorstore from cache")
            return Chroma(persist_directory=str(CHROMA_DB_DIR), embedding_function=embeddings)
        
        logger.info(f"Creating new vectorstore from {PDF_FILE}")
        if not PDF_FILE.exists():
            logger.warning(f"PDF file not found: {PDF_FILE}")
            return None
        
        docs = PyPDFLoader(str(PDF_FILE)).load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        chunks = splitter.split_documents(docs)
        logger.info(f"Created {len(chunks)} chunks from PDF")
        return Chroma.from_documents(chunks, embeddings, persist_directory=str(CHROMA_DB_DIR))
    except Exception as e:
        logger.error(f"Error loading vectorstore: {e}")
        return None

@st.cache_resource
def get_mcp_client():
    return EmployeeMCPClient()

vectorstore = load_vectorstore()
mcp = get_mcp_client()

# ─────────────────────────────────────────────────────────────────────────────
# RAG helpers
# ─────────────────────────────────────────────────────────────────────────────
def retrieve(query: str) -> str:
    try:
        if vectorstore is None:
            logger.warning("Vectorstore not available")
            return "Knowledge base not available."
        results = vectorstore.similarity_search(query, k=RAG_TOP_K)
        return "\n\n".join([doc.page_content for doc in results])
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        return ""

def generate_answer(query: str, context: str, mcp_context: str = "") -> str:
    try:
        full_context = context
        if mcp_context:
            full_context += f"\n\n--- Live Employee MCP Data ---\n{mcp_context}"
        
        response = chat(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "You are an expert HR AI assistant. Answer the question using "
                        "the provided document context and live employee data.\n\n"
                        f"Context:\n{full_context}"
                    ),
                },
                {"role": "user", "content": query},
            ],
        )
        logger.info(f"Generated answer for query: {query[:50]}...")
        return response["message"]["content"]
    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return f"Error generating answer: {str(e)}"

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar — Employee Inputs
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔧 Employee Details")
    st.markdown("---")

    employee_id = st.text_input("👤 Employee ID", value=DEFAULT_EMPLOYEE_ID)
    month = st.selectbox("📅 Month", ["2024-01", "2024-02", "2024-03", "2024-04"], index=3)
    quarter = st.selectbox("📆 Quarter", ["Q1-2024", "Q2-2024", "Q3-2024", "Q4-2024"])
    year = st.selectbox("📅 Year", ["2024", "2023", "2025"])

    st.markdown("---")
    st.subheader("🐙 GitHub Settings")
    github_username = st.text_input("GitHub Username", placeholder="e.g. torvalds")
    github_token = st.text_input(
        "GitHub Token (optional)", type="password",
        help="Generate at GitHub → Settings → Developer Settings → PAT"
    )

    st.markdown("---")
    fetch_btn = st.button("🚀 Fetch All MCP Data", type="primary")
    clear_btn = st.button("🗑️ Clear Cache")
    
    if clear_btn:
        st.session_state.mcp_data = {}
        logger.info("Cache cleared by user")
        st.success("Cache cleared!")

# ─────────────────────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────────────────────
if "mcp_data" not in st.session_state:
    st.session_state.mcp_data = {}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─────────────────────────────────────────────────────────────────────────────
# Fetch MCP data on button click
# ─────────────────────────────────────────────────────────────────────────────
if fetch_btn:
    try:
        with st.spinner("⚙️ Calling all MCP tools..."):
            data = {}
            logger.info(f"Fetching MCP data for employee: {employee_id}")
            
            data["attendance"] = mcp.get_attendance(employee_id, month)
            data["tasks"] = mcp.get_task_management(employee_id, quarter)
            data["feedback"] = mcp.get_manager_feedback(employee_id, quarter)
            data["training"] = mcp.get_training_certifications(employee_id)
            data["performance_summary"] = mcp.get_performance_summary(employee_id, quarter)
            data["survey"] = mcp.get_employee_survey(employee_id, year)
            
            if github_username:
                data["github"] = mcp.get_github_performance(
                    github_username, github_token, days=90
                )
            
            st.session_state.mcp_data = data
            logger.info("All MCP tools executed successfully")
        st.success("✅ All MCP tools executed successfully!")
    except Exception as e:
        logger.error(f"Error fetching MCP data: {e}")
        st.error(f"❌ Error fetching data: {str(e)}")

# ─────────────────────────────────────────────────────────────────────────────
# Main header
# ─────────────────────────────────────────────────────────────────────────────
st.title("📊 Employee Performance Evaluation System")
st.caption("Powered by RAG + 7 MCP Tools (Attendance · Tasks · Feedback · Training · GitHub · Performance Summary · Survey)")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# Tabs
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📅 Attendance",
    "✅ Task Management",
    "👨‍💼 Manager Feedback",
    "🎓 Training & Certs",
    "🐙 GitHub Performance",
    "📈 Performance Summary",
    "😊 Survey & Engagement",
    "💬 AI Assistant",
])

d = st.session_state.mcp_data

# ── Tab 1: Attendance ────────────────────────────────────────────────────────
with tab1:
    st.subheader("📅 Attendance Tool")
    if "attendance" in d:
        a = d["attendance"]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Days Present", a["days_present"])
        col2.metric("Days Absent", a["days_absent"])
        col3.metric("Late Arrivals", a["late_arrivals"])
        col4.metric("Attendance %", f"{a['attendance_percentage']}%")
        st.success(f"Status: **{a['status']}**")
        with st.expander("📄 Raw JSON"):
            st.json(a)
    else:
        st.info("Click **Fetch All MCP Data** in the sidebar to load attendance data.")

# ── Tab 2: Task Management ───────────────────────────────────────────────────
with tab2:
    st.subheader("✅ Task Management Tool")
    if "tasks" in d:
        t = d["tasks"]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tasks", t["total_tasks_assigned"])
        col2.metric("Completed", t["tasks_completed"])
        col3.metric("On Time %", f"{t['on_time_delivery_pct']}%")
        col4.metric("Grade", t["performance_grade"])
        st.progress(int(t["completion_rate_pct"]), text=f"Completion Rate: {t['completion_rate_pct']}%")
        st.markdown("**Priority Breakdown:**")
        pb = t["priority_breakdown"]
        c1, c2, c3 = st.columns(3)
        c1.metric("🔴 High", pb["high"])
        c2.metric("🟡 Medium", pb["medium"])
        c3.metric("🟢 Low", pb["low"])
        with st.expander("📄 Raw JSON"):
            st.json(t)
    else:
        st.info("Click **Fetch All MCP Data** in the sidebar to load task data.")

# ── Tab 3: Manager Feedback ──────────────────────────────────────────────────
with tab3:
    st.subheader("👨‍💼 Manager Feedback Tool")
    if "feedback" in d:
        f = d["feedback"]
        st.metric("⭐ Overall Rating", f"{f['overall_rating']} / 5.0")
        st.markdown("**Category Scores:**")
        cols = st.columns(3)
        for i, (k, v) in enumerate(f["category_scores"].items()):
            cols[i % 3].metric(k.replace("_", " ").title(), f"{v}/5")
        st.markdown(f"**Strengths:** {', '.join(f['strengths'])}")
        st.markdown(f"**Improvements:** {', '.join(f['areas_for_improvement'])}")
        st.info(f"💬 Manager: *{f['manager_comments']}*")
        rec = f["promotion_recommended"]
        if rec == "Yes":
            st.success(f"🚀 Promotion Recommended: **{rec}**")
        elif rec == "Under Review":
            st.warning(f"🔍 Promotion Recommended: **{rec}**")
        else:
            st.error(f"❌ Promotion Recommended: **{rec}**")
        with st.expander("📄 Raw JSON"):
            st.json(f)
    else:
        st.info("Click **Fetch All MCP Data** in the sidebar to load feedback data.")

# ── Tab 4: Training & Certifications ────────────────────────────────────────
with tab4:
    st.subheader("🎓 Training & Certification Tool")
    if "training" in d:
        tr = d["training"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Certifications", tr["certifications_count"])
        col2.metric("Training Hours", tr["total_training_hours"])
        col3.metric("Learning Index", f"{tr['learning_index']}%")
        st.markdown("**Certifications:**")
        for cert in tr["certifications"]:
            st.markdown(
                f"- 🏅 **{cert['name']}** ({cert['issuer']}) — Score: {cert['score']} | {cert['date']}"
            )
        st.markdown("**Training Courses:**")
        for course in tr["training_courses"]:
            st.markdown(
                f"- 📚 **{course['course']}** ({course['platform']}) — {course['hours']}h"
            )
        with st.expander("📄 Raw JSON"):
            st.json(tr)
    else:
        st.info("Click **Fetch All MCP Data** in the sidebar to load training data.")

# ── Tab 5: GitHub Performance ────────────────────────────────────────────────
with tab5:
    st.subheader("🐙 GitHub MCP Tool")
    if "github" in d:
        g = d["github"]
        if "error" in g:
            st.error(f"GitHub API Error: {g['error']}\n\n💡 {g.get('hint', '')}")
        else:
            ps = g["performance_scores"]
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Commits", g["commit_activity"]["total_commits"])
            col2.metric("PRs Created", g["pull_requests"]["total_created"])
            col3.metric("PRs Merged", g["pull_requests"]["merged"])
            col4.metric("GitHub Score", f"{ps['overall_github_score']}/100")

            st.markdown(f"**Grade: {ps['grade']}** | Commit Score: {ps['commit_score']} | Collaboration: {ps['collaboration_score']}")
            st.progress(min(100, ps["overall_github_score"]), text="Overall GitHub Score")

            st.markdown("**Issue Handling:**")
            ih = g["issue_handling"]
            c1, c2, c3 = st.columns(3)
            c1.metric("Open Issues", ih["open_issues"])
            c2.metric("Closed Issues", ih["closed_issues"])
            c3.metric("Resolution Rate", f"{ih['resolution_rate_pct']}%")

            if g.get("top_languages"):
                st.markdown("**Top Languages:**")
                for lang, commits in g["top_languages"].items():
                    st.markdown(f"- `{lang}`: {commits} commits")

            st.markdown("**Repos Contributed To:**")
            for r in g["commit_activity"].get("repositories", []):
                st.markdown(f"- 📁 `{r}`")

            with st.expander("📄 Raw JSON"):
                st.json(g)
    elif not github_username:
        st.info("Enter a **GitHub Username** in the sidebar and click **Fetch All MCP Data**.")
    else:
        st.info("Click **Fetch All MCP Data** in the sidebar to load GitHub data.")

# ── Tab 6: Performance Summary ───────────────────────────────────────────────
with tab6:
    st.subheader("📈 Performance Summary Tool")
    if "performance_summary" in d:
        ps = d["performance_summary"]
        col1, col2, col3 = st.columns(3)
        col1.metric("Overall Rating", f"{ps['overall_performance_rating']}/5.0")
        col2.metric("Grade", ps["performance_grade"])
        col3.metric("Quarter", ps.get("quarter", "N/A"))
        st.info(f"🎯 {ps['recommendation']}")
        with st.expander("📄 Raw JSON"):
            st.json(ps)
    else:
        st.info("Click **Fetch All MCP Data** in the sidebar to load performance summary.")

# ── Tab 7: Employee Survey ──────────────────────────────────────────────────
with tab7:
    st.subheader("😊 Employee Survey & Engagement Tool")
    if "survey" in d:
        sv = d["survey"]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Engagement", f"{sv['engagement_score']}/5.0")
        col2.metric("Work-Life Balance", f"{sv['work_life_balance_score']}/5.0")
        col3.metric("Career Growth", f"{sv['career_growth_score']}/5.0")
        col4.metric("NPS", sv["net_promoter_score"])
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        col1.metric("Management Satisfaction", f"{sv['management_satisfaction']}/5.0")
        col2.metric("Recommend Company", sv["would_recommend_company"])
        
        with st.expander("📄 Raw JSON"):
            st.json(sv)
    else:
        st.info("Click **Fetch All MCP Data** in the sidebar to load survey data.")

# ── Tab 8: AI Chat Assistant ─────────────────────────────────────────────────
with tab8:
    st.subheader("💬 AI Assistant — RAG + MCP")
    st.caption("Ask anything about the employee. Live MCP data is automatically injected into the AI context.")

    # Show chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask about employee performance, attendance, GitHub activity...")

    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Retrieving from knowledge base..."):
                rag_context = retrieve(user_query)

            # Build MCP context string
            mcp_context_parts = []
            if d:
                for key, val in d.items():
                    mcp_context_parts.append(f"[{key.upper()}]\n{json.dumps(val, indent=2)}")
            mcp_context = "\n\n".join(mcp_context_parts)

            with st.spinner("Generating answer..."):
                answer = generate_answer(user_query, rag_context, mcp_context)

            st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
