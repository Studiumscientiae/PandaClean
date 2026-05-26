# test_datatype.py - Tests for Datatype.py

import os
import pytest
import pandas as pd

import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cleaning.Datatype import (
    convert_to_integer,
    convert_to_float,
    convert_to_string,
    convert_to_datetime,
    convert_to_boolean,
    check_datatypes,
    find_invalid_numeric_values,
    remove_currency_symbols,
)


# ==========================================
# CONVERT TO INTEGER
# ==========================================

def test_convert_to_integer_changes_dtype():
    df = pd.DataFrame({
        "Age": ["10", "20", "30"]
    })

    result = convert_to_integer(df.copy(), "Age")

    assert str(result["Age"].dtype) == "Int64"


def test_convert_to_integer_invalid_values_become_nan():
    df = pd.DataFrame({
        "Age": ["10", "abc", "30"]
    })

    result = convert_to_integer(df.copy(), "Age")

    assert pd.isna(result["Age"][1])


def test_convert_to_integer_valid_conversion():
    df = pd.DataFrame({
        "Age": ["10", "20"]
    })

    result = convert_to_integer(df.copy(), "Age")

    assert result["Age"].tolist() == [10, 20]


# ==========================================
# CONVERT TO FLOAT
# ==========================================

def test_convert_to_float_changes_dtype():
    df = pd.DataFrame({
        "Salary": ["1000.5", "2000.8"]
    })

    result = convert_to_float(df.copy(), "Salary")

    assert pd.api.types.is_float_dtype(result["Salary"])


def test_convert_to_float_invalid_values_become_nan():
    df = pd.DataFrame({
        "Salary": ["1000.5", "invalid"]
    })

    result = convert_to_float(df.copy(), "Salary")

    assert pd.isna(result["Salary"][1])


def test_convert_to_float_valid_conversion():
    df = pd.DataFrame({
        "Salary": ["1000.5", "2000.8"]
    })

    result = convert_to_float(df.copy(), "Salary")

    assert result["Salary"].tolist() == [1000.5, 2000.8]


# ==========================================
# CONVERT TO STRING
# ==========================================

def test_convert_to_string_changes_dtype():
    df = pd.DataFrame({
        "Code": [101, 102]
    })

    result = convert_to_string(df.copy(), "Code")

    assert str(result["Code"].dtype) in ["object", "string","str"]


def test_convert_to_string_converts_values():
    df = pd.DataFrame({
        "Code": [101, 102]
    })

    result = convert_to_string(df.copy(), "Code")

    assert result["Code"].tolist() == ["101", "102"]


# ==========================================
# CONVERT TO DATETIME
# ==========================================

def test_convert_to_datetime_changes_dtype():
    df = pd.DataFrame({
        "Joining Date": ["2024-01-01", "2024-02-01"]
    })

    result = convert_to_datetime(df.copy(), "Joining Date")

    assert pd.api.types.is_datetime64_any_dtype(result["Joining Date"])


def test_convert_to_datetime_invalid_values_become_nat():
    df = pd.DataFrame({
        "Joining Date": ["2024-01-01", "invalid-date"]
    })

    result = convert_to_datetime(df.copy(), "Joining Date")

    assert pd.isna(result["Joining Date"][1])


# ==========================================
# CONVERT TO BOOLEAN
# ==========================================

def test_convert_to_boolean_changes_dtype():
    df = pd.DataFrame({
        "Active": [1, 0, 1]
    })

    result = convert_to_boolean(df.copy(), "Active")

    assert result["Active"].dtype == bool


def test_convert_to_boolean_conversion():
    df = pd.DataFrame({
        "Active": [1, 0]
    })

    result = convert_to_boolean(df.copy(), "Active")

    assert result["Active"].tolist() == [True, False]


# ==========================================
# CHECK DATATYPES
# ==========================================

def test_check_datatypes_returns_series(clean_df):
    result = check_datatypes(clean_df)

    assert isinstance(result, pd.Series)


def test_check_datatypes_contains_columns(clean_df):
    result = check_datatypes(clean_df)

    assert "Employee ID" in result.index


# ==========================================
# FIND INVALID NUMERIC VALUES
# ==========================================

def test_find_invalid_numeric_values_returns_dataframe():
    df = pd.DataFrame({
        "Salary": ["1000", "abc", "3000"]
    })

    result = find_invalid_numeric_values(df.copy(), "Salary")

    assert isinstance(result, pd.DataFrame)


def test_find_invalid_numeric_values_correct_count():
    df = pd.DataFrame({
        "Salary": ["1000", "abc", "xyz"]
    })

    result = find_invalid_numeric_values(df.copy(), "Salary")

    assert len(result) == 2


def test_find_invalid_numeric_values_correct_rows():
    df = pd.DataFrame({
        "Salary": ["1000", "abc", "xyz"]
    })

    result = find_invalid_numeric_values(df.copy(), "Salary")

    assert result["Salary"].tolist() == ["abc", "xyz"]


# ==========================================
# REMOVE CURRENCY SYMBOLS
# ==========================================

def test_remove_currency_symbols_removes_dollar():
    df = pd.DataFrame({
        "Salary": ["$1000", "$2000"]
    })

    result = remove_currency_symbols(df.copy(), "Salary")

    assert result["Salary"].tolist() == ["1000", "2000"]


def test_remove_currency_symbols_removes_commas():
    df = pd.DataFrame({
        "Salary": ["1,000", "2,500"]
    })

    result = remove_currency_symbols(df.copy(), "Salary")

    assert result["Salary"].tolist() == ["1000", "2500"]


def test_remove_currency_symbols_keeps_numbers():
    df = pd.DataFrame({
        "Salary": ["₹5,000.50"]
    })

    result = remove_currency_symbols(df.copy(), "Salary")

    assert result["Salary"][0] == "5000.50"