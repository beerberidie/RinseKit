"""Tests for detector modules."""
from pathlib import Path
import pytest

from vibe_sweeper.detectors import detect_ai_phrases, detect_long_comment_blocks


class TestAIPhraseDetector:
    """Tests for AI phrase detection."""
    
    def test_detect_ai_phrases_finds_matches(self):
        """Test that AI phrases are detected."""
        text = """
# As an AI language model, I can help you
def hello():
    # In this code snippet, we will demonstrate
    print("hello")
"""
        path = Path("test.py")
        
        results = detect_ai_phrases(path, text)
        
        assert len(results) == 2
        assert any(r["phrase"] == "as an ai language model" for r in results)
        assert any(r["phrase"] == "in this code snippet" for r in results)
    
    def test_detect_ai_phrases_case_insensitive(self):
        """Test that detection is case-insensitive."""
        text = "AS AN AI LANGUAGE MODEL, I can help"
        path = Path("test.py")
        
        results = detect_ai_phrases(path, text)
        
        assert len(results) == 1
        assert results[0]["phrase"] == "as an ai language model"
    
    def test_detect_ai_phrases_no_matches(self):
        """Test when no AI phrases are found."""
        text = "def hello():\n    print('hello world')"
        path = Path("test.py")
        
        results = detect_ai_phrases(path, text)
        
        assert len(results) == 0
    
    def test_detect_ai_phrases_custom_phrases(self):
        """Test with custom phrase list."""
        text = "This is a custom phrase to detect"
        path = Path("test.py")
        custom_phrases = ["custom phrase"]
        
        results = detect_ai_phrases(path, text, phrases=custom_phrases)
        
        assert len(results) == 1
        assert results[0]["phrase"] == "custom phrase"
    
    def test_detect_ai_phrases_includes_line_number(self):
        """Test that results include correct line numbers."""
        text = "line 1\nAs an AI language model\nline 3"
        path = Path("test.py")
        
        results = detect_ai_phrases(path, text)
        
        assert len(results) == 1
        assert results[0]["line"] == 2
    
    def test_detect_ai_phrases_result_structure(self):
        """Test that results have correct structure."""
        text = "As an AI language model"
        path = Path("test.py")
        
        results = detect_ai_phrases(path, text)
        
        assert len(results) == 1
        result = results[0]
        assert "file" in result
        assert "line" in result
        assert "phrase" in result
        assert "kind" in result
        assert result["kind"] == "ai_phrase"


class TestLongCommentBlockDetector:
    """Tests for long comment block detection."""
    
    def test_detect_long_comment_blocks_python(self):
        """Test detection of long Python comment blocks."""
        lines = ["# comment"] * 25
        text = "\n".join(lines)
        path = Path("test.py")
        
        results = detect_long_comment_blocks(path, text, max_lines=20)
        
        assert len(results) == 1
        assert results[0]["lines"] == 25
        assert results[0]["start_line"] == 1
        assert results[0]["end_line"] == 25
    
    def test_detect_long_comment_blocks_javascript(self):
        """Test detection of long JavaScript comment blocks."""
        lines = ["// comment"] * 25
        text = "\n".join(lines)
        path = Path("test.js")
        
        results = detect_long_comment_blocks(path, text, max_lines=20)
        
        assert len(results) == 1
        assert results[0]["lines"] == 25
    
    def test_detect_long_comment_blocks_below_threshold(self):
        """Test that short comment blocks are not detected."""
        lines = ["# comment"] * 15
        text = "\n".join(lines)
        path = Path("test.py")
        
        results = detect_long_comment_blocks(path, text, max_lines=20)
        
        assert len(results) == 0
    
    def test_detect_long_comment_blocks_separated_blocks(self):
        """Test that separated comment blocks are counted separately."""
        text = """
# comment block 1
# comment block 1
# comment block 1

def foo():
    pass

# comment block 2
# comment block 2
# comment block 2
"""
        path = Path("test.py")
        
        results = detect_long_comment_blocks(path, text, max_lines=2)
        
        assert len(results) == 2
    
    def test_detect_long_comment_blocks_result_structure(self):
        """Test that results have correct structure."""
        lines = ["# comment"] * 25
        text = "\n".join(lines)
        path = Path("test.py")
        
        results = detect_long_comment_blocks(path, text, max_lines=20)
        
        assert len(results) == 1
        result = results[0]
        assert "file" in result
        assert "start_line" in result
        assert "end_line" in result
        assert "lines" in result
        assert "preview" in result
        assert "kind" in result
        assert result["kind"] == "long_comment_block"
    
    def test_detect_long_comment_blocks_preview(self):
        """Test that preview includes first 5 lines."""
        lines = ["# comment line {}".format(i) for i in range(1, 26)]
        text = "\n".join(lines)
        path = Path("test.py")
        
        results = detect_long_comment_blocks(path, text, max_lines=20)
        
        assert len(results) == 1
        preview = results[0]["preview"]
        assert "# comment line 1" in preview
        assert "# comment line 5" in preview
        # Should not include line 6 or beyond
        assert "# comment line 6" not in preview

