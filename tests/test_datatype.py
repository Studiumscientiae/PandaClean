# test_datatype.py - Tests for Datatype.py

import os
import sys
import pytest
import pandas as pd

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
# HELPER: error response checker
# ==========================================

def is_error(result):
    return isinstance(result, str)


# ==========================================
# CONVERT TO INTEGER
# ==========================================

def test_convert_to_integer_changes_dtype():
    df = pd.DataFrame({"Age": ["10", "20", "30"]})

    result = convert_to_integer(df.copy(), "Age")

    assert not is_error(result)
    assert str(result["Age"].dtype) == "Int64"


def test_convert_to_integer_invalid_column():
    df = pd.DataFrame({"Age": ["10", "20"]})

    result = convert_to_integer(df.copy(), "WrongColumn")

    assert is_error(result)


def test_convert_to_integer_invalid_values():
    df = pd.DataFrame({"Age": ["10", "abc", "30"]})

    result = convert_to_integer(df.copy(), "Age")

    assert not is_error(result)
    assert pd.isna(result["Age"][1])


# ==========================================
# CONVERT TO FLOAT
# ==========================================

def test_convert_to_float_changes_dtype():
    df = pd.DataFrame({"Salary": ["1000.5", "2000.8"]})

    result = convert_to_float(df.copy(), "Salary")

    assert not is_error(result)
    assert pd.api.types.is_float_dtype(result["Salary"])


def test_convert_to_float_invalid_values():
    df = pd.DataFrame({"Salary": ["1000.5", "invalid"]})

    result = convert_to_float(df.copy(), "Salary")

    assert not is_error(result)
    assert pd.isna(result["Salary"][1])


# ==========================================
# CONVERT TO STRING
# ==========================================

def test_convert_to_string_changes_dtype():
    df = pd.DataFrame({"Code": [101, 102]})

    result = convert_to_string(df.copy(), "Code")

    assert not is_error(result)

    assert (
        pd.api.types.is_object_dtype(result["Code"]) or
        pd.api.types.is_string_dtype(result["Code"]))


def test_convert_to_string_values():
    df = pd.DataFrame({"Code": [101, 102]})

    result = convert_to_string(df.copy(), "Code")

    assert not is_error(result)
    assert result["Code"].tolist() == ["101", "102"]


# ==========================================
# CONVERT TO DATETIME
# ==========================================

def test_convert_to_datetime_changes_dtype():
    df = pd.DataFrame({"Joining Date": ["2024-01-01", "2024-02-01"]})

    result = convert_to_datetime(df.copy(), "Joining Date")

    assert not is_error(result)
    assert pd.api.types.is_datetime64_any_dtype(result["Joining Date"])


def test_convert_to_datetime_invalid_values():
    df = pd.DataFrame({"Joining Date": ["2024-01-01", "invalid"]})

    result = convert_to_datetime(df.copy(), "Joining Date")

    assert not is_error(result)
    assert pd.isna(result["Joining Date"][1])


# ==========================================
# CONVERT TO BOOLEAN
# ==========================================

def test_convert_to_boolean_changes_dtype():
    df = pd.DataFrame({"Active": [1, 0, 1]})

    result = convert_to_boolean(df.copy(), "Active")

    assert not is_error(result)
    assert result["Active"].dtype == bool


def test_convert_to_boolean_values():
    df = pd.DataFrame({"Active": [1, 0]})

    result = convert_to_boolean(df.copy(), "Active")

    assert not is_error(result)
    assert result["Active"].tolist() == [True, False]


# ==========================================
# CHECK DATATYPES
# ==========================================

def test_check_datatypes_returns_series():
    df = pd.DataFrame({"A": [1, 2]})

    result = check_datatypes(df)

    assert isinstance(result, pd.Series)


def test_check_datatypes_invalid_input():
    result = check_datatypes("not_a_df")

    assert isinstance(result, str)


# ==========================================
# FIND INVALID NUMERIC VALUES
# ==========================================

def test_find_invalid_numeric_values_count():
    df = pd.DataFrame({"Salary": ["1000", "abc", "xyz"]})

    result = find_invalid_numeric_values(df.copy(), "Salary")

    assert not is_error(result)
    assert len(result) == 2


def test_find_invalid_numeric_values_rows():
    df = pd.DataFrame({"Salary": ["1000", "abc", "xyz"]})

    result = find_invalid_numeric_values(df.copy(), "Salary")

    assert not is_error(result)
    assert result["Salary"].tolist() == ["abc", "xyz"]


# ==========================================
# REMOVE CURRENCY SYMBOLS
# ==========================================

def test_remove_currency_symbols_basic():
    df = pd.DataFrame({"Salary": ["$1000", "$2000"]})

    result = remove_currency_symbols(df.copy(), "Salary")

    assert not is_error(result)
    assert result["Salary"].tolist() == ["1000", "2000"]


def test_remove_currency_symbols_commas():
    df = pd.DataFrame({"Salary": ["1,000", "2,500"]})

    result = remove_currency_symbols(df.copy(), "Salary")

    assert not is_error(result)
    assert result["Salary"].tolist() == ["1000", "2500"]


def test_remove_currency_symbols_currency_symbol():
    df = pd.DataFrame({"Salary": ["₹5,000.50"]})

    result = remove_currency_symbols(df.copy(), "Salary")

    assert not is_error(result)
    assert result["Salary"][0] == "5000.50"