import pandas as pd

def ingest_summary(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }

def print_ingest(summary: dict) -> None:
    print(f"Number of rows: {summary['rows']}")
    print("Columns:", ", ".join(summary["columns"]))
    print("Data types:")
    for col, dt in summary["dtypes"].items():
        print(f"  - {col}: {dt}")