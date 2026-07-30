import json
from pathlib import Path

from agents.demo_support_agent import DemoSupportAgent
from checker.policy_checker import PolicyChecker
from checker.report_generator import generate_markdown_report
from tools.mock_tools import MockToolExecutor


BASE_DIR = Path(__file__).resolve().parent
TEST_CASES_PATH = BASE_DIR / "data" / "test_cases.json"
TOOL_POLICY_PATH = BASE_DIR / "data" / "tool_policy.json"
REPORT_PATH = BASE_DIR / "reports" / "result_report.md"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def run_test_suite(agent_mode: str, test_cases, checker, executor: MockToolExecutor):
    agent = DemoSupportAgent(mode=agent_mode)
    results = []

    print(f"\nRunning test suite for {agent_mode.upper()} agent...\n")

    for test_case in test_cases:
        tool_calls = agent.run(test_case["user_prompt"])
        executed_tool_calls = executor.execute_many(tool_calls)
        result = checker.check(test_case, executed_tool_calls, agent_mode=agent_mode)
        result["agent_mode"] = agent_mode
        result["tool_executions"] = executed_tool_calls
        results.append(result)

        print(f"{result['test_id']} - {result['title']}: {result['status']}")

        if result["issues"]:
            for issue in result["issues"]:
                print(f"  - {issue['severity']} | {issue['type']} | {issue['message']}")

        print()

    return results


def main():
    print("AgentGuard QA is running...")

    test_cases = load_json(TEST_CASES_PATH)
    tool_policy = load_json(TOOL_POLICY_PATH)

    checker = PolicyChecker(tool_policy)
    executor = MockToolExecutor()

    results = []

    results.extend(run_test_suite("unsafe", test_cases, checker, executor))
    results.extend(run_test_suite("safe", test_cases, checker, executor))

    generate_markdown_report(results, str(REPORT_PATH))

    print(f"Report generated: {REPORT_PATH}")


if __name__ == "__main__":
    main()