"""Live Test Lab View for CanarySentinel Dashboard.

Provides safe, interactive, real-time testing of the six scenario workloads
against individual detectors or a side-by-side comparative benchmark.
"""

import time
import uuid
from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st

from canary_sentinel.canary.manager import CanaryManager
from canary_sentinel.core.sandbox import SandboxManager
from canary_sentinel.detection.explanation_engine import DetectionExplanationEngine
from canary_sentinel.experiments.runner import ExperimentRunner
from canary_sentinel.monitoring.monitor import FilesystemMonitor
from canary_sentinel.simulation.response_manager import SimulatedResponseManager
from canary_sentinel.simulation.simulator import ActivitySimulator
from canary_sentinel.storage.db import Database
from canary_sentinel.storage.models import AlertRecord, NormalizedEvent, ScenarioRecord


LAB_SCENARIOS = {
    "normal_file_editing": {
        "title": "Test 1 — Normal File Editing",
        "category": "Benign",
        "description": "Creates, modifies, saves, and renames a standard user document. Expected: No alert (clean pass).",
        "scenario_key": "normal_file_editing",
    },
    "bulk_copying": {
        "title": "Test 2 — Bulk File Copying",
        "category": "Benign",
        "description": "Copies multiple harmless files within sandbox directories. Tests volume thresholds without malicious behavior.",
        "scenario_key": "bulk_copying",
    },
    "canary_touch_benign": {
        "title": "Test 3 — Canary Interaction Only (Indexer Probing)",
        "category": "Benign",
        "description": "Simulates an innocent desktop search indexer scanning a decoy canary file without companion user file damage. Tests Canary false positives vs Hybrid context suppression.",
        "scenario_key": "canary_touch_benign",
    },
    "bulk_renaming": {
        "title": "Test 4 — Bulk File Renaming (Reorganization)",
        "category": "Benign",
        "description": "Renames multiple harmless documents in rapid sequence. Tests Baseline mass-rename heuristic vs Deception specificity.",
        "scenario_key": "bulk_renaming",
    },
    "canary_plus_rapid_bulk": {
        "title": "Test 5 — Canary Interaction + Rapid Bulk Modifications",
        "category": "Suspicious",
        "description": "Simulates ransomware breaching a canary decoy followed by rapid companion file overwrites. Tests rapid detection and early damage containment.",
        "scenario_key": "canary_plus_rapid_bulk",
    },
    "rapid_bulk_without_canary": {
        "title": "Test 6 — Rapid Bulk Activity Without Canary Interaction",
        "category": "Suspicious",
        "description": "Simulates a sophisticated ransomware that intentionally evades decoy tripwires. Demonstrates defense-in-depth: Baseline catches what pure deception misses.",
        "scenario_key": "rapid_bulk_without_canary",
    },
}


