# YAML/XML/JSON Format Converter

A command-line tool for converting between YAML, XML, and JSON file formats.

## Features

- Convert between JSON, YAML, and XML formats
- Automatic file validation
- Error handling with descriptive messages
- Cross-platform compatibility

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
# Convert JSON to YAML
python src\main.py data.json data.yaml --format yaml

# Convert XML to JSON
python src\main.py config.xml config.json --format json

# Convert YAML to XML
python src\main.py settings.yaml settings.xml --format xml
```

## Supported Formats

- **JSON** (`.json`)
- **YAML** (`.yaml`, `.yml`)
- **XML** (`.xml`)

## Development Status

🚧 **Work in Progress** - Currently implementing core conversion functionality.

### Completed Features
- ✅ CLI interface with argument parsing
- ✅ File path validation
- ✅ Error handling and user feedback
- ✅ **JSON Parser Module** - Complete JSON read/write functionality
- ✅ **Type Safety** - MyPy configuration and type annotations
- ✅ **Unit Testing** - Comprehensive test suite for JSON operations
- ✅ **UTF-8 Support** - Full Unicode character handling

### Current Capabilities
- **JSON Processing**: Load, save, validate JSON files with proper error handling
- **Data Normalization**: Automatic conversion of non-dict JSON to dict format
- **File Information**: Extract metadata and validation status from JSON files

### Planned Features
- 🔄 YAML parser and writer
- 🔄 XML parser and writer
- 🔄 Format auto-detection
- 🔄 Batch conversion support
- 🔄 Configuration file support

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
