# Datatype.py used for converting datatypes of dataframe

import pandas as pd

# ================================
# Validate DataFrame + Column
# ================================

def _validate(df, column_name=None):
    if not isinstance(df, pd.DataFrame):
        return False, "Input must be a pandas DataFrame"

    if column_name is not None:
        if column_name not in df.columns:
            return False, f"Column '{column_name}' does not exist"

    return True, None


# ==========================================
# CONVERT COLUMN TO INTEGER
# ==========================================

def convert_to_integer(df, column_name):
    # Converts a column to integer datatype

    valid, error = _validate(df, column_name)
    if not valid:
        return error
    df = df.copy()

    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")

    if df[column_name].isna().all():
        return "Conversion failed: all values became NaN"
    df[column_name] = df[column_name].astype("Int64")
    return df


# ==========================================
# CONVERT COLUMN TO FLOAT
# ==========================================

def convert_to_float(df, column_name):
    # Converts a column to float datatype

    valid, error = _validate(df, column_name)
    if not valid:
        return error
    df = df.copy()
    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    return df


# ==========================================
# CONVERT COLUMN TO STRING
# ==========================================

def convert_to_string(df, column_name):
    # Converts a column to string datatype

    valid, error = _validate(df, column_name)
    if not valid:
        return error
    df = df.copy()
    df[column_name] = df[column_name].astype(str)
    return df


# ==========================================
# CONVERT COLUMN TO DATETIME
# ==========================================

def convert_to_datetime(df, column_name):
    # Converts a column to datetime datatype

    valid, error = _validate(df, column_name)
    if not valid:
        return error

    df = df.copy()
    df[column_name] = pd.to_datetime(df[column_name], errors="coerce")

    if df[column_name].isna().all():
        return "Conversion failed: invalid datetime format"
    return df


# ==========================================
# CONVERT COLUMN TO BOOLEAN
# ==========================================

def convert_to_boolean(df, column_name):
    # Converts a column to boolean datatype

    valid, error = _validate(df, column_name)
    if not valid:
        return error

    df = df.copy()
    df[column_name] = df[column_name].astype(bool)
    return df


# ==========================================
# CHECK DATATYPES OF ALL COLUMNS
# ==========================================

def check_datatypes(df):
    # Returns datatypes of all columns

    if not isinstance(df, pd.DataFrame):
        return "Input must be a pandas DataFrame"

    return df.dtypes


# ==========================================
# Find columns with wrong numeric values
# ==========================================

def find_invalid_numeric_values(df, column_name):
    # Finds rows where numeric conversion fails

    valid, error = _validate(df, column_name)
    if not valid:
        return error

    invalid_rows = df[pd.to_numeric(df[column_name], errors="coerce").isna()]
    return invalid_rows


# ==========================================
# Remove currency symbols
# ==========================================

def remove_currency_symbols(df, column_name):
    # Removes currency symbols and commas

    valid, error = _validate(df, column_name)
    if not valid:
        return error

    df = df.copy()

    df[column_name] = df[column_name].astype(str)
    df[column_name] = df[column_name].str.replace(r"[^0-9.]", "", regex=True)
    return df


# ========================= Datatype.py ends here =================================