"""Configuration View for CanarySentinel Dashboard."""

from typing import Any, Dict
import streamlit as st

from canary_sentinel.core.config import SentinelConfig


def render_configuration(services: Dict[str, Any], is_technical: bool = False) -> None:
    """Render Section 8: Configuration & Threshold Explanations."""
    st.title("⚙️ Detection Thresholds & System Configuration")
    st.caption("Inspect and understand the active parameters governing CanarySentinel detectors and response mechanisms.")

    config: SentinelConfig = services["config"]

    # Simple explanation header
    if not is_technical:
        st.info(
            "💡 **Configuration Guide**: These settings define how sensitive each detector is. "
            "Lowering thresholds makes detectors faster but increases false alarms. "
            "Raising thresholds makes them safer against false alarms but may allow more files to be modified."
        )

    tab_base, tab_canary, tab_hybrid, tab_resp = st.tabs([
        "Configuration A: Baseline",
        "Configuration B: Canary-Only",
        "Configuration C: Hybrid Corroborated",
        "Automated Response",
    ])

    with tab_base:
        st.subheader("Baseline Behavioral Parameters")
        b = config.detection.baseline
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Burst Window (seconds)", f"{b.burst_window_seconds}s")
            st.metric("Burst Count Threshold", f"{b.burst_count_threshold} operations")
            st.metric("Base Risk Score", f"{b.base_risk_score} / 100")
        with col2:
            st.metric("Entropy Threshold", f"{b.entropy_threshold:.1f}")
            st.metric("Mass Rename Threshold", f"{b.mass_rename_threshold} renames")

        st.markdown(r"""
**Threshold Rationale & Impact:**
- **Burst Count ($\ge 6$ ops in 2.0s)**: Catches rapid encryption loops that modify or create files rapidly.
- **Mass Rename ($\ge 4$ renames in 2.0s)**: Ransomware commonly appends extensions (e.g. `.locked`). Note: High-volume desktop reorganizations also trip this threshold.
- **Entropy ($\ge 7.0$)**: Measures byte unpredictability. Plaintext documents score $\approx 3.5$–$5.0$; encrypted payloads score $\approx 7.2$–$7.9$.
""")

    with tab_canary:
        st.subheader("Canary Decoy Parameters")
        c = config.detection.canary_only
        st.metric("Base Risk Score", f"{c.base_risk_score} / 100")
        st.markdown(f"**Monitored Canary Operations:** `{', '.join(c.monitored_events)}`")
        st.markdown(f"**Deployed Decoys Count:** `{config.canary.decoy_count}` files")
        st.markdown(f"**Target Folders:** `{', '.join(config.canary.target_directories)}`")
        st.markdown(f"**Decoy Extensions:** `{', '.join(config.canary.file_extensions)}`")

        st.markdown("""
**Threshold Rationale & Impact:**
- **Zero-Tolerance Tripwire**: Because canary decoys contain no genuine user data, any modification, deletion, or renaming immediately triggers an alert.
- **Limitation**: Pure canary detection cannot distinguish benign desktop search indexers from malicious actors.
""")

    with tab_hybrid:
        st.subheader("Hybrid Corroborated Parameters")
        h = config.detection.hybrid
        h_col1, h_col2 = st.columns(2)
        with h_col1:
            st.metric("Observation Window", f"{h.observation_window_seconds}s")
            st.metric("Min Context Companion Events", f"{h.min_context_events} events")
        with h_col2:
            st.metric("Burst Velocity Threshold", f"{h.burst_velocity_threshold} ops/sec")
            st.metric("Companion Entropy Threshold", f"{h.entropy_threshold:.1f}")

        st.markdown(r"""
**Threshold Rationale & Impact:**
- **Dual-Condition Corroboration**: A canary breach opens an observation window ($3.0\text{s}$). An alert is dispatched ONLY if $\ge 2$ non-canary companion events also occur.
- **Zero False Positive Guarantee**: When an indexer opens a decoy file in isolation (0 companion file modifications), Hybrid suppresses the alarm.
""")

    with tab_resp:
        st.subheader("Automated Response & Containment Protocol")
        r = config.response
        st.metric("Auto-Block Enabled", "YES ✅" if r.auto_block else "NO ❌")
        st.metric("Minimum Severity for Block", r.minimum_severity)
        st.metric("Risk Score Threshold for Block", f"{r.risk_score_threshold} / 100")

        st.info(
            "🛡️ **Safety Reminder**: In this research prototype, 'Containment' activates an internal thread-safe flag "
            "(`is_blocked()`) which signals the synthetic simulator loop to halt subsequent file writes. "
            "It never kills operating-system processes or harms user software."
        )

