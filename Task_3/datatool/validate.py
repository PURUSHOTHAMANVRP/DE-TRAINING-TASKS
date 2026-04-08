import pandas as pd
import numpy as np

def validate_df(df: pd.DataFrame) -> dict:
    missing = df.isna().sum().to_dict()
    duplicates = int(df.duplicated().sum())

    type_issues = {}
    for col in df.columns:
        s = df[col]
        if s.dtype == "object":
            non_null = s.dropna().astype(str).str.strip()
            if len(non_null) == 0:
                continue

            # heuristic: if many values are numeric-like but some aren't => mixed
            numeric_like = pd.to_numeric(non_null, errors="coerce")
            numeric_ratio = numeric_like.notna().mean()

            # if between (0.2 and 0.8), strongly suggests mixed content
            if 0.2 < numeric_ratio < 0.8:
                bad_examples = non_null[numeric_like.isna()].head(5).tolist()
                type_issues[col] = {
                    "issue": "mixed numeric/text in object column",
                    "numeric_like_ratio": float(numeric_ratio),
                    "examples_non_numeric": bad_examples
                }

    return {
        "missing_values": missing,
        "duplicate_rows": duplicates,
        "type_issues": type_issues
    }

def print_validation(report: dict) -> None:
    print("Missing / null values per column:")
    for col, cnt in report["missing_values"].items():
        print(f"  - {col}: {cnt}")

    print(f"\nDuplicate rows: {report['duplicate_rows']}")

    if report["type_issues"]:
        print("\nPotential inconsistent data types detected:")
        for col, info in report["type_issues"].items():
            print(f"  - {col}: {info['issue']} (numeric-like ratio={info['numeric_like_ratio']:.2f})")
            if info["examples_non_numeric"]:
                print(f"    examples: {info['examples_non_numeric']}")
    else:
        print("\nNo obvious inconsistent type issues detected.")
