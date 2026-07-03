from typing import List, Dict, Any


def generate_markdown_report(results: List[Dict[str, Any]], output_path: str) -> None:
    total = len(results)
    passed = len([result for result in results if result["status"] == "PASS"])
    failed = total - passed

    lines = []

    lines.append("# AgentGuard QA Test Report\n")
    lines.append("## Summary\n")
    lines.append(f"- Total Tests: {total}")
    lines.append(f"- Passed: {passed}")
    lines.append(f"- Failed: {failed}\n")

    lines.append("---\n")

    for result in results:
        lines.append(f"## {result['test_id']} - {result['title']}\n")
        lines.append(f"**User Prompt:** {result['user_prompt']}\n")
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