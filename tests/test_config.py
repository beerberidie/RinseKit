"""Tests for configuration module."""
from pathlib import Path
import pytest
import yaml

from vibe_sweeper.config import load_default_config, load_config_from_path


def test_load_default_config():
    """Test loading default configuration."""
    config = load_default_config()
    
    assert "ai_phrases" in config
    assert isinstance(config["ai_phrases"], list)
    assert len(config["ai_phrases"]) > 0
    assert "max_comment_block_lines" in config
    assert isinstance(config["max_comment_block_lines"], int)


def test_load_default_config_has_expected_phrases():
    """Test that default config has expected AI phrases."""
    config = load_default_config()
    
    expected_phrases = [
        "as an ai language model",
        "in this code snippet",
        "this function is responsible for",
    ]
    
    for phrase in expected_phrases:
        assert phrase in config["ai_phrases"]


def test_load_config_from_path_nonexistent():
    """Test loading config when file doesn't exist."""
    config = load_config_from_path(None)
    
    # Should return default config
    assert "ai_phrases" in config
    assert "max_comment_block_lines" in config


def test_load_config_from_path_custom(tmp_path):
    """Test loading custom configuration."""
    custom_config = {
        "ai_phrases": ["custom phrase 1", "custom phrase 2"],
        "max_comment_block_lines": 15,
    }
    
    config_file = tmp_path / "custom.yaml"
    config_file.write_text(yaml.dump(custom_config))
    
    config = load_config_from_path(config_file)
    
    assert "custom phrase 1" in config["ai_phrases"]
    assert "custom phrase 2" in config["ai_phrases"]
    assert config["max_comment_block_lines"] == 15


def test_load_config_from_path_merges_with_defaults(tmp_path):
    """Test that custom config merges with defaults."""
    custom_config = {
        "max_comment_block_lines": 15,
    }
    
    config_file = tmp_path / "custom.yaml"
    config_file.write_text(yaml.dump(custom_config))
    
    config = load_config_from_path(config_file)
    
    # Should have custom value
    assert config["max_comment_block_lines"] == 15
    # Should still have default ai_phrases
    assert "ai_phrases" in config
    assert len(config["ai_phrases"]) > 0


def test_load_config_from_path_empty_file(tmp_path):
    """Test loading config from empty file."""
    config_file = tmp_path / "empty.yaml"
    config_file.write_text("")
    
    config = load_config_from_path(config_file)
    
    # Should return default config
    assert "ai_phrases" in config
    assert "max_comment_block_lines" in config

