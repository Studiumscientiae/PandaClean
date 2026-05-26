# conftest.py - Shared fixtures for all tests.

import pytest
import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_dataset.xlsx")


# ==========================================
# RAW DATAFRAME — loads actual messy file
# Fresh copy every test so no test pollutes another
# ==========================================

@pytest.fixture
def raw_df():
    return pd.read_excel(DATA_PATH)


# ==========================================
# CLEAN DATAFRAME — simple controlled data
# Used for formatting/datatype tests that
# don't need the full messy file
# ==========================================

@pytest.fixture
def clean_df():
    return pd.DataFrame({
        "Employee ID":        ["EMP-1", "EMP-2", "EMP-3"],
        "Full Name":          ["Aman Sharma", "Priya Singh", "Neha Joshi"],
        "Age":                [35, 41, 29],
        "Department":         ["IT", "Marketing", "HR"],
        "Salary":             [82000.0, 55000.0, 70000.0],
        "City":               ["Delhi", "Mumbai", "Bangalore"],
        "Performance Score":  [3.7, 4.5, 3.2],
    })


# ==========================================
# DUPLICATE DATAFRAME — controlled duplicates
# Rows 0 and 1 are exact duplicates intentionally
# ==========================================

@pytest.fixture
def duplicate_df():
    return pd.DataFrame({
        "Employee ID": ["EMP-5", "EMP-5", "EMP-5", "EMP-6"],
        "Full Name":   ["Aman Sharma", "Aman Sharma", "Aman Sharma", "Priya Singh"],
        "Age":         [29, 29, 29, 41],
        "Department":  ["IT", "IT", "IT", "Marketing"],
        "Salary":      [55000, 55000, 55000, 70000],
    })


# ==========================================
# MISSING DATAFRAME — controlled nulls
# ==========================================

@pytest.fixture
def missing_df():
    return pd.DataFrame({
        "Full Name":  ["Aman Sharma", None, "Neha Joshi"],
        "Age":        [35, None, 29],
        "Salary":     [82000.0, None, 70000.0],
        "Department": [None, "Marketing", "HR"],
    })