# CanarySentinel — Experimental Results Report ($N=180$)

**Dataset:** Frozen Academic Benchmark Dataset (`RAW_EXPERIMENT_DATA.csv` / `BENCHMARK_TRIALS_180.csv`)  
**Design:** 10 repetitions $\\times$ 6 scenarios $\\times$ 3 detector configurations = 180 independent trials  

---

## 1. Detector Performance Summary

| Metric | Configuration A: Baseline Behavioral | Configuration B: Canary-Only Decoy | Configuration C: Hybrid Corroborated |
|---|:---:|:---:|:---:|
| **Completed Trials ($N$)** | 60 | 60 | 60 |
| **True Positives (TP)** | 20 | 10 | 10 |
| **False Positives (FP)** | 10 | 10 | **0 (observed in tested trials)** |
| **True Negatives (TN)** | 30 | 30 | **40** |
| **False Negatives (FN)** | **0** | 10 | 10 |
| **Precision** | 66.67% (20/30) | 50.00% (10/20) | **100.00%** (10/10) |
| **Recall (Sensitivity)** | **100.00%** (20/20) | 50.00% (10/20) | 50.00% (10/20) |
| **F1-Score** | **0.8000** | 0.5000 | 0.6667 |
| **False Positive Rate (FPR)** | 25.00% (10/40) | 25.00% (10/40) | **0.00%** (0/40) |
| **Matched S5 Attack Latency (ms)** | 25.80 ms ($\pm 3.47$) | **24.28 ms** ($\pm 6.59$) | 26.10 ms ($\pm 8.43$) |
| **Overall TP Attack Latency (ms)** | 84.92 ms ($\pm 60.86$) | 24.28 ms ($\pm 6.59$) | 26.10 ms ($\pm 8.43$) |
| **Benign FP Latency (ms)** | 271.30 ms (B4 build) | 13.48 ms (B3 probe) | N/A (0 observed FPs) |
| **Avg Files Damaged (All 60)** | **3.05** | 5.05 | 5.05 |
| **Avg Files Damaged (S5 Attack)** | **0.00** | 0.10 | 0.10 |
| **Avg Files Damaged (S6 Attack)** | **6.10** | 10.00 | 10.00 |
| **Ops Prevented (%)** | **65.33%** | 45.42% | 45.42% (99.1% in S5) |

---

## 2. Key Scenario Breakdown
- **Scenario B4 (Bulk Renaming):** Baseline triggered 10/10 false positives due to rapid rename sequence exceeding the mass rename boundary (\\ge 4 renames in 2.0s). Canary and Hybrid recorded 0 false positives.
- **Scenario B3 (Innocent Canary Inspection):** Canary-Only triggered 10/10 false alarms upon decoy touch. Hybrid correctly evaluated companion context and suppressed 10/10 false alarms (0% FPR).
- **Scenario S5 (Canary-Trapped Ransomware):** Hybrid contained simulated attacks in 26.10 ms, limiting damage to 0.10 files out of 11 targeted operations (approximately 99.1% prevented).
- **Scenario S6 (Canary-Evasive Ransomware):** Decoys were untouched; Canary-Only and Hybrid missed detection (0% recall on S6). Baseline caught 10/10 attacks, proving the necessity of behavioral volume heuristics.
