# CanarySentinel — Final Project Change Log
**Document ID:** CS-CHANGELOG-2026-FINAL-01  
**Project:** CanarySentinel — Deception-Augmented Endpoint Security Platform  
**Target:** Final Audit Package & Academic Dossier Reconciliation  
**Date:** November 2, 2026  

---

## Summary of Changes

This change log documents all modifications, statistical corrections, test suite reconciliations, digital forensic investigations, and user interface enhancements implemented in CanarySentinel.

---

### 1. Statistical Methodology Corrections
- **Decoupled True Attack Latency from False Positive Latency:**
  - Removed 10 benign false positive trials (B4 compiler builds at $pprox 271$ ms) from Baseline's attack detection latency calculation.
  - Re-evaluated Baseline true-positive attack latency strictly on S5 and S6 ($n=20$), establishing the true empirical mean of $84.92 \pm 60.86$ ms (Median: $84.92$ ms, 95% CI: $[58.25, 111.59]$ ms).
  - Maintained Canary-Only attack latency strictly on S5 ($n=10$, mean: $24.28 \pm 6.59$ ms) and Hybrid on S5 ($n=10$, mean: $26.10 \pm 8.43$ ms).
- **Matched Scenario S5 Head-to-Head Comparison:**
  - Performed scenario-matched independent comparative tests (Welch's $t$-test and Mann-Whitney $U$ test) across all three detectors on Scenario S5 (`Canary Touch + Rapid Bulk Modifications`).
  - Demonstrated that no statistically significant S5 latency difference was detected ($p = 0.9168$ vs Baseline, $p = 0.5976$ vs Canary-Only; Cohen's $d = 0.048$ and $0.241$). Explicitly documented that equivalence was not established.
  - Recalculated S5 median and IQR values under the explicitly stated standard linear interpolation quantile convention (Type 7 / NumPy default) and nearest-rank convention:
    - Baseline: Median = $27.17$ ms, Type 7 linear IQR = **$2.74$ ms** ($Q_1=24.98, Q_3=27.72$); nearest-rank IQR = **$3.20$ ms**
    - Canary-Only: Median = $25.68$ ms, Type 7 linear IQR = **$6.27$ ms** ($Q_1=20.30, Q_3=26.56$); nearest-rank IQR = **$6.80$ ms**
    - Hybrid: Median = $25.78$ ms, Type 7 linear IQR = **$2.93$ ms** ($Q_1=23.55, Q_3=26.49$); nearest-rank IQR = **$3.75$ ms**
- **Clarified Damage Prevention Metrics:**
  - Retained damage prevention on Scenario S5 at **99.09% ($\approx 99.1\%$) user data damage prevented** ($0.10$ files damaged out of 11 targeted user operations: $\frac{11.0 - 0.10}{11.0} = 99.09\%$).
  - Defined **49.55%** as the unweighted average of scenario-level percentages across attack scenarios ($\frac{99.09\% + 0.00\%}{2} = 49.55\%$, matching the pooled operations prevented ratio $\frac{109}{220} = 49.55\%$).
  - Documented the exact derivation for the **45.42%** operations-based figure as the arithmetic mean of per-trial planned operations ratios across all 20 suspicious attack trials: $\frac{10 \times (10.9/12.0) + 10 \times (0.0/10.0)}{20} = \frac{9.08333}{20} = 45.42\%$ (Numerator: $9.08333$, Denominator: $20$).
- **Overall True Positive Latency Analysis & Scenario Composition:**
  - Evaluated overall attack detection latency, explicitly documenting that Baseline's higher mean ($84.92$ ms across S5 and S6) and Hybrid's lower mean ($26.10$ ms across S5 only) represent differing attack populations and are descriptive detector-specific metrics rather than an apples-to-apples comparison. Hybrid completely missed S6 ($0\%$ recall); the matched S5 comparison ($25.80$ ms vs $26.10$ ms, $p = 0.9168$) remains the sole valid head-to-head comparison.
- **Dedicated Benign False Positive Section:**
  - Created an independent section reporting Baseline B4 false alarms ($271.30 \pm 4.48$ ms) and Canary-Only B3 false alarms ($13.48 \pm 4.17$ ms).
  - Documented Fisher's Exact test proving Hybrid's 0% false positive rate is statistically significant ($p = 0.00102966$).

---

### 2. Test Suite Harmonization & Reconciliation
- **Standardized Test Suite to 56 Passed Tests:**
  - Resolved documentation conflicts between 45, 53, and 56 tests.
  - Documented the exact chronology: 45 original unit tests $ightarrow$ 53 tests after batch provenance and explanation engine additions $ightarrow$ 56 tests after boundary and property tests (`test_canary_paths_methods`, `test_sandbox_dir_property`, `test_canary_only_monitored_event_types`).
  - Executed `pytest -v` resulting in **56 passed in 5.06s**.
  - Synchronized `TESTING_REPORT.md`, `TEST_EXECUTION_REPORT.md`, `PYTEST_CONSOLE_LOG.txt`, `FINAL_AUDIT_REPORT.md`, and dashboard telemetry to 56 tests.

---

### 3. Digital Forensic Provenance Investigation
- **Evidence Preservation:**
  - Backed up `canary_sentinel.db` to `preserved_evidence/canary_sentinel_evidence_backup.db` (SHA-256: `66f67d7009cfabf4ce308d7372fec963d85c68dd732730233d7f4620bcf640fa`).
  - Differentiated historical extracted snapshot (`backup_state_extracted/canary_sentinel.db`, 76 records, unmigrated schema) from preserved 77-record operational database.
  - Curated release evidence package with 11 core benchmark CSVs and cryptographic SHA-256 manifests.
- **Two-Epoch Provenance Resolution:**
  - Reconstructed the forensic execution timeline proving that Epoch 1 (180 benchmark trials) ran from 12:58:28 to 13:01:08 UTC and exported to CSV at 13:01:23 UTC.
  - Explained that Epoch 2 (77 local database trials) resulted from database resets during integration testing and interactive Live Test Lab development.
- **Explanation of `evidence_source="SQLite"`:**
  - Verified that this column records the database from which the CSV was originally exported at 13:01:23 UTC prior to the reset.
- **Cryptographic Scope Clarification:**
  - Explicitly differentiated SHA-256 hash immutability (tamper-evidence relative to recorded hashes) from physical experimental authenticity (reproducibility and execution traces).

---

### 4. Dashboard Enhancements & Bug Fixes
- **Resolved AttributeError on Overview & Live Lab Views:**
  - In `canary_sentinel/canary/manager.py`, added both `canary_paths` property and `get_canary_paths()` method for 100% backward/forward API compatibility.
  - In `canary_sentinel/core/sandbox.py`, added `sandbox_dir` property and ensured `sandbox_path` is always exposed.
  - In `canary_sentinel/dashboard/views_overview.py` and `views_lab.py`, wrapped property accesses in defensive `getattr()` fallbacks.
  - Cleared Streamlit singleton caching to eliminate stale instance retention across code reloads.
- **Added Reports & Downloads View (Section 10):**
  - Implemented centralized compliance and audit deliverables portal (`views_reports.py`).
  - Added one-click download buttons for all 6 individual deliverables.
  - Added primary download button for the complete `CanarySentinel_Final_Audit_Package.zip`.
  - Added dynamic regeneration button that re-runs the report compiler directly from SQLite.

---

### 5. Packaging & Deliverable Artifacts
- **Compiled `CanarySentinel_Final_Audit_Package.zip`:**
  - Bundled all 6 formal deliverables, 12 structured audit directories, raw evidence backups, and `SHA256_MANIFEST.txt`.
  - Retained historical `CanarySentinel_Audit_Package.zip` for full provenance tracking.
