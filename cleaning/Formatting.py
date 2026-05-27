# Formatting.py used for handling formatting of the data

import pandas as pd

# =========================
# Common validation helper
# =========================

def _validate_df(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected pandas DataFrame, got {type(df)}")

    if df.empty:
        raise ValueError("DataFrame is empty")
    return df


# ====================
# Format column names
# ====================

def format_column_name(df):
    # column name is formatted in one go

    try:
        df = _validate_df(df)
        df = df.copy()
        df.columns = df.columns.str.strip()
        df.columns = df.columns.str.title()
        df.columns = df.columns.str.replace(" ", "_")
        return df

    except Exception as e:
        raise Exception(f"Error in format_column_name: {str(e)}")


# ================================
# Removing extra spaces from text
# ================================

def remove_extra_spaces(df):
   # extra spaces before and after the column name is being removed

    try:
        df = _validate_df(df)
        df = df.copy()
        df.columns = df.columns.str.strip()
        return df

    except Exception as e:
        raise Exception(f"Error in remove_extra_spaces: {str(e)}")


# ==================================
# Convert column name to lower case
# ==================================

def convert_to_lowercase(df, column_name):
    # Converts all text to lowercase

    try:
        df = _validate_df(df)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found")
        df = df.copy()
        df[column_name] = df[column_name].astype(str).str.lower()
        return df

    except Exception as e:
        raise Exception(f"Error in convert_to_lowercase: {str(e)}")


# =================================
# Convert column name to uppercase
# =================================

def convert_to_uppercase(df, column_name):
    # Converts all text to uppercase

    try:
        df = _validate_df(df)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found")
        df = df.copy()
        df[column_name] = df[column_name].astype(str).str.upper()
        return df

    except Exception as e:
        raise Exception(f"Error in convert_to_uppercase: {str(e)}")


# ==================================
# Convert column name to title case
# ==================================

def convert_to_titlecase(df, column_name):
    # Converts text into title format

    try:
        df = _validate_df(df)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found")
        df = df.copy()
        df[column_name] = df[column_name].astype(str).str.title()
        return df

    except Exception as e:
        raise Exception(f"Error in convert_to_titlecase: {str(e)}")


# ==========================================
# Replace column names values
# ==========================================

def replace_column_name(df, column_name, old_value, new_value):
    # Replaces old values with new values

    try:
        df = _validate_df(df)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found")
        df = df.copy()
        df[column_name] = df[column_name].replace(old_value, new_value)
        return df

    except Exception as e:
        raise Exception(f"Error in replace_column_values: {str(e)}")


# ==========================================
# Remove special characters
# ==========================================

def remove_special_characters(df, column_name):
    # Removes special characters from text

    try:
        df = _validate_df(df)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found")
        df = df.copy()
        df[column_name] = df[column_name].astype(str).str.replace(
            r"[^a-zA-Z0-9 ]", "", regex=True
        )
        return df

    except Exception as e:
        raise Exception(f"Error in remove_special_characters: {str(e)}")


# ==========================================
# Remove multiple spaces between words
# ==========================================

def remove_multiple_spaces(df, column_name):
    # Removes extra spaces between words

    try:
        df = _validate_df(df)
        if column_name not in df.columns:
            raise ValueError(f"Column '{column_name}' not found")
        df = df.copy()
        df[column_name] = df[column_name].astype(str).str.replace(
            r"\s+", " ", regex=True
        ).str.strip()
        return df

    except Exception as e:
        raise Exception(f"Error in remove_multiple_spaces: {str(e)}")


# =========================== Formatting.py ends here ==================================