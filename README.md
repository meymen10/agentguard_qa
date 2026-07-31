# AgentGuard QA

AgentGuard QA is a lightweight Python-based QA tool designed to detect unsafe or inappropriate tool usage in AI agents.

The project focuses on testing whether an agent calls the correct tools for a given user request. It checks for forbidden tool usage, missing confirmation for high-risk actions, unexpected tool calls, and unsafe agent behavior.

## Project Purpose

AI agents can call tools such as refund processing, account deletion, customer profile access, or support ticket creation. However, these actions may create risks if they are triggered without proper validation or user confirmation.

AgentGuard QA helps validate agent behavior before connecting it to real-world systems.

## Current Features

- Demo customer support agent
- Safe and unsafe agent modes
- Tool call simulation
- Mock tool execution layer
- Tool policy validation
- Forbidden tool usage detection
- Missing confirmation detection for high-risk tools
- Unexpected tool usage detection
- Tool sequence validation
- Issue severity summary
- Markdown, JSON, and HTML report generation
- Streamlit dashboard for interactive report review
- Unit tests for policy checking, reporting, mock tool execution, and dashboard helpers

## Agent Modes

AgentGuard QA currently supports two demo agent modes:

- `unsafe`: Simulates risky agent behavior such as calling high-risk tools without confirmation.
- `safe`: Simulates safer behavior by using validation and confirmation steps before risky actions.

This allows the same test cases to be executed against different agent behaviors and makes tool misuse easier to detect.

## Reporting

AgentGuard QA generates Markdown, JSON, and HTML reports under the `reports/` directory (result_report.md, result_report.json, result_report.html).

Reports include:

- Total test run count
- Passed and failed test counts
- Agent mode summary
- Issue severity summary
- Called tools and mock execution results for each test case
- Detailed issue list for failed scenarios
- Tool sequence validation results

JSON output is machine-readable for CI and dashboards; HTML is a convenient human-friendly view.

## Tool Sequence Validation

AgentGuard QA can validate whether an agent calls tools in the expected order for a given scenario.

For example, a safe refund flow should follow this sequence:

```text
get_order_status
→ check_refund_eligibility
→ ask_user_confirmation
```

The expected sequence can be configured per test case and per agent mode in [data/test_cases.json](data/test_cases.json), and the checker reports whether the observed tool call order matched the expected flow.

## Roadmap

- [x] Add safe and unsafe agent modes
- [x] Add issue severity summary
- [x] Add tool sequence validation
- [x] Add mock tool execution
- [x] Add JSON and HTML report export
- [x] Add Streamlit dashboard
- [ ] Add LLM-based agent integration
- [ ] Add prompt injection test pack

## Project Structure

```text
agentguard_qa/
│
├── agents/
│   └── demo_support_agent.py
│
├── checker/
│   ├── policy_checker.py
│   └── report_generator.py
│
├── data/
│   ├── test_cases.json
│   └── tool_policy.json
│
├── reports/
│   ├── result_report.md
│   ├── result_report.json
│   └── result_report.html
│
├── tests/
│   ├── test_policy_checker.py
│   ├── test_mock_tools.py
│   └── test_report_generator.py
│
├── tools/
│   ├── __init__.py
│   └── mock_tools.py
│
├── app.py
├── dashboard.py
├── requirements.txt
└── README.md
```

## Usage

Run the test suite and generate reports:

- Run all unit tests:
  python -m unittest discover -s tests -p 'test*.py'

- Run the application and produce reports:
  python app.py

Reports are written to the reports/ directory:
- reports/result_report.md   (Markdown)
- reports/result_report.json (Machine-readable JSON)
- reports/result_report.html (Human-friendly HTML view)

Launch the dashboard locally:
- Install dependencies: pip install -r requirements.txt
- Start the dashboard: streamlit run dashboard.py
- Optional: point it at another report file: streamlit run dashboard.py reports/result_report.json

Inspect mock tool executions:
- The mock executor records an execution result for each tool call and includes it in the generated reports under "Tool Executions".
- The checker also validates the observed tool sequence against the expected flow configured per test case.

Contributions and extending the project:
- Add more test cases to data/test_cases.json
- Extend the mock tool layer for new tool types
- Implement a Streamlit dashboard to visualize results
- Integrate with CI to run on pull requests