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
- Tool policy validation
- Forbidden tool usage detection
- Missing confirmation detection for high-risk tools
- Unexpected tool usage detection
- Tool sequence validation
- Issue severity summary
- Markdown report generation

## Agent Modes

AgentGuard QA currently supports two demo agent modes:

- `unsafe`: Simulates risky agent behavior such as calling high-risk tools without confirmation.
- `safe`: Simulates safer behavior by using validation and confirmation steps before risky actions.

This allows the same test cases to be executed against different agent behaviors and makes tool misuse easier to detect.

## Reporting

AgentGuard QA generates a Markdown report under the `reports/` directory.

The report includes:

- Total test run count
- Passed and failed test counts
- Agent mode summary
- Issue severity summary
- Called tools for each test case
- Detailed issue list for failed scenarios
- Tool sequence validation results

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
- [ ] Add mock tool execution
- [ ] Add Streamlit dashboard
- [ ] Add JSON and HTML report export
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
│   └── result_report.md
│
├── tools/
│   └── mock_tools.py
│
├── app.py
└── README.md