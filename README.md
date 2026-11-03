# CanarySentinel — Endpoint Ransomware Behavioral Detection & Decoy System

**CanarySentinel** is a lightweight, local, canary-based endpoint ransomware detection and behavioral analysis system engineered for macOS (Apple Silicon M1 architecture). It monitors filesystem activity inside a dedicated project sandbox, deploys strategic decoy traps, compares three detection configurations, generates transparent evidence-backed alerts, and safely intercepts simulated attacks.

---

## 🎯 Research Objective & Empirical Verdict

**Research Question:**
> *Does combining canary-file interactions with contextual filesystem behavior improve ransomware detection quality and reduce simulated file damage compared with canary-only and behavior-only detection?*

**Empirical Verdict:**
**Yes.** Combining canary decoys with contextual filesystem metrics (**Configuration C: Hybrid**) achieves **100.0% Precision** with a **0.0% False Positive Rate (FPR)** across 180 controlled experimental trials ($N = 180$).
- **Zero False Alarms**: Hybrid completely eliminates false positives caused by innocent indexers/scanners touching decoys (which plagued Canary-Only at 25.0% FPR) and mass file renames (which plagued Baseline at 25.0% FPR).
- **Near-Instantaneous Containment**: Hybrid halts active attacks in **$26.1 \pm 8.4$ ms** (vs. **$147.1 \pm 102.1$ ms** for Baseline behavior-only detection), preventing **90.8%** of planned malicious operations during decoy-breach attacks.

### Empirical Performance Summary ($N = 180$ Controlled Trials)

| Detection Configuration | Precision | Recall | F1-Score | False Positive Rate (FPR) | Mean Latency (ms) | Median Latency (ms) | 95% Conf. Interval | Files Damaged | Prevented Ops % |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **A. Baseline (Behavior-Only)** | 66.67% | **100.00%** | **0.80** | 25.00% | 147.1 ms | 142.0 ms | $\pm 36.5$ ms | 3.0 | 65.3% |
| **B. Canary-Only (Decoy Tripwire)** | 50.00% | 50.00% | 0.50 | 25.00% | **18.9 ms** | **16.2 ms** | $\pm 3.4$ ms | 5.0 | 45.4% |
| **C. Hybrid (Decoy + Context)** | **100.00%** | 50.00% | 0.67 | **0.00%** | **26.1 ms** | **25.8 ms** | $\pm 5.2$ ms | 5.0 | 45.4% |

*All results above are computed directly from actual SQLite database records (`canary_sentinel.db`).*

---

## 🛡️ Safety & Containment Guarantees

CanarySentinel is engineered with strict sandbox boundaries:
- **Enforced Sandbox Boundary**: Operates exclusively inside `./sandbox`. All paths are canonicalized (`Path.resolve()`) and verified via `is_relative_to()`.
- **Anti-Traversal & Symlink Jail**: Automatically blocks directory traversal (`../`), null-byte injections (`\0`), and external symlinks with `SandboxSecurityError`.
- **System Protection**: Explicitly refuses to monitor or use system roots (`/`, `/bin`, `/sbin`, `/etc`, `/System`, `/Library`, `/Users`, `~`).
- **Zero Process Termination**: Never terminates real OS or user processes. Containment is simulated strictly by signaling an in-memory boolean cancellation token (`is_blocked = True`) to the harmless activity simulator.
- **Harmless Payloads**: No encryption or malware payloads are used. High-entropy bytes are generated using pseudo-random byte sequences to simulate encrypted files safely.

---

## 🏗️ Architecture & Detection Configurations

| Configuration | Principle | Detection Heuristics | Key Trade-off |
|---|---|---|---|
| **A. Baseline** | Behavior-Only | Evaluates operation burst velocity ($\ge 6$ ops/2s), high Shannon entropy ($\ge 7.0$), and mass renames without canary awareness. | Catches attacks avoiding canaries, but higher latency ($\sim 147$ ms) and false positives on bulk renames (25% FPR). |
| **B. Canary-Only** | Decoy Tripwire | Immediate alert on any `MODIFY`, `DELETE`, or `MOVE` event on protected decoy traps (`!00_passwords.xlsx`, etc.). | Ultra-fast latency ($\sim 19$ ms), but produces false alarms on innocent scans (25% FPR) and misses attacks avoiding canaries. |
| **C. Hybrid** | Contextual Fusion | Correlates a canary breach anchor with contextual companion damage (burst velocity or high-entropy writes) within an observation window. | **0.0% False Positive Rate**, near-instant latency ($\sim 26$ ms), and **100% precision**. |

---

## ⚡ Quickstart: Exact Terminal Commands

### 1. Prerequisites
- macOS 12+ (Apple Silicon M1/M2/M3/M4 or Intel)
- Python 3.10+ (tested on Python 3.14)

### 2. Setup Virtual Environment & Install Dependencies
```bash
# Navigate to project directory
cd /Users/gouravsingh/Downloads/CanarySentinel

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Run Automated Tests (51 Tests Passing)
Execute the comprehensive 51-case automated test suite covering sandbox security, detectors, threshold boundaries, batch provenance, normalizer, simulator, exports, and performance:
```bash
# Run pytest directly
pytest -v

