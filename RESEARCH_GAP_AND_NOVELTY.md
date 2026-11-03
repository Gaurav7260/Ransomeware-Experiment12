# Research Gap and Novelty Analysis

## 1. Context & Academic Problem Space

Ransomware remains one of the most destructive categories of cyber threats affecting modern enterprise and personal computing environments. Traditional defenses relying on signature-based anti-malware scanners frequently fail against novel, polymorphic, or zero-day ransomware strains. Consequently, academic and industrial research has pivoted toward **deception-based detection** (e.g., canary/decoy files) and **behavioral anomaly detection** (e.g., monitoring file modification volume, access burst velocity, and Shannon entropy).

However, both paradigms, when deployed in isolation, suffer from acute operational trade-offs:

1. **Canary-Only Detection**: Deploys decoy files as tripwires. While detection latency upon breach is minimal, this approach suffers from significant false positive rates when legitimate background software (e.g., Spotlight indexers, automated backup daemons, antivirus quick scans) inspects or touches decoy files. Furthermore, if ransomware traverses files in an order that avoids decoys, detection fails entirely.
2. **Behavior-Only Detection**: Tracks high-level filesystem metrics (entropy spikes, mass file renames, write velocity). While it does not require prior decoy placement, it struggles to differentiate legitimate bulk operations (e.g., archiving folders, compiling codebases, batch renaming photos) from malicious encryption, yielding false alarms and higher detection latencies that permit substantial data destruction before containment triggers.

---

## 2. Identified Research Gap

While existing literature has extensively investigated canary deployment strategies (e.g., Kharraz et al., 2016; Continella et al., 2016) and behavioral filesystem heuristics (e.g., Scaife et al., 2016), there is a distinct gap in **controlled, reproducible comparative benchmarking across identical normalized event streams**:

| Dimension | Typical Prior Work | CanarySentinel Controlled Study |
| :--- | :--- | :--- |
| **Comparative Ground Truth** | Evaluates either canary systems or behavioral classifiers independently against arbitrary malware sets. | Evaluates **Baseline (Behavior-only)**, **Canary-Only**, and **Hybrid (Correlated)** against identical, synchronized event streams. |
| **False Alarm Contextualization** | Treats canary access as binary malicious events or uses static whitelisting. | Dynamically correlates canary breaches with temporal sliding-window companion operations (entropy + burst rate). |
| **Simulated Damage Quantification** | Focuses predominantly on detection accuracy without measuring prevented operations. | Measures simulated user file damage before detection and the percentage of subsequent malicious operations halted. |
| **Local Safety & Reproducibility** | Often relies on live malware inside fragile Windows virtual machines, limiting reproducibility and safety. | Employs safe, deterministic, non-destructive filesystem simulations within an isolated macOS sandbox. |

---

## 3. Positioned Novelty & Research Contribution

> [!IMPORTANT]
> **Academic Integrity Notice**: CanarySentinel does not claim to have invented canary decoys, entropy calculation, or temporal correlation. These concepts have established precedents in security literature.

The contribution of this project is strictly defined as follows:

1. **Controlled Tri-Detector Comparative Architecture**: A clean, modular framework that feeds equivalent, debounced `NormalizedEvent` records simultaneously to three distinct detection engines (Baseline, Canary-Only, Hybrid), eliminating evaluation bias.
2. **Temporal Correlation Engine for Decoy Validation**: A lightweight, explainable heuristic engine that treats canary file breaches as *anchors* rather than definitive alerts. It requires contextual companion activity (Shannon entropy $\ge 6.8$ bits/byte or rapid modification velocity across companion user documents within a 3.0-second window) to escalate to a high-severity containment alert.
3. **Transparent Simulated Damage & Containment Metrics**: Empirical quantification of user document survival rates, measuring exact files damaged prior to tripwire triggering versus operations neutralized via non-destructive response handlers.
4. **macOS Apple Silicon Compatibility**: Implementation and profiling of filesystem observer behavior using Watchdog FSEvents/kqueue debouncing on modern ARM64 architecture, providing empirical latency and resource overhead benchmarks.

---

## 4. Areas Requiring Further Literature Verification

1. **Kernel vs. User-Space Latency**: Further full-text analysis is needed to quantify the exact latency difference between user-space FSEvents/Watchdog monitoring and kernel-level endpoint detection (e.g., macOS Endpoint Security Framework).
2. **Adaptive Decoy Evasion**: Additional literature verification is required regarding recent ransomware strains that actively identify and bypass known honeyfiles based on inode placement or entropy heuristics.

