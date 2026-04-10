# DE-TRAINING-TASKS

A comprehensive data engineering training project demonstrating practical data processing, validation, and transformation workflows using Python.

## Project Overview

This repository contains three progressive data engineering tasks designed to build skills in data processing, Excel manipulation, and CLI tool development:

- **Revenue Tracker Tasks**: Excel-based data extraction and reporting automation
- **DataTool**: A command-line data processing toolkit with validation and transformation capabilities

## Project Structure

```
DE-TRAINING-TASKS/
├── README.md
├── Revenue Tracker/
│   ├── Task_1/
│   │   └── update_output.py          # Excel metrics extraction and reporting
│   └── Task_2/
│       ├── output.py                 # Multi-file revenue mapping
│       └── update_output.py          # Enhanced Excel processing
└── Task_3/
    ├── requirements.txt              # Python dependencies
    ├── datatool/                     # CLI data processing toolkit
    │   ├── __init__.py
    │   ├── cli.py                    # Command-line interface
    │   ├── ingest.py                 # Data ingestion utilities
    │   ├── io_utils.py               # File I/O operations
    │   ├── repl.py                   # Interactive REPL interface
    │   ├── transform.py              # Data cleaning and transformation
    │   ├── utils.py                  # Helper functions
    │   └── validate.py               # Data quality validation
    ├── outputs/                      # Processed data outputs
    └── sample_data/                  # Example datasets
```

## Prerequisites

- Python 3.8+
- Required packages (install via `pip install -r Task_3/requirements.txt`):
  - pandas
  - openpyxl
  - numpy

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd DE-TRAINING-TASKS
   ```

2. Install dependencies for Task 3:
   ```bash
   cd Task_3
   pip install -r requirements.txt
   ```

## Tasks Overview

### Revenue Tracker Tasks

#### Task 1: Excel Metrics Processing
Automates extraction of financial metrics from Excel files and updates output reports.

**Key Features:**
- Parses Excel sheets for revenue, salary allocation, and workforce cost data
- Calculates percentage metrics automatically
- Updates output Excel file with processed data

**Usage:**
```bash
cd "Revenue Tracker/Task_1"
python update_output.py
```

**Input/Output:**
- Input: `Delta3_Apr.xlsx` (with sheets for different months)
- Output: `Delta3_Ouptut.xlsx` (updated with calculated metrics)

#### Task 2: Multi-File Revenue Mapping
Enhanced version that processes multiple Excel files and maps revenue data across projects.

**Key Features:**
- Processes multiple monthly Excel files
- Maps project revenue data to output template
- Handles data consistency across files

**Usage:**
```bash
cd "Revenue Tracker/Task_2"
python output.py
```

**Input Files:**
- `MIS_Final_April.xlsx`
- `MIS_Final_May.xlsx`
- `MIS_Final_June.xlsx`

**Output:** `Delta3_Ouptut.xlsx`

### Task 3: DataTool CLI

A comprehensive command-line toolkit for data engineering operations on CSV and JSON files.

#### Features

- **Data Ingestion**: Load and summarize datasets
- **Data Validation**: Check for missing values, duplicates, and type inconsistencies
- **Data Transformation**: Clean column names, handle missing data, remove duplicates
- **Interactive REPL**: Command-line interface for exploratory data analysis

#### Commands

```bash
# Display dataset summary
python -m datatool.cli ingest sample_data/sample.csv

# Validate data quality
python -m datatool.cli validate sample_data/sample.csv

# Transform and clean data
python -m datatool.cli transform sample_data/sample.csv outputs/cleaned_sample.csv --missing fill

# Start interactive session
python -m datatool.cli repl
```

#### REPL Commands

Once in interactive mode (`datatool>` prompt):

```
ingest <input_file>           # Load and summarize data
validate <input_file>         # Run quality checks
transform <input_file> <output_file> [--missing drop|fill]  # Clean and save data
help                          # Show available commands
exit                          # Quit REPL
```

#### Supported File Formats

- **CSV**: Comma-separated values
- **JSON**: JSON arrays or JSON Lines format

#### Data Quality Checks

The validation module performs:
- Missing value detection per column
- Duplicate row identification
- Type consistency analysis (detects mixed numeric/text columns)

#### Transformation Options

- **Column Cleaning**: Standardizes column names (lowercase, underscores)
- **Duplicate Removal**: Eliminates duplicate rows
- **Missing Data Handling**:
  - `drop`: Remove rows with missing values
  - `fill`: Impute with median (numeric) or mode (categorical)

## Example Usage

### Processing Sample Data

```bash
cd Task_3

# Ingest and summarize
python -m datatool.cli ingest sample_data/sample.csv
# Output: Number of rows: 5
#         Columns: User name, Age, City, Salary
#         Data types: User name: object, Age: object, City: object, Salary: int64

# Validate data quality
python -m datatool.cli validate sample_data/sample.csv
# Output: Missing values, duplicates, and type issues detected

# Transform data (fill missing values)
python -m datatool.cli transform sample_data/sample.csv outputs/cleaned_sample.csv --missing fill
```

## Development Notes

- **Revenue Tracker**: Focuses on Excel automation using `openpyxl` and `pandas`
- **DataTool**: Modular design with separate concerns (I/O, validation, transformation)
- **Error Handling**: Robust file existence checks and data type validation
- **Extensibility**: Easy to add new file formats or transformation rules

## Contributing

1. Follow Python best practices (PEP 8)
2. Add docstrings to functions
3. Include unit tests for new features
4. Update README for significant changes

## License

This project is for educational purposes. See individual task documentation for usage rights.