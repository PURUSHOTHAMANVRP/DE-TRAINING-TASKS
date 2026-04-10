import shlex
from .cli import main as cli_main

HELP_TEXT = """Available commands:
  ingest <input_file>
  validate <input_file>
  transform <input_file> <output_file> [--missing drop|fill]
  help
  exit
"""

def run_repl():
    print("Welcome to datatool interactive mode. Type 'help' to see commands.")
    while True:
        try:
            raw = input("datatool> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            return

        if not raw:
            continue
        if raw.lower() in ("exit", "quit"):
            print("Bye!")
            return
        if raw.lower() == "help":
            print(HELP_TEXT)
            continue

        # Route REPL command into argparse CLI
        try:
            argv = shlex.split(raw)
            cli_main(argv)
        except SystemExit:
            # argparse calls SystemExit on parse errors; keep REPL alive
            continue
        except Exception as e:
            print(f"Error: {e}")