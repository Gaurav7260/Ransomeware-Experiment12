#!/usr/bin/env python3
"""CanarySentinel CLI Management and Runner."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from canary_sentinel.canary.manager import CanaryManager
from canary_sentinel.core.config import SentinelConfig
from canary_sentinel.core.sandbox import SandboxManager
from canary_sentinel.experiments.metrics import MetricsCalculator
from canary_sentinel.experiments.runner import ExperimentRunner
from canary_sentinel.monitoring.monitor import FilesystemMonitor
from canary_sentinel.monitoring.normalizer import EventNormalizer
from canary_sentinel.simulation.response_manager import SimulatedResponseManager
from canary_sentinel.simulation.simulator import ActivitySimulator
from canary_sentinel.storage.db import Database


def get_core():
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
    return config, sandbox, db, canary_mgr, monitor, simulator, runner, metrics_calc


def cmd_reset(args):
    _, sandbox, db, canary_mgr, _, _, _, _ = get_core()
    print("Safely wiping sandbox files...")
    sandbox.reset_sandbox()
    canary_mgr.clear_canaries()
    if args.all:
        print("Resetting database records...")
        db.reset_db()
    print("Reset completed successfully.")


def cmd_status(args):
    config, sandbox, db, canary_mgr, _, _, _, metrics_calc = get_core()
    print(f"=== {config.system.app_name} Status ===")
    print(f"Sandbox Directory: {sandbox.sandbox_path}")
    print(f"Database: {db.db_path}")

    canaries = canary_mgr.verify_integrity()
    print(f"Canary Traps Deployed: {len(canaries)}")
    for rel_path, status in canaries.items():
        print(f"  - {rel_path}: {status}")

    events = db.get_events(limit=10)
    alerts = db.get_alerts(limit=5)
    scenarios = db.get_scenarios(limit=5)
    print(f"Total Logged Events: {len(db.get_events(limit=10000))}")
    print(f"Total Alerts: {len(db.get_alerts(limit=10000))}")
    print(f"Total Scenarios Evaluated: {len(db.get_scenarios(limit=10000))}")


def cmd_deploy_canaries(args):
    _, _, _, canary_mgr, _, _, _, _ = get_core()
    print("Deploying decoy canaries...")
    deployed = canary_mgr.deploy_canaries()
    print(f"Successfully deployed {len(deployed)} decoy files:")
    for d in deployed:
        print(f"  • {d.relative_path} ({d.file_size} bytes)")


def cmd_benchmark(args):
    _, _, _, _, monitor, _, runner, metrics_calc = get_core()
    print(f"Running automated benchmark suite (iterations={args.iterations})...")
    monitor.start()
    try:
        def on_prog(cur, tot, desc):
            print(f"[{cur}/{tot}] {desc}")

        records = runner.run_benchmark_suite(iterations=args.iterations, progress_callback=on_prog)
        print(f"\nBenchmark finished! Evaluated {len(records)} trials.")

        report = metrics_calc.generate_comparison_report()
        print("\n=== RESEARCH VERDICT ===")
        print(report.research_verdict)
        print("\nKey Findings:")
        for kf in report.key_findings:
            print(f"  • {kf}")

        print("\n=== DETECTOR PERFORMANCE MATRIX ===")
        for det_name, m in report.metrics_by_detector.items():
            p_str = f"{m.precision:.2%}" if m.precision is not None else "N/A"
            r_str = f"{m.recall:.2%}" if m.recall is not None else "N/A"
            f_str = f"{m.f1_score:.2f}" if m.f1_score is not None else "N/A"
            fpr_str = f"{m.false_positive_rate:.2%}" if m.false_positive_rate is not None else "N/A"
            print(f"[{det_name.upper()}] Runs={m.total_runs} | Precision={p_str} | Recall={r_str} | "
                  f"F1={f_str} | FPR={fpr_str} | "
                  f"Avg Latency={m.mean_latency_ms:.1f}ms (±{m.std_latency_ms:.1f}ms) | Files Damaged={m.mean_files_damaged:.1f}")
    finally:
        monitor.stop()


def cmd_simulate(args):
    _, _, _, _, monitor, _, runner, _ = get_core()
    print(f"Executing scenario '{args.scenario}' with detector '{args.detector}'...")
    monitor.start()
    try:
        rec = runner.run_trial(scenario_key=args.scenario, detector_config=args.detector)
        print("\n=== Scenario Execution Result ===")
        print(f"Scenario: {rec.scenario_name} ({rec.scenario_type})")
        print(f"Detector: {rec.detector_config}")
        print(f"Detected: {'🚨 YES' if rec.detected else '🟢 NO'}")
        if rec.detection_latency_ms:
            print(f"Detection Latency: {rec.detection_latency_ms:.1f} ms")
        print(f"Damaged Files: {rec.files_damaged}")
        print(f"Operations Prevented: {rec.prevented_ops}/{rec.planned_ops}")
        print(f"Response Triggered: {rec.response_triggered}")
    finally:
        monitor.stop()


def cmd_report(args):
    _, _, db, _, _, _, _, metrics_calc = get_core()
    summary_md = metrics_calc.generate_markdown_summary()
    out_path = Path(args.output or "RESEARCH_SUMMARY.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(summary_md)
    print(f"Generated research summary report at '{out_path}'.")
    print("\n" + summary_md[:500] + "\n...")


def cmd_export(args):
    import pandas as pd
    _, _, db, _, _, _, _, metrics_calc = get_core()
    out_dir = Path(args.output_dir or "./exports")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Export events
    events = db.get_events(limit=10000)
    df_ev = pd.DataFrame([e.to_dict() for e in events])
    df_ev.to_csv(out_dir / "events.csv", index=False)

    # Export alerts
    alerts = db.get_alerts(limit=5000)
    df_al = pd.DataFrame([a.to_dict() for a in alerts])
    df_al.to_csv(out_dir / "alerts.csv", index=False)

    # Export trials
    scenarios = db.get_scenarios(limit=5000)
    df_sc = pd.DataFrame([s.to_dict() for s in scenarios])
    df_sc.to_csv(out_dir / "trials.csv", index=False)

    # Export metrics
    rep = metrics_calc.generate_comparison_report()
    metrics_rows = [
        {
            "detector": k,
            **{attr: getattr(m, attr) for attr in dir(m) if not attr.startswith("_") and not callable(getattr(m, attr))}
        }
        for k, m in rep.metrics_by_detector.items()
    ]
    df_met = pd.DataFrame(metrics_rows)
    df_met.to_csv(out_dir / "metrics_summary.csv", index=False)

    # Export scenario breakdown
    if rep.scenario_breakdown:
        df_sb = pd.DataFrame([
            {
                "scenario_id": r.scenario_id,
                "scenario_name": r.scenario_name,
                "scenario_type": r.scenario_type,
                "detector_config": r.detector_config,
                "total_runs": r.total_runs,
                "detected_count": r.detected_count,
                "detection_rate": r.detection_rate,
                "mean_latency_ms": r.mean_latency_ms,
                "mean_files_damaged": r.mean_files_damaged,
                "mean_ops_prevented_pct": r.mean_ops_prevented_pct,
                "expected_outcome": r.expected_outcome,
                "empirical_status": r.empirical_status,
            }
            for r in rep.scenario_breakdown
        ])
        df_sb.to_csv(out_dir / "scenario_breakdown.csv", index=False)

    print(f"Successfully exported data to '{out_dir}':")
    print(f"  • {out_dir / 'events.csv'} ({len(events)} rows)")
    print(f"  • {out_dir / 'alerts.csv'} ({len(alerts)} rows)")
    print(f"  • {out_dir / 'trials.csv'} ({len(scenarios)} rows)")
    print(f"  • {out_dir / 'metrics_summary.csv'} (3 rows)")
    if rep.scenario_breakdown:
        print(f"  • {out_dir / 'scenario_breakdown.csv'} ({len(rep.scenario_breakdown)} rows)")


def cmd_dashboard(args):
    dashboard_path = Path(__file__).resolve().parent / "canary_sentinel" / "dashboard" / "app.py"
    port = args.port or 8501
    cmd = [sys.executable, "-m", "streamlit", "run", str(dashboard_path), "--server.port", str(port)]
    print(f"Launching Streamlit dashboard on port {port}...")
    subprocess.run(cmd)


def cmd_test(args):
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    print("Running automated test suite...")
    ret = subprocess.run(cmd)
    sys.exit(ret.returncode)


def main():
    parser = argparse.ArgumentParser(description="CanarySentinel Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # test
    subparsers.add_parser("test", help="Run automated pytest suite")

    # dashboard
    p_dash = subparsers.add_parser("dashboard", help="Start the Streamlit dashboard")
    p_dash.add_argument("--port", type=int, default=8501, help="Port to run Streamlit on")

    # benchmark
    p_bench = subparsers.add_parser("benchmark", help="Run comparative benchmark suite")
    p_bench.add_argument("--iterations", type=int, default=1, help="Number of benchmark iterations")

    # simulate
    p_sim = subparsers.add_parser("simulate", help="Run a single harmless scenario trial")
    p_sim.add_argument("--scenario", required=True, help="Scenario key")
    p_sim.add_argument("--detector", default="hybrid", choices=["baseline", "canary_only", "hybrid"], help="Detector configuration")

    # deploy-canaries
    subparsers.add_parser("deploy-canaries", help="Deploy decoy canary files in sandbox")

    # status
    subparsers.add_parser("status", help="Show system status and deployed canaries")

    # reset
    p_res = subparsers.add_parser("reset", help="Safe reset of sandbox and optionally database")
    p_res.add_argument("--all", action="store_true", help="Also wipe SQLite database records")

    # report
    p_rep = subparsers.add_parser("report", help="Generate research summary markdown report")
    p_rep.add_argument("--output", default="RESEARCH_SUMMARY.md", help="Output file path")

    # export
    p_exp = subparsers.add_parser("export", help="Export events, alerts, and trials to CSV")
    p_exp.add_argument("--output-dir", default="./exports", help="Output directory path")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "test": cmd_test,
        "dashboard": cmd_dashboard,
        "benchmark": cmd_benchmark,
        "simulate": cmd_simulate,
        "deploy-canaries": cmd_deploy_canaries,
        "status": cmd_status,
        "reset": cmd_reset,
        "report": cmd_report,
        "export": cmd_export,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
