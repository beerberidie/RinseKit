import os
from pathlib import Path
from typing import Dict, List

DEFAULT_IGNORES = {".git", ".hg", ".svn", ".idea", ".vscode", "__pycache__", "node_modules", "dist", "build"}

EXT_LANG_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".html": "html",
    ".css": "css",
    ".json": "json",
}


def walk_project(root: Path) -> List[Path]:
    files: List[Path] = []
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_IGNORES]
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix.lower() in EXT_LANG_MAP:
                files.append(path)
    return files


def detect_languages(files: List[Path]) -> Dict[str, List[Path]]:
    by_lang: Dict[str, List[Path]] = {}
    for p in files:
        lang = EXT_LANG_MAP.get(p.suffix.lower(), "unknown")
        by_lang.setdefault(lang, []).append(p)
    return by_lang


def read_file_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1")
        except Exception:
            return ""
