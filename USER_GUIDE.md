# CanarySentinel User Guide & Operations Manual

This guide provides step-by-step instructions for operating, experimenting with, and auditing the **CanarySentinel** endpoint ransomware behavioral detection system.

---

## 1. System Requirements & Installation

### 1.1 Prerequisites
- **Operating System**: macOS 12+ (optimized for Apple Silicon M1/M2/M3/M4 or Intel).
- **Python**: Version 3.10 to 3.14.
- **Hardware Target**: 8 GB RAM, $\ge 500$ MB free disk space.
- **Dependencies**: `watchdog`, `psutil`, `streamlit`, `pandas`, `pytest`.

### 1.2 Installation Steps
```bash
# 1. Clone or navigate to the project directory
cd /Users/gouravsingh/Downloads/CanarySentinel

# 2. Create and activate a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 2. Using the Unified CLI (`run_sentinel.py`)

CanarySentinel includes a management CLI (`run_sentinel.py`) that enables headless operation, automated testing, benchmarking, and reporting:

### 2.1 View System Status & Active Canaries
Inspect current sandbox directory, database location, active decoy traps, and event counters:
```bash
python run_sentinel.py status
```

### 2.2 Run Automated Test Suite
Execute the 40 automated pytest unit and safety tests:
```bash
python run_sentinel.py test
```

### 2.3 Deploy Decoy Traps
Deploy 8 strategic decoy canary files across `./sandbox` subdirectories:
```bash
python run_sentinel.py deploy-canaries
```

### 2.4 Execute a Single Scenario Trial
Run any scenario against any of the three detector configurations (`baseline`, `canary_only`, `hybrid`):
```bash
# Run suspicious attack with hybrid detector
python run_sentinel.py simulate --scenario canary_plus_rapid_bulk --detector hybrid

# Run benign canary inspection with canary-only detector (demonstrates false positive)
python run_sentinel.py simulate --scenario canary_touch_benign --detector canary_only

# Run evasive attack with baseline detector
python run_sentinel.py simulate --scenario rapid_bulk_without_canary --detector baseline
```

### 2.5 Run Full Comparative Benchmark Suite
Run all 6 scenarios across all 3 detector configurations (18 total trials):
```bash
python run_sentinel.py benchmark --iterations 1
```

### 2.6 Generate Research Summary Report
Produce a dynamic Markdown research report strictly from actual SQLite trial records:
```bash
python run_sentinel.py report --output RESEARCH_SUMMARY.md
```

### 2.7 Export Data to CSV
Export SQLite tables (`events.csv`, `alerts.csv`, `trials.csv`, `metrics_summary.csv`) to an exports directory:
```bash
python run_sentinel.py export --output-dir ./exports
```

### 2.8 Safe Sandbox & Database Reset
```bash
# Clean sandbox contents safely
python run_sentinel.py reset

