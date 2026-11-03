# CanarySentinel — Detector Evaluation & Architectural Comparison

---

## 1. In-Depth Detector Comparison

### Configuration A: Baseline Behavioral Detector
- **Mechanism:** Monitors overall filesystem activity volume, velocity, mass renames, and Shannon entropy without relying on decoy canaries.
- **Thresholds:** Burst count \ge 6 ops in 2.0s; Mass renames \ge 4 renames in 2.0s; Entropy \ge 7.0.
- **Strengths:** 100.0% Recall — intercepts all simulated attacks, including sophisticated variants that avoid canary files.
- **Weaknesses:** 25.0% False Positive Rate — administrative batch renames (Scenario B4) exceed thresholds and trigger false alarms.

### Configuration B: Canary-Only Decoy Detector
- **Mechanism:** Zero-tolerance tripwire placed on 8 multi-extension decoy files.
- **Thresholds:** Any `CREATE`, `MODIFY`, `DELETE`, or `MOVE` event targeting a canary path.
- **Strengths:** Rapid containment latency (24.28 ms on attacks).
- **Weaknesses:** 25.0% False Positive Rate on benign desktop search indexers (Scenario B3); 50.0% Recall (misses attacks that do not touch decoys).

### Configuration C: Hybrid Corroborated Detector
- **Mechanism:** Dual-condition predicate requiring decoy breach + companion user file churn (\ge 2 events within 3.0s window).
- **Strengths:** Perfect Precision (100.0%) and zero false alarms (0.0% FPR) with near-instant containment latency (26.10 ms).
- **Trade-off:** Requires decoy interaction; missed Scenario S6 (50.0% Recall), proving that Hybrid must operate as a tier alongside Baseline behavioral monitoring.
