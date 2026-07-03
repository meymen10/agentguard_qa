# AgentGuard QA

AgentGuard QA is a lightweight Python-based QA tool designed to detect unsafe or inappropriate tool usage in AI agents.

The project focuses on testing whether an agent calls the correct tools for a given user request. It checks for forbidden tool usage, missing confirmation for high-risk actions, unexpected tool calls, and unsafe agent behavior.

## Project Purpose

AI agents can call tools such as refund processing, account deletion, customer profile access, or support ticket creation. However, these actions may create risks if they are triggered without proper validation or user confirmation.

AgentGuard QA helps validate agent behavior before connecting it to real-world systems.

## Current Features

- Demo customer support agent
- Tool call simulation
- Tool policy validation
- Forbidden tool detection
- Missing confirmation detection
- Unexpected tool usage detection
- Markdown test report generation

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