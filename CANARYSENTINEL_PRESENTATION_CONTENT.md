# CanarySentinel — Master 25-Slide Academic Defence Presentation

**Project Title**: CanarySentinel: Deception-Based Ransomware Detection, Behavioral Analysis and Risk-Aware Response System  
**Research Title**: Evaluating Canary-Triggered Behavioral Corroboration for Early Ransomware Detection and Damage Reduction  
**Audience**: Final-Year Examination Board, Faculty Evaluators, and Industry Reviewers  
**Document**: `research_dossier/12_FINAL_DOCUMENTS/CANARYSENTINEL_PRESENTATION_CONTENT.md`  

---

### Slide 1: Title & Candidacy
- **Title**: CanarySentinel — Deception-Based Ransomware Detection & Risk-Aware Response
- **Subtitle**: Evaluating Canary-Triggered Behavioral Corroboration for Early Ransomware Detection and Damage Reduction
- **Presenters**: [Candidate 1], [Candidate 2], [Candidate 3]
- **Project Supervisor**: [Supervisor Name], Dept. of Computer Science & Engineering
- **Institution**: [Institution / University Name], Academic Year 2025–2026
- **Visual**: Project shield emblem and institutional herald.
- **Speaker Notes**: "Respected members of the examination board, faculty guide, and colleagues, welcome to our final capstone defense. Today, we present CanarySentinel, an empirical investigation into whether canary-triggered behavioral corroboration solves the false-alarm dilemma of deception security and protects user files."

---

### Slide 2: Introduction
- **Key Points**:
  - Endpoint security operates under an asymmetric disadvantage against automated malware.
  - Ransomware represents an immediate, irreversible threat to local documents.
  - Pre-encryption and early-encryption phases are the only temporal windows where containment prevents permanent data destruction.
- **Speaker Notes**: "Unlike espionage malware that operates silently, ransomware is loud, aggressive, and irreversible. Once AES encryption finishes, files are gone. Therefore, defense must prioritize rapid early-stage detection."

---

### Slide 3: The Ransomware Problem
- **Key Points**:
  - Ransomware-as-a-Service (RaaS) has automated intrusion and mass encryption.
  - Multi-threaded traversal routines destroy thousands of files per minute.
  - Paying ransoms provides no guarantee of data recovery and funds cybercrime.
- **Visual**: Attack lifecycle: Phishing $\rightarrow$ Discovery $\rightarrow$ Mass Encryption $\rightarrow$ Extortion.
- **Speaker Notes**: "Modern ransomware operators use multi-threaded pipelines. On high-speed NVMe drives, an endpoint can lose gigabytes of data in under 30 seconds."

---

### Slide 4: Motivation: The Speed vs. Precision Dilemma
- **Key Points**:
  - **The Speed Dilemma**: Encryption is sequential; every millisecond of detection delay destroys additional user files.
  - **The Precision Dilemma**: Automated containment (killing processes) cannot tolerate false alarms. Disrupting developer builds or backups causes business downtime.
- **Speaker Notes**: "This creates the central engineering dilemma: How do we achieve ultra-fast detection without generating false alarms that disrupt legitimate users?"

---

### Slide 5: Problem Statement
- **Key Points**:
  - Signature AV is ineffective against polymorphic zero-day binaries and living-off-the-land scripts.
  - Behavioral anomaly detectors mistake routine batch developer operations for ransomware.
  - Deception tripwires alert instantly but suffer false alarms on accidental clicks and fail on decoy evasion.
- **Speaker Notes**: "Existing defenses force a compromise between alert fatigue and complete blindness."

---

### Slide 6: Research Gap
- **Key Points**:
  - Most deception research evaluates only naive alphabetical directory traversal.
  - Heavyweight hybrid systems rely on deprecated kernel drivers (minifilters, KEXTs).
  - Lack of controlled empirical benchmarks evaluating user-space sliding-window correlation on modern Unix/macOS platforms under deliberate honeypot evasion.
- **Speaker Notes**: "CanarySentinel fills this research gap with an empirical benchmark on Apple Silicon M1."

---

### Slide 7: Research Objectives
- **Key Objectives**:
  1. Build a modular, local macOS prototype in user space.
  2. Implement Baseline, Canary-Only, and Hybrid detection paradigms consuming identical event streams.
  3. Safely simulate benign workloads and ransomware encryption inside an isolated sandbox.
  4. Perform 180 controlled empirical trials and conduct rigorous statistical auditing.
- **Speaker Notes**: "Our primary objective is to scientifically evaluate trade-offs under identical conditions."

---

### Slide 8: Primary Research Question
- **Central Question**:
  *Does combining canary-file interactions with contextual filesystem behavior improve ransomware detection quality and reduce simulated file damage compared with canary-only and behavior-only detection?*
- **Speaker Notes**: "This question directly guides our architecture, scenarios, and hypothesis testing."

---

