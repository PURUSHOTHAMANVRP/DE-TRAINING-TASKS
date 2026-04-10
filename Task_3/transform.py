"""
Stage 1 — Data Transformation Pipeline
Reads ingest.json and produces a clean books_transformed.csv
"""

import os
import json
import re
import logging
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

BASE_URL   = "http://books.toscrape.com/catalogue/"
INPUT_FILE = Path("new_data/raw/books/ingest.json")
OUTPUT_DIR = Path("new_data/transformed/books")
OUTPUT_FILE = OUTPUT_DIR / "books_transformed.csv"

RATING_MAP = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
}


def convert_price(value):
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = re.sub(r"[^\d.]", "", value)
        try:
            return float(cleaned)
        except ValueError:
            pass
    return None


def convert_rating(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        rating = RATING_MAP.get(value.strip())
        if rating is not None:
            return rating
        try:
            return int(float(value.strip()))
        except ValueError:
            pass
    return None


def convert_availability(value):
    if value is None:
        return None
    text = str(value).strip().lower()
    if "stock" in text and "out" not in text:
        return 1
    if "available" in text and "un" not in text:
        return 1
    return 0


def extract_book_id(url):
    if not isinstance(url, str):
        return None
    match = re.search(r"_(\d+)/", url)
    return int(match.group(1)) if match else None


def build_full_url(relative_url):
    if not isinstance(relative_url, str):
        return None
    s = relative_url.strip()
    if s.startswith("http"):
        return s
    s = re.sub(r"^(\.\.\/)+", "", s)
    s = re.sub(r"^catalogue/", "", s)
    return BASE_URL + s


def transform(df):
    log.info("Input: %d rows × %d columns", *df.shape)

    # Price
    price_col = next((c for c in df.columns if "price" in c.lower()), None)
    if price_col:
        df["price"] = df[price_col].apply(convert_price)
        if price_col != "price":
            df.drop(columns=[price_col], inplace=True)

    # Rating
    rating_col = next((c for c in df.columns if "rating" in c.lower()), None)
    if rating_col:
        df["rating"] = df[rating_col].apply(convert_rating)
        if rating_col != "rating":
            df.drop(columns=[rating_col], inplace=True)

    # Availability
    avail_col = next((c for c in df.columns if "avail" in c.lower()), None)
    if avail_col:
        df["availability"] = df[avail_col].apply(convert_availability)
        if avail_col != "availability":
            df.drop(columns=[avail_col], inplace=True)

    # URL + book_id
    url_col = next(
        (c for c in df.columns if c.lower() in ("url", "href", "link", "product_link")),
        None,
    )
    if url_col:
        df["url"]     = df[url_col].apply(build_full_url)
        df["book_id"] = df[url_col].apply(extract_book_id)
        if url_col != "url":
            df.drop(columns=[url_col], inplace=True)

    # Timestamp
    if "ingestion_time" not in df.columns:
        df["ingestion_time"] = datetime.now(timezone.utc).isoformat()

    # Select final columns
    wanted = ["book_id", "title", "price", "rating", "availability",
              "url", "page_number", "ingestion_time"]
    present = [c for c in wanted if c in df.columns]
    df = df[present]

    log.info("Output: %d rows × %d columns", *df.shape)
    return df


def main():
    log.info("=== Stage 1: Transformation ===")
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Run ingest.py first. Not found: {INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as fh:
        raw = json.load(fh)

    df = pd.DataFrame(raw)
    log.info("Loaded %d records", len(df))
    log.info("Columns: %s", list(df.columns))

    df_clean = transform(df)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_clean.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")
    log.info("Written → %s", OUTPUT_FILE)
    log.info("Preview:\n%s", df_clean.head(3).to_string(index=False))
    log.info("=== Done ===")


if __name__ == "__main__":
    main()