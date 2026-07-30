import json
from html import escape
from pathlib import Path
from typing import List, Dict, Any


def build_report_payload(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(results)
    passed = len([result for result in results if result["status"] == "PASS"])
    failed = total - passed
    severity_summary = calculate_severity_summary(results)

    mode_summary = {}

    for result in results:
        mode = result.get("agent_mode", "unknown")

        if mode not in mode_summary:
            mode_summary[mode] = {
                "total": 0,
                "passed": 0,
                "failed": 0
            }

        mode_summary[mode]["total"] += 1

        if result["status"] == "PASS":
            mode_summary[mode]["passed"] += 1
        else:
            mode_summary[mode]["failed"] += 1

    return {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
        },
        "mode_summary": mode_summary,
        "severity_summary": severity_summary,
        "results": results,
    }


def generate_markdown_report(results: List[Dict[str, Any]], output_path: str) -> None:
    payload = build_report_payload(results)
    lines = []

    lines.append("# AgentGuard QA Test Report\n")
    lines.append("## Summary\n")
    lines.append(f"- Total Test Runs: {payload['summary']['total']}")
    lines.append(f"- Passed: {payload['summary']['passed']}")
    lines.append(f"- Failed: {payload['summary']['failed']}\n")

    lines.append("## Agent Mode Summary\n")

    for mode, summary in payload["mode_summary"].items():
        lines.append(f"### {mode.upper()} Agent")
        lines.append(f"- Total: {summary['total']}")
        lines.append(f"- Passed: {summary['passed']}")
        lines.append(f"- Failed: {summary['failed']}\n")

    lines.append("---\n")

    lines.append("## Issue Severity Summary\n")

    if sum(payload["severity_summary"].values()) == 0:
        lines.append("- No issues found.\n")
    else:
        for severity, count in payload["severity_summary"].items():
            lines.append(f"- {severity}: {count}")

        lines.append("")

    for result in payload["results"]:
        agent_mode = result.get("agent_mode", "unknown")

        lines.append(f"## {result['test_id']} - {result['title']}\n")
        lines.append(f"**Agent Mode:** {agent_mode}")
        lines.append(f"**User Prompt:** {result['user_prompt']}")
        lines.append(f"**Status:** {result['status']}\n")

        lines.append("**Called Tools:**")
        for tool in result["called_tools"]:
            lines.append(f"- {tool}")

        tool_executions = result.get("tool_executions", [])
        if tool_executions:
            lines.append("\n**Tool Executions:**")
            for execution in tool_executions:
                details = execution.get("execution", {})
                lines.append(
                    f"- {execution['tool_name']} [{details.get('status', 'unknown')}]"
                )
                message = details.get("message")
                if message:
                    lines.append(f"  - {message}")

        sequence_validation = result.get("tool_sequence_validation", {})
        if sequence_validation:
            lines.append(f"\n**Tool Sequence Validation:** {sequence_validation['status']}")
            lines.append(f"- Expected: {sequence_validation['expected_sequence']}")
            lines.append(f"- Actual: {sequence_validation['actual_sequence']}")
            if sequence_validation['status'] != "SKIP":
                lines.append(f"- Message: {sequence_validation['message']}")

        if result["issues"]:
            lines.append("\n**Issues:**")
            for issue in result["issues"]:
                lines.append(
                    f"- **{issue['severity']}** | {issue['type']} | {issue['message']}"
                )
        else:
            lines.append("\n**Issues:** None")

        lines.append("\n---\n")

    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    with output_path_obj.open("w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def generate_json_report(results: List[Dict[str, Any]], output_path: str) -> None:
    payload = build_report_payload(results)
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    with output_path_obj.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)
        file.write("\n")


def generate_html_report(results: List[Dict[str, Any]], output_path: str) -> None:
    payload = build_report_payload(results)
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)

    sections = []
    for result in payload["results"]:
        issues_html = ""
        if result["issues"]:
            issue_items = "".join(
                f"<li><strong>{escape(issue['severity'])}</strong> | {escape(issue['type'])} | {escape(issue['message'])}</li>"
                for issue in result["issues"]
            )
            issues_html = f"<ul>{issue_items}</ul>"
        else:
            issues_html = "<p>No issues.</p>"

        tool_items = "".join(
            f"<li>{escape(tool)}</li>" for tool in result["called_tools"]
        )
        execution_items = ""
        for execution in result.get("tool_executions", []):
            details = execution.get("execution", {})
            message = details.get("message", "")
            execution_items += (
                f"<li>{escape(execution['tool_name'])} [{escape(str(details.get('status', 'unknown')))}]"
                f"{f' - {escape(message)}' if message else ''}</li>"
            )

        sequence_validation = result.get("tool_sequence_validation", {})
        sequence_html = ""
        if sequence_validation:
            sequence_html = (
                f"<p><strong>Tool Sequence Validation:</strong> {escape(sequence_validation.get('status', ''))}</p>"
                f"<p>Expected: {escape(str(sequence_validation.get('expected_sequence', [])))}</p>"
                f"<p>Actual: {escape(str(sequence_validation.get('actual_sequence', [])))}</p>"
            )
            if sequence_validation.get('status') != 'SKIP':
                sequence_html += f"<p>{escape(sequence_validation.get('message', ''))}</p>"

        sections.append(
            f"<section><h2>{escape(result['test_id'])} - {escape(result['title'])}</h2>"
            f"<p><strong>Agent Mode:</strong> {escape(str(result.get('agent_mode', 'unknown')))}</p>"
            f"<p><strong>User Prompt:</strong> {escape(result['user_prompt'])}</p>"
            f"<p><strong>Status:</strong> {escape(result['status'])}</p>"
            f"<h3>Called Tools</h3><ul>{tool_items}</ul>"
            f"<h3>Tool Executions</h3><ul>{execution_items}</ul>"
            f"{sequence_html}"
            f"<h3>Issues</h3>{issues_html}</section>"
        )

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <title>AgentGuard QA Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; }}
    h1, h2, h3 {{ color: #1f2937; }}
    .summary {{ background: #f3f4f6; padding: 1rem; border-radius: 6px; }}
    section {{ margin-bottom: 2rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 1rem; }}
  </style>
</head>
<body>
  <h1>AgentGuard QA Test Report</h1>
  <div class=\"summary\">
    <p><strong>Total Test Runs:</strong> {payload['summary']['total']}</p>
    <p><strong>Passed:</strong> {payload['summary']['passed']}</p>
    <p><strong>Failed:</strong> {payload['summary']['failed']}</p>
  </div>
  {''.join(sections)}
</body>
</html>
"""

    with output_path_obj.open("w", encoding="utf-8") as file:
        file.write(html)


def calculate_severity_summary(results: List[Dict[str, Any]]) -> Dict[str, int]:
    severity_summary = {
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for result in results:
        for issue in result["issues"]:
            severity = issue["severity"]
            if severity in severity_summary:
                severity_summary[severity] += 1

    return severity_summary