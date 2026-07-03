from typing import List, Dict, Any


def generate_markdown_report(results: List[Dict[str, Any]], output_path: str) -> None:
    total = len(results)
    passed = len([result for result in results if result["status"] == "PASS"])
    failed = total - passed

    lines = []

    lines.append("# AgentGuard QA Test Report\n")
    lines.append("## Summary\n")
    lines.append(f"- Total Test Runs: {total}")
    lines.append(f"- Passed: {passed}")
    lines.append(f"- Failed: {failed}\n")

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

    lines.append("## Agent Mode Summary\n")

    for mode, summary in mode_summary.items():
        lines.append(f"### {mode.upper()} Agent")
        lines.append(f"- Total: {summary['total']}")
        lines.append(f"- Passed: {summary['passed']}")
        lines.append(f"- Failed: {summary['failed']}\n")

    lines.append("---\n")

    for result in results:
        agent_mode = result.get("agent_mode", "unknown")

        lines.append(f"## {result['test_id']} - {result['title']}\n")
        lines.append(f"**Agent Mode:** {agent_mode}")
        lines.append(f"**User Prompt:** {result['user_prompt']}")
        lines.append(f"**Status:** {result['status']}\n")

        lines.append("**Called Tools:**")
        for tool in result["called_tools"]:
            lines.append(f"- {tool}")

        if result["issues"]:
            lines.append("\n**Issues:**")
            for issue in result["issues"]:
                lines.append(
                    f"- **{issue['severity']}** | {issue['type']} | {issue['message']}"
                )
        else:
            lines.append("\n**Issues:** None")

        lines.append("\n---\n")

    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))