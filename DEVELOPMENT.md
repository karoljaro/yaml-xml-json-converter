# Developer Documentation

## Project Structure

```
yaml-xml-json-converter/
├── src/                    # Source code
│   ├── main.py            # CLI entry point
│   └── parsers/           # Format-specific parsers
│       ├── __init__.py    # Parser exports
│       └── json_parser.py # JSON handling
├── tests/                 # Unit tests
│   ├── __init__.py
│   └── test_json_parser.py
├── mypy.ini              # Type checking config
├── requirements.txt      # Dependencies
└── README.md            # User documentation
```

## Code Style & Standards

### Type Annotations
All functions and methods should include proper type annotations:

```python
def function_name(param: str) -> Dict[str, Any]:
    """Function docstring."""
    return {"result": param}
```

### Error Handling
Use specific exception types with descriptive messages:

```python
try:
    # risky operation
    pass
except FileNotFoundError:
    raise FileNotFoundError(f"File not found: {file_path}")
except json.JSONDecodeError as e:
    raise ValueError(f"Invalid JSON format: {e}")
```

### Testing
- Each module should have corresponding test file
- Use descriptive test method names: `test_load_nonexistent_file`
- Include both positive and negative test cases
- Test edge cases (empty files, special characters, etc.)

## Adding New Parsers

To add support for a new format (e.g., YAML):

1. **Create parser module**: `src/parsers/yaml_parser.py`
2. **Implement required methods**:
   ```python
   class YAMLParser:
       @staticmethod
       def load(file_path: Path) -> Dict[str, Any]:
           # Implementation
           pass
       
       @staticmethod
       def save(data: Dict[str, Any], file_path: Path) -> None:
           # Implementation
           pass
       
       @staticmethod
       def validate(file_path: Path) -> bool:
           # Implementation
           pass
       
       @staticmethod
       def get_file_info(file_path: Path) -> Dict[str, Any]:
           # Implementation
           pass
   ```

3. **Update `__init__.py`**:
   ```python
   from .yaml_parser import YAMLParser
   __all__ = ['JSONParser', 'YAMLParser']
   ```

4. **Create comprehensive tests**: `tests/test_yaml_parser.py`

5. **Update main.py** to handle new format in `process_conversion()`

## Running Development Tools

### Type Checking
```bash
mypy src/
```

### Testing with Coverage
```bash
python -m pytest tests/ --cov=src --cov-report=html
```

### Linting (if added)
```bash
flake8 src/ tests/
black src/ tests/
```

## Git Workflow

1. **Feature branches**: `feature/parser-name`
2. **Commit messages**: Use conventional commits
   - `feat:` new features
   - `fix:` bug fixes
   - `docs:` documentation
   - `test:` adding tests
   - `refactor:` code improvements

3. **Before merging**:
   - All tests pass
   - Type checking passes
   - Code is properly documented

## Performance Considerations

- Use streaming for large files when possible
- Implement proper memory management for large datasets
- Consider lazy loading for better performance
- Profile code for bottlenecks before optimizing

## Error Handling Strategy

- **FileNotFoundError**: For missing input files
- **PermissionError**: For access/write permission issues
- **ValueError**: For invalid format/data issues
- **Generic Exception**: For unexpected errors (re-raise with context)

Always provide helpful error messages that guide users toward solutions.
