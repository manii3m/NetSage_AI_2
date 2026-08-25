# NetSage AI – Intelligent Network Diagnostic Platform

**Team Members:**
- **Mayank Vishwakarma** (Father of CSE)
- **Deepak Mishra** (Mother of CSE)

**College:** Lakshmi Narain College Of Technology And Excellence Bhopal (M.P.)  
**Technology Track:** AI Track  

---

## 1. Project Overview
NetSage AI is an intelligent and automated network diagnostic platform designed for Cisco IOS and Cisco Packet Tracer environments. The main purpose of the project is to help network engineers and students identify and understand network faults by analyzing symptoms reported by the user, network topology details, and Cisco CLI command outputs.

While working with network configurations, troubleshooting can often become time-consuming. An engineer may need to go through multiple `show` command outputs, check interface states, verify VLAN configurations, examine routing tables, and identify problems across different OSI layers. NetSage AI is designed to simplify this process by organizing the available network evidence and providing a structured diagnosis.

The project follows a hybrid diagnostic approach. Instead of depending entirely on Artificial Intelligence, the system first uses deterministic, rule-based checks to identify known and common network problems. If a known pattern is detected, the system provides a direct diagnosis based on predefined logic. However, if the available evidence does not match any known rule, the case is passed to a Large Language Model (LLM) for further evidence-based analysis.

This approach gives the project a good balance between reliability and flexibility. Known issues can be handled in a controlled and predictable way, while more complex or unusual problems can still benefit from AI-based reasoning. The final diagnosis is also reviewed by a human before any action is accepted, making the overall workflow safer and more practical for real-world network troubleshooting.

---

## 2. Problem Statement
Network troubleshooting is not always straightforward, especially in multi-layer Cisco network environments. A single connectivity issue can have several possible causes, such as an interface being administratively down, an incorrect IP configuration, a VLAN mismatch, missing routes, access control restrictions, or configuration errors at another layer of the network.

Traditionally, the person troubleshooting the issue needs to manually run multiple Cisco CLI commands and carefully examine the output. This process requires networking knowledge and can take a significant amount of time, particularly for students or less experienced engineers. In many cases, the CLI output itself is lengthy, making it difficult to quickly identify the actual cause of the problem.

Using a completely AI-based solution also creates certain risks. An AI model may make assumptions about information that was never provided or suggest commands that are not appropriate for the actual network configuration. On the other hand, a traditional rule-based system is reliable for known problems but cannot always handle unusual, ambiguous, or complex situations.

NetSage AI was developed to address this gap. The system combines deterministic rule-based validation, LLM-based reasoning, and human review in one workflow. This ensures that known problems are handled predictably, while more complex cases can still receive intelligent analysis without giving the AI unrestricted control over the troubleshooting process.

---

## 3. Proposed Solution
NetSage AI provides an end-to-end workflow for diagnosing network faults using the evidence available from the network environment.

The system receives three main inputs:
1. **Symptom:** The problem reported by the user or network operator.
2. **Topology Note:** Relevant information about the network structure, including devices, interfaces, connections, and other important topology details.
3. **Show Outputs:** Cisco IOS CLI outputs that act as the main evidence for the diagnostic process.

The first stage is handled by the deterministic rule engine in `checker.py`. This component checks the available evidence against predefined patterns and rules for known network problems. If a rule matches, the system immediately generates a structured diagnosis. 

If no rule matches the available evidence, the case is passed to `engine.py`, which prepares the information for LLM-based analysis. The LLM is instructed to reason only from the evidence provided by the system and avoid inventing missing network details.

The final output is returned in a structured format containing:
- Root cause of the problem
- Affected OSI layer
- Confidence score
- Supporting evidence
- Recommended verification command
- Suggested fix steps

---

## 4. System Architecture and Workflow
The architecture is divided into four main areas:

### 4.1 Data Tier
Contains the structured network test cases, case information, and system configuration required by the application. Keeping this information structured allows the diagnostic engine to process cases consistently.

