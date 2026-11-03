# A PROJECT REPORT ON
# CANARYSENTINEL: DECEPTION-BASED RANSOMWARE DETECTION, BEHAVIORAL ANALYSIS AND RISK-AWARE RESPONSE SYSTEM

---

### Submitted in partial fulfillment of the requirements for the award of the degree of
### **BACHELOR OF TECHNOLOGY**
### in
### **COMPUTER SCIENCE AND ENGINEERING**

---

**Submitted By:**  
- **[Student Name 1]** ([Roll No / Registration No])  
- **[Student Name 2]** ([Roll No / Registration No])  
- **[Student Name 3]** ([Roll No / Registration No])  

**Under the Guidance of:**  
**[Supervisor Name]**  
[Supervisor Designation / Department]  

---

### **DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING**
### **[INSTITUTION / UNIVERSITY NAME]**
### **[City, State, PIN]**
### **Academic Year: 2025–2026**

---

## 2. Certificate of Authenticity

This is to certify that the project report entitled **"CanarySentinel: Deception-Based Ransomware Detection, Behavioral Analysis and Risk-Aware Response System"** submitted by **[Student Name 1]**, **[Student Name 2]**, and **[Student Name 3]** in partial fulfillment of the requirements for the award of the Degree of **Bachelor of Technology in Computer Science and Engineering** from **[Institution Name]**, is a bona fide record of work carried out by them under my supervision and guidance.

The results embodied in this report have not been submitted to any other University or Institute for the award of any degree or diploma.

\
\
__________________________  
**[Supervisor Name]**  
Internal Guide / Assistant Professor  
Department of Computer Science and Engineering  
[Institution Name]  

\
\
__________________________  
**[Head of Department Name]**  
Head of Department  
Department of Computer Science and Engineering  
[Institution Name]  

\
\
__________________________  
**External Examiner**  
Date of Evaluation: [DD/MM/YYYY]  

---

## 3. Student Declaration

We hereby declare that the project entitled **"CanarySentinel: Deception-Based Ransomware Detection, Behavioral Analysis and Risk-Aware Response System"** is our original work conducted under the guidance of **[Supervisor Name]**, Department of Computer Science and Engineering, **[Institution Name]**.

We confirm that this report represents our own ideas and analysis, and wherever other sources have been cited, due credit has been given through formal citations and references. This report has not been submitted previously to any other university or institution for the award of any degree, diploma, or certificate.

\
**Signatures of the Candidates:**  

1. ___________________________ ([Student Name 1])  
2. ___________________________ ([Student Name 2])  
3. ___________________________ ([Student Name 3])  

Place: [City]  
Date: [DD/MM/YYYY]  

---

## 4. Acknowledgements

We express our sincere gratitude to our project guide, **[Supervisor Name]**, whose valuable guidance, constructive criticism, and technical insights were indispensable throughout the design, implementation, and empirical evaluation of CanarySentinel.

We are deeply grateful to **[Head of Department Name]**, Head of the Department of Computer Science and Engineering, for providing the necessary laboratory facilities, compute resources, and administrative encouragement.

We extend our heartfelt thanks to our faculty members, laboratory staff, and peers whose insightful discussions and technical advice contributed meaningfully to this research project. Finally, we thank our families for their unwavering encouragement throughout our undergraduate studies.

---

## 5. Abstract

Cryptographic ransomware poses an existential threat to modern digital infrastructure by encrypting sensitive endpoint data and demanding financial ransom for decryption keys. Conventional signature-based defenses fail against novel and polymorphic variants, whereas pure volume-based anomaly detectors incur high false-positive rates during benign batch workloads such as compilation or archiving. Deception technology—specifically canary decoy files—provides ultra-fast tripwire alerts but is vulnerable to accidental false alarms from innocent file access and fails completely when attacks evade decoy paths.

This project introduces **CanarySentinel**, a lightweight, macOS-compatible endpoint ransomware detection and risk-aware response architecture. Implemented in Python 3.12, CanarySentinel monitors filesystem activity within a strictly isolated sandbox, deploys strategic canary files, normalizes operating system events via an asynchronous debouncing pipeline, and evaluates three parallel detection paradigms: Baseline (volume/velocity heuristics), Canary-Only (decoy tripwires), and Hybrid (temporal sliding-window correlation).

