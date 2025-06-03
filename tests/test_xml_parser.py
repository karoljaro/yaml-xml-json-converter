"""
Unit tests for XML Parser module.

This module contains comprehensive tests for the XMLParser class,
including functionality tests, error handling, and edge cases.
"""

import pytest
from pathlib import Path
import tempfile
import sys

sys.path.append(str(Path(__file__).parent.parent / "src"))

from parsers.xml_parser import XMLParser # type: ignore


class TestXMLParser:
    """Test class for XML Parser functionality."""
    
    def setup_method(self) -> None:
        """Setup test environment before each test."""
        self.test_data = {
            "person": {
                "name": "John Doe",
                "age": 30,
                "address": {
                    "street": "123 Main St",
                    "city": "Springfield",
                    "country": "USA"
                },
                "hobbies": ["reading", "swimming", "coding"]
            }
        }
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_file = self.temp_dir / "test.xml"
        self.output_file = self.temp_dir / "output.xml"
    
    def teardown_method(self) -> None:
        """Cleanup test environment after each test."""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except (PermissionError, FileNotFoundError):
            pass
    
    def test_save_and_load_xml(self) -> None:
        """Test basic save and load functionality."""
        XMLParser.save(self.test_data, self.test_file)
        
        assert self.test_file.exists()
        
        loaded_data = XMLParser.load(self.test_file)
        
        # Check structure preservation
        assert "person" in loaded_data
        assert loaded_data["person"]["name"] == "John Doe"
        assert loaded_data["person"]["age"] == "30"  # XML converts numbers to strings
        assert loaded_data["person"]["address"]["city"] == "Springfield"
    
    def test_save_xml_with_attributes(self) -> None:
        """Test XML with attributes handling."""
        data_with_attrs = {
            "book": {
                "@id": "123",
                "@isbn": "978-0123456789",
                "title": "Python Programming",
                "author": "Jane Smith",
                "price": {
                    "@currency": "USD",
                    "#text": "29.99"
                }
            }
        }
        
        XMLParser.save(data_with_attrs, self.test_file)
        loaded_data = XMLParser.load(self.test_file)
        
        assert loaded_data["book"]["@id"] == "123"
        assert loaded_data["book"]["@isbn"] == "978-0123456789"
        assert loaded_data["book"]["title"] == "Python Programming"
        assert loaded_data["book"]["price"]["@currency"] == "USD"
        assert loaded_data["book"]["price"]["#text"] == "29.99"
    
    def test_save_xml_with_lists(self) -> None:
        """Test XML with list handling."""
        data_with_lists = {
            "library": {
                "book": [
                    {"title": "Book One", "author": "Author A"},
                    {"title": "Book Two", "author": "Author B"},
                    {"title": "Book Three", "author": "Author C"}
                ]
            }
        }
        
        XMLParser.save(data_with_lists, self.test_file)
        loaded_data = XMLParser.load(self.test_file)
        
        assert "library" in loaded_data
        assert isinstance(loaded_data["library"]["book"], list)
        assert len(loaded_data["library"]["book"]) == 3
        assert loaded_data["library"]["book"][0]["title"] == "Book One"
        assert loaded_data["library"]["book"][2]["author"] == "Author C"
    
    def test_load_simple_xml(self) -> None:
        """Test loading a simple XML structure."""
        xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<note>
    <to>Tove</to>
    <from>Jani</from>
    <heading>Reminder</heading>
    <body>Don't forget me this weekend!</body>
</note>'''
        
        self.test_file.write_text(xml_content, encoding='utf-8')
        loaded_data = XMLParser.load(self.test_file)
        
        assert "note" in loaded_data
        assert loaded_data["note"]["to"] == "Tove"
        assert loaded_data["note"]["from"] == "Jani"
        assert loaded_data["note"]["heading"] == "Reminder"
        assert loaded_data["note"]["body"] == "Don't forget me this weekend!"
    
    def test_load_xml_with_namespaces(self) -> None:
        """Test loading XML with namespaces."""
        xml_content = '''<?xml version="1.0"?>
<root xmlns:h="http://www.w3.org/TR/html4/" xmlns:f="https://www.w3schools.com/furniture">
    <h:table>
        <h:tr>
            <h:td>Apples</h:td>
            <h:td>Bananas</h:td>
        </h:tr>
    </h:table>
    <f:table>
        <f:name>African Coffee Table</f:name>
        <f:width>80</f:width>
        <f:length>120</f:length>
    </f:table>
