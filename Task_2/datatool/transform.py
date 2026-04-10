import pandas as pd
from .utils import clean_columns

def transform_df(df: pd.DataFrame, missing_strategy: str = "drop") -> pd.DataFrame:
    out = df.copy()

    # clean column names
    out.columns = clean_columns(out.columns)

    # remove duplicates
    out = out.drop_duplicates()

    # handle missing values
    if missing_strategy == "drop":
        out = out.dropna()
    elif missing_strategy == "fill":
        # fill numeric with median, others with mode (or "unknown" if mode missing)
        for col in out.columns:
            if pd.api.types.is_numeric_dtype(out[col]):
                med = out[col].median()
                out[col] = out[col].fillna(med)
            else:
                mode = out[col].mode(dropna=True)
                fill_val = mode.iloc[0] if len(mode) else "unknown"
                out[col] = out[col].fillna(fill_val)
    else:
        raise ValueError("missing_strategy must be 'drop' or 'fill'")

    return out