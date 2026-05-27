# test_file_handler.py - Tests for file_handler.py

import os
import sys
import pytest
import pandas as pd

# Adjust import path based on your project structure
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from File_manager.file_handler import (
    load_excel,
    load_csv,
    save_excel,
    save_csv,
    file_exists,
    is_excel_file,
    is_csv_file,
    get_file_extension,
    file_information
)

# ==========================================
# TEST FILE PATHS
# ==========================================

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "data",
    "sample_dataset.xlsx"
)

GHOST_PATH = os.path.join(
    os.path.dirname(__file__),
    "data",
    "ghost_file.xlsx"
)

CSV_GHOST_PATH = os.path.join(
    os.path.dirname(__file__),
    "data",
    "ghost.csv"
)


# ==========================================
# FIXTURE
# ==========================================

@pytest.fixture
def raw_df():
    return pd.DataFrame({
        "A": [1, 2, 3],
        "B": ["x", "y", "z"]
    })


# ==========================================
# LOAD EXCEL
# ==========================================

def test_load_excel_returns_dataframe():
    df = load_excel(DATA_PATH)

    assert isinstance(df, pd.DataFrame)


def test_load_excel_correct_shape():
    original_df = pd.read_excel(DATA_PATH)
    loaded_df = load_excel(DATA_PATH)

    assert loaded_df.shape == original_df.shape


def test_load_excel_has_same_columns_as_source():
    original_df = pd.read_excel(DATA_PATH)
    loaded_df = load_excel(DATA_PATH)

    assert list(loaded_df.columns) == list(original_df.columns)


def test_load_excel_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_excel(GHOST_PATH)


def test_load_excel_invalid_input_type():
    with pytest.raises(TypeError):
        load_excel(123)


def test_load_excel_wrong_extension():
    with pytest.raises(ValueError):
        load_excel("sample.csv")


# ==========================================
# LOAD CSV
# ==========================================

def test_load_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_csv(CSV_GHOST_PATH)


def test_load_csv_invalid_input_type():
    with pytest.raises(TypeError):
        load_csv(123)


def test_load_csv_wrong_extension():
    with pytest.raises(ValueError):
        load_csv("sample.xlsx")


# ==========================================
# SAVE EXCEL
# ==========================================

def test_save_excel_creates_file(raw_df, tmp_path):
    output_path = str(tmp_path / "output.xlsx")

    result = save_excel(raw_df, output_path)

    assert result is True
    assert os.path.exists(output_path)


def test_save_excel_reloadable(raw_df, tmp_path):
    output_path = str(tmp_path / "output.xlsx")

    save_excel(raw_df, output_path)

    reloaded_df = pd.read_excel(output_path)

    assert reloaded_df.shape == raw_df.shape
    assert list(reloaded_df.columns) == list(raw_df.columns)


def test_save_excel_invalid_dataframe(tmp_path):
    output_path = str(tmp_path / "output.xlsx")

    with pytest.raises(TypeError):
        save_excel("not_a_dataframe", output_path)


def test_save_excel_invalid_output_path(raw_df):
    with pytest.raises(TypeError):
        save_excel(raw_df, 123)


# ==========================================
# SAVE CSV
# ==========================================

def test_save_csv_creates_file(raw_df, tmp_path):
    output_path = str(tmp_path / "output.csv")

    result = save_csv(raw_df, output_path)

    assert result is True
    assert os.path.exists(output_path)


def test_save_csv_reloadable(raw_df, tmp_path):
    output_path = str(tmp_path / "output.csv")

    save_csv(raw_df, output_path)

    reloaded_df = pd.read_csv(output_path)

    assert reloaded_df.shape == raw_df.shape
    assert list(reloaded_df.columns) == list(raw_df.columns)


def test_save_csv_invalid_dataframe(tmp_path):
    output_path = str(tmp_path / "output.csv")

    with pytest.raises(TypeError):
        save_csv("not_a_dataframe", output_path)


def test_save_csv_invalid_output_path(raw_df):
    with pytest.raises(TypeError):
        save_csv(raw_df, 123)


# ==========================================
# FILE EXISTS
# ==========================================

def test_file_exists_true():
    assert file_exists(DATA_PATH) is True


def test_file_exists_false():
    assert file_exists(GHOST_PATH) is False


def test_file_exists_invalid_type():
    with pytest.raises(TypeError):
        file_exists(123)


# ==========================================
# GET FILE EXTENSION
# ==========================================

def test_get_file_extension_xlsx():
    assert get_file_extension(DATA_PATH) == ".xlsx"


def test_get_file_extension_csv():
    assert get_file_extension("data.csv") == ".csv"


def test_get_file_extension_invalid_type():
    with pytest.raises(TypeError):
        get_file_extension(123)


# ==========================================
# CSV FILE CHECK
# ==========================================

def test_is_csv_file_true():
    assert is_csv_file("data.csv") is True


def test_is_csv_file_false():
    assert is_csv_file(DATA_PATH) is False


def test_is_csv_file_invalid_type():
    with pytest.raises(TypeError):
        is_csv_file(123)


# ==========================================
# EXCEL FILE CHECK
# ==========================================

def test_is_excel_file_true():
    assert is_excel_file(DATA_PATH) is True


def test_is_excel_file_false():
    assert is_excel_file("data.csv") is False


def test_is_excel_file_invalid_type():
    with pytest.raises(TypeError):
        is_excel_file(123)


# ==========================================
# FILE INFORMATION
# ==========================================

def test_file_information_returns_dictionary(raw_df):
    info = file_information(raw_df)

    assert isinstance(info, dict)


def test_file_information_contains_keys(raw_df):
    info = file_information(raw_df)

    assert "shape" in info
    assert "columns" in info
    assert "dtypes" in info


def test_file_information_correct_shape(raw_df):
    info = file_information(raw_df)

    assert info["shape"] == (3, 2)


def test_file_information_correct_columns(raw_df):
    info = file_information(raw_df)

    assert info["columns"] == ["A", "B"]


def test_file_information_invalid_input():
    with pytest.raises(TypeError):
        file_information("not_a_dataframe")