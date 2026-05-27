# test_duplicates.py - Tests for Duplicates.py

import os
import sys
import pytest
import pandas as pd

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

# =========================
# TYPE SAFETY TESTS
# =========================

def test_count_duplicates_invalid_input():
    with pytest.raises(Exception):
        count_duplicates("not_a_dataframe")


def test_remove_duplicates_by_column_invalid_column(clean_df):
    with pytest.raises(Exception):
        remove_duplicates_by_column(clean_df, "InvalidColumn")


# =========================
# COUNT DUPLICATES
# =========================

def test_count_duplicates_dynamic(raw_df):
    result = count_duplicates(raw_df)

    # must always be >= 0
    assert result >= 0

    # must match pandas logic
    assert result == raw_df.duplicated().sum()


def test_count_duplicates_clean_data(clean_df):
    assert count_duplicates(clean_df) == 0


# =========================
# CHECK DUPLICATES
# =========================

def test_check_duplicates_returns_dataframe(raw_df):
    result = check_duplicates(raw_df)
    assert isinstance(result, pd.DataFrame)


def test_check_duplicates_matches_pandas(raw_df):
    result = check_duplicates(raw_df)

    expected = raw_df[raw_df.duplicated()]

    assert len(result) == len(expected)


# =========================
# REMOVE DUPLICATES
# =========================

def test_remove_duplicates_removes_all(raw_df):
    result = remove_duplicates(raw_df)

    assert result.duplicated().sum() == 0


def test_remove_duplicates_row_count_rule(raw_df):
    result = remove_duplicates(raw_df)

    # must be <= original rows
    assert len(result) <= len(raw_df)


def test_remove_duplicates_clean_data(clean_df):
    result = remove_duplicates(clean_df)
    assert len(result) == len(clean_df)


# =========================
# REMOVE DUPLICATES BY COLUMN
# =========================

def test_remove_duplicates_by_column_dynamic(raw_df):
    result = remove_duplicates_by_column(raw_df, "Full Name")

    assert result["Full Name"].duplicated().sum() == 0


def test_remove_duplicates_by_column_row_reduction(raw_df):
    result = remove_duplicates_by_column(raw_df, "Full Name")

    assert len(result) <= len(raw_df)


# =========================
# KEEP LAST DUPLICATE
# =========================

def test_keep_last_duplicate_removes_dupes(raw_df):
    result = keep_last_duplicate(raw_df)

    assert result.duplicated().sum() == 0


def test_keep_last_duplicate_consistency(raw_df):
    result_last = keep_last_duplicate(raw_df)
    result_first = remove_duplicates(raw_df)

    # both should be same size OR close (order-independent safety)
    assert len(result_last) <= len(raw_df)
    assert len(result_first) <= len(raw_df)


# =========================
# MARK DUPLICATES
# =========================

def test_mark_duplicates_column_added(raw_df):
    result = mark_duplicates(raw_df)

    assert "is_duplicate" in result.columns


def test_mark_duplicates_bool_column(raw_df):
    result = mark_duplicates(raw_df)

    assert set(result["is_duplicate"].dropna().unique()).issubset({True, False})


def test_mark_duplicates_row_preservation(raw_df):
    result = mark_duplicates(raw_df)

    assert len(result) == len(raw_df)


# =========================
# REMOVE FULL DUPLICATES
# =========================

def test_remove_full_duplicates_behavior(raw_df):
    result = remove_full_duplicates(raw_df)

    assert result.duplicated().sum() == 0


def test_remove_full_duplicates_matches_logic(raw_df):
    result1 = remove_full_duplicates(raw_df)
    result2 = remove_duplicates(raw_df)

    assert len(result1) == len(result2)