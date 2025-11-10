"""Tests for CLI commands."""
from pathlib import Path
import pytest
from typer.testing import CliRunner

from vibe_sweeper.cli import app


runner = CliRunner()


def test_scan_command_help():
    """Test that scan command shows help."""
    result = runner.invoke(app, ["scan", "--help"])
    
    assert result.exit_code == 0
    assert "Scan the repo and print a Markdown report" in result.stdout


def test_run_command_help():
    """Test that run command shows help."""
    result = runner.invoke(app, ["run", "--help"])
    
    assert result.exit_code == 0
    assert "Scan the repo, optionally run formatters" in result.stdout


def test_check_command_help():
    """Test that check command shows help."""
    result = runner.invoke(app, ["check", "--help"])
    
    assert result.exit_code == 0
    assert "Check mode for CI" in result.stdout


def test_scan_command_on_clean_project(tmp_path):
    """Test scan command on a clean project."""
    # Create a simple clean Python file
    test_file = tmp_path / "clean.py"
    test_file.write_text("def hello():\n    print('hello world')\n")
    
    result = runner.invoke(app, ["scan", str(tmp_path)])
    
    assert result.exit_code == 0
    assert "vibe-sweeper report" in result.stdout
    assert "Files scanned: **1**" in result.stdout
    assert "Issues detected: **0**" in result.stdout


def test_scan_command_detects_ai_phrases(tmp_path):
    """Test scan command detects AI phrases."""
    test_file = tmp_path / "ai_code.py"
    test_file.write_text("# As an AI language model, I can help\ndef hello():\n    pass\n")
    
    result = runner.invoke(app, ["scan", str(tmp_path)])
    
    assert result.exit_code == 0
    assert "Issues detected: **1**" in result.stdout
    assert "as an ai language model" in result.stdout


def test_scan_command_with_output_file(tmp_path):
    """Test scan command with output file."""
    test_file = tmp_path / "test.py"
    test_file.write_text("def hello():\n    pass\n")
    output_file = tmp_path / "report.md"
    
    result = runner.invoke(app, ["scan", str(tmp_path), "--output", str(output_file)])
    
    assert result.exit_code == 0
    assert output_file.exists()
    content = output_file.read_text()
    assert "vibe-sweeper report" in content


def test_check_command_exits_zero_on_clean(tmp_path):
    """Test check command exits 0 on clean project."""
    test_file = tmp_path / "clean.py"
    test_file.write_text("def hello():\n    print('hello')\n")
    
    result = runner.invoke(app, ["check", str(tmp_path)])
    
    assert result.exit_code == 0


def test_check_command_exits_one_on_issues(tmp_path):
    """Test check command exits 1 when issues found."""
    test_file = tmp_path / "ai_code.py"
    test_file.write_text("# As an AI language model\ndef hello():\n    pass\n")
    
    result = runner.invoke(app, ["check", str(tmp_path)])
    
    assert result.exit_code == 1
    assert "Issues detected: **1**" in result.stdout


def test_run_command_without_apply(tmp_path):
    """Test run command without --apply flag."""
    test_file = tmp_path / "test.py"
    test_file.write_text("def hello():\n    pass\n")
    
    result = runner.invoke(app, ["run", str(tmp_path)])
    
    assert result.exit_code == 0
    assert "vibe-sweeper report" in result.stdout
    # Should not have formatters section without --apply
    assert "## Formatters" not in result.stdout


def test_run_command_with_apply(tmp_path):
    """Test run command with --apply flag."""
    test_file = tmp_path / "test.py"
    test_file.write_text("def hello():\n    pass\n")
    
    result = runner.invoke(app, ["run", str(tmp_path), "--apply"])
    
    assert result.exit_code == 0
    # Should have formatters section with --apply
    assert "## Formatters" in result.stdout


def test_scan_command_with_custom_config(tmp_path):
    """Test scan command with custom config file."""
    test_file = tmp_path / "test.py"
    test_file.write_text("# Custom phrase to detect\ndef hello():\n    pass\n")
    
    config_file = tmp_path / "custom.yaml"
    config_file.write_text("ai_phrases:\n  - 'custom phrase'\nmax_comment_block_lines: 10\n")
    
    result = runner.invoke(app, ["scan", str(tmp_path), "--config", str(config_file)])
    
    assert result.exit_code == 0
    assert "Issues detected: **1**" in result.stdout
    assert "custom phrase" in result.stdout

