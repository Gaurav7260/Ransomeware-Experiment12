"""Streamlit Dashboard for CanarySentinel — Complete SOC & Research Platform."""

import os
from pathlib import Path
import sys
from typing import Any, Dict

import psutil
import streamlit as st

# Ensure repository root is on PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from canary_sentinel.canary.manager import CanaryManager
from canary_sentinel.core.config import SentinelConfig
from canary_sentinel.core.sandbox import SandboxManager
from canary_sentinel.dashboard.views_alerts import render_alert_center
from canary_sentinel.dashboard.views_analytics import render_analytics
from canary_sentinel.dashboard.views_comparison import render_detector_comparison
from canary_sentinel.dashboard.views_config import render_configuration
from canary_sentinel.dashboard.views_events import render_event_monitor
from canary_sentinel.dashboard.views_guide import render_project_guide
from canary_sentinel.dashboard.views_history import render_experiment_history
from canary_sentinel.dashboard.views_lab import render_live_test_lab
from canary_sentinel.dashboard.views_overview import render_overview
from canary_sentinel.dashboard.views_reports import render_reports_centre
from canary_sentinel.experiments.metrics import MetricsCalculator
from canary_sentinel.experiments.runner import ExperimentRunner
from canary_sentinel.monitoring.monitor import FilesystemMonitor
from canary_sentinel.monitoring.normalizer import EventNormalizer
from canary_sentinel.simulation.response_manager import SimulatedResponseManager
from canary_sentinel.simulation.simulator import ActivitySimulator
from canary_sentinel.storage.db import Database


# Page configuration
st.set_page_config(
    page_title="CanarySentinel — Ransomware Behavioral Detection & Decoy System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_resource
def get_sentinel_services() -> Dict[str, Any]:
    """Initialize core CanarySentinel singletons."""
    config = SentinelConfig.load()
    sandbox = SandboxManager(config.system.sandbox_dir)
    db = Database(config.system.db_path)
    canary_mgr = CanaryManager(sandbox, db, config.canary)
    normalizer = EventNormalizer(sandbox, canary_mgr, config.monitoring.debounce_ms)
    monitor = FilesystemMonitor(sandbox, normalizer)
    response_mgr = SimulatedResponseManager(config.response)
    simulator = ActivitySimulator(sandbox, canary_mgr, response_mgr)
    runner = ExperimentRunner(sandbox, db, canary_mgr, monitor, simulator, response_mgr)
    metrics_calc = MetricsCalculator(db)

    # Automatically ensure monitor is started
    if not monitor.is_running:
        monitor.start()

    return {
        "config": config,
        "sandbox": sandbox,
        "db": db,
        "canary_mgr": canary_mgr,
        "normalizer": normalizer,
        "monitor": monitor,
        "response_mgr": response_mgr,
        "simulator": simulator,
        "runner": runner,
        "metrics_calc": metrics_calc,
    }


def render_sidebar(services: Dict[str, Any]) -> tuple:
    """Render sidebar navigation, view mode toggle, and quick system telemetry."""
    st.sidebar.title("🛡️ CanarySentinel")
    st.sidebar.caption("Deception-Augmented Endpoint Security Platform")

    # Beginner View vs Technical View Toggle (Core Requirement from Part 8)
    view_mode = st.sidebar.radio(
        "Display Mode",
        ["🔰 Beginner View", "⚙️ Technical View"],
        index=0,
        help="Beginner View presents simple explanations and definitions. Technical View shows raw metrics, formulas, and JSON payloads.",
    )
    is_technical = (view_mode == "⚙️ Technical View")

    st.sidebar.markdown("---")

    nav = st.sidebar.radio(
        "Navigation",
        [
            "1. Overview",
            "2. Detector Comparison",
            "3. Live Test Lab",
            "4. Event Monitor",
            "5. Alert Center",
            "6. Experiment History",
            "7. Analytics & Research",
            "8. Configuration",
            "9. Project Guide & FAQ",
            "10. Reports & Downloads",
        ],
        index=0,
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("System Health")
    monitor: FilesystemMonitor = services["monitor"]
    sandbox: SandboxManager = services["sandbox"]
    canary_mgr: CanaryManager = services["canary_mgr"]

    mon_status = "🟢 ACTIVE" if monitor.is_running else "🔴 STOPPED"
    st.sidebar.write(f"**FS Monitor:** {mon_status}")
    st.sidebar.write(f"**Sandbox:** `{sandbox.sandbox_path.name}`")
    st.sidebar.write(f"**Canary Decoys:** {len(canary_mgr._canary_paths)} active")

    # Host resource snapshot
    cpu_cur = psutil.cpu_percent(interval=None)
    mem_cur = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    st.sidebar.write(f"**Host CPU:** {cpu_cur:.1f}%")
    st.sidebar.write(f"**App RAM:** {mem_cur:.1f} MB")

    st.sidebar.markdown("---")

    # Download buttons in sidebar
    st.sidebar.subheader("📦 Official Releases")
    final_app_zip = ROOT_DIR / "CanarySentinel_Final_Application.zip"
    if not final_app_zip.exists():
        final_app_zip = Path("CanarySentinel_Final_Application.zip")
    if final_app_zip.exists():
        with open(final_app_zip, "rb") as af:
            st.sidebar.download_button(
                label="🚀 Download Application (ZIP)",
                data=af.read(),
                file_name="CanarySentinel_Final_Application.zip",
                mime="application/zip",
                use_container_width=True,
                type="primary",
                help="Complete runnable application: source code, dashboard, database, automated tests, and documentation.",
            )

    final_audit_zip = ROOT_DIR / "CanarySentinel_Final_Audit_Package.zip"
    if not final_audit_zip.exists():
        final_audit_zip = Path("CanarySentinel_Final_Audit_Package.zip")
    if final_audit_zip.exists():
        with open(final_audit_zip, "rb") as zf:
            st.sidebar.download_button(
                label="📦 Download Audit Package (ZIP)",
                data=zf.read(),
                file_name="CanarySentinel_Final_Audit_Package.zip",
                mime="application/zip",
                use_container_width=True,
                help="Complete audit dossier: all 6 reports, 12 structured directories, raw benchmark CSVs, SQLite backup, and SHA-256 manifest.",
            )

    if st.sidebar.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()

    return nav, is_technical


def main() -> None:
    services = get_sentinel_services()
    nav_choice, is_technical = render_sidebar(services)

    if nav_choice.startswith("1. Overview"):
        render_overview(services, is_technical=is_technical)
    elif nav_choice.startswith("2. Detector Comparison"):
        render_detector_comparison(services, is_technical=is_technical)
    elif nav_choice.startswith("3. Live Test Lab"):
        render_live_test_lab(services, is_technical=is_technical)
    elif nav_choice.startswith("4. Event Monitor"):
        render_event_monitor(services, is_technical=is_technical)
    elif nav_choice.startswith("5. Alert Center"):
        render_alert_center(services, is_technical=is_technical)
    elif nav_choice.startswith("6. Experiment History"):
        render_experiment_history(services, is_technical=is_technical)
    elif nav_choice.startswith("7. Analytics & Research"):
        render_analytics(services, is_technical=is_technical)
    elif nav_choice.startswith("8. Configuration"):
        render_configuration(services, is_technical=is_technical)
    elif nav_choice.startswith("9. Project Guide"):
        render_project_guide(services, is_technical=is_technical)
    elif nav_choice.startswith("10. Reports & Downloads"):
        render_reports_centre(services, is_technical=is_technical)


if __name__ == "__main__":
    main()
