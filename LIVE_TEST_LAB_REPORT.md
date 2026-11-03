# CanarySentinel — Live Test Lab & Local Telemetry Report

**Database Instance:** `canary_sentinel.db`  
**Total Recorded Trials:** 77  
**Total Logged Events:** 730  
**Total Alerts:** 25  

---

## 1. Live Test Lab Overview
The Live Test Lab module in the Streamlit dashboard (`views_lab.py`) allows interactive execution of the 6 synthetic workloads inside the isolated sandbox:

1. **Test 1 — Normal File Editing [BENIGN]:** Clean pass across all 3 detectors.
2. **Test 2 — Bulk File Copying [BENIGN]:** Verifies volume thresholds without false alarms.
3. **Test 3 — Innocent Canary Probing [BENIGN]:** Demonstrates Hybrid context suppression (0% FPR) vs Canary-Only false alarm.
4. **Test 4 — Bulk File Renaming [BENIGN]:** Demonstrates Baseline false alarm on mass renames vs Deception specificity.
5. **Test 5 — Canary Breach + Rapid Bulk [SUSPICIOUS]:** Demonstrates rapid Hybrid attack containment (26.1 ms, >90% ops prevented).
6. **Test 6 — Rapid Bulk Without Canary [SUSPICIOUS]:** Demonstrates defense-in-depth where Baseline catches evasive malware.

---

## 2. Rule-Based Detection Explanation Engine
Every generated alert is processed by `DetectionExplanationEngine` to provide:
- **Headline:** Severity and risk score summary.
- **What happened:** Telemetry summary of triggering action.
- **Why suspicious:** Behavioral and decoy rule matching rationale.
- **Observed Evidence:** Specific event timestamps, file paths, and entropy scores.
- **Analyst Recommendations:** Prescribed response protocols.
