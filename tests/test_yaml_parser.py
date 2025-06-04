"""
Unit tests for YAML Parser module.

This module contains comprehensive tests for the YAMLParser class,
including functionality tests, error handling, and edge cases.
"""

import pytest
from pathlib import Path
import tempfile
import sys

sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.parsers.yaml_parser import YAMLParser


class TestYAMLParser:
    """Test class for YAML Parser functionality."""
    
    def setup_method(self) -> None:
        """Setup test environment before each test."""
        self.test_data = {
            "name": "Test Data",
            "version": "1.0.0",
            "numbers": [1, 2, 3, 4, 5],
            "settings": {
                "enabled": True,
                "config": "default"
            }
        }
        
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_file = self.temp_dir / "test.yaml"
        self.output_file = self.temp_dir / "output.yaml"
    
    def teardown_method(self) -> None:
        """Cleanup test environment after each test."""
        for file in self.temp_dir.glob("*"):
            file.unlink()
        self.temp_dir.rmdir()
    
    def test_save_and_load_yaml(self) -> None:
        """Test basic save and load functionality."""
        YAMLParser.save(self.test_data, self.test_file)
        
        assert self.test_file.exists()
        
        loaded_data = YAMLParser.load(self.test_file)
        
        assert loaded_data == self.test_data
        assert loaded_data["name"] == "Test Data"
        assert loaded_data["numbers"] == [1, 2, 3, 4, 5]
        assert loaded_data["settings"]["enabled"] is True
    
    def test_load_nonexistent_file(self) -> None:
        """Test loading a file that doesn't exist."""
        nonexistent_file = self.temp_dir / "nonexistent.yaml"
        
        with pytest.raises(FileNotFoundError):
            YAMLParser.load(nonexistent_file)
    
    def test_load_invalid_yaml(self) -> None:
        """Test loading a file with invalid YAML."""
        invalid_yaml_file = self.temp_dir / "invalid.yaml"
        with open(invalid_yaml_file, 'w') as f:
            f.write('invalid: yaml: content: [missing bracket')
        
        with pytest.raises(ValueError):
            YAMLParser.load(invalid_yaml_file)
    
    def test_validate_valid_yaml(self) -> None:
        """Test validation of valid YAML file."""
        YAMLParser.save(self.test_data, self.test_file)
        
        assert YAMLParser.validate(self.test_file) is True
    
    def test_validate_invalid_yaml(self) -> None:
        """Test validation of invalid YAML file."""
        invalid_file = self.temp_dir / "invalid.yaml"
        with open(invalid_file, 'w') as f:
            f.write('invalid: yaml: content: [')
        
        assert YAMLParser.validate(invalid_file) is False
    
    def test_validate_nonexistent_file(self) -> None:
        """Test validation of nonexistent file."""
        nonexistent_file = self.temp_dir / "nonexistent.yaml"
        assert YAMLParser.validate(nonexistent_file) is False
    
    def test_get_file_info_valid(self) -> None:
        """Test getting file information for valid YAML."""
        YAMLParser.save(self.test_data, self.test_file)
        
        info = YAMLParser.get_file_info(self.test_file)
        
        assert info["format"] == "YAML"
        assert info["valid"] is True
        assert info["keys_count"] == 4
        assert info["encoding"] == "utf-8"
        assert info["size_bytes"] > 0
    
    def test_get_file_info_invalid(self) -> None:
        """Test getting file information for invalid YAML."""
        invalid_file = self.temp_dir / "invalid.yaml"
        with open(invalid_file, 'w') as f:
            f.write('invalid: yaml: [')
        
        info = YAMLParser.get_file_info(invalid_file)
        
        assert info["format"] == "YAML"
        assert info["valid"] is False
        assert "error" in info
        assert info["size_bytes"] > 0
    
    def test_load_non_dict_yaml(self) -> None:
        """Test loading YAML that is not a dictionary (array, string, etc.)."""
        array_data = [1, 2, 3, 4, 5]
        YAMLParser.save(array_data, self.test_file)
        
        loaded_data = YAMLParser.load(self.test_file)
        assert isinstance(loaded_data, dict)
        assert loaded_data["data"] == array_data
        
        string_data = "hello world"
        YAMLParser.save(string_data, self.test_file)
        
        loaded_data = YAMLParser.load(self.test_file)
        assert isinstance(loaded_data, dict)
        assert loaded_data["data"] == string_data
    
    def test_utf8_encoding(self) -> None:
        """Test handling of UTF-8 characters."""
        utf8_data = {
            "polish": "żółć",
            "chinese": "你好",
            "emoji": "🚀",
            "special": "àáâãäå"
        }
        
        YAMLParser.save(utf8_data, self.test_file)
        loaded_data = YAMLParser.load(self.test_file)
        
        assert loaded_data == utf8_data
        assert loaded_data["polish"] == "żółć"
        assert loaded_data["chinese"] == "你好"
        assert loaded_data["emoji"] == "🚀"
    
    def test_yaml_specific_features(self) -> None:
        """Test YAML-specific features like multiline strings."""
        yaml_specific_data = {
            "multiline": "This is a\nmultiline string\nwith line breaks",
            "null_value": None,
            "boolean_values": [True, False],
            "quoted_string": "123",  # Should remain as string
            "unquoted_number": 123   # Should remain as number
        }
        
        YAMLParser.save(yaml_specific_data, self.test_file)
        loaded_data = YAMLParser.load(self.test_file)
        
        assert loaded_data == yaml_specific_data
        assert "line breaks" in loaded_data["multiline"]
        assert loaded_data["null_value"] is None
        assert isinstance(loaded_data["quoted_string"], str)
        assert isinstance(loaded_data["unquoted_number"], int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