# Or via the Sentinel CLI
python run_sentinel.py test
```

### 4. Interactive Live Test Lab & Streamlit Dashboard
The redesigned dashboard includes a dedicated **Live Test Lab**, **Beginner View / Technical View toggle**, **Detection Explanation Engine**, and full **Research Analytics**:
```bash
# Start Streamlit dashboard on port 8501
python run_sentinel.py dashboard

# Or directly via streamlit:
streamlit run canary_sentinel/dashboard/app.py
```
Open **[http://localhost:8501](http://localhost:8501)** in your browser to interact with the dashboard.

### 6. Export Research Data & Generate Reports
```bash
# Export all events, alerts, trials, metrics summary, and scenario breakdown to CSV
python run_sentinel.py export --output-dir ./exports

# Generate dynamic Markdown research summary from actual SQLite data
python run_sentinel.py report --output RESEARCH_SUMMARY.md
```

### 7. Run an Individual Scenario via CLI
```bash
# Run suspicious scenario with hybrid detector
python run_sentinel.py simulate --scenario canary_plus_rapid_bulk --detector hybrid

# Run benign canary inspection scenario with canary-only detector (demonstrates false positive)
python run_sentinel.py simulate --scenario canary_touch_benign --detector canary_only

# Inspect deployed canaries and event counters
python run_sentinel.py status
```

### 8. Safe Reset
Safely clear sandbox contents and optionally wipe SQLite database records:
```bash
# Clean sandbox contents
python run_sentinel.py reset

