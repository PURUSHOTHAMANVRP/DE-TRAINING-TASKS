"""
Stage 0 — Data Ingestion Pipeline
Reads all data_page_*.json files, enriches each record with page metadata,
and writes a combined ingest.json to new_data/raw/books/
"""

import os
import json
import re
import glob
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def get_config():
    base_input = Path(os.getenv("INPUT_DIR", "Ingest/data/raw/books"))
    if base_input.exists() and any(base_input.iterdir()):
        dated_dirs = sorted(base_input.glob("????-??-??"), reverse=True)
        input_dir = dated_dirs[0] if dated_dirs else base_input
    else:
        input_dir = base_input
    output_dir = Path("new_data/raw/books")
    return {"input_dir": input_dir, "output_dir": output_dir,
            "output_file": output_dir / "ingest.json"}


def extract_page_number(filename):
    match = re.search(r"data_page_(\d+)\.json$", filename, re.IGNORECASE)
    return int(match.group(1)) if match else None


def load_json_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as exc:
        log.warning("Skipping %s — JSON error: %s", filepath.name, exc)
    except OSError as exc:
        log.warning("Skipping %s — IO error: %s", filepath.name, exc)
    return None


def normalise_to_list(data):
    if isinstance(data, list):
        return data
    for key in ("books", "results", "data", "items"):
        if key in data and isinstance(data[key], list):
            return data[key]
    if isinstance(data, dict):
        return [data]
    return []


def ingest(config):
    input_dir = config["input_dir"]
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    pattern = str(input_dir / "data_page_*.json")
    page_files = sorted(
        glob.glob(pattern),
        key=lambda p: extract_page_number(os.path.basename(p)) or 0,
    )
    if not page_files:
        raise FileNotFoundError(f"No data_page_*.json files found in: {input_dir}")

    log.info("Found %d page file(s)", len(page_files))
    all_books = []
    ingestion_time = datetime.utcnow().isoformat() + "Z"

    for filepath_str in page_files:
        filepath = Path(filepath_str)
        page_number = extract_page_number(filepath.name)
        raw = load_json_file(filepath)
        if raw is None:
            continue
        books = normalise_to_list(raw)
        for book in books:
            book["page_number"] = page_number
            book["source_file"] = filepath.name
            book["ingestion_time"] = ingestion_time
        all_books.extend(books)
        log.info("  Loaded %d records from %s", len(books), filepath.name)

    log.info("Total: %d records ingested", len(all_books))
    return all_books


def write_output(books, config):
    config["output_dir"].mkdir(parents=True, exist_ok=True)
    with open(config["output_file"], "w", encoding="utf-8") as fh:
        json.dump(books, fh, indent=2, ensure_ascii=False)
    log.info("Written → %s", config["output_file"])


def main():
    log.info("=== Stage 0: Ingestion ===")
    config = get_config()
    books = ingest(config)
    write_output(books, config)
    log.info("=== Done ===")


if __name__ == "__main__":
    main()