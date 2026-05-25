# Formatting.py used for handling formatting of the data

# ====================
# Format column names
# ====================

def format_column_name(df):
    # column name is formatted in one go

    df.columns= df.columns.str.strip()
    df.columns= df.columns.str.title()
    df.columns= df.columns.str.replace(" ", "_")
    return df


# ================================
# Removing extra spaces from text
# ================================

def remove_extra_spaces(df):
   # extra spaces before and after the column name is being removed

    df.columns= df.columns.str.strip()
    return df


# ==================================
# Convert column name to lower case
# ==================================

def convert_to_lowercase(df, column_name):
    # Converts all text to lowercase

    df[column_name] = df[column_name].str.lower()
    return df


# =================================
# Convert column name to uppercase
# =================================

def convert_to_uppercase(df, column_name):
    # Converts all text to uppercase

    df[column_name] = df[column_name].str.upper()
    return df


# ==================================
# Convert column name to title case
# ==================================

def convert_to_titlecase(df, column_name):

    # Converts text into title format

    df[column_name] = df[column_name].str.title()
    return df


# ==========================================
# Replace column names values
# ==========================================

def replace_column_name(df, column_name, old_value, new_value):

    # Replaces old values with new values

    df[column_name] = df[column_name].replace(old_value, new_value)
    return df


# ==========================================
# Remove special characters
# ==========================================

def remove_special_characters(df, column_name):

    # Removes special characters from text

    df[column_name] = df[column_name].str.replace(r"[^a-zA-Z0-9 ]", "", regex=True)
    return df


# ==========================================
# Remove multiple spaces between words
# ==========================================

def remove_multiple_spaces(df, column_name):

    # Removes extra spaces between words

    df[column_name] = df[column_name].str.replace(r"\s+", " ", regex=True)
    return df


# =========================== Formatting.py ends here ==================================