def render_live_test_lab(services: Dict[str, Any], is_technical: bool = False) -> None:
    """Render Section 3: Live Test Lab."""
    st.title("🧪 Live Interactive Test Lab")
    st.caption("Execute harmless, controlled synthetic workloads inside the isolated sandbox and observe detector decisions.")

    # Safety & Simulated Containment Disclaimer (Mandatory Requirement)
    st.warning(
        "🛡️ **Safety & Containment Protocol**: All tests operate strictly on synthetic scratch files inside `./sandbox`. "
        "**Simulated containment means the application stops its own harmless attack simulation after detection. "
        "It does not terminate an external operating-system process or modify real user documents.**"
    )

    db: Database = services["db"]
    sandbox: SandboxManager = services["sandbox"]
    canary_mgr: CanaryManager = services["canary_mgr"]
    monitor: FilesystemMonitor = services["monitor"]
    response_mgr: SimulatedResponseManager = services["response_mgr"]
    simulator: ActivitySimulator = services["simulator"]
    runner: ExperimentRunner = services["runner"]

    # Controls Layout
    st.subheader("⚙️ Test Configuration")
    ctrl_col1, ctrl_col2 = st.columns([1.5, 1])

    with ctrl_col1:
        sc_choice = st.selectbox(
            "Select Harmless Scenario",
            list(LAB_SCENARIOS.keys()),
            format_func=lambda k: f"{LAB_SCENARIOS[k]['title']} [{LAB_SCENARIOS[k]['category'].upper()}]",
            help="Select which synthetic workload to execute inside the sandbox.",
        )
        sc_meta = LAB_SCENARIOS[sc_choice]
        st.info(f"**Scenario Goal:** {sc_meta['description']}")

    with ctrl_col2:
        det_mode = st.radio(
            "Select Detector Configuration",
            [
                "hybrid",
                "baseline",
                "canary_only",
                "compare_all",
            ],
            format_func=lambda d: {
                "hybrid": "Configuration C — Hybrid Corroborated (Decoy + Context)",
                "baseline": "Configuration A — Baseline Behavioral (Volume/Entropy)",
                "canary_only": "Configuration B — Pure Canary Decoy (Tripwire)",
                "compare_all": "🔬 Compare All Three Detectors (Isolated Benchmark)",
            }[d],
            index=0,
            help="Choose an individual detector or execute an isolated sequential comparison.",
        )

    btn_c1, btn_c2, btn_c3 = st.columns([1, 1, 1.5])
    with btn_c1:
        run_clicked = st.button("▶️ Run Test Now", type="primary", use_container_width=True)
    with btn_c2:
        reset_clicked = st.button("🔄 Reset Sandbox", use_container_width=True)
    with btn_c3:
        sb_dir = getattr(sandbox, "sandbox_dir", str(getattr(sandbox, "sandbox_path", "./sandbox")))
        st.caption(f"Sandbox Location: `{sb_dir}`")

    # Handle Sandbox Reset
    if reset_clicked:
        with st.spinner("Resetting sandbox and redeploying canaries..."):
            sandbox.reset_sandbox()
            canary_mgr.deploy_canaries()
            response_mgr.reset()
            st.success("✅ Sandbox reset complete. Canaries redeployed safely.")

    # Execution State Container
    if run_clicked:
        batch_id = f"batch_live_{int(time.time())}"
        st.markdown("---")
        st.subheader("📡 Live Execution & Telemetry Stream")

        if det_mode == "compare_all":
            # Sequential Isolated Execution of All 3 Detectors
            st.info("Executing 3 isolated trials with identical initial sandbox conditions...")
            results: List[ScenarioRecord] = []
            progress_bar = st.progress(0.0)
            status_text = st.empty()

            detectors_to_run = ["baseline", "canary_only", "hybrid"]
            for idx, det in enumerate(detectors_to_run):
                status_text.text(f"Running isolated trial {idx + 1}/3: {det.replace('_', ' ').title()} Detector...")
                rec = runner.run_trial(
                    scenario_key=sc_choice,
                    detector_config=det,
                    batch_id=batch_id,
                )
                results.append(rec)
                progress_bar.progress((idx + 1) / 3.0)

            status_text.text("✅ Comparative execution finished!")
            time.sleep(0.2)

            # Display Side-by-Side Comparison Table
            st.subheader("📊 Side-by-Side Live Comparison Matrix")
            cmp_rows = []
            for r in results:
                lat_str = f"{r.detection_latency_ms:.1f} ms" if r.detection_latency_ms else "-"
                cmp_rows.append({
                    "Detector": r.detector_config.replace("_", " ").title(),
                    "Detected Alert": "🚨 ALERT" if r.detected else "✅ NO ALERT",
                    "Containment Latency": lat_str,
                    "Containment Action": "HALTED 🛑" if r.response_triggered else "NONE (Completed)",
                    "Planned Ops": r.planned_ops,
                    "Executed Ops": r.executed_ops,
                    "Prevented Ops": r.prevented_ops,
                    "Files Damaged": r.files_damaged,
                })
            st.dataframe(pd.DataFrame(cmp_rows), use_container_width=True)

            # High-level insight
            st.markdown("### 💡 Comparative Analysis of this Run")
            if sc_meta["category"] == "Benign":
                st.markdown("""
- **False Positive Resistance**: Notice how Hybrid filters out the benign activity (0% false positives), whereas Canary-Only trips if a decoy was inspected (e.g., in Test 3), and Baseline trips if rapid renames occurred (Test 4).
""")
            else:
                st.markdown("""
- **Attack Interception**: Notice how Hybrid and Canary-Only achieve rapid containment (under 30 ms) if a decoy was breached (Test 5), preventing over 90% of operations. If the attack avoids decoys (Test 6), Baseline's volume tracking acts as the safety net.
""")

        else:
            # Single Detector Execution
            with st.spinner(f"Running {sc_meta['title']} on {det_mode.replace('_', ' ').title()} detector..."):
                trial_rec = runner.run_trial(
                    scenario_key=sc_choice,
                    detector_config=det_mode,
                    batch_id=batch_id,
                )

            # Display Single Trial Summary
            st.success(f"Execution Completed in {trial_rec.duration_ms:.1f} ms")

            res_c1, res_c2, res_c3, res_c4 = st.columns(4)
            with res_c1:
                st.metric(
                    label="Detection Outcome",
                    value="🚨 ALERT GENERATED" if trial_rec.detected else "✅ NO ALERT (PASSED)",
                    delta="Suspicious" if trial_rec.detected else "Benign",
                )
            with res_c2:
                lat_val = f"{trial_rec.detection_latency_ms:.1f} ms" if trial_rec.detection_latency_ms else "N/A"
                st.metric(
                    label="Detection Latency",
                    value=lat_val,
                    delta="Response Time",
                )
            with res_c3:
                prev_pct = (trial_rec.prevented_ops / trial_rec.planned_ops * 100.0) if trial_rec.planned_ops > 0 else 0.0
                st.metric(
                    label="Operations Prevented",
                    value=f"{trial_rec.prevented_ops} / {trial_rec.planned_ops} ({prev_pct:.1f}%)",
                    delta=f"{trial_rec.executed_ops} Executed",
                )
            with res_c4:
                st.metric(
                    label="User Files Damaged",
                    value=f"{trial_rec.files_damaged} Files",
                    delta="Simulated Overwrites",
                )

            # Explanation Engine Breakdown
            st.markdown("### 🧠 Detection Explanation Engine Breakdown")
            if trial_rec.alert_id:
                alerts = [a for a in db.get_alerts(limit=50) if a.alert_id == trial_rec.alert_id]
                if alerts:
                    alert = alerts[0]
                    detail = DetectionExplanationEngine.explain_alert(alert)

                    st.markdown(f"#### 🔍 {detail.headline}")
                    st.markdown(f"**What happened?**\n{detail.what_happened}")
                    st.markdown(f"**Why was it flagged as suspicious?**\n{detail.why_suspicious}")

                    st.markdown("**Observed Evidence:**")
                    for ev in detail.observed_evidence:
                        st.markdown(f"- `{ev}`")

                    st.markdown(f"**Detector Inference:**\n{detail.detector_inference}")
                    st.markdown(f"**Containment Status:**\n{detail.containment_status}")
                    st.markdown(f"**Recommended Action:**\n{detail.recommended_action}")
            else:
                st.info(
                    f"**No alert was dispatched for this trial.**\n\n"
                    f"- The detector evaluated all incoming filesystem events from this run.\n"
                    f"- No configured behavioral thresholds (for Baseline) or decoy tripwires (for Canary-Only/Hybrid) were violated.\n"
                    f"- Operations proceeded to completion without containment intervention."
                )

            # Live Event Telemetry Table for this specific trial
            st.markdown("### 📋 Captured Filesystem Events in this Trial")
            events = db.get_events(limit=50, scenario_id=trial_rec.scenario_id)
            if events:
                ev_rows = []
                for e in reversed(events):
                    ev_rows.append({
                        "Timestamp": e.iso_timestamp.split("T")[-1],
                        "Event Type": e.event_type,
                        "Target File": e.path,
                        "Category": "DECORY CANARY 🟡" if e.is_canary else "User Document 📄",
                        "Entropy": f"{e.entropy:.2f}",
                        "Size (Bytes)": e.size_bytes,
                    })
                st.dataframe(pd.DataFrame(ev_rows), use_container_width=True)
            else:
                st.caption("No events captured for this trial ID.")

