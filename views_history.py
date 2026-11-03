"""Experiment History View for CanarySentinel Dashboard."""

from typing import Any, Dict
import pandas as pd
import streamlit as st

from canary_sentinel.storage.db import Database


def render_experiment_history(services: Dict[str, Any], is_technical: bool = False) -> None:
    """Render Section 6: Experiment History & Trial Provenance."""
    st.title("📜 Experiment History & Provenance Log")
    st.caption("Inspect individual scenario trials, batch identifiers, and operational telemetry.")

    db: Database = services["db"]

    # Explicit Provenance Notice (Mandatory Requirement from Part 2)
    st.info(
        "📌 **Research Data Provenance**: Historical experimental CSV export (`batch_2026_01` with 180 trials) "
        "is preserved as the permanent academic benchmark dataset. All newly conducted interactive and benchmark trials "
        "are tagged with distinct batch IDs in the local SQLite database to prevent unverified mixing."
    )

    all_scenarios = db.get_scenarios(limit=1000)

    if not all_scenarios:
        st.warning("No scenario records in local SQLite database. Use the **Live Test Lab** to generate experiment trials.")
        return

    # Extract distinct batches
    batches = sorted(list({s.batch_id for s in all_scenarios if s.batch_id}), reverse=True)
    batch_options = ["ALL BATCHES"] + batches + ["Unassigned / Legacy Local"]

    b_col1, b_col2 = st.columns([1.5, 1])
    with b_col1:
        selected_batch = st.selectbox("Filter by Experiment Batch", batch_options, index=0)
    with b_col2:
        det_filter = st.selectbox("Filter by Detector", ["ALL", "baseline", "canary_only", "hybrid"], index=0)

    # Filter scenarios
    filtered = all_scenarios
    if selected_batch != "ALL BATCHES":
        if selected_batch == "Unassigned / Legacy Local":
            filtered = [s for s in filtered if not s.batch_id]
        else:
            filtered = [s for s in filtered if s.batch_id == selected_batch]

    if det_filter != "ALL":
        filtered = [s for s in filtered if s.detector_config == det_filter]

    st.subheader(f"Completed Scenario Trials ({len(filtered)} trials)")

    trial_rows = []
    for s in filtered:
        lat_str = f"{s.detection_latency_ms:.1f} ms" if s.detection_latency_ms is not None else "-"
        prev_pct = (s.prevented_ops / s.planned_ops * 100.0) if s.planned_ops > 0 else 0.0
        trial_rows.append({
            "Trial ID": s.scenario_id,
            "Batch": s.batch_id or "legacy_local",
            "Scenario Name": s.scenario_name,
            "Type": s.scenario_type.upper(),
            "Detector": s.detector_config.replace("_", " ").title(),
            "Detected": "🚨 YES" if s.detected else "✅ NO",
            "Latency": lat_str,
            "Planned": s.planned_ops,
            "Executed": s.executed_ops,
            "Prevented": f"{s.prevented_ops} ({prev_pct:.0f}%)",
            "Files Damaged": s.files_damaged,
            "Duration": f"{s.duration_ms:.0f} ms",
        })

    df_trials = pd.DataFrame(trial_rows)
    st.dataframe(df_trials, use_container_width=True)

    # CSV Export Button
    csv_trials = df_trials.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export Stored Trial Records (CSV)",
        data=csv_trials,
        file_name="canary_sentinel_trials_history.csv",
        mime="text/csv",
    )

