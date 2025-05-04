import pandas as pd


def get_descriptive_stats(df, include='all'):
    """
    Generates descriptive statistics of a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        include (str, list-like, optional): Which columns to include in the statistics.
            - 'all' (default): All columns.
            - List of column names: Include specific columns.
            - List of data types (e.g., ['number', 'category']): Include columns of those types.

    Returns:
        pd.DataFrame: Descriptive statistics.
    """
    return df.describe(include=include)


def calculate_correlations(df, method='pearson', min_periods=1):
    """
    Calculates the correlation matrix of a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        method (str, optional): Correlation method ('pearson', 'kendall', 'spearman').
            Defaults to 'pearson'.
        min_periods (int, optional): Minimum number of observations required to compute the correlation.

    Returns:
        pd.DataFrame: Correlation matrix.
    """
    numeric_df = df.select_dtypes(include=['number'])
    return numeric_df.corr(method=method, min_periods=min_periods)


def group_and_aggregate(df, group_cols, agg_dict):
    """
    Groups a DataFrame by specified columns and aggregates other columns.

    Args:
        df (pd.DataFrame): The DataFrame to aggregate.
        group_cols (str or list of str): Columns to group by.
        agg_dict (dict):  Dictionary specifying aggregation functions for columns.
                         Example: {'column1': 'sum', 'column2': ['mean', 'max']}

    Returns:
        pd.DataFrame: The aggregated DataFrame.
    """

    return df.groupby(group_cols).agg(agg_dict)
