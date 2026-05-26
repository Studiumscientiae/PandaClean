# test_missing.py - Tests for Missing.py

import os
import pytest
import pandas as pd

import sys
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


# ==========================================
# CHECK MISSING VALUE
# ==========================================

def test_check_missing_detects_nulls(raw_df):
    result = check_missing_value(raw_df)
    # From your actual file — these columns have nulls
    assert result["Employee ID"] == 13
    assert result["Salary"]      == 14
    assert result["Join Date"]   == 19
    assert result["Email"]       == 16
    assert result["Phone"]       == 13

def test_check_missing_returns_series(raw_df):
    result = check_missing_value(raw_df)
    assert isinstance(result, pd.Series)

def test_check_missing_full_name_has_no_nulls(raw_df):
    result = check_missing_value(raw_df)
    assert result["Full Name"] == 0     # Full Name has no missing values


# ==========================================
# DROP MISSING ROW
# ==========================================

def test_drop_missing_row_removes_all_nulls(missing_df):
    result = drop_missing_row(missing_df)
    assert result.isnull().sum().sum() == 0

def test_drop_missing_row_reduces_count(missing_df):
    original = len(missing_df)
    result   = drop_missing_row(missing_df)
    assert len(result) < original

def test_drop_missing_row_on_actual_file(raw_df):
    result = drop_missing_row(raw_df)
    assert result.isnull().sum().sum() == 0


# ==========================================
# FILL MISSING VALUE
# ==========================================

def test_fill_missing_value_fills_all_nulls(missing_df):
    result = fill_missing_value(missing_df, value="unknown")
    assert result.isnull().sum().sum() == 0

def test_fill_missing_value_correct_string(missing_df):
    result = fill_missing_value(missing_df, value="N/A")
    assert "N/A" in result["Full Name"].values

def test_fill_missing_value_numeric(missing_df):
    result = fill_missing_value(missing_df, value=0)
    assert 0 in result["Age"].values

def test_fill_missing_default_value_is_unknown(missing_df):
    result = fill_missing_value(missing_df)
    assert "unknown" in result["Full Name"].values


# ==========================================
# FILL MISSING NUMERIC WITH MEAN
# ==========================================

def test_fill_mean_removes_numeric_nulls(missing_df):
    result      = fill_missing_numeric_with_mean(missing_df)
    numeric_cols = result.select_dtypes(include=["number"]).columns
    assert result[numeric_cols].isnull().sum().sum() == 0

def test_fill_mean_value_is_correct(missing_df):
    # Age: [35, None, 29] → mean = 32.0
    result = fill_missing_numeric_with_mean(missing_df)
    assert result["Age"].iloc[1] == 32.0

def test_fill_mean_does_not_touch_non_numeric(missing_df):
    result = fill_missing_numeric_with_mean(missing_df)
    # Full Name and Department are strings — still has nulls
    assert result["Full Name"].isnull().sum() > 0


# ==========================================
# FILL MISSING NUMERIC WITH MEDIAN
# ==========================================

def test_fill_median_removes_numeric_nulls(missing_df):
    result       = fill_missing_numeric_with_median(missing_df)
    numeric_cols = result.select_dtypes(include=["number"]).columns
    assert result[numeric_cols].isnull().sum().sum() == 0

def test_fill_median_value_is_correct(missing_df):
    # Age: [35, None, 29] → median = 32.0
    result = fill_missing_numeric_with_median(missing_df)
    assert result["Age"].iloc[1] == 32.0


# ==========================================
# FILL MISSING NUMERIC WITH MODE
# ==========================================

def test_fill_mode_removes_numeric_nulls(missing_df):
    result       = fill_missing_numeric_with_mode(missing_df)
    numeric_cols = result.select_dtypes(include=["number"]).columns
    assert result[numeric_cols].isnull().sum().sum() == 0


# ==========================================
# DROP EMPTY COLUMN
# ==========================================

def test_drop_empty_column_removes_all_null_col(raw_df):
    raw_df["AllNullCol"] = None       # inject a fully empty column
    result = drop_empty_column(raw_df)
    assert "AllNullCol" not in result.columns

def test_drop_empty_column_keeps_partial_null_cols(raw_df):
    result = drop_empty_column(raw_df)
    # Employee ID has some nulls but not all — must be kept
    assert "Employee ID" in result.columns

def test_drop_empty_column_returns_dataframe(raw_df):
    result = drop_empty_column(raw_df)
    assert isinstance(result, pd.DataFrame)