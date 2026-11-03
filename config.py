"""Configuration manager for CanarySentinel."""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SystemConfig:
    app_name: str = "CanarySentinel"
    version: str = "1.0.0"
    sandbox_dir: str = "./sandbox"
    db_path: str = "./canary_sentinel.db"
    log_level: str = "INFO"


@dataclass
class CanaryConfig:
    decoy_count: int = 8
    target_directories: List[str] = field(
        default_factory=lambda: ["", "documents", "finance", "projects", "backups"]
    )
    file_extensions: List[str] = field(
        default_factory=lambda: [".docx", ".xlsx", ".pdf", ".sql", ".csv", ".txt"]
    )
    naming_prefixes: List[str] = field(
        default_factory=lambda: ["!00_", "!aa_", "aaa_", "_urgent_", "0_confidential_"]
    )


@dataclass
class MonitoringConfig:
    debounce_ms: int = 50
    ignore_patterns: List[str] = field(
        default_factory=lambda: ["*.tmp", "*.swp", ".DS_Store", "*~"]
    )


@dataclass
class BaselineConfig:
    burst_window_seconds: float = 2.0
    burst_count_threshold: int = 6
    entropy_threshold: float = 7.0
    mass_rename_threshold: int = 4
    base_risk_score: int = 65


@dataclass
class CanaryOnlyConfig:
    monitored_events: List[str] = field(
        default_factory=lambda: ["MODIFY", "DELETE", "MOVE"]
    )
    base_risk_score: int = 85


@dataclass
class HybridConfig:
    observation_window_seconds: float = 3.0
    min_context_events: int = 2
    burst_velocity_threshold: float = 3.0
    entropy_threshold: float = 6.8
    base_risk_score: int = 95


@dataclass
class DetectionConfig:
    baseline: BaselineConfig = field(default_factory=BaselineConfig)
    canary_only: CanaryOnlyConfig = field(default_factory=CanaryOnlyConfig)
    hybrid: HybridConfig = field(default_factory=HybridConfig)


@dataclass
class ResponseConfig:
    auto_block: bool = True
    minimum_severity: str = "HIGH"
    risk_score_threshold: int = 70


@dataclass
class SentinelConfig:
    system: SystemConfig = field(default_factory=SystemConfig)
    canary: CanaryConfig = field(default_factory=CanaryConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    detection: DetectionConfig = field(default_factory=DetectionConfig)
    response: ResponseConfig = field(default_factory=ResponseConfig)

    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "SentinelConfig":
        """Load configuration from a JSON file or use defaults."""
        path = Path(config_path) if config_path else Path("config.json")
        if not path.exists():
            return cls()

        try:
            with open(path, "r", encoding="utf-8") as f:
                data: Dict[str, Any] = json.load(f)

            system_data = data.get("system", {})
            canary_data = data.get("canary", {})
            monitoring_data = data.get("monitoring", {})
            detection_data = data.get("detection", {})
            response_data = data.get("response", {})

            baseline_data = detection_data.get("baseline", {})
            canary_only_data = detection_data.get("canary_only", {})
            hybrid_data = detection_data.get("hybrid", {})

            return cls(
                system=SystemConfig(**system_data),
                canary=CanaryConfig(**canary_data),
                monitoring=MonitoringConfig(**monitoring_data),
                detection=DetectionConfig(
                    baseline=BaselineConfig(**baseline_data),
                    canary_only=CanaryOnlyConfig(**canary_only_data),
                    hybrid=HybridConfig(**hybrid_data),
                ),
                response=ResponseConfig(**response_data),
            )
        except Exception:
            return cls()