Across 180 controlled empirical trials ($N = 180$), the Hybrid configuration eliminated false alarms entirely (**Precision = 100.0%**, **FPR = 0.0%**), compared to an unacceptable 25.0% false-positive rate in both Baseline and Canary-Only configurations. During canary-targeted attacks, Hybrid achieved containment within **26.1 ms**, limiting damage to **0.10 files** on average and preventing **approximately 99.1%** of targeted user operations. However, in attacks designed to evade decoys, Hybrid missed the attack entirely (**Recall = 50.0%**), whereas Baseline detected all attacks (**Recall = 100.0%**, **$F_1 = 0.80$**). These empirical findings demonstrate that while hybrid correlation successfully solves the false-alarm dilemma of deception systems, it must be paired with behavioral monitoring as a multi-layered defense-in-depth architecture.

---

## 6. Table of Contents

- 1. Title Page
- 2. Certificate of Authenticity
- 3. Student Declaration
- 4. Acknowledgements
- 5. Abstract
- 6. Table of Contents
- 7. List of Figures
- 8. List of Tables
- 9. Chapter 1: Introduction
  - 1.1 Overview and Motivation
  - 1.2 Problem Statement
  - 1.3 Research Objectives
- 10. Chapter 2: Existing System Analysis
  - 2.1 Overview of Conventional Approaches
  - 2.2 Drawbacks of Current Solutions
- 11. Chapter 3: Proposed System
  - 3.1 System Overview
  - 3.2 Key Features and Novelty
  - 3.3 Proposed Architecture
- 12. Chapter 4: Literature Review
  - 4.1 Evolution of Ransomware Defenses
  - 4.2 Comparative Analysis of Prior Systems
- 13. Chapter 5: Feasibility Study
  - 5.1 Technical Feasibility
  - 5.2 Economic Feasibility
  - 5.3 Operational Feasibility
- 14. Chapter 6: Requirement Analysis
  - 6.1 Functional Requirements
  - 6.2 Non-Functional Requirements
- 15. Chapter 7: Hardware and Software Specifications
- 16. Chapter 8: System Architecture & Design
  - 8.1 Modular Subsystem Architecture
  - 8.2 Security Boundaries
- 17. Chapter 9: UML and Data Flow Diagrams
- 18. Chapter 10: Module Descriptions
- 19. Chapter 11: Database Design and Schema
- 20. Chapter 12: Implementation Details
- 21. Chapter 13: User Interface and Dashboard
- 22. Chapter 14: Experimental Methodology
- 23. Chapter 15: Results and Discussion
- 24. Chapter 16: Software Testing & Verification
- 25. Chapter 17: Security & Safety Analysis
- 26. Chapter 18: System Limitations
- 27. Chapter 19: Conclusion
- 28. Chapter 20: Future Scope
- 29. References
- 30. Appendix

---

## 7. List of Figures

- **Figure 9.1**: High-Level System Architecture of CanarySentinel
- **Figure 9.2**: End-to-End Filesystem Telemetry and Event Data Flow
- **Figure 9.3**: Multi-Paradigm Detection Workflow (Configurations A, B, C)
- **Figure 9.4**: Hybrid Sliding-Window Correlation Sequence
- **Figure 9.5**: Automated Response and Process Containment State Machine
- **Figure 9.6**: Database Entity-Relationship (ER) Diagram
- **Figure 9.7**: Physical Deployment and macOS User-Space Boundary
- **Figure 9.8**: UML Use-Case Diagram for CanarySentinel Operators
- **Figure 9.9**: Streamlit Dashboard Overview and Real-Time Telemetry
- **Figure 9.10**: Comparative Detector Performance Charts

---

## 8. List of Tables

- **Table 4.1**: Comprehensive Literature Comparison Matrix
- **Table 11.1**: SQLite Database Schema Definitions
- **Table 14.1**: Standardized Behavioral Simulation Scenarios (B1–B4, S5–S6)
- **Table 15.1**: Side-by-Side Detector Performance Comparison ($N = 180$)
- **Table 15.2**: Confusion Matrices for Configurations A, B, and C
- **Table 15.3**: Scenario-by-Scenario Evaluation Breakdown
- **Table 15.4**: Detection Latency Distribution and 95% Confidence Intervals
- **Table 15.5**: System Resource Utilization Across Configurations
- **Table 16.1**: Summary of Automated Unit and Integration Test Cases (45 Passing)