### Slide 9: Formal Hypotheses
- **$H_1$ (False-Positive Suppression)**: Corroboration eliminates false alarms from innocent canary reads ($\text{FPR} = 0.0\%$).
- **$H_2$ (Damage Reduction)**: Canary assistance detects attacks significantly faster, cutting file damage by $>70\%$.
- **$H_3$ (Universal Superiority)**: Hybrid detection universally outperforms baseline and canary-only models across all metrics.
- **Speaker Notes**: "We formulated these three hypotheses before conducting our empirical runs."

---

### Slide 10: Related Work & Prior Literature
- **Foundational Systems**:
  - **CryptoDrop** (Scaife et al., 2016): Entropy deltas and file type changes.
  - **ShieldFS** (Continella et al., 2016): Copy-on-write driver self-healing (12–18% CPU).
  - **R-Sentry** (Al-rimy et al., 2019): Honeyfiles paired with memory cognitive trajectories.
  - **RansomFisher** (Ku et al., 2021): Proved that non-linear traversal evades honeypots.
- **Visual**: Summary of `research_dossier/08_LITERATURE_REVIEW/RESEARCH_COMPARISON_MATRIX.md`.
- **Speaker Notes**: "Our work builds on landmark peer-reviewed research, while addressing the evasion challenge identified by Ku et al."

---

### Slide 11: Proposed Solution: CanarySentinel
- **Key Components**:
  - **Isolated Sandbox**: Enforces strict path canonicalization around `./sandbox`.
  - **Canary Manager**: Deploys 8 strategic decoys with SHA-256 baselines.
  - **Event Normalizer**: Deduplicates FSEvents bursts within a 50 ms debouncing window.
  - **Parallel Detectors**: Baseline, Canary-Only, and Hybrid.
  - **Simulated Response**: Safe internal software block flag.
- **Speaker Notes**: "CanarySentinel combines deception tripwires with kinematic filesystem velocity."

---

### Slide 12: Modular System Architecture
- **Visual**: Mermaid diagram `diagrams/system_architecture.mmd`.
- **Key Flow**: Sandbox I/O $\rightarrow$ FSEvents $\rightarrow$ Watchdog $\rightarrow$ Normalizer $\rightarrow$ Parallel Detectors $\rightarrow$ Risk Engine $\rightarrow$ SQLite & Streamlit Dashboard.
- **Speaker Notes**: "Crucially, all three detectors receive the exact same normalized event stream simultaneously, guaranteeing equi-telemetry fairness."

---

### Slide 13: Technology Stack & Execution Environment
- **Platform**: Apple Silicon M1 (arm64, 8 GB Unified Memory, macOS Sequoia 15.3).
- **Core Languages**: Python 3.12+ and SQLite 3.46.0 (WAL mode).
- **Key Dependencies**: `watchdog 6.0.0`, `psutil 7.0.0`, `streamlit 1.43.0`, `pandas 2.2.3`, `pytest 8.3.5`.
- **Resource Footprint**: < 38 MB RAM, ~25% single-core CPU overhead.
- **Speaker Notes**: "The architecture is lightweight, cross-platform, and runs entirely in user space."

---

### Slide 14: Three Detection Configurations
- **Configuration A: Baseline Detector**:
  - Rate $> 8\text{ ops in 2s}$, mass renames $\ge 4$, entropy $\ge 7.2$. Ignores canaries.
- **Configuration B: Canary-Only Detector**:
  - Intercepts `is_canary == True` on modify/delete/move. Immediate alert.
- **Configuration C: Hybrid Detector**:
  - Correlates canary breach with surrounding context velocity ($\ge 3$ ops in 3s) or companion high-entropy writes.
- **Speaker Notes**: "Here are our three detection engines. Hybrid requires both spatial decoy contact and temporal velocity."

---

### Slide 15: Experimental Methodology & Fairness
- **Strict Methodology**:
  - All trials execute inside isolated sandbox directory.
  - Synthetic high-entropy bytes written without malicious payloads.
  - Automated 150 ms settling window between runs prevents event bleed.
  - All metrics recalculated directly from raw SQLite trial records.
- **Speaker Notes**: "Our methodology guarantees reproducibility and absolute scientific honesty."

---

### Slide 16: The Six Standardized Scenarios
- **Benign Workloads (Negative Class, $N_{\text{neg}} = 40$)**:
  - B1: Normal File Editing (5 ops)
  - B2: Bulk Copying (6 ops)
  - B3: Canary Touch Without Follow-up (4 ops)
  - B4: Bulk Renaming (6 ops)
- **Attack Workloads (Positive Class, $N_{\text{pos}} = 20$)**:
  - S5: Canary Touch + Rapid Bulk Modifications (12 ops)
  - S6: Rapid Bulk Modifications Without Canary (10 ops)
- **Speaker Notes**: "Scenario S6 specifically tests what happens when an attacker knows to avoid honeypot files."

---

