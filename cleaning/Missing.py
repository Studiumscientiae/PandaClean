# Missing.py file used for handling missing values

# =====================
# Check missing values
# =====================

def check_missing_value(df):
    # checking null values per column and returning them

    missing_df = df.isnull().sum()
    return missing_df


# ==================================
# Dropping rows with missing values
# ==================================

def drop_missing_row(df):
    # Remove rows that have missing values

    drop_df = df.dropna()
    return drop_df


# =======================================
# Fill missing value with specific value
# =======================================

def fill_missing_value(df, value="unknown"):
    # filling missing value with specific value

    specific_df= df.fillna(value)
    return specific_df

# ======================================
# Fill missing numeric values with mean
# ======================================

def fill_missing_numeric_with_mean(df):
    # missing numerical values are being replace by mean value

    numeric_df= df.select_dtypes(include=["number"]).columns

    for column in numeric_df:
        mean_value= df[column].mean()
        df[column]= df[column].fillna(mean_value)
    return df


# ========================================
# Fill missing numeric values with median
# ========================================

def fill_missing_numeric_with_median(df):
    # missing numerical values are being replace by median value

    numeric_df= df.select_dtypes(include=["number"]).columns

    for column in numeric_df:
        median_value= df[column].median()
        df[column]=df[column].fillna(median_value)
    return df


# ======================================
# Fill missing numeric values with mode
# ======================================

def fill_missing_numeric_with_mode(df):
    # missing numerical values are being replace by mode value

    numeric_df= df.select_dtypes(include=["number"]).columns

    for column in numeric_df:
        mode_value= df[column].mode()
        df[column]= df[column].fillna(mode_value[0])
    return df


# =======================
# Removing empty columns
# =======================

def drop_empty_column(df):
    # Removes columns where all values are missing

    drop_df= df.dropna(axis=1, how="all")
    return drop_df


# =========================== Missing.py ends here ==============================