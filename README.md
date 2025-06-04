# YAML/XML/JSON Format Converter

**Project Status: COMPLETED ✅**  
*Full-featured command-line converter supporting all major data formats with comprehensive test coverage (39 tests passing).*

A command-line tool for converting between YAML, XML, and JSON file formats with full bidirectional conversion support.

## Features

- **Complete Format Support**: Convert between JSON, YAML, and XML formats
- **Bidirectional Conversion**: Full support for all format combinations (JSON↔YAML↔XML)
- **XML Advanced Features**: 
  - Attributes handling with `@` prefix notation
  - Text content with `#text` notation
  - Namespace support
  - Pretty-printed output
- **Automatic File Validation**: Built-in format validation for all supported types
- **Error Handling**: Descriptive error messages and proper exception handling
- **Cross-platform Compatibility**: Works on Windows, Linux, and macOS
- **Type Safety**: Full MyPy type checking support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/karoljaro/yaml-xml-json-converter.git
cd yaml-xml-json-converter
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python src\main.py input_file output_file --format target_format
```

### Examples

```bash
# Convert JSON to YAML (✅ Available)
python src\main.py data.json data.yaml --format yaml

# Convert YAML to JSON (✅ Available)
python src\main.py config.yaml config.json --format json

# Convert JSON to XML (✅ Available)
python src\main.py data.json data.xml --format xml

# Convert XML to JSON (✅ Available)
python src\main.py config.xml config.json --format json

# Convert YAML to XML (✅ Available)
python src\main.py config.yaml config.xml --format xml

# Convert XML to YAML (✅ Available)
python src\main.py data.xml data.yaml --format yaml

# Convert JSON to JSON (✅ Available - validation/formatting)
python src\main.py input.json output.json --format json

# Convert YAML to YAML (✅ Available - validation/formatting)
python src\main.py input.yaml output.yaml --format yaml

# XML conversions (🔄 Coming in Phase 4)
# python src\main.py config.xml config.json --format json
# python src\main.py settings.yaml settings.xml --format xml
```

## Supported Formats

- **JSON** (`.json`)
- **YAML** (`.yaml`, `.yml`)
- **XML** (`.xml`)

## Development Status

✅ **Phase 4 Complete** - All core conversion functionality implemented and tested.

### Completed Features
- ✅ CLI interface with argument parsing
- ✅ File path validation and automatic directory creation
- ✅ Error handling and user feedback
- ✅ **JSON Parser Module** - Complete JSON read/write functionality
- ✅ **YAML Parser Module** - Complete YAML read/write functionality with PyYAML
- ✅ **XML Parser Module** - Complete XML read/write functionality with attributes and namespaces
- ✅ **Type Safety** - MyPy configuration and type annotations
- ✅ **Unit Testing** - Comprehensive test suite (39 tests total)
- ✅ **UTF-8 Support** - Full Unicode character handling
- ✅ **Bidirectional Conversion** - All format combinations (JSON↔YAML↔XML)

### Current Capabilities
- **JSON Processing**: Load, save, validate JSON files with proper error handling
- **YAML Processing**: Load, save, validate YAML files with PyYAML integration
- **XML Processing**: Load, save, validate XML files with attributes (`@prefix`) and text content (`#text`)
- **Format Conversion**: Convert between JSON, YAML, and XML formats seamlessly
- **Data Normalization**: Automatic conversion of non-dict data to dict format
- **File Information**: Extract metadata and validation status from all supported formats
- **Advanced XML Features**: 
  - XML attributes handling with `@` prefix notation
  - Text content with `#text` notation
  - Multiple elements with same tag (converted to arrays)
  - Namespace preservation
  - Pretty-printed output with proper indentation

### Test Coverage
- **JSON Parser**: 12 comprehensive tests
- **YAML Parser**: 10 comprehensive tests  
- **XML Parser**: 17 comprehensive tests
- **Total**: 39 tests covering all functionality

### XML Conversion Examples

The XML parser handles complex structures including attributes and text content:

```xml
<!-- Input XML -->
<book id="123" isbn="978-0123456789">
    <title>Python Programming</title>
    <author>Jane Smith</author>
    <price currency="USD">29.99</price>
</book>
```

```json
// Converted to JSON
{
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
```

## Contributing

This project uses Git branching for feature development:

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit
3. Push branch: `git push origin feature/your-feature`
4. Create Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_json_parser.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Development Tools

This project uses several development tools for code quality:

- **MyPy**: Static type checking configured for Python 3.13
- **Pytest**: Unit testing framework with comprehensive test coverage
- **Git**: Version control with feature branches

### Type Checking

The project is configured with MyPy for static type analysis:

```bash
# Run MyPy type checking
mypy src/

# Configuration in mypy.ini:
# - Python version 3.13
# - Source path: src/
# - Full type safety enabled
```

## API Documentation

### JSONParser Class

The `JSONParser` class provides static methods for JSON file operations:

```python
from parsers.json_parser import JSONParser
from pathlib import Path

# Load JSON file
data = JSONParser.load(Path("input.json"))

# Save data to JSON file
JSONParser.save(data, Path("output.json"))

# Validate JSON file
is_valid = JSONParser.validate(Path("file.json"))

# Get file information
info = JSONParser.get_file_info(Path("file.json"))
```

### YAMLParser Class

The `YAMLParser` class provides static methods for YAML file operations:

```python
from parsers.yaml_parser import YAMLParser
from pathlib import Path

# Load YAML file
data = YAMLParser.load(Path("input.yaml"))

# Save data to YAML file (with proper formatting)
YAMLParser.save(data, Path("output.yaml"))

# Validate YAML file
is_valid = YAMLParser.validate(Path("file.yaml"))

# Get file information
info = YAMLParser.get_file_info(Path("file.yaml"))
```

### Format Conversion Example

```python
from parsers.json_parser import JSONParser
from parsers.yaml_parser import YAMLParser
from pathlib import Path

# Load JSON and save as YAML
json_data = JSONParser.load(Path("data.json"))
YAMLParser.save(json_data, Path("data.yaml"))

# Load YAML and save as JSON
yaml_data = YAMLParser.load(Path("config.yaml"))
JSONParser.save(yaml_data, Path("config.json"))
```
