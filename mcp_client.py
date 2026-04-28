"""
Employee Performance MCP Client
================================
Synchronous wrapper around the async MCP Python SDK.
Spawns mcp_server.py as a subprocess via stdio transport
and exposes one method per tool.

Usage:
    client = EmployeeMCPClient()
    data = client.get_attendance("EMP001", "2024-04")
    data = client.get_github_performance("octocat", github_token="ghp_...")
"""

import asyncio
import json
import sys
import threading
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ─────────────────────────────────────────────────────────────────────────────
# Async helper — runs in its own thread to avoid conflicts with Streamlit
# ─────────────────────────────────────────────────────────────────────────────
def _run_async(coro):
    """Run an async coroutine safely from a synchronous context (e.g., Streamlit)."""
    result = None
    exc = None

    def _thread():
        nonlocal result, exc
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(coro)
        except Exception as e:
            exc = e
        finally:
            loop.close()

    t = threading.Thread(target=_thread, daemon=True)
    t.start()
    t.join()

    if exc:
        raise exc
    return result


# ─────────────────────────────────────────────────────────────────────────────
# Core async call
# ─────────────────────────────────────────────────────────────────────────────
async def _call_tool_async(tool_name: str, arguments: dict) -> str:
    server_script = str(Path(__file__).parent / "mcp_server.py")
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments=arguments)
            if result.content:
                return result.content[0].text
            return "{}"


# ─────────────────────────────────────────────────────────────────────────────
# Public client class
# ─────────────────────────────────────────────────────────────────────────────
class EmployeeMCPClient:
    """Synchronous MCP client for the Employee Performance Evaluation server."""

    def _call(self, tool_name: str, arguments: dict) -> dict:
        raw = _run_async(_call_tool_async(tool_name, arguments))
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"error": "Invalid JSON from server", "raw": raw}

    # ── Tool 1 ──────────────────────────────────────────────────────────────
    def get_attendance(self, employee_id: str, month: str = "2024-04") -> dict:
        """Fetch attendance record for an employee."""
        return self._call("get_attendance", {"employee_id": employee_id, "month": month})

    # ── Tool 2 ──────────────────────────────────────────────────────────────
    def get_task_management(self, employee_id: str, quarter: str = "Q1-2024") -> dict:
        """Fetch task completion metrics for an employee."""
        return self._call("get_task_management", {"employee_id": employee_id, "quarter": quarter})

    # ── Tool 3 ──────────────────────────────────────────────────────────────
    def get_manager_feedback(self, employee_id: str, quarter: str = "Q1-2024") -> dict:
        """Fetch manager evaluation scores and comments."""
        return self._call("get_manager_feedback", {"employee_id": employee_id, "quarter": quarter})

    # ── Tool 4 ──────────────────────────────────────────────────────────────
    def get_training_certifications(self, employee_id: str) -> dict:
        """Fetch training hours and certifications for an employee."""
        return self._call("get_training_certifications", {"employee_id": employee_id})

    # ── Tool 6 ──────────────────────────────────────────────────────────────
    def get_peer_review(self, employee_id: str, quarter: str = "Q1-2024") -> dict:
        """Fetch simulated peer review data for an employee."""
        return self._call("get_peer_review", {"employee_id": employee_id, "quarter": quarter})

    # ── Tool 7 ──────────────────────────────────────────────────────────────
    def get_wellness(self, employee_id: str, month: str = "2024-04") -> dict:
        """Fetch synthetic wellness data for an employee."""
        return self._call("get_wellness", {"employee_id": employee_id, "month": month})

    def get_github_performance(
        self,
        github_username: str,
        github_token: str = "",
        days: int = 90,
    ) -> dict:
        """Fetch real GitHub performance data via the GitHub API."""
        return self._call(
            "get_github_performance",
            {
                "github_username": github_username,
                "github_token": github_token,
                "days": days,
            },
        )

    # ── Tool 8 ──────────────────────────────────────────────────────────────
    def get_compensation(self, employee_id: str, year: str = "2024") -> dict:
        """Fetch synthetic compensation data for an employee."""
        return self._call("get_compensation", {"employee_id": employee_id, "year": year})

    def get_full_evaluation(
        self,
        employee_id: str,
        github_username: str = "",
        github_token: str = "",
        month: str = "2024-04",
        quarter: str = "Q1-2024",
    ) -> dict:
        """
        Convenience method — calls all 5 tools and returns a combined report.
        GitHub tool is skipped if no username is provided.
        """
        report = {
            "employee_id": employee_id,
            "generated_at": __import__("datetime").datetime.now().isoformat(),
            "attendance": self.get_attendance(employee_id, month),
            "task_management": self.get_task_management(employee_id, quarter),
            "manager_feedback": self.get_manager_feedback(employee_id, quarter),
            "training_certifications": self.get_training_certifications(employee_id),
        }
        if github_username:
            report["github_performance"] = self.get_github_performance(
                github_username, github_token, days=90
            )
        # new optional tools – always included if data is desired; they are lightweight
        report["peer_review"] = self.get_peer_review(employee_id, quarter)
        report["wellness"] = self.get_wellness(employee_id, month)
        report["compensation"] = self.get_compensation(employee_id, year="2024")
        return report
        # (duplicate block removed)
