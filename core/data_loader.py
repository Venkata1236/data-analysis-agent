# core/data_loader.py
# Loads and validates CSV files for the Data Analysis Agent
# Makes the dataframe globally accessible to all custom tools

import pandas as pd
import os

# Global dataframe — shared across all tools
_dataframe = None
_filename = ""


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Loads a CSV file into a global pandas DataFrame.
    All custom tools access this shared dataframe.

    Args:
        file_path: path to the CSV file

    Returns:
        pandas DataFrame
    """
    global _dataframe, _filename

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.endswith(".csv"):
        raise ValueError("Only CSV files are supported.")

    _dataframe = pd.read_csv(file_path)
    _filename = os.path.basename(file_path)

    print(f"✅ Loaded {_filename}: {len(_dataframe)} rows × {len(_dataframe.columns)} columns")
    print(f"   Columns: {list(_dataframe.columns)}")

    return _dataframe


def load_csv_from_bytes(file_bytes: bytes, filename: str) -> pd.DataFrame:
    """
    Loads a CSV from raw bytes (for Streamlit file uploader).

    Args:
        file_bytes: raw bytes of the CSV
        filename  : name of the file

    Returns:
        pandas DataFrame
    """
    global _dataframe, _filename
    import io

    _dataframe = pd.read_csv(io.BytesIO(file_bytes))
    _filename = filename

    print(f"✅ Loaded {_filename}: {len(_dataframe)} rows × {len(_dataframe.columns)} columns")

    return _dataframe


def get_dataframe() -> pd.DataFrame:
    """Returns the currently loaded dataframe."""
    global _dataframe
    if _dataframe is None:
        raise ValueError("No CSV loaded. Please load a CSV file first.")
    return _dataframe


def get_filename() -> str:
    """Returns the currently loaded filename."""
    return _filename


def get_dataframe_info() -> str:
    """
    Returns a summary of the loaded dataframe.
    Used to give the agent context about the data.
    """
    global _dataframe, _filename
    if _dataframe is None:
        return "No CSV loaded."

    info = f"""
Dataset: {_filename}
Rows: {len(_dataframe)}
Columns: {len(_dataframe.columns)}
Column names: {list(_dataframe.columns)}
Data types: {_dataframe.dtypes.to_dict()}
Sample data (first 3 rows):
{_dataframe.head(3).to_string()}
    """
    return info.strip()