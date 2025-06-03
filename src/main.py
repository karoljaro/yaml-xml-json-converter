import argparse

def main():
    parser = argparse.ArgumentParser(
        description="YAML, XML, JSON format converter",
        epilog="Example: python src\main.py input.json output.yaml --format yaml"
    )
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("output_file", help="Output file path")
    parser.add_argument("--format", choices=["yaml", "xml", "json"], help="Output format", required=True)

    args = parser.parse_args()

    print(f"Converting {args.input_file} to {args.output_file} in {args.format} format...")

if __name__ == "__main__":
    main()