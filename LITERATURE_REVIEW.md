# CanarySentinel Literature Review: Endpoint Ransomware Detection Paradigms

## 1. Introduction and Threat Landscape

Ransomware has evolved into one of the most destructive threats targeting corporate and consumer computing infrastructure. Modern ransomware variants (e.g., LockBit, BlackCat/ALPHV, Conti) leverage robust asymmetric-symmetric hybrid cryptographic schemes (e.g., Curve25519 with ChaCha20, or RSA-4096 with AES-256) to systematically deny access to user data until a ransom is paid.

Because cryptographic operations are computationally irreversible once completed, the primary objective of endpoint ransomware defense is **early, accurate detection and rapid, automated containment** before widespread data loss occurs.

---

## 2. Detection Paradigms in Extant Literature

### 2.1 Static and Signature-Based Detection
Traditional antivirus (AV) and endpoint protection platforms (EPP) historically relied on file hashes, byte signatures, and heuristic import table analysis. 

- **Limitations**: Modern ransomware operators routinely evade static signatures via code obfuscation, runtime packers, custom polymorphism, and Living-off-the-Land (LotL) binaries. By the time a signature is distributed via threat intelligence feeds, victim files are already encrypted.

### 2.2 Pure Behavioral and Filesystem Heuristics
Seminal systems such as *CryptoDrop* (Scaife et al., 2016) and *ShieldFS* (Continella et al., 2016) shifted focus toward observing runtime filesystem modifications:
- **Metrics Evaluated**: File operation velocity (burst rate), mass sequential file renaming, mass deletion of shadow copies, and Shannon entropy calculations on file write buffers.
- **Shannon Entropy**: Encrypted data resembles uniformly distributed pseudorandom bytes, characterized by high Shannon entropy:
  $$H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i) \approx 7.9 - 8.0 \text{ bits/byte}$$
- **Limitations**:
  1. **High False Positive Rate (FPR)**: Legitimate administrative and user operations—such as archiving files with ZIP/gzip, transferring encrypted backups, or batch renaming photos—mirror ransomware volume and entropy profiles.
  2. **Elevated Containment Latency**: To avoid false positives, volume heuristics require an accumulation threshold (e.g., 5 to 10 modified files), allowing meaningful user file damage before detection triggers.

### 2.3 Honeypot and Canary Decoy Files
Honeypots and decoy tripwire files (Kharraz et al., 2015, *UNVEIL*; Moore, 2017) introduce synthetic files placed into strategic directory locations:
- **Mechanism**: The system registers decoy files (e.g., `!00_passwords.xlsx`) in high-value directories. Any read, write, rename, or deletion of a decoy triggers an immediate security alert.
- **Advantages**: Minimal CPU overhead, simple deployment, and immediate containment latency ($\sim 10 - 25$ ms).
- **Limitations**:
  1. **High False Positive Rate (FPR) on Innocent Scans**: Legitimate background services—such as macOS Spotlight metadata indexers, routine Antivirus background scans, enterprise backup agents, or accidental user clicks—touch canary files, causing false alarms and disruptive containment.
  2. **Evasion Susceptibility**: Ransomware that sorts targets randomly, encrypts files in reverse alphabetical order, or targets specific proprietary extensions (e.g., `.mdf`, `.vhdx`) may completely miss canary files, resulting in false negatives.

### 2.4 Contextual Fusion (Hybrid Detection)
Recent research explores **multi-signal contextual correlation** to bridge the gap between decoy simplicity and behavioral robustness:
- **Concept**: Rather than treating a canary touch as an isolated boolean trigger, the canary signal serves as an **anchor event** that initiates a high-sensitivity observation window.
- **Verification**: The detection engine requires contextual companion indicators (e.g., high-entropy writes or abnormal operation velocity on surrounding user files) within a bounded temporal window ($\Delta t \le 3.0$ seconds).
- **Benefit**: Innocent isolated canary inspections (e.g., Spotlight indexer) expire harmlessly without an alert, while active ransomware campaigns are confirmed and halted within milliseconds.

---

## 3. CanarySentinel Positioning and Research Contribution

**CanarySentinel** was designed to empirically validate the contextual fusion hypothesis in a controlled, lightweight local prototype:

| Paradigm | Exemplar Systems | Detection Basis | CanarySentinel Analog |
|---|---|---|---|
| **Behavior-Only** | CryptoDrop, ShieldFS | Velocity, Entropy, Mass Renames | **Configuration A: Baseline** |
| **Decoy-Only** | UNVEIL, Bait-based EDR | Decoy file access/touch | **Configuration B: Canary-Only** |
| **Contextual Fusion** | Hybrid correlation frameworks | Decoy touch + Contextual filesystem damage | **Configuration C: Hybrid** |

By feeding the identical normalized filesystem event stream into all three configurations simultaneously, CanarySentinel provides reproducible, empirical evidence comparing the precision, latency, and damage prevention of each paradigm.

---

## 4. Key Literature References

1. **Scaife, N., Carter, H., Traynor, P., & Butler, K. (2016).** *CryptoLock (and Drop It): Stopping Ransomware at the File System.* IEEE 36th International Conference on Distributed Computing Systems (ICDCS).
2. **Continella, A., Guagnelli, A., Zingaro, F., et al. (2016).** *ShieldFS: a Self-healing, Ransomware-aware Filesystem.* 32nd Annual Computer Security Applications Conference (ACSAC).
3. **Kharraz, A., Robertson, W., Balzarotti, D., Bilge, L., & Kirda, E. (2015).** *Cutting the Gordian Knot: A Look Under the Hood of Ransomware Attacks.* International Conference on Detection of Intrusions and Malware, and Vulnerability Assessment (DIMVA).
4. **Moore, C. (2017).** *Detecting Ransomware with Decoy Documents and Machine Learning.* IEEE International Conference on Big Data.
5. **Shannon, C. E. (1948).** *A Mathematical Theory of Communication.* Bell System Technical Journal, 27(3), 379–423.

