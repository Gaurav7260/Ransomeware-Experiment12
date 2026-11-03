# CanarySentinel — Final Independent Technical Audit Report
**Document ID:** CS-AUDIT-FINAL-2026-REC-01  
**Lead Auditor:** Independent Technical Review Team  
**Scope:** Architecture, Detection Algorithms, Empirical Results, Provenance, Testing & Dashboard  
**Status:** FULLY RECONCILED & COMPLIANT  
**Date:** November 2, 2026  

---

## 1. Executive Summary

CanarySentinel is an endpoint security research platform designed to evaluate **deception-augmented behavioral detection** against simulated ransomware workloads. The platform compares three architectural configurations:
- **Configuration A (Baseline Behavioral):** Monitors file modification velocity, entropy, and mass renames.
- **Configuration B (Canary-Only Decoy):** Uses passive decoy files as tripwires.
- **Configuration C (Hybrid Corroborated):** Corroborates decoy interactions with contextual filesystem burst activity.

This Final Independent Technical Audit confirms that all previously identified inconsistencies, reporting ambiguities, and runtime issues have been completely investigated, resolved, and verified.

---

## 2. Reconciled Project Status Matrix

| Project Dimension | Prior Audit Status | Final Reconciled Status | Evidence / Verification |
|:---|:---:|:---:|:---|
| **Automated Test Suite** | 45 / 53 conflicting | **56 / 56 Passed (100%)** | `pytest -v` passing in 5.06s; full console log recorded |
| **Attack Latency Analysis** | Pooled with FPs ($n=30$) | **Decoupled True Attack Latency** | Baseline: $84.92$ ms ($n=20$); Hybrid: $26.10$ ms ($n=10$) |
| **Scenario S5 Comparison** | Not matched | **Matched Head-to-Head ($n=10$)** | Hybrid vs Baseline: $p = 0.9168$; Hybrid vs Canary: $p = 0.5976$ |
| **False Positive Latencies** | Mixed into attack speed | **Reported Separately** | Baseline B4: $271.30$ ms; Canary B3: $13.48$ ms; Hybrid: 0 FPs |
| **Database Provenance** | 180 CSV vs 77 DB conflict | **Two-Epoch Reconstruction** | Benchmark (Epoch 1) exported before DB reset in dev (Epoch 2); reconstructed and supported by available artifacts |
| **Evidence Preservation** | Unsaved working copy | **Byte-for-Byte Preserved** | `preserved_evidence/` holds backup DB & curated release CSVs with SHA-256 |
| **SHA-256 Manifest** | Ambiguous authenticity claim | **Integrity vs Authenticity Separated** | Clarified hash immutability vs execution provenance; findings reconstructed and supported by artifacts |
| **Dashboard Reliability** | AttributeError on overview/lab | **Completely Fixed & Safeguarded** | `getattr()` defensive properties & fresh singleton reload |
| **Downloadable Deliverables** | Fragmented | **Unified Reports Centre** | All 6 formal deliverables downloadable directly in UI |

---

## 3. Empirical Research Findings Summary

### 3.1 Detection Accuracy & Specificity
- **Configuration A (Baseline):** Sensitivity = 100.0% ($20/20$), Specificity = 75.0% ($30/40$), FPR = 25.0% ($10/40$), Precision = 66.7% ($20/30$), F1 = 0.800.
- **Configuration B (Canary-Only):** Sensitivity = 50.0% ($10/20$), Specificity = 75.0% ($30/40$), FPR = 25.0% ($10/40$), Precision = 50.0% ($10/20$), F1 = 0.500.
- **Configuration C (Hybrid):** Sensitivity = 50.0% ($10/20$), Specificity = **100.0% ($40/40$)**, FPR = **0.0% ($0/40$)**, Precision = **100.0% ($10/10$)**, F1 = 0.667.
- **Statistical Significance:** Hybrid's elimination of false positives is statistically significant ($p = 0.00102966$, Fisher's Exact test).

