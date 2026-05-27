# file_handler.py

import pandas as pd
import os


# ==========================================
# LOAD CSV FILE
# ==========================================

def load_csv(file_path):

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    if not is_csv_file(file_path):
        raise ValueError("File is not a CSV file")

    if not file_exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    df = pd.read_csv(file_path)
    return df


# ==========================================
# LOAD EXCEL FILE
# ==========================================

def load_excel(file_path):

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    if not is_excel_file(file_path):
        raise ValueError("File is not an Excel file")

    if not file_exists(file_path):
        raise FileNotFoundError(f"Excel file not found: {file_path}")

    df = pd.read_excel(file_path)
    return df


# ==========================================
# SAVE DATAFRAME AS CSV
# ==========================================

def save_csv(df, output_path):

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    if not isinstance(output_path, str):
        raise TypeError("output_path must be a string")

    df.to_csv(output_path, index=False)
    return True


# ==========================================
# SAVE DATAFRAME AS EXCEL
# ==========================================

def save_excel(df, output_path):

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    if not isinstance(output_path, str):
        raise TypeError("output_path must be a string")

    df.to_excel(output_path, index=False)
    return True


# ==========================================
# CHECK FILE EXISTS
# ==========================================

def file_exists(file_path):

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    return os.path.exists(file_path)


# ==========================================
# GET FILE EXTENSION
# ==========================================

def get_file_extension(file_path):

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    return os.path.splitext(file_path)[1]


# ==========================================
# CHECK IF FILE IS CSV
# ==========================================

def is_csv_file(file_path):

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    return file_path.lower().endswith(".csv")


# ==========================================
# CHECK IF FILE IS EXCEL
# ==========================================

def is_excel_file(file_path):

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    return file_path.lower().endswith((".xlsx", ".xls"))


# ==========================================
# DISPLAY BASIC FILE INFORMATION
# ==========================================

def file_information(df):

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict()
    }


# ==================== File_handler.py ends here ====================