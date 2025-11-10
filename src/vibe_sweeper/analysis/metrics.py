from typing import List, Dict
from pathlib import Path


def basic_stats(files: List[Path], findings: List[Dict]) -> Dict[str, int]:
    return {
        "file_count": len(files),
        "issue_count": len(findings),
    }
