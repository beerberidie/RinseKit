from pathlib import Path
from typing import List, Dict

COMMENT_PREFIXES = ("#", "//", "/*", "*")


def detect_long_comment_blocks(path: Path, text: str, max_lines: int = 20) -> List[Dict]:
    lines = text.splitlines()
    blocks = []
    current_block = []
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(COMMENT_PREFIXES):
            current_block.append((idx, line))
        else:
            if current_block:
                blocks.append(current_block)
                current_block = []
    if current_block:
        blocks.append(current_block)

    results: List[Dict] = []
    for block in blocks:
        if len(block) > max_lines:
            start_line = block[0][0]
            end_line = block[-1][0]
            preview = "\n".join(l for _, l in block[:5])
            results.append(
                {
                    "file": str(path),
                    "start_line": start_line,
                    "end_line": end_line,
                    "lines": len(block),
                    "preview": preview,
                    "kind": "long_comment_block",
                }
            )
    return results