### Slide 17: Experimental Dataset & Trial Distribution
- **Dataset Structure ($N = 180$ Controlled Trials)**:
  - 3 Configurations $\times$ 6 Scenarios $\times$ 10 Repetitions = 180 Trials.
  - Exactly 60 trials per detector configuration.
  - 100% completed trials, 0 failed runs, 0 duplicate IDs.
- **Visual**: Data distribution matrix.
- **Speaker Notes**: "Every single trial was logged to SQLite and exported to RAW_EXPERIMENT_DATA.csv."

---

### Slide 18: Results: Side-by-Side Performance Comparison
- **Master Metrics Table**:
  - **Baseline**: Precision = 66.7%, Recall = **100.0%**, F1 = **0.80**, FPR = 25.0%, Latency = 147.1 ms (TP latency = 84.9 ms).
  - **Canary-Only**: Precision = 50.0%, Recall = 50.0%, F1 = 0.50, FPR = 25.0%, Latency = **18.9 ms**.
  - **Hybrid**: Precision = **100.0%**, Recall = 50.0%, F1 = 0.67, FPR = **0.0%**, Latency = 26.1 ms.
- **Speaker Notes**: "Notice two vital rows: False Positive Rate and Recall. Hybrid achieves 0% false alarms, but Baseline achieves 100% recall."

---

### Slide 19: Statistical Validation & Significance
- **Welch's $t$-test (Latency)**: $t = 6.3887, p < 0.0001$, Cohen's $d = 1.35$ (Very large effect size).
- **Fisher's Exact Test (False Positives)**: $p = 0.0011$ (Hybrid significantly suppresses false alarms).
- **Fisher's Exact Test (Recall)**: $p = 0.0004$ (Baseline significantly outperforms Hybrid in recall).
- **Speaker Notes**: "All primary performance differences are statistically significant at $p < 0.01$."

---

### Slide 20: Scenario Breakdown & Discrepancy Resolution
- **Resolution of Discrepancies**:
  - **Operations Prevented (~99.1% in S5 vs 49.5% overall)**: In S5, Hybrid prevents ~99.1% of targeted user ops (0.10 files damaged). In S6, it prevents 0.0%. Mean user ops prevented across both attack scenarios is 49.55%!
  - **Baseline False Positives**: Occurred in Scenario B4 (`Bulk Renaming`) due to mass-rename threshold.
- **Speaker Notes**: "This scenario analysis completely reconciles our reported empirical numbers."

---

### Slide 21: Research Contribution: The Defense-in-Depth Cascade
- **The Core Academic Contribution**:
  - Hybrid is **not** universally superior; it cannot replace behavioral monitoring.
  - **Proposed Production EDR Architecture**:
    - **Tier 1 (Fast-Path - Hybrid Engine)**: Dispatches instant `SIGKILL` in 26 ms with 100% precision.
    - **Tier 2 (Safety-Net - Baseline Engine)**: Dispatches `SIGSTOP` (suspension) for review when velocity is high without canary contact.
- **Speaker Notes**: "This two-tier cascade delivers both rapid containment and complete threat coverage."

---

### Slide 22: Limitations & Threats to Validity
- **Honest Limitations**:
  - Asynchronous user-space event delay (10–25 ms) commits initial writes before alerts fire.
  - Synthetic pseudo-random byte writes rather than live polymorphic malware.
  - Static canary filenames vulnerable to reverse-engineering.
- **Speaker Notes**: "We acknowledge that user-space monitoring cannot prevent the very first write without a kernel extension."

---

### Slide 23: Future Scope & Roadmap
- **Roadmap**:
  1. Migrate to Apple's native `EndpointSecurity.framework` (`es_client`) for synchronous pre-write blocking.
  2. Implement reinforcement learning for dynamic, adaptive canary placement.
  3. Benchmark against live weaponized malware in an isolated hypervisor sandbox.
- **Speaker Notes**: "Future work will bring synchronous blocking and machine-learning adaptive placement."

---

### Slide 24: Conclusion
- **Summary**:
  - Proved that temporal sliding-window corroboration solves the false-alarm problem (0.0% FPR).
  - Measured 26.1 ms latency limiting damage to 0.10 files (~99.1% of user operations prevented) in canary-targeted attacks.
  - Proved that decoy evasion creates a 50% blind spot, establishing the necessity of defense-in-depth.
  - Verified across 180 controlled empirical trials with 56 passing automated tests in 5.06s.
- **Speaker Notes**: "In conclusion, CanarySentinel provides rigorous empirical evidence for the future of deception-based endpoint security."

---

### Slide 25: References & Open Defence
- **Selected References**: Scaife (2016), Continella (2016), Kharraz (2015), Al-rimy (2019), Ku (2021), Moore (2017).
- **Acknowledgements**: Thank you to our project supervisor and faculty evaluators.
- **Open for Questions**: We invite questions from the examination board.
- **Speaker Notes**: "Thank you for your time. We are now ready for your questions."

