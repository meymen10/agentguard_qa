import json
import sys
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_REPORT_PATH = BASE_DIR / "reports" / "result_report.json"


def load_report_payload(report_path: str | Path | None = None) -> Dict[str, Any]:
    path = Path(report_path or DEFAULT_REPORT_PATH)
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def build_dashboard_data(payload: Dict[str, Any]) -> Dict[str, Any]:
    results = payload.get("results", [])
    summary = payload.get("summary", {})
    mode_summary = payload.get("mode_summary", {})
    severity_summary = payload.get("severity_summary", {})

    tool_usage_counts: Dict[str, int] = {}
    issue_types: Dict[str, int] = {}

    for result in results:
        for tool_name in result.get("called_tools", []):
            tool_usage_counts[tool_name] = tool_usage_counts.get(tool_name, 0) + 1

        for issue in result.get("issues", []):
            issue_type = issue.get("type", "UNKNOWN")
            issue_types[issue_type] = issue_types.get(issue_type, 0) + 1

    return {
        "summary": summary,
        "mode_summary": mode_summary,
        "severity_summary": severity_summary,
        "results": results,
        "tool_usage_counts": dict(sorted(tool_usage_counts.items())),
        "issue_types": dict(sorted(issue_types.items())),
        "failed_results": [result for result in results if result.get("status") == "FAIL"],
        "passed_results": [result for result in results if result.get("status") == "PASS"],
    }


def render_dashboard(payload: Dict[str, Any]) -> None:
    try:
        import streamlit as st
    except ImportError as exc:
        raise SystemExit("Install streamlit to run the dashboard: pip install -r requirements.txt") from exc

    dashboard_data = build_dashboard_data(payload)

    st.set_page_config(page_title="AgentGuard QA Dashboard", layout="wide")
    st.title("AgentGuard QA Dashboard")

    summary = dashboard_data["summary"]
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Runs", summary.get("total", 0))
    col2.metric("Passed", summary.get("passed", 0))
    col3.metric("Failed", summary.get("failed", 0))

    st.subheader("Agent Mode Summary")
    mode_rows = []
    for mode_name, mode_stats in dashboard_data["mode_summary"].items():
        mode_rows.append(
            {
                "Agent Mode": mode_name.upper(),
                "Total": mode_stats.get("total", 0),
                "Passed": mode_stats.get("passed", 0),
                "Failed": mode_stats.get("failed", 0),
            }
        )
    st.table(mode_rows)

    st.subheader("Issue Severity Summary")
    severity_rows = [
        {"Severity": severity, "Count": count}
        for severity, count in dashboard_data["severity_summary"].items()
    ]
    st.table(severity_rows)

    st.subheader("Tool Usage")
    tool_rows = [
        {"Tool": tool_name, "Calls": count}
        for tool_name, count in dashboard_data["tool_usage_counts"].items()
    ]
    st.table(tool_rows)

    st.subheader("Issue Types")
    issue_rows = [
        {"Issue Type": issue_type, "Count": count}
        for issue_type, count in dashboard_data["issue_types"].items()
    ]
    st.table(issue_rows)

    st.subheader("Failed Test Cases")
    if dashboard_data["failed_results"]:
        failed_rows = [
            {
                "Test ID": result.get("test_id", ""),
                "Title": result.get("title", ""),
                "Agent Mode": result.get("agent_mode", "unknown"),
                "Issues": len(result.get("issues", [])),
            }
            for result in dashboard_data["failed_results"]
        ]
        st.table(failed_rows)
    else:
        st.write("No failures detected.")


def main() -> None:
    report_path = DEFAULT_REPORT_PATH
    if len(sys.argv) > 1:
        report_path = Path(sys.argv[1])

    payload = load_report_payload(report_path)
    render_dashboard(payload)


if __name__ == "__main__":
    main()
