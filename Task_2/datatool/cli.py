import argparse
from .io_utils import read_input, write_output
from .ingest import ingest_summary, print_ingest
from .validate import validate_df, print_validation
from .transform import transform_df

def build_parser():
    parser = argparse.ArgumentParser(prog="datatool", description="CLI Data Engineering Tool")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="Read file and display dataset summary")
    p_ingest.add_argument("input_file")

    p_validate = sub.add_parser("validate", help="Run data quality checks")
    p_validate.add_argument("input_file")

    p_transform = sub.add_parser("transform", help="Clean and write data")
    p_transform.add_argument("input_file")
    p_transform.add_argument("output_file")
    p_transform.add_argument("--missing", choices=["drop", "fill"], default="drop",
                             help="How to handle missing values")

    p_repl = sub.add_parser("repl", help="Start interactive datatool> session")

    return parser

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "ingest":
        df = read_input(args.input_file)
        summary = ingest_summary(df)
        print_ingest(summary)

    elif args.command == "validate":
        df = read_input(args.input_file)
        report = validate_df(df)
        print_validation(report)

    elif args.command == "transform":
        df = read_input(args.input_file)
        cleaned = transform_df(df, missing_strategy=args.missing)
        write_output(cleaned, args.output_file)
        print(f"Saved cleaned data to: {args.output_file}")

    elif args.command == "repl":
        from .repl import run_repl
        run_repl()

if __name__ == "__main__":
    main()