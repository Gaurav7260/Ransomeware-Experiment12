"""Sandbox boundary enforcement and security validation for CanarySentinel."""

import os
import shutil
from pathlib import Path
from typing import List, Union


class SandboxSecurityError(Exception):
    """Raised when an operation attempts to breach or access outside the sandbox boundary."""
    pass


class SandboxManager:
    """Enforces strict sandbox filesystem isolation."""

    _SYSTEM_TREES_FORBIDDEN = [
        "/bin",
        "/sbin",
        "/etc",
        "/private/etc",
        "/System",
        "/Library",
    ]

    _EXACT_FORBIDDEN = [
        "/",
        "/usr",
        "/var",
        "/private",
        "/private/var",
        "/Users",
        str(Path.home()),
    ]

    def __init__(self, sandbox_dir: Union[str, Path] = "./sandbox"):
        self.raw_sandbox_dir = str(sandbox_dir)
        self.sandbox_path = Path(sandbox_dir).resolve()

        # Build resolved forbidden roots
        system_trees_resolved = set()
        for p in self._SYSTEM_TREES_FORBIDDEN:
            try:
                system_trees_resolved.add(Path(p).resolve())
            except Exception:
                system_trees_resolved.add(Path(p))

        exact_forbidden_resolved = set()
        for p in self._EXACT_FORBIDDEN:
            try:
                exact_forbidden_resolved.add(Path(p).resolve())
            except Exception:
                exact_forbidden_resolved.add(Path(p))

        # Guard: verify the sandbox path itself is not a sensitive system root or user home directory
        if self.sandbox_path in exact_forbidden_resolved or self.sandbox_path in system_trees_resolved:
            raise SandboxSecurityError(
                f"Refusing to use sensitive system or home directory as sandbox: {self.sandbox_path}"
            )

        for st in system_trees_resolved:
            if st != Path("/") and st in self.sandbox_path.parents:
                raise SandboxSecurityError(
                    f"Refusing to use sensitive system directory tree as sandbox: {self.sandbox_path}"
                )

        # Ensure sandbox is created
        self.sandbox_path.mkdir(parents=True, exist_ok=True)

    @property
    def sandbox_dir(self) -> str:
        """Return sandbox root path as string."""
        return str(self.sandbox_path)

    def validate_path(self, target_path: Union[str, Path], check_symlink: bool = True) -> Path:
        """Validate that a target path resolves strictly inside the sandbox boundary.

        Args:
            target_path: Path to validate (can be relative or absolute).
            check_symlink: If True, resolves symlink targets and ensures they remain in sandbox.

        Returns:
            Resolved Path object strictly inside sandbox.

        Raises:
            SandboxSecurityError: If the path attempts directory traversal or resolves outside sandbox.
        """
        if not target_path:
            raise SandboxSecurityError("Empty path is invalid")

        # Check for null bytes
        if "\0" in str(target_path):
            raise SandboxSecurityError("Path contains null byte injection attempt")

        path_obj = Path(target_path)

        # If relative, anchor to sandbox path
        if not path_obj.is_absolute():
            resolved = (self.sandbox_path / path_obj).resolve()
        else:
            resolved = path_obj.resolve()

        # Check containment via is_relative_to
        try:
            is_inside = resolved.is_relative_to(self.sandbox_path)
        except AttributeError:
            # Fallback for older python
            is_inside = (resolved == self.sandbox_path or self.sandbox_path in resolved.parents)

        if not is_inside:
            raise SandboxSecurityError(
                f"Security violation: path '{target_path}' resolves outside sandbox boundary '{self.sandbox_path}'"
            )

        # Check symlink target if path exists and is symlink
        if check_symlink and (os.path.islink(resolved) or (path_obj.is_symlink() if hasattr(path_obj, "is_symlink") else False)):
            real_target = Path(os.path.realpath(resolved))
            try:
                symlink_inside = real_target.is_relative_to(self.sandbox_path)
            except AttributeError:
                symlink_inside = (real_target == self.sandbox_path or self.sandbox_path in real_target.parents)

            if not symlink_inside:
                raise SandboxSecurityError(
                    f"Security violation: symlink '{target_path}' targets outside sandbox '{real_target}'"
                )

        return resolved

    def relative_to_sandbox(self, target_path: Union[str, Path]) -> str:
        """Return relative path string relative to sandbox directory."""
        validated = self.validate_path(target_path, check_symlink=False)
        try:
            return str(validated.relative_to(self.sandbox_path))
        except ValueError:
            return str(validated.name)

    def is_inside_sandbox(self, target_path: Union[str, Path]) -> bool:
        """Non-raising containment check."""
        try:
            self.validate_path(target_path)
            return True
        except SandboxSecurityError:
            return False

    def init_sandbox_structure(self, subdirectories: List[str]) -> None:
        """Initialize standard target directory subtrees inside sandbox."""
        self.sandbox_path.mkdir(parents=True, exist_ok=True)
        for subdir in subdirectories:
            if subdir:
                subdir_path = self.validate_path(subdir)
                subdir_path.mkdir(parents=True, exist_ok=True)

    def reset_sandbox(self) -> None:
        """Safely clear all files and subdirectories inside the sandbox without deleting the root."""
        if not self.sandbox_path.exists():
            self.sandbox_path.mkdir(parents=True, exist_ok=True)
            return

        for item in self.sandbox_path.iterdir():
            # Double check containment
            resolved_item = self.validate_path(item, check_symlink=False)
            if resolved_item.is_dir() and not resolved_item.is_symlink():
                shutil.rmtree(resolved_item, ignore_errors=True)
            else:
                try:
                    resolved_item.unlink(missing_ok=True)
                except OSError:
                    pass
