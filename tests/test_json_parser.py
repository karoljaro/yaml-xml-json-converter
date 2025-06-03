"""
Unit tests for JSON Parser module.

This module contains comprehensive tests for the JSONParser class,
including functionality tests, error handling, and edge cases.
"""

import pytest
from pathlib import Path
import tempfile
import sys

sys.path.append(str(Path(__file__).parent.parent / "src"))

from parsers.json_parser import JSONParser # type: ignore


class TestJSONParser:
    """Test class for JSON Parser functionality."""
    
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
        self.test_file = self.temp_dir / "test.json"
        self.output_file = self.temp_dir / "output.json"
    
    def teardown_method(self) -> None:
        """Cleanup test environment after each test."""
        for file in self.temp_dir.glob("*"):
            file.unlink()
        self.temp_dir.rmdir()
    
    def test_save_and_load_json(self) -> None:
        """Test basic save and load functionality."""
        JSONParser.save(self.test_data, self.test_file)
        
        assert self.test_file.exists()
        
        loaded_data = JSONParser.load(self.test_file)
        
        assert loaded_data == self.test_data
        assert loaded_data["name"] == "Test Data"
        assert loaded_data["numbers"] == [1, 2, 3, 4, 5]
        assert loaded_data["settings"]["enabled"] is True
    
    def test_load_nonexistent_file(self) -> None:
        """Test loading a file that doesn't exist."""
        nonexistent_file = self.temp_dir / "nonexistent.json"
        
        with pytest.raises(FileNotFoundError):
            JSONParser.load(nonexistent_file)
    
    def test_load_invalid_json(self) -> None:
        """Test loading a file with invalid JSON."""
        invalid_json_file = self.temp_dir / "invalid.json"
        with open(invalid_json_file, 'w') as f:
            f.write('{"invalid": json, "missing": quotes}')
        
        with pytest.raises(ValueError):
            JSONParser.load(invalid_json_file)
    
    def test_save_non_serializable_data(self) -> None:
        """Test saving data that cannot be serialized to JSON."""
        non_serializable = {"data": set([1, 2, 3])}
        
        with pytest.raises(ValueError):
            JSONParser.save(non_serializable, self.test_file)
    
    def test_validate_valid_json(self) -> None:
        """Test validation of valid JSON file."""
        JSONParser.save(self.test_data, self.test_file)
        
        assert JSONParser.validate(self.test_file) is True
    
    def test_validate_invalid_json(self) -> None:
        """Test validation of invalid JSON file."""
        invalid_file = self.temp_dir / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write('invalid json content')
        
        assert JSONParser.validate(invalid_file) is False
    
    def test_validate_nonexistent_file(self) -> None:
        """Test validation of nonexistent file."""
        nonexistent_file = self.temp_dir / "nonexistent.json"
        assert JSONParser.validate(nonexistent_file) is False
    
    def test_get_file_info_valid(self) -> None:
        """Test getting file information for valid JSON."""
        JSONParser.save(self.test_data, self.test_file)
        
        info = JSONParser.get_file_info(self.test_file)
        
        assert info["format"] == "JSON"
        assert info["valid"] is True
        assert info["keys_count"] == 4
        assert info["encoding"] == "utf-8"
        assert info["size_bytes"] > 0
    
    def test_get_file_info_invalid(self) -> None:
        """Test getting file information for invalid JSON."""
        invalid_file = self.temp_dir / "invalid.json"
        with open(invalid_file, 'w') as f:
            f.write('invalid json')
        
        info = JSONParser.get_file_info(invalid_file)
        
        assert info["format"] == "JSON"
        assert info["valid"] is False
        assert "error" in info
        assert info["size_bytes"] > 0
    
    def test_load_non_dict_json(self) -> None:
        """Test loading JSON that is not a dictionary (array, string, etc.)."""
        array_data = [1, 2, 3, 4, 5]
        JSONParser.save(array_data, self.test_file)
        
        loaded_data = JSONParser.load(self.test_file)
        assert isinstance(loaded_data, dict)
        assert loaded_data["data"] == array_data
        
        string_data = "hello world"
        JSONParser.save(string_data, self.test_file)
        
        loaded_data = JSONParser.load(self.test_file)
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
        
        JSONParser.save(utf8_data, self.test_file)
        loaded_data = JSONParser.load(self.test_file)
        
        assert loaded_data == utf8_data
        assert loaded_data["polish"] == "żółć"
        assert loaded_data["chinese"] == "你好"
        assert loaded_data["emoji"] == "🚀"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
