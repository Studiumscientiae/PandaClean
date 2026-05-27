# Missing.py file used for handling missing values

import pandas as pd

# =====================
# Check missing values
# =====================

def check_missing_value(df):
    # checking null values per column and returning them

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")

    return df.isnull().sum()

# ==================================
# Dropping rows with missing values
# ==================================

def drop_missing_row(df):
    # Remove rows that have missing values

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")

    return df.dropna()


# =======================================
# Fill missing value with specific value
# =======================================

def fill_missing_value(df, value="unknown"):
    # filling missing value with specific value

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")

    return df.fillna(value)

# ====================================================================
# Fill missing numeric values with mean
# ====================================================================

def fill_missing_numeric_with_mean(df: pd.DataFrame) -> pd.DataFrame:
    # Fill missing numeric values with column mean

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")
    df = df.copy()

    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) == 0:
        raise ValueError("No numeric columns found")

    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mean())
    return df


# ====================================================================
# Fill missing numeric values with median
# ====================================================================

def fill_missing_numeric_with_median(df: pd.DataFrame) -> pd.DataFrame:
    # missing numerical values are being replace by median value

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")
    df = df.copy()

    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) == 0:
        raise ValueError("No numeric columns found")

    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())
    return df

# ====================================================================
# Fill missing numeric values with mode
# ====================================================================

def fill_missing_numeric_with_mode(df: pd.DataFrame) -> pd.DataFrame:
    # missing numerical values are being replace by mode value

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")
    df = df.copy()

    numeric_cols = df.select_dtypes(include=["number"]).columns

    if len(numeric_cols) == 0:
        raise ValueError("No numeric columns found")

    for col in numeric_cols:
        if df[col].isnull().any():
            mode_values = df[col].mode()
            if not mode_values.empty:
                df[col] = df[col].fillna(mode_values[0])
    return df


# =======================
# Removing empty columns
# =======================

def drop_empty_column(df):
    # Removes columns where all values are missing

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")
    return df.dropna(axis=1, how="all")


# =========================== Missing.py ends here ==============================