"""Event Monitor View for CanarySentinel Dashboard."""

from typing import Any, Dict
import pandas as pd
import streamlit as st

from canary_sentinel.storage.db import Database


def render_event_monitor(services: Dict[str, Any], is_technical: bool = False) -> None:
    """Render Section 4: Event Monitor (Live Event Stream)."""
    st.title("📡 Filesystem Event Monitor")
    st.caption("Real-time and stored operating-system filesystem events captured by the watchdog notification pipeline.")

    db: Database = services["db"]

    # Filter Controls
    f_c1, f_c2, f_c3, f_c4 = st.columns(4)
    with f_c1:
        ev_type_filter = st.selectbox("Event Type", ["ALL", "CREATE", "MODIFY", "DELETE", "MOVE"], index=0)
    with f_c2:
        canary_filter = st.selectbox("Category", ["ALL", "Canary Decoys Only", "User Files Only"], index=0)
    with f_c3:
        limit_val = st.slider("Max Events to Display", min_value=25, max_value=500, value=100, step=25)
    with f_c4:
        path_search = st.text_input("Path Filter", "", placeholder="e.g. .docx or documents")

    # Query events
    is_canary_arg = None
    if canary_filter == "Canary Decoys Only":
        is_canary_arg = True
    elif canary_filter == "User Files Only":
        is_canary_arg = False

    events = db.get_events(limit=limit_val, is_canary=is_canary_arg)

    if ev_type_filter != "ALL":
        events = [e for e in events if e.event_type == ev_type_filter]
    if path_search:
        events = [e for e in events if path_search.lower() in e.path.lower()]

    st.subheader(f"📋 Event Audit Log ({len(events)} events shown)")

    if events:
        table_rows = []
        for e in events:
            cat_label = "🟡 CANARY DECOY" if e.is_canary else "📄 User File"
            time_str = e.iso_timestamp.split("T")[-1] if "T" in e.iso_timestamp else str(e.timestamp)
            table_rows.append({
                "Time": time_str,
                "Event Type": e.event_type,
                "File Path": e.path,
                "Category": cat_label,
                "Entropy": f"{e.entropy:.2f}",
                "Size (Bytes)": e.size_bytes,
                "PID": e.process_id or "-",
                "Scenario ID": e.scenario_id or "-",
            })

        df_events = pd.DataFrame(table_rows)
        st.dataframe(df_events, use_container_width=True)

        # CSV Export
        csv_data = df_events.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Export Filtered Events to CSV",
            data=csv_data,
            file_name="canary_sentinel_events.csv",
            mime="text/csv",
        )
    else:
        st.info("No filesystem events matching filter criteria. Execute a scenario in the **Live Test Lab** to generate events.")

