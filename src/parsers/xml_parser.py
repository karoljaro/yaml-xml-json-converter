"""
XML Parser module for handling XML file operations.

This module provides functionality to read from and write to XML files
with proper error handling and validation.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, Union
import xml.dom.minidom


class XMLParser:
    """Parser for XML file operations."""
    
    @staticmethod
    def load(file_path: Path) -> Dict[str, Any]:
        """
        Load data from an XML file.
        
        Args:
            file_path: Path to the XML file to read
            
        Returns:
            Dictionary containing the parsed XML data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the XML is invalid or malformed
            PermissionError: If there's no permission to read the file
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            data = XMLParser._element_to_dict(root)
            
            if root.tag:
                return {root.tag: data}
            else:
                return data if isinstance(data, dict) else {"data": data}
                
        except FileNotFoundError:
            raise FileNotFoundError(f"XML file not found: {file_path}")
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML format in {file_path}: {e}")
        except PermissionError:
            raise PermissionError(f"No permission to read file: {file_path}")
        except Exception as e:
            raise ValueError(f"Error reading XML file {file_path}: {e}")
    
    @staticmethod
    def save(data: Union[Dict[str, Any], Any], file_path: Path) -> None:
        """
        Save data to an XML file.
        
        Args:
            data: Data to save (dictionary or other XML-serializable object)
            file_path: Path where to save the XML file
            
        Raises:
            PermissionError: If there's no permission to write the file
            ValueError: If the data is not XML serializable
        """
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            if isinstance(data, dict):
                if len(data) == 1:
                    root_name = list(data.keys())[0]
                    root_data = data[root_name]
                else:
                    root_name = "root"
                    root_data = data
            else:
                root_name = "root"
                root_data = {"data": data}
            
            root = XMLParser._dict_to_element(root_name, root_data)
            
            rough_string = ET.tostring(root, encoding='unicode')
            reparsed = xml.dom.minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="  ")
            
            lines = [line for line in pretty_xml.split('\n') if line.strip()]
            formatted_xml = '\n'.join(lines) + '\n'
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(formatted_xml)
                
        except PermissionError:
            raise PermissionError(f"No permission to write file: {file_path}")
        except Exception as e:
            raise ValueError(f"Error writing XML file {file_path}: {e}")
    
    @staticmethod
    def validate(file_path: Path) -> bool:
        """
        Validate if a file contains valid XML.
        
        Args:
            file_path: Path to the XML file to validate
            
        Returns:
            True if the XML is valid, False otherwise
        """
        try:
            XMLParser.load(file_path)
            return True
        except (ValueError, FileNotFoundError, PermissionError):
            return False
    
    @staticmethod
    def get_file_info(file_path: Path) -> Dict[str, Any]:
        """
        Get information about an XML file.
        
        Args:
            file_path: Path to the XML file
            
        Returns:
            Dictionary with file information
        """
        try:
            data = XMLParser.load(file_path)
            
            def count_elements(obj: Any) -> int:
                if isinstance(obj, dict):
                    return sum(count_elements(v) for v in obj.values()) + len(obj)
                elif isinstance(obj, list):
                    return sum(count_elements(item) for item in obj)
                else:
                    return 1
            
            return {
                "format": "XML",
                "valid": True,
                "size_bytes": file_path.stat().st_size,
                "elements_count": count_elements(data),
                "encoding": "utf-8"
            }
        except Exception as e:            
            return {
                "format": "XML",
                "valid": False,
                "error": str(e),
                "size_bytes": file_path.stat().st_size if file_path.exists() else 0
            }
    
    @staticmethod
    def _element_to_dict(element: ET.Element) -> Any:
        """
        Convert XML element to dictionary.
        
        Args:
            element: XML element to convert
            
        Returns:
            Dictionary representation of the element
        """
        result: Dict[str, Any] = {}
        if element.attrib:
            for attr, value in element.attrib.items():
                result[f"@{attr}"] = value
        
        # Handle text content
        if element.text and element.text.strip():
            if len(element) == 0 and not element.attrib:
                return element.text.strip()
            else:
                result["#text"] = element.text.strip()
        
        # Handle child elements
        children: Dict[str, Any] = {}
        for child in element:
            child_data = XMLParser._element_to_dict(child)
            
            if child.tag in children:
                if not isinstance(children[child.tag], list):
                    children[child.tag] = [children[child.tag]]
                children[child.tag].append(child_data)
            else:
                children[child.tag] = child_data
        result.update(children)
        
        if (len(result) == 1 and 
            not any(k.startswith('@') or k == '#text' for k in result.keys()) and
            not element.attrib and
            not isinstance(list(result.values())[0], list)):
            return list(result.values())[0]
        
        return result if result else None
    
    @staticmethod
    def _dict_to_element(tag: str, data: Any) -> ET.Element:
        """
        Convert dictionary to XML element.
        
        Args:
            tag: Tag name for the element
            data: Data to convert
            
        Returns:
            XML Element
        """
        element = ET.Element(tag)
        
        if isinstance(data, dict):
            text_content = None
            
            for key, value in data.items():
                if key.startswith('@'):
                    # Attribute
                    attr_name = key[1:]
                    element.set(attr_name, str(value))
                elif key == '#text':
                    text_content = str(value)
                elif isinstance(value, list):
                    for item in value:
                        child = XMLParser._dict_to_element(key, item)
                        element.append(child)
                else:
                    child = XMLParser._dict_to_element(key, value)
                    element.append(child)
            
            if text_content:
                element.text = text_content
                
        elif isinstance(data, list):
            for i, item in enumerate(data):
                child = XMLParser._dict_to_element(f"item{i}", item)
                element.append(child)
        else:
            element.text = str(data)
        
        return element
