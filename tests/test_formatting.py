# test_formatting.py - Tests for Formatting.py

import os
import pytest
import pandas as pd

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from cleaning.Formatting import (
    format_column_name,
    remove_extra_spaces,
    convert_to_lowercase,
    convert_to_uppercase,
    convert_to_titlecase,
    replace_column_name,
    remove_special_characters,
    remove_multiple_spaces,
)


# ==========================================
# FORMAT COLUMN NAME
# ==========================================

def test_format_column_name_no_spaces(raw_df):
    result = format_column_name(raw_df)
    for col in result.columns:
        assert " " not in col           # spaces replaced with _

def test_format_column_name_is_title_case(raw_df):
    result = format_column_name(raw_df)
    # e.g. "Full Name" → "Full_Name" — first letter of each word is upper
    for col in result.columns:
        parts = col.split("_")
        for part in parts:
            assert part[0].isupper()

def test_format_column_name_no_leading_trailing_spaces(raw_df):
    result = format_column_name(raw_df)
    for col in result.columns:
        assert col == col.strip()

def test_format_column_name_returns_dataframe(raw_df):
    result = format_column_name(raw_df)
    assert isinstance(result, pd.DataFrame)


# ==========================================
# REMOVE EXTRA SPACES (column names)
# ==========================================

def test_remove_extra_spaces_strips_columns():
    df = pd.DataFrame({"  Full Name  ": [1], " Age ": [2]})
    result = remove_extra_spaces(df)
    for col in result.columns:
        assert col == col.strip()

def test_remove_extra_spaces_no_change_on_clean(raw_df):
    result = remove_extra_spaces(raw_df)
    assert list(result.columns) == list(raw_df.columns)


# ==========================================
# CONVERT TO LOWERCASE
# ==========================================

def test_convert_to_lowercase_city(raw_df):
    result = convert_to_lowercase(raw_df, "City")
    valid  = result["City"].dropna()
    assert all(valid == valid.str.lower())

def test_convert_to_lowercase_department(raw_df):
    result = convert_to_lowercase(raw_df, "Department")
    valid  = result["Department"].dropna()
    assert all(valid == valid.str.lower())

def test_convert_to_lowercase_on_clean_df(clean_df):
    result = convert_to_lowercase(clean_df, "Full Name")
    assert result["Full Name"].iloc[0] == "aman sharma"


# ==========================================
# CONVERT TO UPPERCASE
# ==========================================

def test_convert_to_uppercase_city(raw_df):
    result = convert_to_uppercase(raw_df, "City")
    valid  = result["City"].dropna()
    assert all(valid == valid.str.upper())

def test_convert_to_uppercase_on_clean_df(clean_df):
    result = convert_to_uppercase(clean_df, "Full Name")
    assert result["Full Name"].iloc[0] == "AMAN SHARMA"


# ==========================================
# CONVERT TO TITLE CASE
# ==========================================

def test_convert_to_titlecase_city(raw_df):
    # Your file has mixed case cities like "delhi", "Delhi", "DELHI"
    result = convert_to_titlecase(raw_df, "City")
    valid  = result["City"].dropna()
    assert all(valid == valid.str.title())

def test_convert_to_titlecase_normalises_delhi(raw_df):
    result = convert_to_titlecase(raw_df, "City")
    city_values = result["City"].dropna().unique()
    # After title case, "delhi" and "Delhi" both become "Delhi"
    assert "delhi" not in city_values
    assert "Delhi" in city_values


# ==========================================
# REPLACE COLUMN VALUE
# ==========================================

def test_replace_column_name_changes_value(raw_df):
    result = replace_column_name(raw_df, "Department", "IT", "Information Technology")
    assert "IT" not in result["Department"].dropna().values
    assert "Information Technology" in result["Department"].values

def test_replace_column_name_no_side_effects(clean_df):
    original_len = len(clean_df)
    result = replace_column_name(clean_df, "Department", "HR", "Human Resources")
    assert len(result) == original_len      # row count unchanged

def test_replace_column_name_city(raw_df):
    result = replace_column_name(raw_df, "City", "delhi", "Delhi")
    assert "delhi" not in result["City"].dropna().values


# ==========================================
# REMOVE SPECIAL CHARACTERS
# ==========================================

def test_remove_special_characters_from_email(raw_df):
    # inject special chars
    raw_df["Email"] = raw_df["Email"].fillna("").str.replace("@", "#test@")
    result = remove_special_characters(raw_df, "Email")
    assert result["Email"].str.contains("#").sum() == 0

def test_remove_special_characters_on_clean_df(clean_df):
    clean_df["Full Name"] = ["Ali@ce!", "B#ob", "Char$lie"]
    result = remove_special_characters(clean_df, "Full Name")
    for val in result["Full Name"]:
        assert "@" not in val
        assert "#" not in val
        assert "$" not in val

def test_remove_special_characters_keeps_alphanumeric(clean_df):
    clean_df["Full Name"] = ["Alice123", "Bob456", "Charlie789"]
    result = remove_special_characters(clean_df, "Full Name")
    assert list(result["Full Name"]) == ["Alice123", "Bob456", "Charlie789"]


# ==========================================
# REMOVE MULTIPLE SPACES
# ==========================================

def test_remove_multiple_spaces_between_words(clean_df):
    clean_df["Full Name"] = ["Aman  Sharma", "Priya   Singh", "Neha Joshi"]
    result = remove_multiple_spaces(clean_df, "Full Name")
    for val in result["Full Name"]:
        assert "  " not in val          # no double spaces

def test_remove_multiple_spaces_result_correct(clean_df):
    clean_df["Full Name"] = ["Aman   Sharma", "Priya Singh", "Neha  Joshi"]
    result = remove_multiple_spaces(clean_df, "Full Name")
    assert result["Full Name"].iloc[0] == "Aman Sharma"
    assert result["Full Name"].iloc[2] == "Neha Joshi"