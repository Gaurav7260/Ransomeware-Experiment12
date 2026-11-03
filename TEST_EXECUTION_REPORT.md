# CanarySentinel — Automated Test Suite Execution Report

**Execution Timestamp:** 2026-11-03 18:13:52  
**Platform:** macOS (darwin) — Python 3.14.0  
**Test Framework:** Pytest 9.2.0  
**Total Collected Tests:** 56  
**Passed:** 56 | **Failed:** 0 | **Skipped:** 0 | **Errors:** 0  

---

## 1. Test Suite Coverage Summary

| Test Module | Test Count | Focus Area | Result |
|---|:---:|---|:---:|
| `tests/test_sandbox_safety.py` | 10 | Path traversal (`../`), null-byte injection, symlink isolation, sandbox reset, `sandbox_dir` property. | 100% PASS |
| `tests/test_detectors.py` | 6 | Baseline burst/rename evaluation, Canary-only tripwire response, Hybrid context corroboration. | 100% PASS |
| `tests/test_canary_manager.py` | 6 | Decoy deployment, integrity verification (`ACTIVE`, `MODIFIED`, `DELETED`), `get_canary_paths()`. | 100% PASS |
| `tests/test_database.py` | 4 | Transactional persistence, querying, batch provenance tags, table reset. | 100% PASS |
| `tests/test_metrics.py` | 4 | Metric formulation, zero-division safety, scenario breakdown, markdown generation. | 100% PASS |
| `tests/test_scenarios.py` | 5 | Benign editing, bulk copying, bulk renaming, benign decoy probing, ransomware trial. | 100% PASS |
| `tests/test_risk_engine.py` | 6 | Severity ranking, evidence creation, threshold blocking, OS process safety verification. | 100% PASS |
| `tests/test_monitor_normalizer.py` | 4 | Watchdog event normalization, debouncing, canary categorization. | 100% PASS |
| `tests/test_performance.py` | 1 | Event normalization latency, detector processing throughput (< 1.0 ms/event). | 100% PASS |
| `tests/test_cli_and_exports.py` | 1 | CLI commands and CSV export validation. | 100% PASS |
| `tests/test_integration_flow.py` | 1 | End-to-end event generation $\rightarrow$ detection $\rightarrow$ alert $\rightarrow$ simulated response. | 100% PASS |
| `tests/test_threshold_boundaries.py` | 3 | Boundary tests for Hybrid companion events ($n=2$), Baseline renames ($n=4$), event types. | 100% PASS |
| `tests/test_batch_provenance_and_lab.py` | 3 | Batch ID isolation, explanation engine formatting, cooperative containment safety. | 100% PASS |