### 3.2 Detection Latency & Overheads
- On attacks touching decoys (S5), Hybrid achieves an average detection latency of **$26.10 \pm 8.43$ ms**, which shows no statistically significant latency difference compared to pure Canary-Only tripwires ($24.28 \pm 6.59$ ms, $p = 0.5976$) or pure Baseline ($25.80 \pm 3.47$ ms, $p = 0.9168$). Equivalence was not established, as formal equivalence testing within predefined margins was not evaluated and confidence intervals allow for minor differences in either direction.
- Overall attack latency comparisons ($84.92$ ms vs $26.10$ ms) reflect scenario composition asymmetry: Baseline detected evasive S6 attacks (averaging $144.05$ ms), whereas Hybrid missed S6 entirely. When matched on identical Scenario S5 attacks, no statistically significant latency difference was detected.

### 3.3 Damage Reduction
- On decoy-traversing attacks (S5), both Canary-Only and Hybrid contain the attack after only $0.10$ files damaged out of 11 targeted operations (**99.09%** user data damage prevention: $\frac{11.0 - 0.10}{11.0} = 99.09\% \approx 99.1\%$).
- Across all 20 suspicious attack trials, the unweighted scenario-level prevention mean is **49.55%** ($\frac{99.09\% + 0.0\%}{2}$, matching the pooled operations prevented ratio $109/220$), while the per-trial operations prevented ratio is **45.42%** (derived from the mean ratio across 20 trials: $9.08333 / 20$).
- On targeted/evasive attacks (S6), Baseline contained the attack after $6.10$ files damaged (preventing 3.90 operations). Because S6 evades decoys, Canary-Only and Hybrid did not trigger.

---

## 4. Completed Feature & Implementation Verification

- [x] **Filesystem Monitor:** Watchdog observer with recursive monitoring, directory filtering, and synthetic event debouncing.
- [x] **Event Normalizer:** Canonical path resolution, sandboxed containment, relative path calculation, and decoy tagging.
- [x] **Canary Decoy Manager:** Dynamic deployment across sandbox subtrees, integrity hash verification, and property/getter API compatibility.
- [x] **Baseline Detector:** Sliding-window burst velocity monitoring, mass rename heuristic, and decoy-blind threshold evaluation.
- [x] **Canary Detector:** Immediate tripwire alerting on any decoy file modification or rename.
- [x] **Hybrid Detector:** Corroborated two-stage detection requiring canary interaction plus contextual filesystem velocity ($N \ge 2$ events).
- [x] **Simulation Engine:** 6 synthetic workloads (B1-B4, S5, S6) executed strictly inside the sandbox boundary.
- [x] **Response Manager:** Non-destructive containment simulating process isolation without terminating real OS processes.
- [x] **Streamlit SOC Dashboard:** 10 interactive views including Beginner/Technical toggle, Live Test Lab, Event Monitor, Alert Center, and Reports Centre.
- [x] **Independent Audit Package:** Complete archive with 12 structured directories, raw benchmark CSVs, SQLite backup, and verified SHA-256 manifest.

---

## 5. Documented Research Limitations

1. **User-Space Filesystem Monitoring Overhead:** Watchdog operates via user-space event hooks (FSEvents on macOS, inotify on Linux). In high-throughput enterprise environments, kernel-level drivers (e.g., eBPF or Windows Minifilter drivers) would be required to prevent event drops.
2. **Evasion by Decoy-Aware Ransomware:** As demonstrated by Scenario S6, adversaries who specifically enumerate and avoid canary decoy filenames can bypass pure decoy and hybrid systems. Hybrid deception must be deployed as an accelerant within a layered defense-in-depth architecture that retains fallback behavioral heuristics.
3. **Synthetic Workload Scope:** Workloads simulate file encryption patterns (rapid write, rename, entropy change) but do not execute live malware binaries or attempt kernel privilege escalation.
