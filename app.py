import json
from pathlib import Path

from agents.demo_support_agent import DemoSupportAgent
from checker.policy_checker import PolicyChecker
from checker.report_generator import generate_markdown_report


BASE_DIR = Path(__file__).resolve().parent
TEST_CASES_PATH = BASE_DIR / "data" / "test_cases.json"
TOOL_POLICY_PATH = BASE_DIR / "data" / "tool_policy.json"
REPORT_PATH = BASE_DIR / "reports" / "result_report.md"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    print("AgentGuard QA is running...\n")

    test_cases = load_json(TEST_CASES_PATH)
    tool_policy = load_json(TOOL_POLICY_PATH)

    agent = DemoSupportAgent()
    checker = PolicyChecker(tool_policy)

    results = []

    for test_case in test_cases:
        tool_calls = agent.run(test_case["user_prompt"])
        result = checker.check(test_case, tool_calls)
        results.append(result)

        print(f"{result['test_id']} - {result['title']}: {result['status']}")

        if result["issues"]:
            for issue in result["issues"]:
                print(f"  - {issue['severity']} | {issue['type']} | {issue['message']}")

        print()

    generate_markdown_report(results, str(REPORT_PATH))

    print(f"Report generated: {REPORT_PATH}")


if __name__ == "__main__":
    main()