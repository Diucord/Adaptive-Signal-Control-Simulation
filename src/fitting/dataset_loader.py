"""
dataset_loader.py
----------------------
Utility function for loading CSV files containing
arrival or departure interval data.

Expected CSV format:

    arr_time
    1.25
    0.98
    1.42
    ...

Or:

    dep_time
    2.11
    1.87
    3.01
    ...

This loader does not modify data.
"""

import pandas as pd


def load_dataset(path):
    """
    Load a dataset CSV file into a pandas DataFrame.

    Args:
        path (str): Path to the CSV file containing interval data.

    Returns:
        pandas.DataFrame:
            DataFrame containing columns such as
            'arr_time' or 'dep_time'.
    """
    df = pd.read_csv(path)
    return df