### 4.2 Diagnostic Core
The main processing part of the system, which includes:
- Deterministic rule checker
- Main diagnostic engine
- LLM prompt and analysis logic

The deterministic checker always runs first. If it successfully identifies a known issue, the system returns the diagnosis. If it cannot find a matching rule, the diagnostic engine sends the available evidence to the LLM as a controlled fallback mechanism.

### 4.3 Human-in-the-Loop Gate
The HITL Gate is an important safety layer. The diagnosis is displayed to the operator, who can review the result and decide whether it is appropriate. The operator can:
- **Approve** the proposed action
- **Edit** the suggested commands or fix steps
- **Reject** the diagnosis if it is incorrect

### 4.4 Audit and Logging Layer
Records important information about the diagnostic process and the final human decision, tracking false positives, human overrides, and edge cases for future system improvements.

---

## 5. Overall System Workflow
1. The operator selects or provides a network diagnostic case.
2. The system loads the symptom, topology information, and Cisco CLI outputs.
3. The deterministic checker analyzes the evidence first.
4. If a known issue is identified, a structured diagnosis is generated directly.
5. If no rule matches, the diagnostic engine sends the available evidence to the LLM.
6. The LLM returns an evidence-based diagnosis in the required format.
7. The result is displayed on the dashboard for human review.
8. The operator can approve, edit, or reject the proposed action.
9. The final decision and diagnostic information are stored for auditing.

---

## 6. Technology Stack
- **Python (3.10+):** Core application logic, diagnostic processing, JSON handling, and integration.
- **Streamlit:** Interactive dashboard where users view cases, examine results, and review actions.
- **Pandas:** Loading and processing structured network case data efficiently.
- **JSON:** Structured format for communication between the engine, LLM, and app.
- **Cisco IOS CLI & Packet Tracer:** Primary diagnostic environment scenarios.
- **Markdown & Mermaid.js:** Project documentation and architecture representation.

---

## 7. Team Roles and Responsibilities
The project is divided into four major development roles:

### Role 1: Project Lead
Responsible for the overall direction, planning, and coordination. Defines requirements, designs high-level architecture, plans the hybrid workflow, and ensures the project remains within its intended scope.

### Role 2: Backend Developer
Responsible for building the core diagnostic functionality (e.g. `checker.py`, `engine.py`). Implements deterministic rules, manages module flow, handles JSON parsing, and handles LLM response validation.

### Role 3: Integration Developer
Connects major components, primarily focusing on integrating the LLM with the Python application. Prepares system prompts, passes relevant evidence, and handles API validation securely.

### Role 4: Testing and Validation Developer
Responsible for ensuring reliable, valid, and safe diagnostic results. Prepares network fault test cases, executes functional testing, tracks false positives, and verifies the human-in-the-loop flow.

---

## 8. Key Feature: Human-in-the-Loop Validation
An AI-generated recommendation is never automatically treated as the final action. The operator acts as the final gatekeeper, deciding whether to Approve, Edit, or Reject the diagnosis. This approach is especially useful for complex/ambiguous network problems. Human review also creates a powerful feedback mechanism logged in the audit trails to improve future LLM prompting.

---

## 9. Key Strengths of the Project
- **Deterministic Rules** provide predictable and reliable handling of known network problems.
- **LLM-Based Reasoning** provides flexibility for cases that cannot be handled by predefined rules alone.
- **Human Validation** ensures the final action remains under human control.
- **Modular Architecture** makes the system easy to test and extend with new diagnostic rules.

---

## 10. Conclusion
NetSage AI is a practical software project that brings together Python development, Cisco networking concepts, deterministic rule-based analysis, LLM integration, and human validation to address real network troubleshooting problems. Designed not to depend completely on AI, it follows a structured hybrid approach, reducing unnecessary dependence on LLMs while maximizing diagnostic safety and reliability through Human-in-the-Loop oversight.
