"""Tests for report generation."""
from pathlib import Path
import pytest

from vibe_sweeper.report import build_markdown_report


def test_build_markdown_report_no_findings(tmp_path):
    """Test report generation with no findings."""
    files = [Path("test1.py"), Path("test2.py")]
    findings = []
    
    report = build_markdown_report(tmp_path, files, findings)
    
    assert "# vibe-sweeper report" in report
    assert "Files scanned: **2**" in report
    assert "Issues detected: **0**" in report
    assert "No issues detected. Looking clean. ✨" in report


def test_build_markdown_report_with_ai_phrases(tmp_path):
    """Test report generation with AI phrase findings."""
    files = [Path("test.py")]
    findings = [
        {
            "file": "test.py",
            "line": 5,
            "phrase": "as an ai language model",
            "kind": "ai_phrase",
        },
        {
            "file": "test.py",
            "line": 10,
            "phrase": "in this code snippet",
            "kind": "ai_phrase",
        },
    ]
    
    report = build_markdown_report(tmp_path, files, findings)
    
    assert "Files scanned: **1**" in report
    assert "Issues detected: **2**" in report
    assert "as an ai language model" in report
    assert "in this code snippet" in report
    assert "line 5" in report
    assert "line 10" in report


def test_build_markdown_report_with_long_comments(tmp_path):
    """Test report generation with long comment block findings."""
    files = [Path("test.py")]
    findings = [
        {
            "file": "test.py",
            "start_line": 1,
            "end_line": 25,
            "lines": 25,
            "preview": "# comment preview",
            "kind": "long_comment_block",
        },
    ]
    
    report = build_markdown_report(tmp_path, files, findings)
    
    assert "Files scanned: **1**" in report
    assert "Issues detected: **1**" in report
    assert "long comment block" in report
    assert "lines 1-25" in report
    assert "(25 lines)" in report


def test_build_markdown_report_with_formatters(tmp_path):
    """Test report generation with formatter results."""
    files = [Path("test.py")]
    findings = []
    formatter_results = {
        "ruff": {"returncode": 0, "stdout": "", "stderr": ""},
        "biome": {"returncode": -1, "stdout": "", "stderr": "command not found"},
    }
    
    report = build_markdown_report(tmp_path, files, findings, formatter_results)
    
    assert "## Formatters" in report
    assert "ruff" in report
    assert "return code `0`" in report
    assert "biome" in report
    assert "return code `-1`" in report


def test_build_markdown_report_includes_root_path(tmp_path):
    """Test that report includes root path."""
    files = []
    findings = []
    
    report = build_markdown_report(tmp_path, files, findings)
    
    assert f"Root: `{tmp_path.resolve()}`" in report


def test_build_markdown_report_mixed_findings(tmp_path):
    """Test report with both AI phrases and long comments."""
    files = [Path("test.py")]
    findings = [
        {
            "file": "test.py",
            "line": 5,
            "phrase": "as an ai language model",
            "kind": "ai_phrase",
        },
        {
            "file": "test.py",
            "start_line": 10,
            "end_line": 35,
            "lines": 26,
            "preview": "# comment",
            "kind": "long_comment_block",
        },
    ]
    
    report = build_markdown_report(tmp_path, files, findings)
    
    assert "Issues detected: **2**" in report
    assert "AI phrase" in report
    assert "long comment block" in report

