from pathlib import Path
from typing import Optional, List, Dict, Tuple

import typer

from .scanner import walk_project, detect_languages, read_file_text
from .detectors import detect_ai_phrases, detect_long_comment_blocks
from .refactors import run_formatters
from .report import build_markdown_report
from .config import load_config_from_path

app = typer.Typer(help="vibe-sweeper – clean up AI-ish / vibe-coded repositories.")


def _collect_findings(root: Path, cfg: Dict) -> Tuple[List[Path], List[Dict]]:
    files = walk_project(root)
    findings: List[Dict] = []
    for path in files:
        text = read_file_text(path)
        if not text:
            continue
        findings.extend(detect_ai_phrases(path, text, cfg.get("ai_phrases")))
        findings.extend(
            detect_long_comment_blocks(path, text, max_lines=cfg.get("max_comment_block_lines", 20))
        )
    return files, findings


@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to the project root."),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config YAML (vibe.yaml)."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Write report to this file path."),
):
    """Scan the repo and print a Markdown report."""
    root = Path(path)
    cfg_path = Path(config) if config else (root / "vibe.yaml")
    cfg = load_config_from_path(cfg_path if cfg_path.exists() else None)

    files, findings = _collect_findings(root, cfg)
    report = build_markdown_report(root, files, findings, formatter_results=None)

    if output:
        out_path = Path(output)
        out_path.write_text(report, encoding="utf-8")
        typer.echo(f"Report written to {out_path}")
    else:
        typer.echo(report)


@app.command()
def run(
    path: str = typer.Argument(".", help="Path to the project root."),
    apply: bool = typer.Option(False, "--apply", help="Apply external formatters where possible."),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config YAML (vibe.yaml)."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Write report to this file path."),
):
    """Scan the repo, optionally run formatters, and print a report."""
    root = Path(path)
    cfg_path = Path(config) if config else (root / "vibe.yaml")
    cfg = load_config_from_path(cfg_path if cfg_path.exists() else None)

    files, findings = _collect_findings(root, cfg)
    languages = detect_languages(files)
    formatter_results = None

    if apply:
        formatter_results = run_formatters(root, languages)

    report = build_markdown_report(root, files, findings, formatter_results=formatter_results)

    if output:
        out_path = Path(output)
        out_path.write_text(report, encoding="utf-8")
        typer.echo(f"Report written to {out_path}")
    else:
        typer.echo(report)


@app.command()
def check(
    path: str = typer.Argument(".", help="Path to the project root."),
    config: Optional[str] = typer.Option(None, "--config", "-c", help="Path to config YAML (vibe.yaml)."),
):
    """Check mode for CI – exits with non-zero status if issues are found."""
    root = Path(path)
    cfg_path = Path(config) if config else (root / "vibe.yaml")
    cfg = load_config_from_path(cfg_path if cfg_path.exists() else None)

    files, findings = _collect_findings(root, cfg)
    report = build_markdown_report(root, files, findings, formatter_results=None)
    typer.echo(report)

    if findings:
        raise typer.Exit(code=1)
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