# Clean sandbox contents AND wipe SQLite database records
python run_sentinel.py reset --all
```

---

## 3. Interactive Web Dashboard Walkthrough

### 3.1 Launching the Dashboard
Launch Streamlit on local port 8501:
```bash
python run_sentinel.py dashboard
```
Open your browser to: **[http://localhost:8501](http://localhost:8501)**.

### 3.2 Dashboard Sections

```
┌────────────────────────────────────────────────────────────────────────┐
│  🛡️ CanarySentinel Dashboard Navigation                                 │
├────────────────────────────────────────────────────────────────────────┤
│  1. Overview & Telemetry           - System health, metrics & activity │
│  2. Decoy & Sandbox Controls       - Deploy canaries, verify, purge    │
│  3. Live Event Stream              - Filterable event log with CSV     │
│  4. Incidents & Evidence Alerts    - Audit cards & structured rationale│
│  5. Simulation & Experiments       - Single & benchmark trial runner   │
│  6. Comparative Research Analysis  - Confusion matrix & report download│
└────────────────────────────────────────────────────────────────────────┘
```

#### Section 1: Overview & Telemetry
- **KPI Cards**: Displays Total Events, Total Alerts Raised, Scenarios Evaluated, and Active Decoy Traps.
- **Host & Monitor Telemetry**: Live status of Watchdog observer, process memory footprint, and CPU load.
- **Activity Summary**: Event type distributions and severity breakdown charts.
- **Recent Activity Feed**: The 8 most recent filesystem operations.

#### Section 2: Decoy & Sandbox Controls
- **Deploy Canaries**: One-click generation of realistic synthetic bait files.
- **Verify Integrity**: Audits disk hashes against the database registry to classify each canary as `ACTIVE`, `MODIFIED`, or `DELETED`.
- **Safe Reset Controls**: Confirmation checkboxes must be checked before sandbox purge or database wipe buttons become enabled, preventing accidental data loss.

#### Section 3: Live Event Stream
- **Search & Filter**: Real-time filtering by file path substring, asset category (Canary vs User), event action (`CREATE`, `MODIFY`, `DELETE`, `MOVE`), and row limits.
- **Entropy Highlighting**: Visual indicators classifying files as High ($H \ge 7.0$), Medium, or Low entropy.
- **CSV Export**: One-click download button for filtered events.

#### Section 4: Incidents & Evidence Alerts
- **Severity Badges**: Color-coded indicators (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
- **Audit Cards**: Expand each alert to inspect:
  - Quantitative Risk Score gauge ($0 - 100$).
  - Detection Confidence level ($0 - 100\%$).
  - Containment Response Status (`BLOCKED`, `PREVENTED`, `NONE`).
  - Structured text explanation detailing triggered heuristics.
  - Linked triggering event and correlated supporting events with relative timestamps ($\Delta t$).
- **CSV Export**: Export all incident alerts to CSV.

#### Section 5: Simulation & Experiments
- **Scenario Catalog**: Descriptions, planned operation counts, and expected detector outcomes for all 6 scenarios.
- **Single Scenario Execution**: Interactive trial runner with live latency and damage metrics.
- **Automated Benchmark Suite**: Run the 18-trial matrix with real-time progress bar.
- **Historical Trial Log**: Complete trial table with scenario IDs, durations, damaged files, and ops prevented (%).

#### Section 6: Comparative Research Analysis
- **Empirical Verdict**: Direct answer to the research question based on SQLite data.
- **Performance Matrix**: Side-by-side table displaying Precision, Recall, F1, FPR, Latency range, Files Damaged, and Operations Prevented.
- **Confusion Matrix Breakdown**: 2x2 grid displaying TP, FP, TN, FN counts for each detector configuration.
- **Comparative Charts**: Interactive Altair charts comparing detection quality, containment effectiveness, and resource overhead.
- **Report Generator**: Download button to export a Markdown report (`CANARY_SENTINEL_RESEARCH_SUMMARY.md`) or CSV summary.

---

## 4. Understanding Alerts and Evidence

Every security alert generated by CanarySentinel adheres to a transparent, reproducible structure:

```text
=== HYBRID DETECTOR ALERT (CRITICAL) ===
Risk Score: 100/100 | Severity: CRITICAL
Triggering Action: MODIFY on 'documents/user_doc_01.txt' (Entropy: 7.82, Size: 2048B, Canary: False)

Identified Risk Factors:
  • Canary file breached: '!00_corporate_passwords.xlsx' (MODIFY) confirmed by contextual filesystem damage
  • High-entropy modification on 2 companion file(s) (entropy >= 6.8)

Correlated Contextual Evidence (2 events):
  - [MODIFY] [CANARY] !00_corporate_passwords.xlsx (entropy=5.17, delta_t=0.03s)
  - [MODIFY] documents/user_doc_02.txt (entropy=7.84, delta_t=0.01s)

Action Recommendation: Intercept and prevent subsequent operations.
```
- **Risk Score**: Derived from severity weights of matched indicators.
- **Evidence Trail**: Captures exact companion events that confirmed the attack within the observation window.
- **Zero OS Disruption**: Containment signals the harmless simulator to abort planned operations without killing real processes.

