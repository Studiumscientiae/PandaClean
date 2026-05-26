# test_duplicates.py - Tests for Duplicates.py

import os
import pytest
import pandas as pd

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cleaning.Duplicates import (
    check_duplicates,
    count_duplicates,
    remove_duplicates,
    remove_duplicates_by_column,
    keep_last_duplicate,
    mark_duplicates,
    remove_full_duplicates,
)


# ==========================================
# COUNT DUPLICATES
# ==========================================

def test_count_duplicates_on_actual_file(raw_df):
    # Your file has rows 51 & 52 as exact duplicates of row 50 (EMP-5)
    count = count_duplicates(raw_df)
    assert count == 2

def test_count_duplicates_on_controlled_data(duplicate_df):
    # duplicate_df has 2 duplicate rows of EMP-5
    count = count_duplicates(duplicate_df)
    assert count == 2

def test_count_duplicates_on_clean_data(clean_df):
    assert count_duplicates(clean_df) == 0


# ==========================================
# CHECK DUPLICATES
# ==========================================

def test_check_duplicates_returns_dataframe(raw_df):
    result = check_duplicates(raw_df)
    assert isinstance(result, pd.DataFrame)

def test_check_duplicates_correct_count(raw_df):
    result = check_duplicates(raw_df)
    assert len(result) == 2

def test_check_duplicates_correct_employee(raw_df):
    result = check_duplicates(raw_df)
    # The duplicated rows are EMP-5 Aman Sharma
    assert all(result["Full Name"] == "Aman Sharma")


# ==========================================
# REMOVE DUPLICATES
# ==========================================

def test_remove_duplicates_leaves_no_duplicates(raw_df):
    result = remove_duplicates(raw_df)
    assert result.duplicated().sum() == 0

def test_remove_duplicates_reduces_row_count(raw_df):
    result = remove_duplicates(raw_df)
    assert len(result) == 51       # 53 rows - 2 duplicates = 51

def test_remove_duplicates_on_clean_data(clean_df):
    result = remove_duplicates(clean_df)
    assert len(result) == len(clean_df)     # nothing removed


# ==========================================
# REMOVE DUPLICATES BY COLUMN
# ==========================================

def test_remove_duplicates_by_column_full_name(raw_df):
    result = remove_duplicates_by_column(raw_df, "Full Name")
    assert result["Full Name"].duplicated().sum() == 0

def test_remove_duplicates_by_column_reduces_rows(raw_df):
    original = len(raw_df)
    result   = remove_duplicates_by_column(raw_df, "Full Name")
    assert len(result) < original

def test_remove_duplicates_by_column_department(raw_df):
    result = remove_duplicates_by_column(raw_df, "Department")
    assert result["Department"].duplicated().sum() == 0


# ==========================================
# KEEP LAST DUPLICATE
# ==========================================

def test_keep_last_removes_duplicates(raw_df):
    result = keep_last_duplicate(raw_df)
    assert result.duplicated().sum() == 0

def test_keep_last_same_row_count_as_remove(raw_df):
    # keep_last and remove_duplicates should give same row count
    result_last  = keep_last_duplicate(raw_df)
    result_first = remove_duplicates(raw_df)
    assert len(result_last) == len(result_first)

def test_keep_last_retains_last_occurrence(duplicate_df):
    # EMP-5 appears at index 0, 1, 2 — after keep_last, index 2 stays
    result = keep_last_duplicate(duplicate_df)
    emp5_rows = result[result["Employee ID"] == "EMP-5"]
    assert len(emp5_rows) == 1
    assert emp5_rows.index[0] == 2


# ==========================================
# MARK DUPLICATES
# ==========================================

def test_mark_duplicates_adds_column(raw_df):
    result = mark_duplicates(raw_df)
    assert "is_duplicate" in result.columns

def test_mark_duplicates_column_is_bool(raw_df):
    result = mark_duplicates(raw_df)
    assert result["is_duplicate"].dtype == bool

def test_mark_duplicates_correct_true_count(raw_df):
    result = mark_duplicates(raw_df)
    assert result["is_duplicate"].sum() == 2

def test_mark_duplicates_does_not_remove_rows(raw_df):
    result = mark_duplicates(raw_df)
    assert len(result) == len(raw_df)


# ==========================================
# REMOVE FULL DUPLICATES
# ==========================================

def test_remove_full_duplicates_same_as_remove(raw_df):
    result1 = remove_full_duplicates(raw_df)
    result2 = remove_duplicates(raw_df)
    assert len(result1) == len(result2)

def test_remove_full_duplicates_no_duplicates_remain(raw_df):
    result = remove_full_duplicates(raw_df)
    assert result.duplicated().sum() == 0