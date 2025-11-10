"""Tests for scanner module."""
import tempfile
from pathlib import Path
import pytest

from vibe_sweeper.scanner import (
    walk_project,
    detect_languages,
    read_file_text,
    EXT_LANG_MAP,
)


def test_walk_project_finds_python_files(tmp_path):
    """Test that walk_project finds Python files."""
    # Create test files
    (tmp_path / "test.py").write_text("print('hello')")
    (tmp_path / "test.js").write_text("console.log('hello')")
    (tmp_path / "test.txt").write_text("ignored")
    
    files = walk_project(tmp_path)
    
    assert len(files) == 2
    assert any(f.name == "test.py" for f in files)
    assert any(f.name == "test.js" for f in files)
    assert not any(f.name == "test.txt" for f in files)


def test_walk_project_ignores_common_dirs(tmp_path):
    """Test that walk_project ignores common directories."""
    # Create ignored directories
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "test.py").write_text("ignored")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "test.js").write_text("ignored")
    (tmp_path / "test.py").write_text("found")
    
    files = walk_project(tmp_path)
    
    assert len(files) == 1
    assert files[0].name == "test.py"


def test_detect_languages():
    """Test language detection from file extensions."""
    files = [
        Path("test.py"),
        Path("test.js"),
        Path("test.jsx"),
        Path("test.ts"),
        Path("test.tsx"),
        Path("test.html"),
        Path("test.css"),
        Path("test.json"),
    ]
    
    by_lang = detect_languages(files)
    
    assert "python" in by_lang
    assert len(by_lang["python"]) == 1
    assert "javascript" in by_lang
    assert len(by_lang["javascript"]) == 2  # .js and .jsx
    assert "typescript" in by_lang
    assert len(by_lang["typescript"]) == 2  # .ts and .tsx
    assert "html" in by_lang
    assert "css" in by_lang
    assert "json" in by_lang


def test_read_file_text_utf8(tmp_path):
    """Test reading UTF-8 encoded files."""
    test_file = tmp_path / "test.py"
    content = "# Hello 世界\nprint('test')"
    test_file.write_text(content, encoding="utf-8")
    
    result = read_file_text(test_file)
    
    assert result == content


def test_read_file_text_handles_decode_errors(tmp_path):
    """Test that read_file_text handles decode errors gracefully."""
    test_file = tmp_path / "test.py"
    # Write binary data that's not valid UTF-8
    test_file.write_bytes(b"\xff\xfe\xfd")
    
    result = read_file_text(test_file)
    
    # Should return something (latin-1 fallback) or empty string
    assert isinstance(result, str)


def test_ext_lang_map_coverage():
    """Test that EXT_LANG_MAP has expected extensions."""
    expected_extensions = [".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".json"]
    
    for ext in expected_extensions:
        assert ext in EXT_LANG_MAP
    
    assert EXT_LANG_MAP[".py"] == "python"
    assert EXT_LANG_MAP[".js"] == "javascript"
    assert EXT_LANG_MAP[".ts"] == "typescript"

