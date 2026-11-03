# CanarySentinel — Experiment Provenance & Discrepancy Reconciliation

**Audit Objective:** Conclusively reconcile the relationship between the 180-trial academic CSV export and the 77-trial SQLite database using cautious, evidence-grounded findings reconstructed and supported by available artifacts.

---

## 1. Forensic Reconstruction and Provenance Determination
Based on available disk artifacts, export logs, and database records, the provenance timeline is **reconstructed and supported by available artifacts**:

1. **Academic Benchmark Dataset ($N=180$):**
   - Executed via `run_sentinel.py benchmark --iterations 10` on 2026-11-02 from `12:58:28` to `13:01:08`.
   - Generated 180 trials, 1,691 events, and 60 alerts across 10 balanced repetitions of all 6 scenarios and 3 detectors.
   - Exported at `13:01:23` to `exports/trials.csv` and archived in `research_dossier/03_EXPERIMENTAL_DATA/RAW_EXPERIMENT_DATA.csv` (SHA-256: `ada005249b4a6eae1efbcdb3db204a121fb954a47e52d3f55c76ae5548902241`).
2. **Distinct Database Snapshots Identified:**
   - **Historical Extracted Snapshot (`backup_state_extracted/canary_sentinel.db`):** An earlier pre-migration database snapshot (SHA-256: `3ea5949b2a40edae3fd72ae51852e0160face4e10edcbf90046586383ef9cb22`) containing 76 scenario records, 725 events, and 25 alerts, with an unmigrated schema lacking the `batch_id` column.
   - **Preserved Operational Telemetry Database (`canary_sentinel.db` / `canary_sentinel_evidence_backup.db`):** The verified 77-trial operational database (SHA-256: `66f67d7009cfabf4ce308d7372fec963d85c68dd732730233d7f4620bcf640fa`) containing 77 scenarios (76 historical + 1 `batch_verification_test` trial), 730 events, 25 alerts, and the migrated schema with the `batch_id` column.
   - These two database snapshots are distinct and must not be conflated.
3. **Audit Archive Inventory:**
   - The audit package contains 11 curated evidence and experiment CSV files (benchmark trials, metrics breakdown, confusion matrices, and export dumps), along with the preserved database and cryptographic manifests. Claims of '49 CSV files' originated from uncurated development archives containing virtual-environment library test files and do not describe the curated release package.

---

## 2. ID Reconciliation Matrix

| Dataset | Total Trials | Trial ID Namespace | Timestamp Range | Purpose |
|---|:---:|---|---|---|
| **Archived Benchmark (CSV)** | 180 | `baseline_bulk_copying_f06fc6`, etc. | 2026-11-02 12:58:28 – 13:01:08 | Academic paper, statistical tests, thesis evaluation |
| **Operational Database (SQLite)** | 77 | `hybrid_normal_file_editing_a1f7e1`, etc. | 2026-11-02 16:13:24 – 16:41:26 | Live Streamlit dashboard, telemetry log, interactive test lab |

---

## 3. Discrepancy Resolution
- **Zero ID Overlap:** Zero overlap occurs between the two datasets because the database was reset between the benchmark execution and subsequent development runs, generating fresh unique UUID-suffixed trial IDs.
- **Reporting Clarity:** In all research papers and audit packages, the 180-trial dataset is clearly identified as the **Frozen Academic Benchmark Dataset**, while the 77-trial database is identified as the **Current Operational Telemetry Database**.