---

## 9. Chapter 1: Introduction

### 1.1 Overview and Motivation
Cryptographic ransomware represents an acute operational threat across corporate and consumer computing environments. Attackers leverage living-off-the-land binaries, script interpreters, and custom compiled binaries to systematically encrypt user documents and demand ransoms. Because modern encryption algorithms cannot be broken without quantum computation or key exposure, defense must prioritize pre-encryption or early-encryption detection and automated containment.

### 1.2 Problem Statement
Endpoint defense faces a dilemma:
- **Heuristic behavioral engines** detect mass modifications but generate frequent false alarms during benign developer builds or backups.
- **Canary honeypots** alert instantly upon decoy access but false-alarm on accidental single-file inspections and remain blind when attackers skip decoys.
- **The Core Question**: Does corroborating canary interactions with contextual filesystem behavior improve detection precision and limit file damage without introducing fatal blind spots?

### 1.3 Research Objectives
1. Implement a complete, modular, local prototype on macOS Apple Silicon.
2. Monitor filesystem activity inside a strictly enforced sandbox.
3. Compare three detection configurations (Baseline, Canary-Only, Hybrid).
4. Implement a safe activity simulator executing benign and synthetic encryption workloads.
5. Provide a Streamlit dashboard with real-time telemetry, experiment execution, and metric visualization.
6. Conduct 180 controlled empirical trials and perform rigorous mathematical verification.

---

## 10. Chapter 2: Existing System Analysis

### 2.1 Overview of Conventional Approaches
1. **Signature-Based Antivirus (AV)**: Computes hashes and inspects byte patterns. Fails against polymorphic zero-day payloads.
2. **Behavioral Volume Monitors (e.g., CryptoDrop)**: Evaluates file entropy and modification rates. Effective but prone to false alarms during legitimate batch tasks.
3. **Pure Decoy Tripwires (e.g., Honeypot shares)**: Deploys decoy files. High speed, but vulnerable to false alarms from desktop indexers and complete evasion from non-linear directory crawlers.

### 2.2 Drawbacks of Current Solutions
- High False-Positive Rate (FPR) disrupting business operations.
- Kernel driver dependencies causing OS instability and lack of cross-platform portability.
- Single point of failure: honeypot evasion renders pure deception useless.

---

## 11. Chapter 3: Proposed System

### 3.1 System Overview
**CanarySentinel** is a user-space endpoint detection and response system designed for macOS. It pairs strategic canary deployment with a temporal sliding-window correlation engine that evaluates surrounding filesystem velocity before dispatching high-severity alerts.

### 3.2 Key Features and Novelty
1. **Correlated Context Engine**: Requires both a canary hit and burst velocity ($\ge 3$ ops in 5.0s), eliminating uncorroborated false positives.
2. **Asynchronous Debouncing Pipeline**: Deduplicates raw macOS FSEvents within a 100 ms window to prevent alert flooding.
3. **Strict Sandbox Safety**: Enforces directory resolution constraints preventing symlink escapes or unauthorized modifications.
4. **Transparent Risk Engine**: Computes normalized risk scores ($0–100$) with human-readable evidence strings.

---

## 12. Chapter 4: Literature Review

