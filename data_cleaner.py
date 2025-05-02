import pandas as pd


def clean_missing_values(df, method='drop', fill_value=None):
    """
    Handles missing values in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to clean.
        method (str, optional): The method for handling missing values.
            - 'drop':  Remove rows with any missing values.
            - 'mean':  Fill missing values with the mean of the column.
            - 'median': Fill missing values with the median of the column.
            - 'ffill':  Forward fill missing values.
            - 'bfill':  Backward fill missing values.
            - 'constant': Fill missing values with a specified 'fill_value'.
            Defaults to 'drop'.
        fill_value: Value to use when method is 'constant'. Defaults to None.

    Returns:
        pd.DataFrame: The DataFrame with missing values handled.

    Raises:
        ValueError: If an invalid method is provided.
    """
    if method == 'drop':
        df_cleaned = df.dropna()
    elif method == 'mean':
        df_cleaned = df.fillna(df.mean(numeric_only=True))
    elif method == 'median':
        df_cleaned = df.fillna(df.median(numeric_only=True))
    elif method == 'ffill':
        df_cleaned = df.fillna(method='ffill')
    elif method == 'bfill':
        df_cleaned = df.fillna(method='bfill')
    elif method == 'constant':
        if fill_value is None:
            raise ValueError(
                "fill_value must be specified when method is 'constant'.")
        df_cleaned = df.fillna(fill_value)
    else:
        raise ValueError("Invalid method for handling missing values.")
    return df_cleaned


def remove_duplicates(df, subset=None, keep='first'):
    """
    Removes duplicate rows from a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to clean.
        subset (str or list of str, optional): Columns to consider for identifying duplicates.
            If None, all columns are used. Defaults to None.
        keep (str, optional): Which duplicate to keep.
            - 'first' (default): Keep the first occurrence.
            - 'last': Keep the last occurrence.
            - False: Drop all duplicates.

    Returns:
        pd.DataFrame: The DataFrame with duplicates removed.
    """
    df_cleaned = df.drop_duplicates(subset=subset, keep=keep)
    return df_cleaned


def filter_data(df, column, condition, value):
    """
    Filters a DataFrame based on a given condition.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column to filter on.
        condition (str): The filtering condition ('==', '!=', '>', '<', '>=', '<=', 'in', 'not in').
        value: The value to filter by.  For 'in'/'not in', value should be a list.

    Returns:
        pd.DataFrame: The filtered DataFrame.

    Raises:
        ValueError: If an invalid condition is provided.
    """

    if condition == '==':
        df_filtered = df[df[column] == value]
    elif condition == '!=':
        df_filtered = df[df[column] != value]
    elif condition == '>':
        df_filtered = df[df[column] > value]
    elif condition == '<':
        df_filtered = df[df[column] < value]
    elif condition == '>=':
        df_filtered = df[df[column] >= value]
    elif condition == '<=':
        df_filtered = df[df[column] <= value]
    elif condition == 'in':
        df_filtered = df[df[column].isin(value)]
    elif condition == 'not in':
        df_filtered = df[~df[column].isin(value)]
    else:
        raise ValueError(f"Invalid condition: {condition}")
    return df_filtered