</root>'''
        
        self.test_file.write_text(xml_content, encoding='utf-8')
        loaded_data = XMLParser.load(self.test_file)
        
        assert "root" in loaded_data
        data = loaded_data["root"]
        assert any("table" in str(key) for key in data.keys())
    
    def test_validate_valid_xml(self) -> None:
        """Test validation of valid XML."""
        XMLParser.save(self.test_data, self.test_file)
        
        assert XMLParser.validate(self.test_file) == True
    
    def test_validate_invalid_xml(self) -> None:
        """Test validation of invalid XML."""
        invalid_xml = "<invalid><unclosed></invalid>"
        self.test_file.write_text(invalid_xml, encoding='utf-8')
        
        assert XMLParser.validate(self.test_file) == False
    
    def test_validate_nonexistent_file(self) -> None:
        """Test validation of non-existent file."""
        non_existent = self.temp_dir / "nonexistent.xml"
        
        assert XMLParser.validate(non_existent) == False
    
    def test_get_file_info_valid(self) -> None:
        """Test getting file info for valid XML."""
        XMLParser.save(self.test_data, self.test_file)
        
        info = XMLParser.get_file_info(self.test_file)
        
        assert info["format"] == "XML"
        assert info["valid"] == True
        assert info["size_bytes"] > 0
        assert info["elements_count"] > 0
        assert info["encoding"] == "utf-8"
    
    def test_get_file_info_invalid(self) -> None:
        """Test getting file info for invalid XML."""
        invalid_xml = "<broken><xml"
        self.test_file.write_text(invalid_xml, encoding='utf-8')
        
        info = XMLParser.get_file_info(self.test_file)
        
        assert info["format"] == "XML"
        assert info["valid"] == False
        assert "error" in info
        assert info["size_bytes"] > 0
    
    def test_load_file_not_found(self) -> None:
        """Test loading non-existent file."""
        non_existent = self.temp_dir / "nonexistent.xml"
        
        with pytest.raises(FileNotFoundError, match="XML file not found"):
            XMLParser.load(non_existent)
    
    def test_load_invalid_xml_format(self) -> None:
        """Test loading file with invalid XML format."""
        invalid_xml = "<invalid><unclosed></invalid>"
        self.test_file.write_text(invalid_xml, encoding='utf-8')
        
        with pytest.raises(ValueError, match="Invalid XML format"):
            XMLParser.load(self.test_file)    
    def test_save_empty_dict(self) -> None:
        """Test saving empty dictionary."""
        empty_data: dict = {}
        
        XMLParser.save(empty_data, self.test_file)
        loaded_data = XMLParser.load(self.test_file)
        
        assert "root" in loaded_data
    
    def test_save_simple_value(self) -> None:
        """Test saving simple string value."""
        simple_data = "Hello World"
        
        XMLParser.save(simple_data, self.test_file)
        loaded_data = XMLParser.load(self.test_file)
        
        assert "root" in loaded_data
        assert loaded_data["root"] == "Hello World"
    
    def test_save_to_nonexistent_directory(self) -> None:
        """Test saving to non-existent directory (should create it)."""
        deep_path = self.temp_dir / "subdir" / "test.xml"
        
        XMLParser.save(self.test_data, deep_path)
        
        assert deep_path.exists()
        loaded_data = XMLParser.load(deep_path)
        assert "person" in loaded_data
    
    def test_complex_nested_structure(self) -> None:
        """Test complex nested XML structure."""
        complex_data = {
            "company": {
                "@name": "TechCorp",
                "@founded": "2020",
                "departments": {
                    "department": [
                        {
                            "@id": "1",
                            "name": "Engineering",
                            "employees": {
                                "employee": [
                                    {"name": "Alice", "role": "Senior Developer"},
                                    {"name": "Bob", "role": "DevOps Engineer"}
                                ]
                            }
                        },
                        {
                            "@id": "2",
                            "name": "Marketing",
                            "employees": {
                                "employee": {
                                    "name": "Charlie",
                                    "role": "Marketing Manager"
                                }
                            }
                        }
                    ]
                }
            }
        }
        
        XMLParser.save(complex_data, self.test_file)
        loaded_data = XMLParser.load(self.test_file)
        
        assert loaded_data["company"]["@name"] == "TechCorp"
        assert loaded_data["company"]["@founded"] == "2020"
        
        departments = loaded_data["company"]["departments"]["department"]
        assert isinstance(departments, list)
        assert len(departments) == 2
        
        eng_dept = departments[0]
        assert eng_dept["@id"] == "1"
        assert eng_dept["name"] == "Engineering"
        assert isinstance(eng_dept["employees"]["employee"], list)
        assert len(eng_dept["employees"]["employee"]) == 2
        marketing_dept = departments[1]
        assert marketing_dept["@id"] == "2"
        assert marketing_dept["name"] == "Marketing"
        assert marketing_dept["employees"]["name"] == "Charlie"
        assert marketing_dept["employees"]["role"] == "Marketing Manager"
    
    def test_xml_roundtrip_preservation(self) -> None:
        """Test that data survives roundtrip conversion."""
        original_data = {
            "config": {
                "@version": "1.0",
                "database": {
                    "host": "localhost",
                    "port": "5432",
                    "name": "mydb"
                },
                "features": {
                    "feature": [
                        {"name": "auth", "enabled": "true"},
                        {"name": "cache", "enabled": "false"},
                        {"name": "logging", "enabled": "true"}
                    ]
                },
                "description": {
                    "@lang": "en",
                    "#text": "Application configuration file"
                }
            }
        }
        
        XMLParser.save(original_data, self.test_file)
        loaded_data = XMLParser.load(self.test_file)
        
        config = loaded_data["config"]
        assert config["@version"] == "1.0"
        assert config["database"]["host"] == "localhost"
        assert config["database"]["port"] == "5432"
        assert config["description"]["@lang"] == "en"
        assert config["description"]["#text"] == "Application configuration file"
        
        features = config["features"]["feature"]
        assert isinstance(features, list)
        assert len(features) == 3
        assert features[0]["name"] == "auth"
        assert features[0]["enabled"] == "true"
