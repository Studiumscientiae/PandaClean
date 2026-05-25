# file_handler.py

import pandas as pd
import os


# ==========================================
# LOAD CSV FILE
# ==========================================

def load_csv(file_path):

    # Loads a CSV file into a dataframe.

    try:
        df = pd.read_csv(file_path)
        print("CSV file loaded successfully.")
        return df

    except Exception as error:
        print("Error loading CSV file:")
        print(error)


# ==========================================
# LOAD EXCEL FILE
# ==========================================

def load_excel(file_path):

    # Loads an Excel file into a dataframe.

    try:
        df = pd.read_excel(file_path)
        print("Excel file loaded successfully.")
        return df

    except Exception as error:
        print("Error loading Excel file:")
        print(error)


# ==========================================
# SAVE DATAFRAME AS CSV
# ==========================================

def save_csv(df, output_path):

    # Saves dataframe as CSV file.

    try:
        df.to_csv(output_path, index=False)
        print("CSV file saved successfully.")

    except Exception as error:
        print("Error saving CSV file:")
        print(error)


# ==========================================
# SAVE DATAFRAME AS EXCEL
# ==========================================

def save_excel(df, output_path):

    # Saves dataframe as Excel file.

    try:
        df.to_excel(output_path, index=False)
        print("Excel file saved successfully.")

    except Exception as error:
        print("Error saving Excel file:")
        print(error)


# ==========================================
# CHECK FILE EXISTS
# ==========================================

def file_exists(file_path):

    # Checks whether file exists.

    return os.path.exists(file_path)


# ==========================================
# GET FILE EXTENSION
# ==========================================

def get_file_extension(file_path):

    # Returns file extension.

    return os.path.splitext(file_path)[1]


# ==========================================
# CHECK IF FILE IS CSV
# ==========================================

def is_csv_file(file_path):

    # Checks whether file is CSV.

    return file_path.endswith(".csv")


# ==========================================
# CHECK IF FILE IS EXCEL
# ==========================================

def is_excel_file(file_path):

    # Checks whether file is Excel

    return file_path.endswith((".xlsx", ".xls"))


# ==========================================
# DISPLAY BASIC FILE INFORMATION
# ==========================================

def file_information(df):

    # Displays basic dataframe information.

    print("\nShape of DataFrame:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns)

    print("\nDatatypes:")
    print(df.dtypes)


# ==================== File_handler.py ends here ====================