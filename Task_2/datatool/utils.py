import re

def clean_column_name(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"[\s\-]+", "_", s)
    s = re.sub(r"[^a-z0-9_]", "", s)
    s = re.sub(r"_+", "_", s)
    return s

def clean_columns(cols):
    return [clean_column_name(c) for c in cols]