# CanarySentinel — Database Integrity & Schema Report

**Database File:** `canary_sentinel.db`  
**Integrity Check Status:** `ok` (Zero corruption detected)  
**Verification Timestamp:** 2026-11-03 18:13:52  

---

## 1. Table Record Counts

| Table Name | Actual Row Count | Primary Key | Description |
|---|:---:|---|---|
| `scenarios` | **77** | `scenario_id` | Scenario trial execution records and containment metrics |
| `events` | **730** | `event_id` | Individual normalized filesystem operations |
| `alerts` | **25** | `alert_id` | Evidence-backed detection incidents and containment actions |
| `canaries` | **8** | `canary_id` | Deployed canary decoy tracking and integrity hashes |
| `system_metrics` | **77** | `metric_id` | Sampled CPU percentage and RAM footprint per scenario trial |

---

## 2. Integrity and Uniqueness Checks
- **Primary Key Duplicates:** 0 across all tables (`scenario_id`, `event_id`, `alert_id`, `canary_id`, `metric_id`).
- **Orphan Check:** All 25 alerts correlate to valid scenario IDs.
- **Batch IDs Present in Database:** `[None, 'batch_verification_test']`
- **Database File SHA-256 Hash:** `66f67d7009cfabf4ce308d7372fec963d85c68dd732730233d7f4620bcf640fa`
