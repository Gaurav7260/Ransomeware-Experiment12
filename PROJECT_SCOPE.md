# CanarySentinel Project Scope & Feature Matrix

## 1. Executive Summary

**CanarySentinel** is a local, lightweight, canary-based endpoint ransomware detection and behavioral analysis MVP developed for macOS (Apple Silicon M1 architecture). Its design is centered on investigating a core research question:

> *Does combining canary-file interactions with contextual filesystem behavior improve ransomware detection quality and reduce simulated file damage compared with canary-only and behavior-only detection?*

---

## 2. In-Scope: Completed Features (Current MVP)

The following components and capabilities have been fully implemented, integrated, and verified:

### 2.1 Core Safety & Isolation Layer
- **Dedicated Project Sandbox**: Enforced directory containment strictly within `./sandbox`.
- **Directory Traversal Protection**: Rejection of path traversal (`../`), null-byte injections (`\0`), and absolute path escapes via `pathlib.Path.resolve()` and `is_relative_to()`.
- **Symlink Jail Enforcement**: Verification that targets of symlinks remain inside the sandbox boundary.
- **System Root Immunity**: Explicit refusal to initialize on or monitor sensitive system roots (`/`, `/bin`, `/sbin`, `/etc`, `/System`, `/Library`, `/Users`, `~`).
- **Safe Reset Mechanisms**: Non-destructive filesystem reset and SQLite table truncation with user confirmation checks.

### 2.2 Canary Decoy Management
- **Deceptive Baits**: 8 high-value decoy templates (`!00_corporate_passwords.xlsx`, `aaa_employee_salaries.csv`, etc.) placed across root and subdirectories (`documents`, `finance`, `projects`, `backups`).
- **Alphabetical Priority**: Prefixes (`!00_`, `aaa_`, `0_`) designed to capture sequential alphabetical malware traversals.
- **Integrity Validation**: SHA-256 hash tracking and disk status classification (`ACTIVE`, `MODIFIED`, `DELETED`).
- **O(1) In-Memory Lookup**: Fast memory set for sub-millisecond canary identification during event normalization.

### 2.3 Monitoring & Normalization
- **Apple Silicon macOS Monitoring**: Watchdog observer optimized for macOS (FSEvents/kqueue).
- **Event Debouncer**: 50ms sliding window to coalesce rapid macOS OS buffer flushes without loss of genuine burst operations.
- **Shannon Entropy Engine**: Real-time calculation ($0.0 - 8.0$ bits/byte) on file write chunks to identify simulated encryption.
- **Normalized Event Stream**: Standardized `NormalizedEvent` records containing event type, path, extension, canary flag, size, entropy, process metadata, and scenario IDs.

### 2.4 Tri-Configuration Detection Engines
- **Configuration A: Baseline (Behavior-Only)**: Evaluates burst velocity ($\ge 6$ ops/2s), high entropy ($\ge 7.0$), and mass renaming without canary awareness.
- **Configuration B: Canary-Only (Decoy Tripwire)**: Triggers immediate alerts on any `MODIFY`, `DELETE`, or `MOVE` on protected canaries.
- **Configuration C: Hybrid (Correlated Context)**: Fuses a canary breach anchor with contextual companion damage within a 3.0-second observation window.

### 2.5 Transparent Risk & Severity Engine
- **Quantitative Risk Scoring**: 0–100 integer score with explicit weightings.
- **Severity Tiers**: `LOW` (0–34), `MEDIUM` (35–69), `HIGH` (70–89), `CRITICAL` (90–100).
- **Audit Explanations**: Human-readable rationale detailing triggering event, identified risk factors, supporting events, and containment recommendations.

### 2.6 Harmless Activity Simulator & Safe Response
- **6 Standardized Scenarios**:
  - Benign: `normal_file_editing`, `bulk_copying`, `bulk_renaming`, `canary_touch_benign`.
  - Suspicious: `canary_plus_rapid_bulk`, `rapid_bulk_without_canary`.
- **Non-Destructive Simulation**: Pseudo-random high-entropy bytes without real cryptography or payloads.
- **Token-Based Interception**: The response manager signals an internal cancellation token (`is_blocked = True`). The simulator aborts remaining planned operations without terminating any OS or user processes.

### 2.7 Persistence, Metrics & Reporting
- **SQLite Database**: Thread-safe storage with Write-Ahead Logging (`WAL` mode) and 5000ms busy timeout.
- **Metrics Calculator**: Confusion matrix (TP, FP, TN, FN), Precision, Recall, F1-Score, False Positive Rate (FPR), Latency (mean/min/max), Files Damaged, and Operations Prevented (%).
- **Exporting Capabilities**:
  - Export events, alerts, and trials to CSV.
  - Export performance metrics summary to CSV.
  - Dynamically generate structured Markdown research summaries (`CANARY_SENTINEL_RESEARCH_SUMMARY.md`).

### 2.8 Streamlit Dashboard & Unified CLI
- **Interactive Multi-View Dashboard**: Overview & Telemetry, Decoy & Sandbox Controls, Live Event Stream, Incidents & Evidence Alerts, Simulation & Experiments, Comparative Research Analysis.
- **Unified CLI (`run_sentinel.py`)**: Subcommands for `test`, `dashboard`, `benchmark`, `simulate`, `status`, `deploy-canaries`, `reset`, `report`, and `export`.

---

## 3. Out-of-Scope: Future Enterprise Extensions

The following items are deliberately excluded from this prototype to prioritize a lightweight, fully working, and secure local application:

| Feature | Reason for Exclusion | Planned Future Direction |
|---|---|---|
| **Real Ransomware Payloads** | Strict safety requirement; risk of host system compromise. | Keep prohibited in non-isolated environments; test in isolated hypervisors only. |
| **Kernel / System Extensions** | Requires Apple Developer Team IDs and kernel entitlements (`EndpointSecurity.framework`). | Enterprise agent extension via `es_new_client`. |
| **Arbitrary Process Killing** | Safety requirement; risk of terminating critical user workflows. | Safe process suspension or cgroup freezing via signed daemon. |
| **Heavyweight Machine Learning** | Violates 8 GB RAM and lightweight local constraint. | Lightweight on-device tree-based classifier (e.g. ONNX runtime). |
| **Cloud Telemetry / SIEM** | Strictly local development without external dependencies. | Optional Syslog / Splunk / Elastic exporter plugin. |
| **Network Share / SMB Interception** | Focused strictly on local filesystem endpoint behavior. | Samba / SMB honeypot file share extension. |

