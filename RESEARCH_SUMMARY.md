# CanarySentinel Empirical Research Summary

## 1. Executive Summary
- **Total Scenarios Evaluated**: 180
- **Research Verdict**: YES (WITH DEFENSE-IN-DEPTH TRADE-OFFS): Combining canary-file interactions with contextual filesystem behavior optimizes detection quality by achieving perfect Precision (100.0%) and eliminating false alarms (0.0% FPR) with near-instant containment latency (26.1 ms). However, it is not universally superior: Baseline behavior detection achieves higher overall recall (100.0% vs. 50.0%) and F1-score (0.80 vs. 0.67) by catching attacks that evade canary traps, demonstrating that hybrid decoy detection must be deployed alongside behavioral volume tracking.

## 2. Key Empirical Findings
- Hybrid achieved perfect Precision (100.0%) vs Baseline (66.7%) and Canary-Only (50.0%) by eliminating false alarms.
- Hybrid achieved zero false alarms (FPR: 0.0%) compared to Canary-only (25.0%) and Baseline (25.0%) by contextualizing innocent decoy interactions.
- Containment Latency: Hybrid halted simulated attacks in 26.1 ± 8.4 ms, delivering near-instant response with only 1.8 ms correlation overhead compared to pure Canary-Only (24.3 ms on S5).
- Coverage Limitation & Defense-in-Depth: Hybrid and Canary-Only missed decoy-evading attacks (Scenario S6, Recall: 50.0%), whereas Baseline behavior tracking caught 100.0% of attacks, demonstrating that canary detection complements rather than replaces behavioral volume tracking.

## 3. Comparative Performance Matrix

| Metric | Configuration A: Baseline | Configuration B: Canary-Only | Configuration C: Hybrid |
|---|:---:|:---:|:---:|
| **Completed Trials** | 60 | 60 | 60 |
| **True Positives (TP)** | 20 | 10 | 10 |
| **False Positives (FP)** | 10 | 10 | 0 |
| **True Negatives (TN)** | 30 | 30 | 40 |
| **False Negatives (FN)** | 0 | 10 | 10 |
| **Precision** | 66.67% | 50.00% | 100.00% |
| **Recall** | 100.00% | 50.00% | 50.00% |
| **F1-Score** | 0.80 | 0.50 | 0.67 |
| **False Positive Rate (FPR)** | 25.00% | 25.00% | 0.00% |
| **Mean Latency (ms)** | 147.1 ± 102.1 ms | 18.9 ± 7.7 ms | 26.1 ± 8.4 ms |
| **Median Latency (ms)** | 142.0 ms | 16.2 ms | 25.8 ms |
| **95% Confidence Interval** | ± 36.5 ms | ± 3.4 ms | ± 5.2 ms |
| **Latency Range [Min, Max]** | [18.9, 276.5] ms | [5.5, 38.1] ms | [15.8, 46.9] ms |
| **Mean Damaged Files** | 3.0 ± 3.1 | 5.0 ± 5.1 | 5.0 ± 5.1 |
| **Subsequent Ops Prevented** | 65.3% | 45.4% | 45.4% |
| **Avg CPU Overhead** | 25.9% | 26.6% | 25.4% |
| **Avg Memory Footprint** | 37.2 MB | 37.4 MB | 37.7 MB |

## 4. Scenario-Level Empirical Breakdown

| Scenario | Category | Detector | Trials | Det. Rate | Mean Latency | Damaged Files | Prevented Ops % | Status |
|---|---|---|:---:|:---:|:---:|:---:|:---:|---|
| Normal File Editing | BENIGN | Baseline | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Normal File Editing | BENIGN | Canary Only | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Normal File Editing | BENIGN | Hybrid | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Bulk Copying | BENIGN | Baseline | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Bulk Copying | BENIGN | Canary Only | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Bulk Copying | BENIGN | Hybrid | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Bulk Renaming | BENIGN | Baseline | 10 | 100% | 271.3 ms | 0.0 | 33.3% | ⚠️ False Positive (10/10 flagged) |
| Bulk Renaming | BENIGN | Canary Only | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Bulk Renaming | BENIGN | Hybrid | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Canary Touch Without Suspicious Follow-up | BENIGN | Baseline | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Canary Touch Without Suspicious Follow-up | BENIGN | Canary Only | 10 | 100% | 13.5 ms | 0.0 | 75.0% | ⚠️ False Positive (10/10 flagged) |
| Canary Touch Without Suspicious Follow-up | BENIGN | Hybrid | 10 | 0% | - | 0.0 | 0.0% | ✅ True Negative (Pass) |
| Canary Touch + Rapid Bulk Modifications | SUSPICIOUS | Baseline | 10 | 100% | 25.8 ms | 0.0 | 91.7% | ✅ Detected (10/10) |
| Canary Touch + Rapid Bulk Modifications | SUSPICIOUS | Canary Only | 10 | 100% | 24.3 ms | 0.1 | 90.8% | ✅ Detected (10/10) |
| Canary Touch + Rapid Bulk Modifications | SUSPICIOUS | Hybrid | 10 | 100% | 26.1 ms | 0.1 | 90.8% | ✅ Detected (10/10) |
| Rapid Bulk Modifications Without Canary | SUSPICIOUS | Baseline | 10 | 100% | 144.0 ms | 6.1 | 39.0% | ✅ Detected (10/10) |
| Rapid Bulk Modifications Without Canary | SUSPICIOUS | Canary Only | 10 | 0% | - | 10.0 | 0.0% | ❌ Missed Attack (0 detected) |
| Rapid Bulk Modifications Without Canary | SUSPICIOUS | Hybrid | 10 | 0% | - | 10.0 | 0.0% | ❌ Missed Attack (0 detected) |

## 5. Methodological Interpretation
- **Baseline (Behavior-Only)** catches attacks without canary interaction, but incurs higher containment latency and false positives on legitimate batch file operations.
- **Canary-Only (Decoy Tripwire)** achieves the lowest containment latency on canaries, but generates false alarms when benign utilities inspect decoy files and misses evasive attacks.
- **Hybrid (Correlated Context)** demonstrates zero false positive rate on benign canary touches while preserving fast reaction times when canary breaches correlate with companion file modifications.

*(Report generated dynamically from recorded SQLite telemetry by CanarySentinel)*