A review of foundational literature informs CanarySentinel's architecture:
- **CryptoDrop (Scaife et al., 2016)** [[REF-01]](literature/REFERENCES.md#ref-01): Demonstrated that file entropy and rapid modification heuristics detect ransomware early.
- **ShieldFS (Continella et al., 2016)** [[REF-02]](literature/REFERENCES.md#ref-02): Proved that copy-on-write staging limits damage but introduces high kernel CPU overhead.
- **R-Sentry (Al-rimy et al., 2019)** [[REF-04]](literature/REFERENCES.md#ref-04): Combined honeyfiles with process memory trajectories to suppress false alarms.
- **RansomFisher (Ku et al., 2021)** [[REF-06]](literature/REFERENCES.md#ref-06): Highlighted the critical weakness of decoy files—showing that selective traversal avoids decoys entirely.

*(Refer to `literature/LITERATURE_REVIEW.md` and `literature/LITERATURE_COMPARISON_MATRIX.csv` for exhaustive details).*

---

## 13. Chapter 5: Feasibility Study

1. **Technical Feasibility**: Built using standard Python 3.12 libraries (`watchdog`, `psutil`, `sqlite3`, `streamlit`). Operates entirely in user space with zero kernel extensions.
2. **Economic Feasibility**: Completely open-source, local development requiring zero cloud APIs or commercial licensing fees.
3. **Operational Feasibility**: Resource-efficient footprint ($<38\text{ MB RAM}$, $<26\%\text{ CPU}$), compatible with standard workstation operations.

---

## 14. Chapter 6: Requirement Analysis

### 6.1 Functional Requirements
- **FR-1**: Deploy and register 8 strategic canary decoys with SHA-256 baseline hashing.
- **FR-2**: Ingest and debounce asynchronous filesystem events from macOS FSEvents.
- **FR-3**: Concurrently execute Baseline, Canary-Only, and Hybrid detection pipelines.
- **FR-4**: Safely terminate malicious simulator processes upon alert generation.
- **FR-5**: Persist events, alerts, actions, and trials in an ACID-compliant SQLite database.
- **FR-6**: Provide an interactive web dashboard for real-time monitoring and empirical research export.

### 6.2 Non-Functional Requirements
- **NFR-1 (Safety)**: Simulator must be physically incapable of modifying files outside `sandbox/`.
- **NFR-2 (Latency)**: Hybrid alert generation must execute in $<50\text{ ms}$.
- **NFR-3 (Reliability)**: Zero database deadlocks or corrupted records across batch trials.

---

## 15. Chapter 7: Hardware and Software Specifications

- **Hardware Platform**: Apple Mac mini / MacBook (Apple Silicon M1, 8-core CPU, 8 GB RAM, 256 GB SSD).
- **Operating System**: macOS Sequoia 15.3 (Darwin 24.3.0, arm64).
- **Core Language**: Python 3.12.9.
- **Key Libraries**: `watchdog 6.0.0`, `psutil 7.0.0`, `streamlit 1.43.0`, `pandas 2.2.3`, `pytest 8.3.5`.
- **Storage**: SQLite 3.46.0.

---

## 16. Chapter 8: System Architecture & Design

CanarySentinel comprises eight core subsystems:
1. **Sandbox Isolation Layer**: Confines all monitoring, simulation, and decoy files to `sandbox/`.
2. **Canary Manager**: Generates, registers, and verifies decoys (`000_canary.txt`, etc.).
3. **Filesystem Monitor**: Ingests OS filesystem telemetry via `watchdog.observers`.
4. **Event Normalizer**: Debounces events and tags decoy flags.
5. **Detection Suite**: Houses Baseline, Canary-Only, and Hybrid detection engines.
6. **Risk Engine**: Normalizes threat severity and generates evidence-backed alerts.
7. **Response Manager**: Terminates offending simulator PIDs via POSIX signals.
8. **Persistence & UI**: SQLite database and multi-page Streamlit dashboard.

---

## 17. Chapter 9: UML and Data Flow Diagrams

*(All complete Mermaid diagrams are maintained under `research_dossier/diagrams/` and `docs/diagrams/`).*

### Figure 9.1: System Architecture
```mermaid
flowchart TD
    SB["Sandbox Directory (sandbox/)"] -->|FSEvents| WD["Watchdog Monitor"]
    WD --> NORM["Event Normalizer & Debouncer"]
    NORM --> D_BASE["Baseline Detector (Velocity)"]
    NORM --> D_CAN["Canary-Only Detector (Tripwire)"]
    NORM --> D_HYB["Hybrid Detector (Sliding Window)"]
    D_BASE --> RE["Risk Engine"]
    D_CAN --> RE
    D_HYB --> RE
    RE --> RESP["Simulated Response Manager"]
    RESP -->|SIGTERM| SIM["Harmless Simulator"]
    RE --> DB[("SQLite DB")]
    DB --> UI["Streamlit Dashboard"]
```

---

## 18. Chapter 10: Module Descriptions

1. **`canary_manager.py`**: Deploys 8 canary files with lexicographical prefixes (`000_`) and diverse extensions (`.txt`, `.pdf`, `.docx`, `.db`). Computes SHA-256 hashes and verifies integrity.
2. **`fs_monitor.py`**: Wraps `watchdog.observers.Observer` to capture filesystem callbacks. Implements queueing and thread lifecycle management.
3. **`event_normalizer.py`**: Implements time-window debouncing (100 ms) to suppress duplicate OS events and enriches raw records into `NormalizedEvent` dataclasses.
4. **`detectors/baseline_detector.py`**: Evaluates moving-average event velocity. Triggers when rate $> 5\text{ ops/sec}$ and burst $> 5\text{ ops}$.
5. **`detectors/canary_detector.py`**: Intercepts events where `is_canary = True`. Triggers immediate alert upon modification or deletion.
6. **`detectors/hybrid_detector.py`**: Maintains a 5.0-second sliding event deque. Correlates canary hits with surrounding non-canary burst volume ($\ge 3$ events).
7. **`risk_engine.py`**: Evaluates detector signals, applying risk weights: Canary hit (+40), velocity anomaly (+30), rapid deletion (+20). Outputs scores $0–100$.
8. **`simulator/activity_simulator.py`**: Executes controlled workloads (B1–B4, S5–S6) strictly inside the sandbox using dummy text buffers.
9. **`response/response_manager.py`**: Dispatches `SIGTERM` exclusively to verified simulator PIDs. Implements safety checks preventing accidental system termination.
10. **`storage/database.py`**: Thread-safe SQLite layer with WAL mode, parameterized queries, and automatic migrations.
11. **`experiments/runner.py`**: Orchestrates automated batch trials across configurations and scenarios.
12. **`experiments/metrics.py`**: Calculates precision, recall, F1, FPR, latency, confidence intervals, and file damage metrics.

---

## 19. Chapter 11: Database Design and Schema

**Table 11.1: Core Tables in `canary_sentinel.db`**
- `canaries`: `id`, `path`, `original_hash`, `current_hash`, `created_at`, `status`.
- `events`: `id`, `timestamp`, `event_type`, `path`, `is_canary`, `file_size`, `entropy`, `scenario_id`.
- `alerts`: `id`, `timestamp`, `detector_type`, `severity`, `risk_score`, `evidence`, `triggered_by`, `scenario_id`.
- `actions`: `id`, `timestamp`, `alert_id`, `action_type`, `target_pid`, `status`, `outcome_details`.
- `experiment_runs`: `run_id`, `scenario_id`, `detector_type`, `status`, `total_events`, `files_damaged`, `ops_prevented`, `latency_ms`, `started_at`, `completed_at`.
- `system_metrics`: `id`, `scenario_id`, `timestamp`, `cpu_percent`, `memory_mb`, `thread_count`.

---

## 20. Chapter 12: Implementation Details

- **Language & Runtime**: Python 3.12.9.
- **Thread Safety**: Detectors operate on decoupled event queues; SQLite connections use connection pooling and WAL mode.
- **Sandboxing**: Hardcoded root path canonicalization (`os.path.realpath`) prevents directory traversal attacks (`../`).
- **Signal Handling**: Responses utilize POSIX `os.kill(pid, signal.SIGTERM)` followed by verification polling.

---

## 21. Chapter 13: User Interface and Dashboard

The Streamlit dashboard (`app.py`) provides six distinct operational views:
1. **Overview & Telemetry**: Live status of filesystem monitoring, sandbox health, active canaries, total events, alerts, and system health metrics.
2. **Decoy & Sandbox Controls**: Deploy, inspect, and regenerate canary files; safe sandbox reset with clear confirmation dialogues.
3. **Live Event Stream**: Real-time table of normalized events with filtering by event type and canary status.
4. **Incidents & Evidence Alerts**: Granular alert feed detailing severity, risk scores, and evidence strings.
5. **Simulation & Experiments**: Controls to launch single scenarios or batch experimental trials.
6. **Comparative Research Analysis**: Side-by-side performance matrix, scenario breakdowns, latency comparisons, and CSV export.

---

## 22. Chapter 14: Experimental Methodology

The experimental framework evaluated three configurations across six standardized scenarios:
- **Configurations**: Baseline (A), Canary-Only (B), Hybrid (C).
- **Scenarios**:
  - `B1`: Single read (Benign)
  - `B2`: Rapid edit of 10 developer docs (Benign)
  - `B3`: Accidental read of `000_canary.txt` (Benign)
  - `B4`: Mixed burst of 3 operations (Benign)
  - `S5`: Rapid encryption of canaries + 10 user docs (Attack)
  - `S6`: Rapid encryption of 10 user docs skipping canaries (Attack)
- **Trial Count**: 10 repetitions $\times$ 6 scenarios $\times$ 3 configurations = **180 trials**.

---

## 23. Chapter 15: Results and Discussion

### 15.1 Summary of Evaluated Metrics ($N = 180$)

**Table 15.1: Comparative Performance Summary**

| Metric | Baseline | Canary-Only | Hybrid |
|:---|:---:|:---:|:---:|
| Total Trials | 60 | 60 | 60 |
| TP / FP / TN / FN | 20 / 10 / 30 / 0 | 10 / 10 / 30 / 10 | 10 / 0 / 40 / 10 |
| **Precision** | 66.67% | 50.00% | **100.00%** |
| **Recall** | **100.00%** | 50.00% | 50.00% |
| **$F_1$-Score** | **0.8000** | 0.5000 | 0.6667 |
| **False Positive Rate** | 25.00% | 25.00% | **0.00%** |
| **Mean Latency** | 147.1 ms | **18.9 ms** | 26.1 ms |
| 95% Confidence Interval | $\pm 36.5$ ms | $\pm 3.4$ ms | $\pm 5.2$ ms |
| Mean Files Damaged | **3.05** | 5.05 | 5.05 |
| Damage in S5 (Canary Hit) | 1.10 files | **0.10 files** | **0.10 files** |
| Damage in S6 (Canary Evaded)| **5.00 files** | 10.00 files | 10.00 files |
| Mean Ops Prevented | **65.33%** | 45.42% | 45.42% |
| Ops Prevented in S5 | 100.0% | **~99.1%** | **~99.1%** |
| Ops Prevented in S6 | **55.24%** | 0.00% | 0.00% |

### 15.2 Discussion of Findings
1. **Hybrid Solves False Alarms**: In Scenario B3, Hybrid rejected the single canary read because no surrounding velocity occurred, achieving **0.0% FPR** and **100% Precision**.
2. **Rapid Containment Limits Damage**: In Scenario S5, Hybrid halted the attack in **26.1 ms**, limiting damage to **0.10 files** out of 11 targeted operations (approximately 99.1% prevented).
3. **The Evasion Blindspot**: In Scenario S6, because malware avoided canaries, Hybrid failed entirely (Recall = 50%), whereas Baseline's behavioral heuristic detected the attack in 147.1 ms.
4. **Architectural Implication**: Hybrid cannot stand alone; it must serve as an aggressive fast-path trigger alongside a behavioral safety net.

---

## 24. Chapter 16: Software Testing & Verification

CanarySentinel was subjected to automated unit and integration testing via `pytest`. All **56 automated tests passed** in 5.06 seconds:

**Table 16.1: Automated Test Suite Summary**

| Test Module | Coverage Scope | Tests | Status |
|:---|:---|:---:|:---:|
| `test_canary_manager.py` | Deployment, hashing, tampering detection, cleanup | 6 | **PASS** |
| `test_fs_monitor.py` | Event capturing, thread start/stop, queue handling | 4 | **PASS** |
| `test_event_normalizer.py`| Path canonicalization, debouncing, deduplication | 5 | **PASS** |
| `test_detectors.py` | Baseline thresholds, canary tripwire, hybrid sliding window | 8 | **PASS** |
| `test_risk_engine.py` | Score calculation, severity mapping, evidence strings | 4 | **PASS** |
| `test_simulator.py` | Sandbox bounds, benign scenarios, synthetic encryption | 5 | **PASS** |
| `test_response_manager.py`| Target verification, safe PID signaling, whitelist checks | 4 | **PASS** |
| `test_database.py` | ACID operations, WAL concurrency, migrations | 5 | **PASS** |
| `test_experiments.py` | Batch execution, metric recalculation, export | 4 | **PASS** |
| **Total** | **Comprehensive Full-System Test Suite** | **45** | **100% PASS** |

---

## 25. Chapter 17: Security & Safety Analysis

1. **Sandbox Enforcement**: Absolute path verification prevents directory traversal (`os.path.commonpath`).
2. **Response Safety**: Whitelist checks prevent signaling system daemons (`PID 1`, parent processes). Only child simulator PIDs are eligible for termination.
3. **Database Integrity**: Parameterized SQL queries eliminate SQL injection vulnerabilities.

---

## 26. Chapter 18: System Limitations

1. **User-Space Event Delay**: Notifications via `watchdog` arrive asynchronously (10–25 ms after disk commit), preventing pre-write synchronous blocking.
2. **Decoy Discovery Vulnerability**: Malware inspecting file entropy baselines or known naming formats could identify canaries.
3. **Process Attribution**: Resolving the originating process PID in user space relies on system sampling rather than inline kernel call attribution.

---

## 27. Chapter 19: Conclusion

CanarySentinel successfully demonstrates that cross-correlating canary interactions with contextual filesystem behavior solves the false-alarm epidemic of deception systems, delivering **100% precision** and achieving containment in **26.1 ms**. However, because deception tripwires remain vulnerable to evasion, a hybrid engine cannot serve as a solitary defense. Instead, combining hybrid fast-path triggers with behavioral safety nets provides the optimal trade-off between false-alarm suppression and complete threat coverage.

---

## 28. Chapter 20: Future Scope

1. **macOS Endpoint Security Framework**: Transition from `watchdog` to native Darwin `EndpointSecurity.framework` (`es_client`) for synchronous pre-write blocking.
2. **Adaptive Decoy Placement**: Deploy machine-learning agents to dynamically position decoys along high-probability ransomware traversal routes.
3. **Live Malware Benchmarking**: Evaluate the architecture inside isolated virtual machines against real-world ransomware families.

---

## 29. References

*(Refer to `literature/REFERENCES.md` for complete bibliographic citations and DOIs).*

1. Scaife, N., et al. (2016). *CryptoDrop: Early detection for ransomware*. IEEE ICDCS.
2. Continella, A., et al. (2016). *ShieldFS: a self-healing, ransomware-aware filesystem*. ACM ACSAC.
3. Kharraz, A., et al. (2015). *Cutting the Gordian Knot: A Look Under the Hood of Ransomware Analysis*. Springer DIMVA.
4. Al-rimy, B. A. S., et al. (2019). *R-Sentry: Pseudo feedback-based early detection method for crypto-ransomware*. Elsevier Computers & Security.
5. Park, J., et al. (2021). *GuardFS: A File System for Integrated Detection and Mitigation of Linux-Based Ransomware*. IEEE TIFS.
6. Ku, S., et al. (2021). *RansomFisher: A Behavior-Based Detection and Mitigation Framework for Ransomware Without Relying on Decoy Files*. IEEE Access.
7. Moore, C. (2017). *Detecting Ransomware with Honeypot Techniques*. IEEE ICCC.
8. Mehnaz, S., et al. (2018). *RWGuard: A Real-Time Detection and Resilient Recovery System Against Ransomware*. IEEE ICDCS.
9. Shannon, C. E. (1948). *A Mathematical Theory of Communication*. Bell System Technical Journal.
10. Arp, D., et al. (2022). *Dos and Don'ts of Machine Learning in Computer Security*. CACM.

---

## 30. Appendix

### Appendix A: Installation and Execution Commands
```bash
# Environment setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run automated test suite
pytest -v

# Launch interactive Streamlit dashboard
streamlit run canary_sentinel/dashboard/app.py
```

### Appendix B: File Integrity Verification Hashes
- Database: `canary_sentinel.db` (180 verified trials)
- Source Modules: `canary_sentinel/` (14 Python modules, 100% clean imports)

