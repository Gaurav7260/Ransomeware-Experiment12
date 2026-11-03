"""Project Guide and Educational Reference View for CanarySentinel Dashboard."""

from typing import Any, Dict
import streamlit as st


def render_project_guide(services: Dict[str, Any], is_technical: bool = False) -> None:
    """Render Section 9: Project Guide & Metric Glossary."""
    st.title("📚 CanarySentinel Learning Guide & Metric Glossary")
    st.caption("A beginner-friendly and technical reference explaining deception defense, ransomware mechanics, and experimental metrics.")

    tab_faq, tab_glossary, tab_architecture, tab_limitations = st.tabs([
        "Frequently Asked Questions (FAQ)",
        "Comprehensive Metric Glossary",
        "How Deception Defense Works",
        "Research Scope & Limitations",
    ])

    with tab_faq:
        st.subheader("💡 Frequently Asked Questions")

        with st.expander("1. What is CanarySentinel?", expanded=True):
            st.markdown("""
**CanarySentinel** is an endpoint security research prototype that investigates whether combining **canary decoy files** with **filesystem behavioral analysis** can detect and contain ransomware earlier and with fewer false alarms than either method alone.
""")

        with st.expander("2. What is ransomware and why is early detection difficult?", expanded=False):
            st.markdown("""
Ransomware is malicious software that encrypts a user's files and demands a ransom for the decryption key.
- **The Challenge:** Modern ransomware acts quickly, using legitimate operating-system file operations (`open`, `write`, `rename`). Antivirus signatures often lag behind new variants by hours or days.
- **The Timing Problem:** If detection takes several seconds, thousands of user files may already be encrypted.
""")

        with st.expander("3. What is a canary file?", expanded=False):
            st.markdown("""
A **canary file** (decoy tripwire) is a synthetic, sacrificial document (such as `!00_urgent.xlsx`) placed in directories where ransomware is likely to traverse. Legitimate users have no reason to modify these files. If any process alters a canary, it serves as an immediate early warning.
""")

        with st.expander("4. Why does pure Canary-Only detection cause false alarms?", expanded=False):
            st.markdown("""
Legitimate background utilities—such as Windows Search Indexer, macOS Spotlight, backup software, or antivirus scanners—frequently scan files in directories. If an indexer touches a canary, a pure canary detector sounds a false alarm.
""")

        with st.expander("5. What is the Hybrid Corroborated approach?", expanded=False):
            st.markdown("""
The **Hybrid detector** requires two pieces of corroborating evidence:
1. A canary decoy file was accessed or altered.
2. Companion user files are also being rapidly altered or rewritten with high entropy within a short observation window (3 seconds).

This eliminates indexer false alarms while stopping real attacks with minimal damage.
""")

    with tab_glossary:
        st.subheader("📖 Metric & Technical Glossary")
        st.caption("Structured pattern: Technical Term → Simple Meaning → Why It Matters → Example")

        terms = [
            (
                "True Positive (TP)",
                "The system correctly detected an actual simulated attack.",
                "Measures how effectively attacks are intercepted.",
                "Scenario S5 (ransomware) triggered an alert and halted.",
            ),
            (
                "False Positive (FP)",
                "The system raised a security alarm for harmless, innocent activity.",
                "False alarms waste analysts' time and cause alert fatigue.",
                "Baseline flagged a bulk file renaming task as an attack.",
            ),
            (
                "True Negative (TN)",
                "The system correctly remained silent during normal, harmless user activity.",
                "Confirms system stability under daily office workloads.",
                "Normal document editing completed with zero alerts.",
            ),
            (
                "False Negative (FN)",
                "An attack occurred, but the system completely failed to detect it.",
                "Missed attacks allow ransomware to encrypt all files.",
                "Hybrid missed Scenario S6 because the attack avoided canaries.",
            ),
            (
                "Precision (Exactness)",
                "When the alarm rings, how often is it a real attack?",
                "High precision eliminates false alarm fatigue.",
                "Hybrid achieved 100% Precision (every alert was a real attack).",
            ),
            (
                "Recall (Coverage / Sensitivity)",
                "Out of all attacks that occurred, how many were caught?",
                "High recall ensures no attacks slip past undetected.",
                "Baseline achieved 100% Recall; Hybrid achieved 50% Recall.",
            ),
            (
                "F1-Score",
                "A balanced harmonic average of Precision and Recall (0.0 to 1.0).",
                "Evaluates whether a detector balances accuracy with coverage.",
                "Baseline scored 0.80; Hybrid scored 0.67.",
            ),
            (
                "False Positive Rate (FPR)",
                "The percentage of harmless tasks that trigger a false alarm.",
                "Lower is better; 0% means zero false alarms.",
                "Hybrid scored 0.0% FPR; Baseline and Canary scored 25.0% FPR.",
            ),
            (
                "Detection Latency",
                "The time in milliseconds between attack start and detection.",
                "Faster detection halts attacks before they encrypt more files.",
                "Pure canaries alerted in 18.9 ms; Hybrid alerted in 26.1 ms.",
            ),
            (
                "Shannon Entropy",
                "A mathematical measure of byte unpredictability (0.0 to 8.0).",
                "Encrypted files look like random noise (entropy > 7.0).",
                "Plaintext text files score ~3.5–4.5; AES-encrypted data scores ~7.8.",
            ),
            (
                "Simulated Containment",
                "Halting the internal simulator's loop upon detection.",
                "Protects the host while safely evaluating response metrics.",
                "The simulator checks `is_blocked()` before each write.",
            ),
        ]

        for term, simple, why, ex in terms:
            with st.expander(f"📌 {term}"):
                st.markdown(f"**Simple Meaning:** {simple}")
                st.markdown(f"**Why It Matters:** {why}")
                st.markdown(f"**Concrete Example:** {ex}")

    with tab_architecture:
        st.subheader("🏛️ How Deception Defense Works")
        st.markdown("""
```
User & Malicious Filesystem Activity
               │
               ▼
   [ Watchdog Filesystem Monitor ]
               │  (FSEvents / inotify notifications)
               ▼
   [ Event Normalizer & Debouncer ]
       ├─ Classifies: Is target a Decoy Canary?
       ├─ Computes Shannon Entropy & Size
       └─ Dispatches NormalizedEvent
               │
               ├─────────────────────────┬─────────────────────────┐
               ▼                         ▼                         ▼
     [ Baseline Detector ]    [ Canary-Only Detector ]    [ Hybrid Detector ]
     • Volume Velocity        • Decoy Tripwire Breach     • Decoy Breach AND
     • Entropy Threshold      • Instant Alert             • Contextual Churn
     • Mass Rename Check                                  • Zero False Positives
               │                         │                         │
               └─────────────────────────┼─────────────────────────┘
                                         ▼
                            [ Risk & Severity Engine ]
                            • Scores Risk: 0 - 100
                            • Maps Severity (LOW to CRITICAL)
                            • Builds Forensic Proof
                                         │
                                         ▼
                       [ Simulated Response Manager ]
                       • Activates thread-safe block flag
                       • Simulator halts synthetic writes
```
""")

    with tab_limitations:
        st.subheader("⚠️ Academic Scope & Real-World Limitations")
        st.markdown("""
1. **User-Space Latency Floor**: Because CanarySentinel relies on user-space filesystem notifications (`watchdog`), notifications arrive after the operating system has written the data. A minimum of 1-2 files may be touched before an alert is dispatched.
2. **Canary Avoidance Evasion**: If sophisticated malware knows decoy naming patterns or traverses only specific user folders without touching decoys, canary-dependent detectors will not trigger. This is why a defense-in-depth model with Baseline behavioral volume tracking is required.
3. **Synthetic Workloads in Sandbox**: All experiments use non-destructive simulated file operations inside `./sandbox`. Kernel driver evasion and advanced process hollowing are not modeled.
4. **Cooperative Containment**: Containment stops the simulator's cooperative loop. It does not implement real-world operating system process termination (`SIGKILL`).
""")