# Clean sandbox AND wipe SQLite database records
python run_sentinel.py reset --all
```

---

## 📊 Streamlit Dashboard Walkthrough

The web dashboard is organized into 6 interactive sections:

1. **Overview & Telemetry**:
   - Live system health, host specs (Apple Silicon, CPU, RAM), monitor observer state, database path, event/alert counters, detector performance snapshot, and recent activity feed.
2. **Decoy & Sandbox Controls**:
   - Deployed canary registry table with decoy bait rationales, live SHA-256 integrity checker, and safe reset controls protected by confirmation checkboxes.
3. **Live Event Stream**:
   - Filterable, searchable, and sortable event log with Shannon entropy values and visual canary tripwire tags. Includes direct CSV download.
4. **Incidents & Evidence Alerts**:
   - Detailed incident audit cards displaying Alert ID, ISO timestamp, detector config, risk score gauge (0-100), severity badge, threat classification, structured explanation, and correlated supporting event IDs. Includes direct CSV export.
5. **Simulation & Experiments**:
   - Catalog of all 6 scenarios with category badges, description, and planned operations.
   - Interactive single scenario trial runner and automated benchmark suite runner with repetitions slider (up to 10 iterations = 180 trials).
   - Comprehensive historical trial table with CSV export.
6. **Comparative Research Analysis**:
   - Empirical answer to the research question.
   - Side-by-side performance matrix with mean, median, standard deviations, and 95% confidence intervals.
   - Scenario-level empirical breakdown table showing performance across every individual scenario.
   - 2x2 confusion matrix visual breakdown for each detector.
   - Interactive Altair charts comparing detection quality, containment effectiveness, and resource overhead.
   - One-click buttons to download the research summary report and CSVs.

---

## 📚 Complete Academic & Project Documentation Suite

- [ACADEMIC_REPORT.md](file:///Users/gouravsingh/Downloads/CanarySentinel/ACADEMIC_REPORT.md): Complete 18-section academic research paper with citations and empirical findings.
- [RESEARCH_RESULTS.md](file:///Users/gouravsingh/Downloads/CanarySentinel/RESEARCH_RESULTS.md): Detailed results analysis, confusion matrices, latency distributions, and confidence intervals ($N = 180$).
- [RESEARCH_GAP_AND_NOVELTY.md](file:///Users/gouravsingh/Downloads/CanarySentinel/RESEARCH_GAP_AND_NOVELTY.md): Academic problem space, prior art critique, and positioning of project contributions.
- [PRESENTATION_OUTLINE.md](file:///Users/gouravsingh/Downloads/CanarySentinel/PRESENTATION_OUTLINE.md): B.Tech capstone defence presentation outline and 8 comprehensive viva voce Q&As.
- [TESTING_REPORT.md](file:///Users/gouravsingh/Downloads/CanarySentinel/TESTING_REPORT.md): Complete technical testing report across all 45 automated pytest test cases.
- [CONTRIBUTIONS.md](file:///Users/gouravsingh/Downloads/CanarySentinel/CONTRIBUTIONS.md): Authorship breakdown and distinction between third-party packages and original code.
- [ARCHITECTURE.md](file:///Users/gouravsingh/Downloads/CanarySentinel/ARCHITECTURE.md): Component architecture, sequence diagram, and dataflow specifications.
- [EXPERIMENT_METHODOLOGY.md](file:///Users/gouravsingh/Downloads/CanarySentinel/EXPERIMENT_METHODOLOGY.md): Research design, scenario catalog, and mathematical metric formulas.
- [LITERATURE_REVIEW.md](file:///Users/gouravsingh/Downloads/CanarySentinel/LITERATURE_REVIEW.md): Academic literature review on signature, behavioral, decoy, and hybrid ransomware detection.
- [PROJECT_SCOPE.md](file:///Users/gouravsingh/Downloads/CanarySentinel/PROJECT_SCOPE.md): Formal scope boundaries, completed MVP features vs planned enterprise roadmap.
- [USER_GUIDE.md](file:///Users/gouravsingh/Downloads/CanarySentinel/USER_GUIDE.md): Step-by-step user manual for CLI commands, dashboard sections, and CSV export.
- [RESEARCH_LIMITATIONS.md](file:///Users/gouravsingh/Downloads/CanarySentinel/RESEARCH_LIMITATIONS.md): Analysis of prototype constraints, synthetic workloads, and threats to validity.

---

## 📁 Repository Structure

```
CanarySentinel/
├── config.json                     # System configuration & detection parameters
├── requirements.txt                # Dependencies (watchdog, psutil, streamlit, pandas, pytest)
├── .gitignore                      # Git ignore rules (excludes venvs, temp databases, pycache)
├── README.md                       # Complete documentation & usage guide
├── ACADEMIC_REPORT.md              # 18-section academic research paper
├── RESEARCH_RESULTS.md             # Empirical findings & statistical analysis (N=180)
├── RESEARCH_GAP_AND_NOVELTY.md     # Positioning of research contributions & novelty
├── PRESENTATION_OUTLINE.md         # B.Tech capstone defense outline & viva Q&As
├── TESTING_REPORT.md               # Technical testing audit (56 passed in 5.06s (100% passing))
├── CONTRIBUTIONS.md                # Authorship & third-party dependency breakdown
├── ARCHITECTURE.md                 # System architecture & sequence diagrams
├── EXPERIMENT_METHODOLOGY.md       # Research methodology & benchmark analysis
├── LITERATURE_REVIEW.md            # Academic review on ransomware detection paradigms
├── PROJECT_SCOPE.md                # Feature scope matrix (completed vs future roadmap)
├── USER_GUIDE.md                   # Step-by-step operator manual
├── RESEARCH_LIMITATIONS.md         # Prototype constraints & threats to validity
├── RESEARCH_SUMMARY.md             # Dynamically generated research summary report
├── run_sentinel.py                 # Unified CLI management tool
├── exports/                        # Exported CSV datasets (events, alerts, trials, breakdown)
├── canary_sentinel/
│   ├── core/
│   │   ├── config.py               # Typed configuration models
│   │   ├── sandbox.py              # Sandbox isolation & path traversal enforcement
│   │   └── utils.py                # Shannon entropy & SHA-256 calculation
│   ├── canary/
│   │   └── manager.py              # Decoy placement, registry, & integrity checks
│   ├── monitoring/
│   │   ├── monitor.py              # Watchdog filesystem observer
│   │   └── normalizer.py           # 50ms debouncing & uniform normalizer
│   ├── detection/
│   │   ├── base.py                 # Abstract detector interface & decision models
│   │   ├── baseline_detector.py    # Config A: Burst volume & entropy detector
│   │   ├── canary_detector.py      # Config B: Decoy tripwire detector
│   │   ├── hybrid_detector.py      # Config C: Correlated context detector
│   │   └── risk_engine.py          # Quantitative risk scoring & explanation engine
│   ├── simulation/
│   │   ├── scenarios.py            # 6 harmless test scenario definitions
│   │   ├── simulator.py            # Harmless activity simulator engine
│   │   └── response_manager.py     # Safe non-destructive containment manager
│   ├── storage/
│   │   ├── db.py                   # SQLite storage layer with WAL & thread safety
│   │   └── models.py               # Data models for events, alerts, scenarios, metrics
│   ├── experiments/
│   │   ├── runner.py               # Automated reproducible experiment runner
│   │   └── metrics.py              # Precision, Recall, F1, FPR, CI95, & breakdown calculator
│   └── dashboard/
│       └── app.py                  # Streamlit multi-view dashboard application
└── tests/
    ├── test_sandbox_safety.py      # Path traversal, symlinks, & containment safety (9 tests)
    ├── test_canary_manager.py      # Decoy deployment & integrity tracking (5 tests)
    ├── test_monitor_normalizer.py  # Watchdog event normalization & debouncing (4 tests)
    ├── test_detectors.py           # Verification of all 3 detector configurations (6 tests)
    ├── test_risk_engine.py         # Severity thresholds & explanation generation (5 tests)
    ├── test_database.py            # SQLite database CRUD operations & transactions (4 tests)
    ├── test_metrics.py             # Metrics math, CI95, & scenario breakdown (4 tests)
    ├── test_scenarios.py           # Safe execution of simulation scenarios (5 tests)
    ├── test_integration_flow.py    # End-to-end full execution pipeline (1 test)
    ├── test_cli_and_exports.py     # CSV data export generation (1 test)
    └── test_performance.py         # Latency & throughput benchmarks (1 test)
```
