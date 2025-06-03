import argparse
from pathlib import Path
import sys

def validate_files(input_path: Path, output_path: Path) -> None:
    """Validate input and output file paths."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file does not exist: {input_path}")
    
    if not input_path.is_file():
        raise ValueError(f"Input path is not a file: {input_path}")
    
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        raise PermissionError(f"No write permission for: {output_path.parent}")

def main():
    parser = argparse.ArgumentParser(
        description="YAML, XML, JSON format converter",
        epilog=r"Example: python src\main.py input.json output.yaml --format yaml"
    )
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    parser.add_argument("--format", choices=["yaml", "xml", "json"], help="Output format", required=True)

    args = parser.parse_args()

    input_path = Path(args.input_file)
    output_path = Path(args.output_file)

    try:
        validate_files(input_path=input_path, output_path=output_path)
        print(f"Converting {args.input_file} to {args.output_file} in {args.format} format...")
    except (FileNotFoundError, ValueError, PermissionError) as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()