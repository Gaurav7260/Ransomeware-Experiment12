"""Canary decoy file manager."""

import uuid
from pathlib import Path
from typing import Dict, List, Optional, Set

from canary_sentinel.core.config import CanaryConfig
from canary_sentinel.core.sandbox import SandboxManager
from canary_sentinel.core.utils import (
    calculate_file_hash,
    get_iso_timestamp,
)
from canary_sentinel.storage.db import Database
from canary_sentinel.storage.models import CanaryRecord


class CanaryManager:
    """Manages deployment, tracking, and integrity validation of canary decoy files."""

    DECOY_TEMPLATES = [
        ("!00_corporate_passwords.xlsx", "User Credentials and Enterprise System Access Tokens"),
        ("!00_master_financials_2026.pdf", "CONFIDENTIAL: Annual Financial Statement & Profit Margins"),
        ("aaa_employee_salaries.csv", "Employee Name, Role, SSN, Base Salary, Bonus"),
        ("0_database_backup_production.sql", "CREATE TABLE users (id INT, password_hash VARCHAR(255));"),
        ("!aa_cryptocurrency_cold_wallet.txt", "Seed Phrase: confidential canary recovery phrase test"),
        ("_urgent_merger_acquisition_terms.docx", "Project Titan: Acquisition Framework & Valuation"),
        ("00_client_contracts_signed.pdf", "CLIENT AGREEMENT: Master Services Agreement for Client"),
        ("aaa_api_secret_keys.env", "AWS_SECRET_ACCESS_KEY=CANARY_KEY_DO_NOT_TAMPER_019283"),
    ]

    def __init__(
        self,
        sandbox: SandboxManager,
        db: Database,
        config: Optional[CanaryConfig] = None,
    ):
        self.sandbox = sandbox
        self.db = db
        self.config = config or CanaryConfig()
        # In-memory lookup sets for ultra-fast check in event normalizer/detectors
        self._canary_paths: Set[str] = set()
        self._canary_records: Dict[str, CanaryRecord] = {}
        self._load_from_db()

    def _load_from_db(self) -> None:
        """Load currently registered canaries from database."""
        records = self.db.get_canaries()
        self._canary_paths.clear()
        self._canary_records.clear()
        for r in records:
            norm_path = Path(r.relative_path).as_posix()
            self._canary_paths.add(norm_path)
            self._canary_records[norm_path] = r

    def is_canary(self, relative_path: str) -> bool:
        """Check if a relative path is a registered canary decoy."""
        norm_path = Path(relative_path).as_posix()
        return norm_path in self._canary_paths

    @property
    def canary_paths(self) -> List[str]:
        """Return sorted list of registered relative canary paths."""
        return sorted(list(self._canary_paths))

    def get_canary_paths(self) -> List[str]:
        """Return sorted list of registered relative canary paths."""
        return sorted(list(self._canary_paths))

    def get_canary(self, relative_path: str) -> Optional[CanaryRecord]:
        """Get canary record by relative path."""
        norm_path = Path(relative_path).as_posix()
        return self._canary_records.get(norm_path)

    def deploy_canaries(self) -> List[CanaryRecord]:
        """Deploy decoy canary files across configured sandbox subdirectories."""
        deployed = []
        target_dirs = self.config.target_directories
        self.sandbox.init_sandbox_structure(target_dirs)

        count = 0
        max_decoys = min(len(self.DECOY_TEMPLATES), self.config.decoy_count)

        for i in range(max_decoys):
            filename, content_seed = self.DECOY_TEMPLATES[i]
            target_dir = target_dirs[i % len(target_dirs)]

            rel_target = Path(target_dir) / filename if target_dir else Path(filename)
            abs_target = self.sandbox.validate_path(rel_target)

            # Generate synthetic decoy content
            content = (
                f"--- CANARY SENTINEL DECOY IDENTIFIER ---\n"
                f"CANARY_ID: {uuid.uuid4()}\n"
                f"HEADER: {content_seed}\n"
                f"SECURITY_NOTICE: This is an active decoy trap for CanarySentinel detection.\n"
                f"TIMESTAMP: {get_iso_timestamp()}\n"
                f"INTEGRITY_SALT: 9f8a3c4e2b1d0e5f7a8b9c0d1e2f3a4b\n"
                f"PAYLOAD: {content_seed * 4}\n"
            )

            # Write file safely inside sandbox
            abs_target.parent.mkdir(parents=True, exist_ok=True)
            with open(abs_target, "w", encoding="utf-8") as f:
                f.write(content)

            file_size = abs_target.stat().st_size
            file_hash = calculate_file_hash(abs_target)
            rel_str = self.sandbox.relative_to_sandbox(abs_target)
            norm_rel = Path(rel_str).as_posix()

            record = CanaryRecord(
                canary_id=str(uuid.uuid4()),
                relative_path=norm_rel,
                filename=filename,
                file_hash=file_hash,
                file_size=file_size,
                created_at=get_iso_timestamp(),
                status="ACTIVE",
            )

            self.db.save_canary(record)
            self._canary_paths.add(norm_rel)
            self._canary_records[norm_rel] = record
            deployed.append(record)
            count += 1

        return deployed

    def verify_integrity(self) -> Dict[str, str]:
        """Check the status of all registered canaries on disk.

        Returns:
            Dict mapping relative_path -> status ("ACTIVE", "MODIFIED", "DELETED")
        """
        results = {}
        for rel_path, record in list(self._canary_records.items()):
            try:
                abs_path = self.sandbox.validate_path(rel_path)
            except Exception:
                results[rel_path] = "DELETED"
                continue

            if not abs_path.exists():
                status = "DELETED"
            else:
                curr_hash = calculate_file_hash(abs_path)
                if curr_hash != record.file_hash:
                    status = "MODIFIED"
                else:
                    status = "ACTIVE"

            results[rel_path] = status
            if status != record.status:
                record.status = status
                self.db.update_canary_status(record.canary_id, status)

        return results

    def clear_canaries(self) -> None:
        """Remove all canary files from disk and database."""
        for rel_path in self._canary_paths:
            try:
                abs_path = self.sandbox.validate_path(rel_path)
                if abs_path.exists():
                    abs_path.unlink()
            except Exception:
                pass

        self._canary_paths.clear()
        self._canary_records.clear()
        self.db.clear_canaries()

