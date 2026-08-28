# NetSage AI – Intelligent Network Diagnostic Platform

<div align="center">

![NetSage AI Logo](https://img.shields.io/badge/NetSage%20AI-Network%20Diagnostic%20Platform-blue)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

**Team Members:**
- **Mayank Vishwakarma** (Team Lead & Backend Developer)
- **Deepak Mishra** (Integration & Testing Developer)

**College:** Lakshmi Narain College Of Technology And Excellence Bhopal (M.P.)  
**Technology Track:** AI Track  
**Project Status:** Active Development

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Proposed Solution](#3-proposed-solution)
4. [System Architecture](#4-system-architecture)
5. [System Arrangement & Components](#5-system-arrangement--components)
6. [Data Flow Diagram](#6-data-flow-diagram)
7. [Workflow & Process](#7-workflow--process)
8. [Project Structure](#8-project-structure)
9. [Technology Stack](#9-technology-stack)
10. [Installation & Setup](#10-installation--setup)
11. [Team Roles & Responsibilities](#11-team-roles--responsibilities)
12. [Key Features](#12-key-features)
13. [Contributing Guidelines](#13-contributing-guidelines)

---

## 1. Project Overview

NetSage AI is an **intelligent and automated network diagnostic platform** designed for Cisco IOS and Cisco Packet Tracer environments. It helps network engineers and students identify and understand network faults by analyzing symptoms, network topology details, and Cisco CLI command outputs using a hybrid approach combining deterministic rules and AI-driven reasoning.

### Core Purpose
- **Automate Network Troubleshooting:** Simplify the process of analyzing multiple `show` command outputs
- **Reduce Diagnostic Time:** Identify root causes across multiple OSI layers quickly
- **Maintain Safety & Control:** Ensure human operators remain in control of all actions
- **Learn from Patterns:** Track diagnostic patterns and improve the system over time

### Key Characteristics
- **Hybrid Diagnostic Approach:** Combines rule-based checks with LLM-based reasoning
- **Evidence-Driven Analysis:** All conclusions are based on provided network evidence only
- **Human-in-the-Loop:** Final decisions always reviewed and approved by operators
- **Modular & Extensible:** Easy to add new diagnostic rules and extend functionality

---

## 2. Problem Statement

### Challenges in Current Network Troubleshooting

**Manual & Time-Consuming Process:**
- Network engineers must manually run multiple Cisco CLI commands
- Parse lengthy, complex command outputs
- Cross-reference information across multiple devices
- Identify patterns requiring deep networking knowledge

**Typical Issues Encountered:**
- Interface configurations (administratively down, link issues)
- IP addressing problems (duplicate IPs, incorrect subnet masks)
- VLAN misconfigurations (native VLAN mismatches, missing VLANs)
- Routing problems (missing routes, unreachable gateways)
- Protocol issues (OSPF mismatches, DHCP problems)
- Access control restrictions (ACL denials)
- NAT configuration errors
- DNS and DHCP complications

**Limitations of Existing Approaches:**

| Approach | Pros | Cons |
|----------|------|------|
| **Manual Analysis** | Precise, controlled | Time-consuming, requires expertise |
| **Rule-Based Systems** | Fast, predictable | Cannot handle complex/ambiguous cases |
| **Pure AI/LLM** | Flexible, comprehensive | May hallucinate, unreliable, unsafe |

NetSage AI bridges this gap by combining the best of each approach.

---

## 3. Proposed Solution

### Solution Architecture

NetSage AI implements a **three-stage hybrid diagnostic pipeline:**

```
┌─────────────────────────────────────────────────────────────┐
│                     DIAGNOSTIC PIPELINE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Stage 1: INPUT COLLECTION                                  │
│  ├─ User Symptom Description                                │
│  ├─ Network Topology Information                            │
│  └─ Cisco CLI Show Command Outputs                          │
│           │                                                  │
│           ▼                                                  │
│  Stage 2: DETERMINISTIC RULE-BASED CHECKING                 │
│  ├─ Pattern Matching (14+ predefined rules)                 │
│  ├─ Evidence Validation                                     │
│  ├─ Immediate Diagnosis (if matched)                        │
│  └─ Pass to AI (if no match)                                │
│           │                                                  │
│           ▼                                                  │
│  Stage 3: AI-DRIVEN EVIDENCE ANALYSIS                        │
│  ├─ LLM Processing (Google Generative AI)                   │
│  ├─ Structured Prompt Engineering                           │
│  ├─ Evidence-Based Reasoning                                │
│  └─ Diagnosis Generation                                    │
│           │                                                  │
│           ▼                                                  │
│  Stage 4: HUMAN-IN-THE-LOOP REVIEW                          │
│  ├─ Dashboard Display                                       │
│  ├─ Operator Decision (Approve/Edit/Reject)                 │
│  └─ Audit Logging                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Output Format

The system generates structured diagnosis with:
- **Root Cause Analysis:** Identified network issue
- **OSI Layer Classification:** Which layer the problem affects
- **Confidence Score:** Reliability of the diagnosis
- **Supporting Evidence:** Specific CLI output excerpts
- **Verification Command:** Command to confirm the issue
- **Fix Steps:** Recommended resolution actions

---

## 4. System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Streamlit Dashboard (app.py)                              │  │
│  │  ├─ Case Selection Interface                              │  │
│  │  ├─ Diagnosis Display                                     │  │
│  │  ├─ Human Review Panel                                    │  │
│  │  ├─ Analytics & KPI Dashboard                             │  │
│  │  └─ Dark/Light Theme Toggle                               │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BUSINESS LOGIC LAYER                        │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Diagnostic Engine (engine.py)                             │  │
│  │  ├─ Orchestrate diagnosis workflow                        │  │
│  │  ├─ Coordinate checker & AI modules                       │  │
│  │  └─ Aggregate results                                     │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Rule-Based Checker (checker.py)                           │  │
│  │  ├─ 14+ Cisco-specific rules                              │  │
│  │  ├─ Pattern matching engine                               │  │
│  │  ├─ Severity classification                               │  │
│  │  └─ Rule ID: R001-R014+                                   │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  AI Integration Layer (ai_client.py)                       │  │
│  │  ├─ Google Generative AI API                              │  │
│  │  ├─ Prompt engineering & templates                        │  │
│  │  ├─ Response validation & parsing                         │  │
│  │  └─ Structured JSON output                                │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA ACCESS LAYER                          │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Audit Logger (audit.py)                                   │  │
│  │  ├─ Decision tracking                                     │  │
│  │  ├─ KPI calculation                                       │  │
│  │  ├─ False positive detection                              │  │
│  │  └─ Audit trail storage (JSON)                            │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Utilities & Helpers (utils.py)                            │  │
│  │  ├─ Data parsing & transformation                         │  │
│  │  ├─ Validation functions                                  │  │
│  │  └─ Common utilities                                      │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA & STORAGE LAYER                         │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  /data/                                                    │  │
│  │  ├─ cases.csv (Test case library)                         │  │
│  │  └─ audit_log.json (Audit trail)                          │  │
│  └────────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  External Services                                         │  │
│  │  └─ Google Generative AI API                              │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. System Arrangement & Components

### 5.1 Core Modules

#### **app.py** - Streamlit Frontend Application
- **Purpose:** User-facing dashboard and interface
- **Responsibilities:**
  - Display diagnostic cases
  - Show diagnosis results
  - Handle human-in-the-loop decisions (Approve/Edit/Reject)
  - Render analytics and KPIs
  - Theme management (dark/light mode)
- **Key Functions:**
  - Case loading and selection
  - Result visualization
  - Decision logging

#### **engine.py** - Diagnostic Orchestrator
- **Purpose:** Coordinate the overall diagnostic workflow
- **Responsibilities:**
  - Orchestrate rule checker and AI modules
  - Manage fallback logic (checker → AI)
  - Aggregate and structure results
  - Handle error cases
- **Key Functions:**
  - `run_diagnosis(case_data)` - Main entry point

#### **checker.py** - Deterministic Rule Engine
- **Purpose:** Fast pattern-based fault detection
- **Responsibilities:**
  - Define and execute 14+ network diagnostic rules
  - Pattern matching using regex
  - Severity classification
  - Evidence extraction
- **Rules Covered:**
  - Interface status problems (R001-R002)
  - IP addressing issues (R003-R004)
  - Gateway and routing problems (R005, R008)
  - VLAN misconfigurations (R006-R007)
  - DHCP and DNS issues (R009-R010)
  - ACL and NAT problems (R011-R012)
  - Trunk and protocol issues (R013-R014)

#### **ai_client.py** - LLM Integration Layer
- **Purpose:** Interface with Google Generative AI
- **Responsibilities:**
  - Prepare prompts with network evidence
  - Call generative AI API
  - Parse and validate responses
  - Format results to JSON
- **Key Functions:**
  - `get_diagnosis(case_data, findings)` - AI-based analysis

#### **audit.py** - Audit & Analytics
- **Purpose:** Track decisions and system performance
- **Responsibilities:**
  - Log human decisions (approve/reject/edit)
  - Track false positives and overrides
  - Calculate key performance indicators
  - Maintain audit trail for compliance
- **Key Functions:**
  - `log_decision()` - Record operator action
  - `get_kpis()` - Calculate system metrics
  - `load_audit_log()` - Retrieve audit data

#### **utils.py** - Shared Utilities
- **Purpose:** Common functions and helpers
- **Responsibilities:**
  - Data parsing and transformation
  - Validation functions
  - Common utilities used across modules

### 5.2 Data Components

#### **data/cases.csv** - Test Case Library
- Structured test cases for diagnostic validation
- Fields: Case ID, Symptom, Topology, Show Outputs, Expected Diagnosis
- Used for testing, validation, and training

#### **data/audit_log.json** - Audit Trail
- JSON log of all diagnostic decisions
- Tracks: Timestamp, Case ID, Diagnosis, Human Decision, Confidence
- Enables audit trail and performance analysis

#### **prompts/** - Prompt Templates
- `diagnose_prompt.md` - LLM system prompt with instructions
- Guides AI to evidence-based reasoning only
- Ensures consistent output format

---

## 6. Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                      USER INPUTS                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │   Symptom    │  │   Topology   │  │  Cisco CLI Outputs   │   │
│  │  Description │  │   Information│  │   (show commands)    │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  engine.run_diag()  │
                 └─────────────────────┘
                            │
              ┌─────────────┴──────────────┐
              │                            │
              ▼                            ▼
    ┌──────────────────┐       ┌──────────────────┐
    │  checker.py      │       │  ai_client.py    │
    │                  │       │                  │
    │ Rule Matching    │       │ LLM Processing   │
    │ Pattern Regex    │       │ Prompt Prep      │
    │ Evidence Extract │       │ API Call         │
    └──────────────────┘       └──────────────────┘
              │                            │
              └─────────────┬──────────────┘
                            │
              ┌─────────────▼──────────────┐
              │   Structured Diagnosis    │
              │  (JSON format)             │
              │  ├─ Root Cause             │
              │  ├─ OSI Layer              │
              │  ├─ Confidence             │
              │  ├─ Evidence               │
              │  ├─ Verify Command         │
              │  └─ Fix Steps              │
              └─────────────┬──────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  app.py - Dashboard     │
              │  Display & Review       │
              └─────────────┬───────────┘
                            │
              ┌─────────────▼──────────────┐
              │   Human Decision          │
              │  ├─ Approve               │
              │  ├─ Edit                  │
              │  └─ Reject                │
              └─────────────┬──────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │  audit.py               │
              │  Log & Store Decision   │
              │  ├─ Decision Record     │
              │  ├─ Confidence Track    │
              │  └─ Analytics Update    │
              └─────────────────────────┘
```

---

## 7. Workflow & Process

### Complete Diagnostic Workflow

```
START
  │
  ├─ Step 1: Load Case Data
  │  └─ Input: Symptom, Topology, CLI Outputs
  │
  ├─ Step 2: Run Deterministic Checker
  │  ├─ Match against 14+ rules
  │  ├─ Extract evidence
  │  └─ Decision: Found Rule? 
  │      ├─ YES → Generate Diagnosis (FAST)
  │      └─ NO  → Continue to Step 3
  │
  ├─ Step 3: Prepare for AI Analysis
  │  └─ Format evidence with prompt template
  │
  ├─ Step 4: Call Generative AI API
  │  └─ Get evidence-based diagnosis
  │
  ├─ Step 5: Structure Output
  │  └─ Format as JSON with all required fields
  │
  ├─ Step 6: Display on Dashboard
  │  └─ Show to operator for review
  │
  ├─ Step 7: Human Review & Decision
  │  ├─ Approve → Accept diagnosis
  │  ├─ Edit   → Modify and approve
  │  └─ Reject → Provide feedback
  │
  ├─ Step 8: Log Decision to Audit Trail
  │  └─ Record: Diagnosis, Decision, Confidence
  │
  └─ Step 9: Update Analytics
     └─ Recalculate KPIs
END
```

### Decision Matrix

| Scenario | Checker Result | AI Result | Decision |
|----------|---|---|---|
| **Known Issue** | Rule Match ✓ | - | Direct diagnosis |
| **Unknown Issue** | No Match | AI Match | AI-based diagnosis |
| **Ambiguous** | Partial Match | Partial Match | Composite diagnosis |
| **Conflicting** | Rule ✗ vs AI ✓ | Both presented | Operator chooses |

---

## 8. Project Structure

```
NetStage AI/
│
├── README.md                          # Project documentation (this file)
├── requirements.txt                   # Python dependencies
├── .env                              # Environment variables
│
├── src/                              # Core application modules
│   ├── __init__.py
│   ├── app.py                        # Streamlit dashboard
│   ├── engine.py                     # Diagnostic orchestrator
│   ├── checker.py                    # Rule-based checker (14+ rules)
│   ├── ai_client.py                  # LLM integration
│   ├── audit.py                      # Audit logging & analytics
│   ├── utils.py                      # Utility functions
│   └── seed_audit_log.py             # Audit log initialization
│
├── data/                             # Data layer
│   ├── cases.csv                     # Test cases
│   └── audit_log.json                # Audit trail
│
├── prompts/                          # AI prompt templates
│   └── diagnose_prompt.md            # Diagnostic prompt
│
├── docs/                             # Documentation
│   └── model_audit_log.md            # Audit format documentation
│
├── tests/                            # Test suite
│   └── test_checker.py               # Unit tests for checker
│
├── scripts/                          # Utility scripts
│   ├── update_cases.py               # Case management
│   ├── create_docx.py                # Report generation
│   ├── color_charts.py               # Visualization helpers
│   └── ...
│
├── StreamLit/                        # Additional Streamlit configs
│
└── Summary & Architecture/           # Project documentation
    ├── OVERVIEW.docx
    ├── Summary (Deepak).docx
    └── summary (Mayank).docx
```

---

## 9. Technology Stack

### Backend & Core
- **Python 3.10+** - Core application logic, data processing
- **Pandas** - Data loading, CSV processing, DataFrame manipulation

### Frontend & UI
- **Streamlit** - Interactive web dashboard
- **Plotly Express** - Interactive charts and KPI visualization

### AI & LLM Integration
- **Google Generative AI** - LLM for evidence-based diagnosis
- **Python-dotenv** - Secure environment variable management

### Data Format & Storage
- **JSON** - Structured data exchange (case data, audit logs, responses)
- **CSV** - Test case library (cases.csv)

### Network Environments (Testing)
- **Cisco IOS** - Target network operating system
- **Cisco Packet Tracer** - Simulation environment

### Documentation & Architecture
- **Markdown** - Documentation format
- **Mermaid.js** - Architecture diagrams

### Development Tools
- **Git** - Version control
- **pytest** - Unit testing framework

---

## 10. Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git
- Google Cloud API credentials (for Generative AI)

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd "NetStage AI"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_api_key_here
STREAMLIT_THEME=light
```

### Step 5: Seed Audit Log (First Time)
```bash
python src/seed_audit_log.py
```

### Step 6: Run Application
```bash
streamlit run src/app.py
```

Application will open at: `http://localhost:8501`

---

## 11. Team Roles & Responsibilities

### Role 1: Project Lead (Mayank Vishwakarma)
**Responsibilities:**
- Overall project direction and planning
- Architecture design and system coordination
- Requirement definition and scope management
- Quality assurance and code review
- Documentation and knowledge sharing

**Key Contributions:**
- Hybrid diagnostic approach design
- System architecture planning
- Rule engine specifications

### Role 2: Backend Developer (Mayank Vishwakarma)
**Responsibilities:**
- Core diagnostic functionality implementation
- Rule engine development (`checker.py`)
- Diagnostic orchestration (`engine.py`)
- JSON parsing and data handling
- Module integration and testing

**Key Modules:**
- `checker.py` - Rule-based fault detection
- `engine.py` - Workflow orchestration
- `utils.py` - Utility functions

### Role 3: Integration Developer (Deepak Mishra)
**Responsibilities:**
- LLM integration (`ai_client.py`)
- Prompt engineering and optimization
- API validation and error handling
- Structured output formatting
- Security and credential management

**Key Modules:**
- `ai_client.py` - Google Generative AI integration
- `prompts/` - Prompt templates

### Role 4: Testing & Validation Developer (Deepak Mishra)
**Responsibilities:**
- Test case creation and management
- Functional testing and validation
- False positive tracking and analysis
- Performance metrics and KPIs
- Human-in-the-loop workflow validation

**Key Modules:**
- `tests/` - Test suite
- `data/cases.csv` - Test case library
- `audit.py` - Analytics and KPI tracking

---

## 12. Key Features

### ✅ Hybrid Diagnostic Approach
- **Deterministic First:** Fast, reliable diagnosis for known issues
- **AI-Powered Fallback:** Flexibility for complex, unusual cases
- **Evidence-Based:** All conclusions grounded in provided data only

### ✅ 14+ Diagnostic Rules
- Interface status and configuration issues
- IP addressing and VLAN problems
- Routing and gateway issues
- DHCP and DNS configuration problems
- ACL and NAT misconfigurations
- Protocol-specific issues (OSPF)
- Trunk encapsulation errors

### ✅ Human-in-the-Loop Control
- **Approve** diagnosis without changes
- **Edit** recommendations before approval
- **Reject** and provide feedback for learning

### ✅ Comprehensive Audit Trail
- Decision tracking for compliance
- False positive detection and analysis
- Performance metrics and KPIs
- Feedback mechanism for system improvement

### ✅ Beautiful Dashboard Interface
- Dark/Light theme support
- Case selection and management
- Diagnosis visualization
- Analytics and KPI display
- Minimal, vintage design aesthetic

### ✅ Structured Output
- Root cause analysis
- OSI layer classification
- Confidence scoring
- Supporting evidence extraction
- Verification commands
- Step-by-step fix instructions

---

## 13. Contributing Guidelines

### Development Workflow
1. Create a branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes following the project structure
3. Test thoroughly using `pytest`
4. Commit with clear messages: `git commit -m "Add: Description of change"`
5. Push to branch: `git push origin feature/your-feature-name`
6. Create a Pull Request with detailed description

### Adding New Diagnostic Rules
1. Add rule definition to `checker.py` with:
   - Unique rule ID (R015+)
   - Rule type and severity
   - Regex pattern matching
   - Clear recommendation
2. Add test cases to `test_checker.py`
3. Update documentation with rule description
4. Test against test cases in `data/cases.csv`

### Code Standards
- Follow PEP 8 style guide
- Include docstrings for all functions and classes
- Add type hints where applicable
- Write unit tests for new functionality
- Update README when adding major features

---

## 🚀 Future Enhancements

- [ ] Extended rule library (20+ rules)
- [ ] Multi-device diagnostic correlation
- [ ] Machine learning model for rule suggestion
- [ ] Real-time network simulation
- [ ] Advanced analytics and reporting
- [ ] Integration with Cisco Prime/DNAC
- [ ] Mobile companion app
- [ ] Community rule sharing platform

---

## 📄 License

This project is developed as part of academic coursework at Lakshmi Narain College of Technology and Excellence. For licensing inquiries, please contact the development team.

---

## 📞 Support & Contact

For questions, issues, or suggestions:
- **Mayank Vishwakarma** - Backend Architecture & Core Logic
- **Deepak Mishra** - Integration & Testing

---

## 🙏 Acknowledgments

- Lakshmi Narain College of Technology and Excellence Bhopal
- Cisco Learning Network
- Google Generative AI Team
- Open-source Python community

---

**Last Updated:** August 28, 2026  
**Version:** 1.0.0  
**Status:** Active Development
