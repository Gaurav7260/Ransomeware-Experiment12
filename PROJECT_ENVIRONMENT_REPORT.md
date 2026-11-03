# CanarySentinel — Project Environment & GitHub Deployment Guide

---

## 1. System Architecture
```
CanarySentinel/
├── canary_sentinel/
│   ├── canary/          # Decoy generation, tracking, integrity validation
│   ├── core/            # Configuration and sandbox security boundary
│   ├── dashboard/       # Streamlit 9-view SOC platform & Reports Centre
│   ├── detection/       # Baseline, Canary-Only, Hybrid, and Explanation Engine
│   ├── experiments/     # Benchmarking runner and statistical metrics calculator
│   ├── monitoring/      # Watchdog monitor, event normalizer, Shannon entropy
│   ├── reports/         # Automated audit package and report generator
│   ├── simulation/      # Synthetic benign and ransomware scenarios, response manager
│   └── storage/         # SQLite transactional database layer with batch provenance
├── tests/               # 56 automated unit, integration, boundary, and security tests
├── research_dossier/    # Academic paper, B.Tech report, statistical analyses, diagrams
└── config.json          # System configuration and detection thresholds
```

---

## 2. Installation and Execution
```bash
# 1. Setup Virtual Environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Run Automated Test Suite
pytest -v

# 3. Launch Interactive SOC Dashboard
streamlit run canary_sentinel/dashboard/app.py --server.port 8501

# 4. Run CLI Benchmark
python run_sentinel.py benchmark --iterations 10
```
