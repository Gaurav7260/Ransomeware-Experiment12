# Project Contributions & Authorship Breakdown

## 1. Summary of Contributions

CanarySentinel was designed and developed as a complete, working local MVP to investigate whether combining canary-file interactions with contextual filesystem behavior improves ransomware detection quality and reduces simulated file damage compared with canary-only and behavior-only detection.

The contributions span four major areas:

1. **System Architecture & Sandbox Security Engineering**
   - Engineered a robust, zero-leak path validation and containment engine in `canary_sentinel/core/sandbox.py`.
   - Built strict defenses against directory traversal (`../`), null-byte injection, symlink escapes, and system root directory hijacking (`/`, `/System`, `/Library`, `/etc`, `/Users`).
   - Implemented thread-safe, SQLite-backed persistent storage using Write-Ahead Logging (WAL) and configurable busy timeouts.

2. **Filesystem Monitoring & Signal Normalization**
   - Designed a non-blocking Watchdog observer thread anchored exclusively to `./sandbox`.
   - Engineered a 50ms sliding-window debouncer in `canary_sentinel/monitoring/normalizer.py` to suppress duplicate macOS FSEvents notifications.
   - Standardized disparate filesystem signals into a strongly-typed `NormalizedEvent` entity with dynamic Shannon entropy calculation ($0.0 - 8.0$ bits/byte).

3. **Multi-Detector Research Implementation**
   - **Configuration A (Baseline Detector)**: Implemented volume burst tracking, high Shannon entropy thresholding ($\ge 7.0$), and mass rename detection without canary awareness.
   - **Configuration B (Canary-Only Detector)**: Implemented instantaneous tripwire detection based on cryptographic baseline state checks and fast in-memory decoy lookup.
   - **Configuration C (Hybrid Correlated Detector)**: Authored a temporal correlation engine that anchors on canary breach events and verifies companion filesystem context within a 3.0-second sliding window before triggering containment.
   - **Transparent Risk Engine**: Authored a deterministic 0–100 risk scoring algorithm with four severity tiers and human-auditable rule explanations.

4. **Harmless Simulation & Safety Response Management**
   - Designed 6 standardized test scenarios (4 benign, 2 suspicious) that operate strictly on generated test documents inside `./sandbox`.
   - Authored an atomic non-destructive containment manager in `canary_sentinel/simulation/response_manager.py` that halts simulator operation loops without terminating real operating-system processes.
   - Built an automated 18-trial benchmark runner and statistical metrics calculator computing Precision, Recall, F1, FPR, latency, simulated file damage, and operations prevented.

5. **User Interface & Research Dashboard**
   - Authored an interactive Streamlit dashboard featuring 6 views: Overview & Telemetry, Decoy & Sandbox Controls, Live Event Stream, Incidents & Evidence Alerts, Simulation & Experiments, and Comparative Research Analysis.
   - Integrated dynamic CSV data exports and automated Markdown research summary generation.

---

## 2. Distinction: Third-Party Dependencies vs. Authored Code

| Component | Technology / Library | Role in Project | Originality |
| :--- | :--- | :--- | :--- |
| **Filesystem Event Hook** | `watchdog` (Python) | Captures OS-level filesystem notifications | Third-party library utilized for OS event hook |
| **Event Debouncing & Normalization** | `canary_sentinel/monitoring/` | 50ms sliding window and `NormalizedEvent` translation | **Original CanarySentinel code** |
| **Decoy Deployment & Integrity** | `canary_sentinel/canary/` | Alphabetical priority lures and SHA-256 tracking | **Original CanarySentinel code** |
| **Detection Engines (A, B, C)** | `canary_sentinel/detection/` | Baseline burst, Canary tripwire, and Hybrid temporal correlation | **Original CanarySentinel code** |
| **Risk Scoring & Explanations** | `canary_sentinel/detection/risk_engine.py` | Explainable quantitative risk and severity mapping | **Original CanarySentinel code** |
| **Sandbox Containment** | `canary_sentinel/core/sandbox.py` | Path canonicalization, traversal checks, symlink jail | **Original CanarySentinel code** |
| **Harmless Simulation Engine** | `canary_sentinel/simulation/` | 6 harmless synthetic filesystem scenarios | **Original CanarySentinel code** |
| **Containment Manager** | `canary_sentinel/simulation/response_manager.py` | Non-destructive atomic loop interception | **Original CanarySentinel code** |
| **Data Persistence** | `sqlite3` (Python standard library) | Relational database engine | Python standard library |
| **Data Models & Schema** | `canary_sentinel/storage/` | Relational tables, WAL setup, and dataclasses | **Original CanarySentinel code** |
| **System Telemetry** | `psutil` | CPU (%) and RAM (MB) sampling | Third-party utility library |
| **Research Dashboard** | `streamlit`, `pandas` | Interactive web dashboard and tabular views | Framework utilized; **all dashboard views authored** |
| **Automated Testing** | `pytest` | Test runner framework | Framework utilized; **56 automated tests authored** |

