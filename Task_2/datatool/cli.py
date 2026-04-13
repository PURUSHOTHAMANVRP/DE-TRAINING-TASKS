import sys
import argparse
from .io_utils import read_input, write_output
from .ingest import ingest_summary, print_ingest
from .validate import validate_df, print_validation
from .transform import transform_df


def build_parser():
    parser = argparse.ArgumentParser(
        prog="datatool",
        description="CLI Data Engineering Tool"
    )
    sub = parser.add_subparsers(dest="command")

    ingest_p = sub.add_parser("ingest", help="Ingest a file")
    ingest_p.add_argument("input_file")

    validate_p = sub.add_parser("validate", help="Validate a file")
    validate_p.add_argument("input_file")

    transform_p = sub.add_parser("transform", help="Transform a file")
    transform_p.add_argument("input_file")
    transform_p.add_argument("output_file")
    transform_p.add_argument("--missing", choices=["drop", "fill"], default="drop")

    return parser


def run_command(args):
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
        print(f"Saved cleaned data to {args.output_file}")


def main(argv=None):
    """
    argv = None  -> normal run using sys.argv (terminal usage)
    argv = [...] -> called from REPL (so we parse that list)
    """
    # If called from REPL, argv is a list like ["ingest", "file.csv"]
    if argv is not None:
        parser = build_parser()
        args = parser.parse_args(argv)
        if args.command is None:
            # user typed nothing or invalid subcommand
            parser.print_help()
            return
        run_command(args)
        return

    # If started without args in terminal -> interactive REPL
    if len(sys.argv) == 1:
        from .repl import run_repl
        run_repl()
        return

    # Otherwise argparse one-shot mode using terminal args
    parser = build_parser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return
    run_command(args)


if __name__ == "__main__":
    main()