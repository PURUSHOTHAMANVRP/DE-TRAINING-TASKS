import pandas as pd
from pathlib import Path

def read_input(path: str) -> pd.DataFrame:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    suffix = p.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(p)
    elif suffix == ".json":
        # supports JSON array of objects OR JSON lines (try both)
        try:
            return pd.read_json(p)
        except ValueError:
            return pd.read_json(p, lines=True)
    else:
        raise ValueError("Unsupported file type. Use .csv or .json")

def write_output(df: pd.DataFrame, path: str) -> None:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".csv":
        df.to_csv(p, index=False)
    elif suffix == ".json":
        df.to_json(p, orient="records", indent=2)
    else:
        raise ValueError("Unsupported output type. Use .csv or .json")
