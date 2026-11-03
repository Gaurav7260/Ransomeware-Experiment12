# CanarySentinel Research Limitations & Threat to Validity

## 1. Overview

While **CanarySentinel** provides empirical proof-of-concept evidence regarding the efficacy of combining canary decoys with contextual filesystem behavior, rigorous academic and industrial evaluation requires transparent documentation of its methodological boundaries, threat models, and architectural constraints.

---

## 2. Methodological & Technical Limitations

### 2.1 Synthetic Workload vs. Weaponized Ransomware
- **Safe Simulation Boundary**: To ensure complete safety on the host machine, CanarySentinel does **not** execute real ransomware binaries or real cryptographic routines (e.g., AES-256 or ChaCha20).
- **Entropy Emulation**: High entropy is simulated by writing blocks of pseudo-random bytes (`random.getrandbits(8)`). While statistically equivalent in Shannon entropy ($H \approx 7.8 - 7.9$ bits/byte), real ransomware often exhibits distinct file header structures, specialized extension appending, and ransom note drop sequences that may differ in operational cadence.
- **Evasion Techniques**: Weaponized ransomware frequently employs process hollowing, direct NT / XNU system calls, and driver-level unhooking to conceal activity from user-space monitors.

### 2.2 User-Space Monitoring vs. Kernel-Level Interception
- **Asynchronous Event Delivery**: CanarySentinel relies on `watchdog`, which leverages macOS `FSEvents` and `kqueue`. These APIs operate asynchronously in user space.
- **Pre-Write vs. Post-Write Containment**: 
  - In CanarySentinel, an alert is triggered *after* an initial event notification arrives from the kernel. Although detection latency is rapid ($\sim 20 - 25$ ms), several file write operations may execute before the simulator receives the containment signal.
  - In enterprise production EDR solutions, synchronous kernel-level hooks (e.g., Apple's `EndpointSecurity.framework` via `es_new_client` or Windows Minifilter drivers) intercept I/O requests *before* modifications are committed to the filesystem.

### 2.3 Decoy Evasion Strategies
- **Traversal Ordering**: CanarySentinel deploys canaries with prefixes such as `!00_`, `aaa_`, and `0_` to exploit the standard alphabetical traversal patterns observed in mass ransomware (e.g., LockBit, WannaCry).
- **Targeted & Evasive Attacks**: As demonstrated by scenario `rapid_bulk_without_canary`, adversaries that explicitly enumerate targets in reverse alphabetical order (`Z -> A`), randomize target order, or restrict operations to specific database extensions (e.g., `.mdf`, `.sqlite`) can bypass decoy tripwires completely.
- **Implication**: Decoy density and randomized decoy naming are necessary in production to increase the probability of early tripwire contact.

### 2.4 Observation Window Dynamics
- **Temporal Parameterization**: The Hybrid configuration enforces a 3.0-second observation window around canary touch events.
- **Low-and-Slow Attack Profiles**: Advanced persistent threats (APTs) or bespoke ransomware modifying a single user file every few minutes ("drip encryption") could evade a narrow observation window if the contextual burst rate never crosses the threshold. Persistent state across extended sessions would be required to mitigate this threat.

### 2.5 Sandbox Isolation vs. Full-Disk Complexity
- **Containment Scope**: CanarySentinel operates exclusively inside `./sandbox` to guarantee the safety of user documents and system directories.
- **Environmental Factors**: Real-world endpoints feature complex I/O environments: active background indexing (Spotlight), cloud storage synchronization (iCloud, OneDrive, Dropbox), compiler build artifacts, and package manager churn. While CanarySentinel models typical benign patterns (normal editing, bulk copying, bulk renaming, innocent indexer touches), real enterprise workloads present higher ambient background entropy.

---

## 3. Threats to Validity

### 3.1 Construct Validity
- *Are we measuring ransomware detection quality accurately?*
  - **Strengths**: Using standard, widely accepted information retrieval and security metrics: Precision, Recall, F1-Score, False Positive Rate (FPR), Detection Latency (ms), Damaged Files, and Prevented Operations.
  - **Mitigation**: All three configurations consume the exact same normalized event stream under identical operating conditions, ensuring unbiased relative comparison.

### 3.2 Internal Validity
- *Could confounding variables explain performance differences?*
  - **Mitigation**: Confounding factors were tightly controlled by resetting sandbox file trees, standardizing initial document sets, fixing decoy placements, and recording individual trial parameters with unique scenario IDs in SQLite.

### 3.3 External Validity
- *Can these findings be generalized to diverse operating systems and production environments?*
  - **Boundary**: Findings apply directly to filesystem-level endpoint behavioral detection on macOS POSIX environments. Porting to Windows requires adapting the filesystem observer to ReadDirectoryChangesW or USN Journaling, though the underlying contextual fusion logic remains platform-agnostic.

---

## 4. Recommendations for Future Research

1. **Synchronous Kernel Integration**: Port the detection engine to Apple's `EndpointSecurity.framework` to evaluate pre-write blocking and zero-damage containment.
2. **Adaptive Decoy Generation**: Implement dynamic decoy generation that mimics the user's active file types, naming conventions, and recent file access histories.
3. **Cross-Session Long-Term Memory**: Expand the observation window into a persistent graph-based event history to detect low-and-slow ransomware variants.

