# conftest.py - Shared fixtures for all tests.

import os
import pytest
import pandas as pd


# ==========================================
# TEST DATA PATH
# ==========================================

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "data",
    "sample_dataset.xlsx"
)


# ==========================================
# RAW DATAFRAME
# Dynamically loads actual dataset
# Fresh copy returned every test
# ==========================================

@pytest.fixture
def raw_df():
    return pd.read_excel(DATA_PATH).copy()


# ==========================================
# DYNAMIC EXPECTED COLUMNS
# Automatically adapts if dataset changes
# ==========================================

@pytest.fixture
def expected_columns(raw_df):
    return raw_df.columns.tolist()


# ==========================================
# DYNAMIC EXPECTED SHAPE
# Automatically adapts if dataset changes
# ==========================================

@pytest.fixture
def expected_shape(raw_df):
    return raw_df.shape


# ==========================================
# CLEAN DATAFRAME
# Controlled clean dataset
# Useful for formatting/datatype tests
# ==========================================

@pytest.fixture
def clean_df():
    return pd.DataFrame({
        "Employee ID": ["EMP-1", "EMP-2", "EMP-3"],
        "Full Name": ["Aman Sharma", "Priya Singh", "Neha Joshi"],
        "Age": [35, 41, 29],
        "Department": ["IT", "Marketing", "HR"],
        "Salary": [82000.0, 55000.0, 70000.0],
        "City": ["Delhi", "Mumbai", "Bangalore"],
        "Performance Score": [3.7, 4.5, 3.2],
    })


# ==========================================
# DUPLICATE DATAFRAME
# Controlled duplicate rows
# Useful for duplicate handling tests
# ==========================================

@pytest.fixture
def duplicate_df():
    return pd.DataFrame({
        "Employee ID": ["EMP-5", "EMP-5", "EMP-5", "EMP-6"],
        "Full Name": ["Aman Sharma", "Aman Sharma", "Aman Sharma", "Priya Singh"],
        "Age": [29, 29, 29, 41],
        "Department": ["IT", "IT", "IT", "Marketing"],
        "Salary": [55000, 55000, 55000, 70000],
    })


# ==========================================
# MISSING DATAFRAME
# Controlled missing values
# Useful for missing value handling tests
# ==========================================

@pytest.fixture
def missing_df():
    return pd.DataFrame({
        "Full Name": ["Aman Sharma", None, "Neha Joshi"],
        "Age": [35, None, 29],
        "Salary": [82000.0, None, 70000.0],
        "Department": [None, "Marketing", "HR"],
    })


# ==========================================
# GENERATED DATAFRAME
# Fully dynamic dataframe for scalability tests
# ==========================================

@pytest.fixture
def generated_df():

    rows = 10

    return pd.DataFrame({
        "A": range(rows),
        "B": [f"name_{i}" for i in range(rows)],
        "C": [i * 10 for i in range(rows)]
    })


# ==========================================
# PARAMETRIZED DATAFRAME
# Runs tests on multiple dataset sizes
# ==========================================

@pytest.fixture(params=[10, 100, 1000])
def variable_df(request):

    rows = request.param

    return pd.DataFrame({
        "A": range(rows),
        "B": range(rows)
    })