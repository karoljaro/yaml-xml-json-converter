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

### Planned Features
- 🔄 JSON parser and writer
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
