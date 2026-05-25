# Datatype.py used for converting datatypes of dataframe

import pandas as pd

# ==========================================
# CONVERT COLUMN TO INTEGER
# ==========================================

def convert_to_integer(df, column_name):

    #Converts a column to integer datatype

    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    df[column_name] = df[column_name].astype("Int64")
    return df


# ==========================================
# CONVERT COLUMN TO FLOAT
# ==========================================

def convert_to_float(df, column_name):

    # Converts a column to float datatype

    df[column_name] = pd.to_numeric(df[column_name], errors="coerce")
    return df


# ==========================================
# CONVERT COLUMN TO STRING
# ==========================================

def convert_to_string(df, column_name):

    # Converts a column to string datatype

    df[column_name] = df[column_name].astype(str)
    return df


# ==========================================
# CONVERT COLUMN TO DATETIME
# ==========================================

def convert_to_datetime(df, column_name):

    # Converts a column to datetime datatype

    df[column_name] = pd.to_datetime(df[column_name],errors="coerce")
    return df


# ==========================================
# CONVERT COLUMN TO BOOLEAN
# ==========================================

def convert_to_boolean(df, column_name):

    # Converts a column to boolean datatype

    df[column_name] = df[column_name].astype(bool)
    return df


# ==========================================
# CHECK DATATYPES OF ALL COLUMNS
# ==========================================

def check_datatypes(df):

    # Returns datatypes of all columns

    return df.dtypes


# ==========================================
# Find columns with wrong numeric values
# ==========================================

def find_invalid_numeric_values(df, column_name):

    # Finds rows where numeric conversion fails

    invalid_rows = df[pd.to_numeric(df[column_name], errors="coerce").isna()]
    return invalid_rows


# ==========================================
# Remove currency symbols
# ==========================================

def remove_currency_symbols(df, column_name):

    # Removes currency symbols and commas

    df[column_name] = df[column_name].str.replace(r"[^0-9.]","",regex=True)
    return df


# ========================= Datatype.py ends here =================================