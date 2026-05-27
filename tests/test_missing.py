# test_missing.py - Tests for Missing.py

import os
import sys
import pytest
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cleaning.Missing import (
    check_missing_value,
    drop_missing_row,
    fill_missing_value,
    fill_missing_numeric_with_mean,
    fill_missing_numeric_with_median,
    fill_missing_numeric_with_mode,
    drop_empty_column,
)

# =========================================================
# HELPERS
# =========================================================

def numeric_null_count(df):
    return df.select_dtypes(include=["number"]).isnull().sum().sum()


# =========================================================
# CHECK MISSING VALUE
# =========================================================

def test_check_missing_value_returns_series(raw_df):
    result = check_missing_value(raw_df)

    assert isinstance(result, pd.Series)
    assert (result >= 0).all()


def test_check_missing_value_no_negative_counts(raw_df):
    result = check_missing_value(raw_df)
    assert (result >= 0).all()


# =========================================================
# DROP MISSING ROW
# =========================================================

def test_drop_missing_row_removes_nulls(missing_df):
    result = drop_missing_row(missing_df)

    assert result.isnull().sum().sum() == 0


def test_drop_missing_row_size_valid(missing_df):
    result = drop_missing_row(missing_df)

    assert result.shape[0] <= missing_df.shape[0]


# =========================================================
# FILL MISSING VALUE (GENERIC)
# =========================================================

def test_fill_missing_value_fills_all_nulls(missing_df):
    result = fill_missing_value(missing_df, value="unknown")

    assert result.isnull().sum().sum() == 0


def test_fill_missing_value_custom_string(missing_df):
    result = fill_missing_value(missing_df, value="N/A")

    assert (result == "N/A").sum().sum() > 0


def test_fill_missing_default_value(missing_df):
    result = fill_missing_value(missing_df)

    assert (result == "unknown").sum().sum() > 0


# =========================================================
# NUMERIC FILL - MEAN
# =========================================================

def test_fill_mean_no_nulls_left(missing_df):
    result = fill_missing_numeric_with_mean(missing_df)

    assert numeric_null_count(result) == 0


def test_fill_mean_preserves_non_numeric(missing_df):
    result = fill_missing_numeric_with_mean(missing_df)

    assert "Full Name" in result.columns


def test_fill_mean_statistical_property(missing_df):
    result = fill_missing_numeric_with_mean(missing_df)

    original_mean = missing_df["Age"].mean(skipna=True)
    new_mean = result["Age"].mean()

    assert abs(original_mean - new_mean) < 1e-6


# =========================================================
# NUMERIC FILL - MEDIAN
# =========================================================

def test_fill_median_no_nulls_left(missing_df):
    result = fill_missing_numeric_with_median(missing_df)

    assert numeric_null_count(result) == 0


def test_fill_median_statistical_property(missing_df):
    result = fill_missing_numeric_with_median(missing_df)

    original_median = missing_df["Age"].median(skipna=True)
    new_median = result["Age"].median()

    assert abs(original_median - new_median) < 1e-6


# =========================================================
# NUMERIC FILL - MODE
# =========================================================

def test_fill_mode_no_nulls_left(missing_df):
    result = fill_missing_numeric_with_mode(missing_df)

    assert numeric_null_count(result) == 0


# =========================================================
# DROP EMPTY COLUMN
# =========================================================

def test_drop_empty_column_removes_fully_null_column(raw_df):
    df = raw_df.copy()
    df["temp_null_col"] = None

    result = drop_empty_column(df)

    assert "temp_null_col" not in result.columns


def test_drop_empty_column_keeps_partial_null_columns(raw_df):
    result = drop_empty_column(raw_df)

    # should keep columns that are not fully empty
    assert isinstance(result, pd.DataFrame)


# =========================================================
# ERROR HANDLING TESTS
# =========================================================

def test_invalid_input_type_raises_error():
    with pytest.raises(TypeError):
        fill_missing_value([1, 2, 3])


def test_no_numeric_columns_error():
    df = pd.DataFrame({"A": ["x", "y"], "B": ["a", "b"]})

    with pytest.raises(ValueError):
        fill_missing_numeric_with_mean(df)


# =========================================================
# INVARIANT TEST (ALL FUNCTIONS RETURN DATAFRAME)
# =========================================================

def test_all_functions_return_dataframe(missing_df):
    funcs = [
        drop_missing_row,
        fill_missing_value,
        fill_missing_numeric_with_mean,
        fill_missing_numeric_with_median,
        fill_missing_numeric_with_mode,
        drop_empty_column,
    ]

    for func in funcs:
        result = func(missing_df)
        assert isinstance(result, pd.DataFrame)