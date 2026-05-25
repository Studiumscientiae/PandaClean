# Duplicates.py file used for handling duplicated values

# =====================
# Check duplicate rows
# =====================

def check_duplicates(df):
    # checking duplicate rows and returning them

    duplicate_rows= df[df.duplicated()]
    return duplicate_rows


# =================
# Count duplicates
# =================

def count_duplicates(df):
    # Count total duplicate rows

    total_duplicates= df.duplicated().sum()
    return total_duplicates


# ==================
# Remove duplicates
# ==================

def remove_duplicates(df):
    # Remove duplicate rows

    drop_df= df.drop_duplicates()
    return drop_df


# ======================================
# Remove duplicates by specific column
# ======================================

def remove_duplicates_by_column(df,column_name):
    # remove duplicate rows by specific column

    drop_df= df.drop_duplicates(subset=[column_name])
    return drop_df


# =====================================
# Keep last duplicate instead of first
# =====================================

def keep_last_duplicate(df):
    # keeping the last duplicated row instead of first

    drop_df= df.drop_duplicates(keep="last")
    return drop_df


# ================
# Mark duplicates
# ================

def mark_duplicates(df):
    # Marking the duplicated values by adding new row with values true/false

    df["is_duplicate"]= df.duplicated()
    return df


# =================================================
# Remove identical rows same as 3 function on page
# =================================================

def remove_full_duplicates(df):
    # Remove duplicate rows

    drop_df= df.drop_duplicates(keep="first")
    return drop_df


# =========================== Duplicates.py ends here ==============================