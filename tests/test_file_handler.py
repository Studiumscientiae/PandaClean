# test_file_handler.py - Tests for file_handler.py

import os
import pytest
import pandas as pd

# Adjust import path based on your project structure
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from File_manager.file_handler import (
    load_excel, load_csv, save_excel, save_csv,
    file_exists, is_excel_file, is_csv_file,
    get_file_extension, file_information
)

DATA_PATH  = os.path.join(os.path.dirname(__file__), "data", "sample_dataset.xlsx")
GHOST_PATH = os.path.join(os.path.dirname(__file__), "data", "ghost_file.xlsx")

EXPECTED_COLUMNS = [
    "Employee ID", "Full Name", "Age", "Department",
    "Salary", "Join Date", "Email", "Phone", "City", "Performance Score"
]


# ==========================================
# LOAD EXCEL
# ==========================================

def test_load_excel_returns_dataframe():
    df = load_excel(DATA_PATH)
    assert df is not None
    assert isinstance(df, pd.DataFrame)

def test_load_excel_correct_shape():
    df = load_excel(DATA_PATH)
    assert df.shape == (53, 10)     # 53 rows, 10 columns from your actual file

def test_load_excel_has_expected_columns():
    df = load_excel(DATA_PATH)
    assert list(df.columns) == EXPECTED_COLUMNS

def test_load_excel_file_not_found():
    # Should return None and print error (current behaviour)
    result = load_excel(GHOST_PATH)
    assert result is None


# ==========================================
# LOAD CSV
# ==========================================

def test_load_csv_file_not_found():
    result = load_csv("tests/data/ghost.csv")
    assert result is None


# ==========================================
# SAVE EXCEL
# ==========================================

def test_save_excel_creates_file(raw_df, tmp_path):
    out = str(tmp_path / "output.xlsx")
    save_excel(raw_df, out)
    assert os.path.exists(out)

def test_save_excel_reloadable(raw_df, tmp_path):
    out = str(tmp_path / "output.xlsx")
    save_excel(raw_df, out)
    reloaded = pd.read_excel(out)
    assert reloaded.shape == raw_df.shape
    assert list(reloaded.columns) == list(raw_df.columns)


# ==========================================
# SAVE CSV
# ==========================================

def test_save_csv_creates_file(raw_df, tmp_path):
    out = str(tmp_path / "output.csv")
    save_csv(raw_df, out)
    assert os.path.exists(out)

def test_save_csv_reloadable(raw_df, tmp_path):
    out = str(tmp_path / "output.csv")
    save_csv(raw_df, out)
    reloaded = pd.read_csv(out)
    assert reloaded.shape == raw_df.shape


# ==========================================
# FILE CHECKS
# ==========================================

def test_file_exists_true():
    assert file_exists(DATA_PATH) == True

def test_file_exists_false():
    assert file_exists(GHOST_PATH) == False

def test_is_excel_file_true():
    assert is_excel_file(DATA_PATH) == True

def test_is_excel_file_false():
    assert is_excel_file("data.csv") == False

def test_is_csv_file_true():
    assert is_csv_file("data.csv") == True

def test_is_csv_file_false():
    assert is_csv_file(DATA_PATH) == False

def test_get_file_extension_xlsx():
    assert get_file_extension(DATA_PATH) == ".xlsx"

def test_get_file_extension_csv():
    assert get_file_extension("data.csv") == ".csv"


# ==========================================
# FILE INFORMATION
# ==========================================

def test_file_information_runs_without_error(raw_df, capsys):
    # capsys captures print output — no crash = pass
    file_information(raw_df)
    captured = capsys.readouterr()
    assert "Shape" in captured.out
    assert "Column Names" in captured.out