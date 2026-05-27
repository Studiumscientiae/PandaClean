# Duplicates.py file used for handling duplicated values

import pandas as pd

# =====================
# Common validation
# =====================

def _validate_df(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")

    if df.empty:
        raise ValueError("DataFrame is empty")

    return df


# =====================
# Check duplicate rows
# =====================

def check_duplicates(df):
    # checking duplicate rows and returning them

    try:
        df = _validate_df(df)
        return df[df.duplicated()]

    except Exception as e:
        raise Exception(f"Error in check_duplicates: {str(e)}")


# =================
# Count duplicates
# =================

def count_duplicates(df):
    # Count total duplicate rows

    try:
        df = _validate_df(df)
        return df.duplicated().sum()

    except Exception as e:
        raise Exception(f"Error in count_duplicates: {str(e)}")


# ==================
# Remove duplicates
# ==================

def remove_duplicates(df):
    # Remove duplicate rows

    try:
        df = _validate_df(df)
        return df.drop_duplicates()

    except Exception as e:
        raise Exception(f"Error in remove_duplicates: {str(e)}")


# ======================================
# Remove duplicates by specific column
# ======================================

def remove_duplicates_by_column(df,column_name):
    # remove duplicate rows by specific column

    try:
        df = _validate_df(df)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found")
        return df.drop_duplicates(subset=[column_name])

    except Exception as e:
        raise Exception(f"Error in remove_duplicates_by_column: {str(e)}")


# =====================================
# Keep last duplicate instead of first
# =====================================

def keep_last_duplicate(df):
    # keeping the last duplicated row instead of first

    try:
        df = _validate_df(df)
        return df.drop_duplicates(keep="last")

    except Exception as e:
        raise Exception(f"Error in keep_last_duplicate: {str(e)}")


# ================
# Mark duplicates
# ================

def mark_duplicates(df):
    # Marking the duplicated values by adding new row with values true/false

    try:
        df = _validate_df(df)
        df = df.copy()
        df["is_duplicate"] = df.duplicated()
        return df

    except Exception as e:
        raise Exception(f"Error in mark_duplicates: {str(e)}")


# =================================================
# Remove identical rows same as 3 function on page
# =================================================

def remove_full_duplicates(df):
    # Remove duplicate rows

    try:
        df = _validate_df(df)
        return df.drop_duplicates(keep="first")

    except Exception as e:
        raise Exception(f"Error in remove_full_duplicates: {str(e)}")


# =========================== Duplicates.py ends here ==============================