"""
Employee Performance MCP Server
================================
5 Tools:
  1. get_attendance          - Attendance records
  2. get_task_management     - Task completion metrics
  3. get_manager_feedback    - Manager ratings & comments
  4. get_training_certifications - Learning & certs
  5. get_github_performance  - Real GitHub API data (commits, PRs, issues, reviews)

Run as stdio server:  python mcp_server.py
"""

from mcp.server.fastmcp import FastMCP
import json
import random
from datetime import datetime, timedelta

mcp = FastMCP("Employee Performance Evaluation Server")


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 1 — Attendance
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_attendance(employee_id: str, month: str = "2024-04") -> str:
    """
    Fetch monthly attendance record for an employee.
    Returns present/absent days, late arrivals, and attendance percentage.
    """
    random.seed(employee_id + month)
    working_days = 22
    present = random.randint(18, 22)
    absent = working_days - present
    late = random.randint(0, 3)
    pct = round((present / working_days) * 100, 2)

    data = {
        "tool": "Attendance Tool",
        "employee_id": employee_id,
        "month": month,
        "working_days": working_days,
        "days_present": present,
        "days_absent": absent,
        "late_arrivals": late,
        "attendance_percentage": pct,
        "status": "Excellent" if pct >= 95 else "Good" if pct >= 85 else "Average",
    }
    return json.dumps(data, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 2 — Task Management
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_task_management(employee_id: str, quarter: str = "Q1-2024") -> str:
    """
    Fetch task assignment and completion data for an employee in a quarter.
    Returns completion rate, on-time delivery, and priority breakdown.
    """
    random.seed(employee_id + quarter)
    total = random.randint(25, 50)
    completed = random.randint(int(total * 0.7), total)
    on_time = random.randint(int(completed * 0.65), completed)
    high = random.randint(3, 10)
    medium = random.randint(5, 15)
    low = random.randint(2, 10)

    data = {
        "tool": "Task Management Tool",
        "employee_id": employee_id,
        "quarter": quarter,
        "total_tasks_assigned": total,
        "tasks_completed": completed,
        "tasks_pending": total - completed,
        "tasks_completed_on_time": on_time,
        "tasks_delayed": completed - on_time,
        "completion_rate_pct": round((completed / total) * 100, 2),
        "on_time_delivery_pct": round((on_time / completed) * 100, 2) if completed else 0,
        "priority_breakdown": {"high": high, "medium": medium, "low": low},
        "performance_grade": (
            "A" if completed / total >= 0.95
            else "B" if completed / total >= 0.80
            else "C"
        ),
    }
    return json.dumps(data, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 3 — Manager Feedback
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_manager_feedback(employee_id: str, quarter: str = "Q1-2024") -> str:
    """
    Fetch manager evaluation scores and qualitative feedback for an employee.
    Covers communication, technical skills, teamwork, and more.
    """
    random.seed(employee_id + quarter + "feedback")

    def score():
        return round(random.uniform(3.0, 5.0), 1)

    strengths_pool = [
        "Strong problem-solving ability",
        "Proactive communication",
        "Excellent team collaboration",
        "Deep technical knowledge",
        "Reliable and consistent delivery",
        "Creative thinking and innovation",
    ]
    improvements_pool = [
        "Documentation needs improvement",
        "Could delegate tasks more effectively",
        "Needs to manage time better on large projects",
        "Should participate more in code reviews",
    ]

    overall = score()
    data = {
        "tool": "Manager Feedback Tool",
        "employee_id": employee_id,
        "quarter": quarter,
        "overall_rating": overall,
        "rating_scale": "5.0",
        "category_scores": {
            "communication": score(),
            "technical_skills": score(),
            "teamwork": score(),
            "problem_solving": score(),
            "initiative": score(),
            "time_management": score(),
        },
        "strengths": random.sample(strengths_pool, 3),
        "areas_for_improvement": random.sample(improvements_pool, 2),
        "manager_comments": (
            "A consistent performer who delivers quality work and supports teammates. "
            "Shows strong ownership of tasks and communicates blockers early."
        ),
        "promotion_recommended": "Yes" if overall >= 4.5 else "Under Review" if overall >= 3.8 else "No",
    }
    return json.dumps(data, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 4 — Training & Certifications
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_training_certifications(employee_id: str) -> str:
    """
    Fetch training hours and professional certifications completed by an employee.
    Useful for learning & development evaluation.
    """
    random.seed(employee_id + "training")

    all_certs = [
        {"name": "AWS Solutions Architect", "issuer": "Amazon", "date": "2023-06-15", "score": 87, "status": "Active"},
        {"name": "Google Professional Data Engineer", "issuer": "Google", "date": "2023-11-20", "score": 91, "status": "Active"},
        {"name": "Certified Kubernetes Administrator", "issuer": "CNCF", "date": "2024-01-10", "score": 78, "status": "Active"},
        {"name": "TensorFlow Developer Certificate", "issuer": "Google", "date": "2024-02-05", "score": 84, "status": "Active"},
        {"name": "Microsoft Azure AI Engineer", "issuer": "Microsoft", "date": "2023-09-01", "score": 80, "status": "Active"},
    ]
    all_trainings = [
        {"course": "Advanced Python for AI", "platform": "Coursera", "completed": "2024-02-01", "hours": 40},
        {"course": "LangChain Fundamentals", "platform": "Internal", "completed": "2024-03-15", "hours": 16},
        {"course": "MLOps Practices", "platform": "Udemy", "completed": "2024-01-20", "hours": 24},
        {"course": "RAG & Vector Databases", "platform": "DeepLearning.AI", "completed": "2024-04-01", "hours": 12},
        {"course": "Docker & Kubernetes for Data Engineers", "platform": "Pluralsight", "completed": "2023-12-10", "hours": 30},
    ]

    selected_certs = random.sample(all_certs, random.randint(2, 4))
    selected_trainings = random.sample(all_trainings, random.randint(2, 4))
    total_hours = sum(t["hours"] for t in selected_trainings)

    data = {
        "tool": "Training & Certification Tool",
        "employee_id": employee_id,
        "certifications_count": len(selected_certs),
        "certifications": selected_certs,
        "trainings_completed": len(selected_trainings),
        "training_courses": selected_trainings,
        "total_training_hours": total_hours,
        "learning_index": round(random.uniform(70, 100), 1),
        "skill_growth_rating": "Excellent" if total_hours >= 80 else "Good" if total_hours >= 40 else "Average",
    }
    return json.dumps(data, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# TOOL 5 — GitHub Performance (Real GitHub API)
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_github_performance(
    github_username: str,
    github_token: str = "",
    days: int = 90,
) -> str:
    """
    Fetch real GitHub performance metrics for a technical employee.
    Includes commit activity, pull requests, issue handling,
    code review participation, and language proficiency.
    Requires a GitHub Personal Access Token for higher rate limits.
    """
    try:
        from github import Github, Auth, GithubException

        # Authenticate
        if github_token:
            g = Github(auth=Auth.Token(github_token))
        else:
            g = Github()  # unauthenticated – limited to 60 req/hour

        since_date = datetime.utcnow() - timedelta(days=days)
        since_str = since_date.strftime("%Y-%m-%d")

        user = g.get_user(github_username)

        # ── Commit activity across owned repos ──────────────────────────────
        total_commits = 0
        repos_contributed = []
        languages: dict = {}

        for repo in user.get_repos():
            if repo.fork:
                continue
            try:
                commits = repo.get_commits(author=github_username, since=since_date)
                count = commits.totalCount
                if count > 0:
                    total_commits += count
                    repos_contributed.append(repo.name)
                    if repo.language:
                        languages[repo.language] = languages.get(repo.language, 0) + count
            except GithubException:
                continue

        # ── Pull Requests ────────────────────────────────────────────────────
        try:
            pr_search = g.search_issues(
                f"author:{github_username} type:pr created:>{since_str}"
            )
            merged_search = g.search_issues(
                f"author:{github_username} type:pr is:merged created:>{since_str}"
            )
            total_prs = pr_search.totalCount
            merged_prs = merged_search.totalCount
        except Exception:
            total_prs = merged_prs = 0

        # ── Issues ───────────────────────────────────────────────────────────
        try:
            open_issues = g.search_issues(
                f"author:{github_username} type:issue is:open"
            ).totalCount
            closed_issues = g.search_issues(
                f"author:{github_username} type:issue is:closed"
            ).totalCount
        except Exception:
            open_issues = closed_issues = 0

        # ── Code Reviews (PR review comments) ────────────────────────────────
        try:
            review_comments = g.search_issues(
                f"commenter:{github_username} type:pr updated:>{since_str}"
            ).totalCount
        except Exception:
            review_comments = 0

        # ── Scores ───────────────────────────────────────────────────────────
        commit_score = min(100, total_commits * 2)
        collab_score = min(100, (total_prs + closed_issues + review_comments) * 4)
        overall = min(100, round((commit_score * 0.4 + collab_score * 0.6), 1))

        g.close()

        data = {
            "tool": "GitHub MCP Tool",
            "github_username": github_username,
            "evaluation_period_days": days,
            "profile": {
                "public_repos": user.public_repos,
                "followers": user.followers,
                "account_created": str(user.created_at)[:10],
            },
            "commit_activity": {
                "total_commits": total_commits,
                "repos_contributed_to": len(repos_contributed),
                "repositories": repos_contributed[:10],
            },
            "pull_requests": {
                "total_created": total_prs,
                "merged": merged_prs,
                "merge_rate_pct": round((merged_prs / total_prs) * 100, 1) if total_prs else 0,
            },
            "issue_handling": {
                "open_issues": open_issues,
                "closed_issues": closed_issues,
                "resolution_rate_pct": (
                    round(closed_issues / (open_issues + closed_issues) * 100, 1)
                    if (open_issues + closed_issues) > 0
                    else 0
                ),
            },
            "code_review_participation": review_comments,
            "top_languages": dict(
                sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
            ),
            "performance_scores": {
                "commit_score": commit_score,
                "collaboration_score": collab_score,
                "overall_github_score": overall,
                "grade": "A" if overall >= 80 else "B" if overall >= 60 else "C",
            },
        }
        return json.dumps(data, indent=2)

    except Exception as e:
        return json.dumps({
            "tool": "GitHub MCP Tool",
            "github_username": github_username,
            "error": str(e),
            "hint": "Check that the username exists and your token has 'repo' scope.",
        }, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
# TOOL 6 — Peer Review
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_peer_review(employee_id: str, quarter: str = "Q1-2024") -> str:
    """
    Simulate peer review scores from teammates for the given employee.
    Returns avg score, number of reviewers, and sample comments.
    """
    random.seed(employee_id + quarter + "peer")
    reviewers = random.randint(2, 6)
    scores = [round(random.uniform(3.5, 5.0), 2) for _ in range(reviewers)]
    avg_score = round(sum(scores) / reviewers, 2)
    comments_pool = [
        "Excellent collaborator and always helpful.",
        "Delivers high-quality code on time.",
        "Great at knowledge sharing.",
        "Can improve documentation practices.",
        "Shows initiative in solving complex problems.",
    ]
    sample_comments = random.sample(comments_pool, min(3, len(comments_pool)))
    data = {
        "tool": "Peer Review Tool",
        "employee_id": employee_id,
        "quarter": quarter,
        "reviewers_count": reviewers,
        "average_score": avg_score,
        "score_scale": "5.0",
        "sample_comments": sample_comments,
    }
    return json.dumps(data, indent=2)

# ─────────────────────────────────────────────────────────────────────────────
# TOOL 7 — Wellness
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_wellness(employee_id: str, month: str = "2024-04") -> str:
    """
    Provide a synthetic wellness snapshot for an employee.
    Includes stress level, sleep hours, and activity score.
    """
    random.seed(employee_id + month + "wellness")
    stress = random.randint(1, 10)  # 1 = low, 10 = high
    sleep_hours = round(random.uniform(5.5, 8.5), 1)
    activity = random.randint(0, 100)  # percentage of daily activity goal met
    data = {
        "tool": "Wellness Tool",
        "employee_id": employee_id,
        "month": month,
        "stress_level": stress,
        "average_sleep_hours": sleep_hours,
        "activity_score_pct": activity,
        "overall_wellness": "Good" if stress <= 4 and activity >= 70 else "Average" if stress <= 6 else "Poor",
    }
    return json.dumps(data, indent=2)

# ─────────────────────────────────────────────────────────────────────────────
# TOOL 8 — Compensation
# ─────────────────────────────────────────────────────────────────────────────
@mcp.tool()
def get_compensation(employee_id: str, year: str = "2024") -> str:
    """
    Return synthetic compensation data: base salary, bonus, equity, and total comp.
    """
    random.seed(employee_id + year + "comp")
    base_salary = random.randint(70_000, 180_000)
    bonus = random.randint(5_000, 30_000)
    equity = random.randint(0, 50_000)
    total = base_salary + bonus + equity
    data = {
        "tool": "Compensation Tool",
        "employee_id": employee_id,
        "year": year,
        "base_salary_usd": base_salary,
        "annual_bonus_usd": bonus,
        "equity_usd": equity,
        "total_compensation_usd": total,
        "grade": "A" if total >= 150_000 else "B" if total >= 100_000 else "C",
    }
    return json.dumps(data, indent=2)

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run(transport="stdio")
