from pathlib import Path
from typing import List, Dict
from ..analysis.metrics import basic_stats


def build_markdown_report(root: Path, files, findings: List[Dict], formatter_results=None) -> str:
    stats = basic_stats(files, findings)
    root = root.resolve()

    lines = []
    lines.append("# vibe-sweeper report")
    lines.append("")
    lines.append(f"Root: `{root}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Files scanned: **{stats['file_count']}**")
    lines.append(f"- Issues detected: **{stats['issue_count']}**")
    lines.append("")

    if formatter_results:
        lines.append("## Formatters")
        lines.append("")
        for name, res in formatter_results.items():
            if not isinstance(res, dict):
                continue
            rc = res.get("returncode")
            lines.append(f"- **{name}**: return code `{rc}`")
        lines.append("")

    if not findings:
        lines.append("## Findings")
        lines.append("")
        lines.append("No issues detected. Looking clean. ✨")
        return "\n".join(lines)

    lines.append("## Findings")
    lines.append("")
    for f in findings:
        kind = f.get("kind", "issue")
        file = f.get("file", "?")
        if kind == "ai_phrase":
            lines.append(f"- `{file}`: line {f['line']} – AI phrase: `{f['phrase']}`")
        elif kind == "long_comment_block":
            lines.append(
                f"- `{file}`: lines {f['start_line']}-{f['end_line']} – long comment block ({f['lines']} lines)"
            )
        else:
            lines.append(f"- `{file}`: {kind}")

    return "\n".join(lines)
