"""Utility functions for hashing, entropy calculation, and formatting."""

import datetime
import hashlib
import math
from pathlib import Path
from typing import Optional, Union


def get_iso_timestamp(epoch_time: Optional[float] = None) -> str:
    """Return an ISO 8601 formatted timestamp string."""
    if epoch_time is not None:
        dt = datetime.datetime.fromtimestamp(epoch_time, tz=datetime.timezone.utc)
    else:
        dt = datetime.datetime.now(datetime.timezone.utc)
    return dt.isoformat()


def calculate_entropy(data: bytes) -> float:
    """Calculate the Shannon entropy of a byte sequence (0.0 to 8.0 bits per byte).

    Low entropy (< 4.5): repetitive text, zero-padded data.
    Medium entropy (4.5 - 6.5): standard structured text, code, documents.
    High entropy (> 7.2): compressed or encrypted data.
    """
    if not data:
        return 0.0

    length = len(data)
    byte_counts = [0] * 256
    for b in data:
        byte_counts[b] += 1

    entropy = 0.0
    for count in byte_counts:
        if count > 0:
            p_i = count / length
            entropy -= p_i * math.log2(p_i)

    return round(entropy, 4)


def calculate_file_entropy(file_path: Union[str, Path], max_bytes: int = 65536) -> float:
    """Read up to max_bytes from file and compute Shannon entropy."""
    path = Path(file_path)
    if not path.is_file() or not path.exists():
        return 0.0

    try:
        with open(path, "rb") as f:
            chunk = f.read(max_bytes)
            return calculate_entropy(chunk)
    except (OSError, PermissionError):
        return 0.0


def calculate_file_hash(file_path: Union[str, Path]) -> str:
    """Compute SHA-256 hash of a file."""
    path = Path(file_path)
    if not path.is_file() or not path.exists():
        return ""

    hasher = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (OSError, PermissionError):
        return ""


def format_bytes(num_bytes: int) -> str:
    """Format byte count to human-readable string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} TB"

