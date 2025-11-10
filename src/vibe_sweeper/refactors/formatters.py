import subprocess
from pathlib import Path
from typing import Dict, Any, List


def _run_cmd(cmd: List[str], cwd: Path) -> Dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        }
    except FileNotFoundError:
        return {
            "cmd": cmd,
            "returncode": -1,
            "stdout": "",
            "stderr": "command not found",
        }


def run_formatters(root: Path, languages: Dict[str, Any]) -> Dict[str, Any]:
    """Run external formatters where possible. Best-effort only."""
    results: Dict[str, Any] = {}
    root = root.resolve()

    if "python" in languages:
        results["ruff"] = _run_cmd(["ruff", "check", ".", "--fix"], cwd=root)

    if any(lang in languages for lang in ("javascript", "typescript", "html", "css", "json")):
        results["biome"] = _run_cmd(["biome", "check", ".", "--apply"], cwd=root)

    return results
