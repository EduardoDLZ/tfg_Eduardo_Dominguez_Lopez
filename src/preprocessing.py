import pandas as pd
import numpy as np
import os
from src.utils import intro
from sklearn.preprocessing import LabelEncoder

def compare_datasets(
        df1: pd.DataFrame, 
        df2: pd.DataFrame,
) -> None:
    """Compare the basic structure of two DataFrames."""

    intro("Compare df1 vs df2")
    print(f"df1 shape: {df1.shape}")
    print(f"df2 shape: {df2.shape}")

    # print("Columns only in df1:")
    # print(sorted(set(df1.columns) - set(df2.columns)) or "None")
    # print("Columns only in df2:")
    # print(sorted(set(df2.columns) - set(df1.columns)) or "None")

    r0, c0 = df1.shape
    r1, c1 = df2.shape
    rows_dropped = r0 - r1
    cols_dropped = c0 - c1
    print(f"Rows dropped: {rows_dropped} ({rows_dropped / r0 * 100:.2f}%)")
    print(f"Columns dropped: {cols_dropped} ({cols_dropped / c0 * 100:.2f}%)")
    dropped_columns = sorted(set(df1.columns) - set(df2.columns))
    if dropped_columns:
        print("Dropped columns:")
        for col in dropped_columns:
            print(f"  - {col}")

def assess_data_quality(df: pd.DataFrame, ) -> dict[str, list[str]]:
    """Assess universal data-quality problems given a DataFrame"""

    intro("Universal Data-Quality Assessment")
    if df.empty:
        print("- DataFrame is empty")
        return {
            "missing_features": [],
            "infinite_features": [],
            "negative_features": [],
            "constant_features": [],
        }

    # Remove whitespaces from column names
    df.columns = df.columns.str.strip()
    numeric_cols = df.select_dtypes(include=np.number).columns

    # Missing values
    missing_features = [
        col for col in df.columns 
        if df[col].isnull().any()
    ]
    if len(missing_features) > 0:
        print(f"- {len(missing_features)} columns with missing values:")
        for f in missing_features:
            n_missing = df[f].isnull().sum()
            pct_missing = 100 * n_missing / len(df)
            print(f"  - {f}: {n_missing} missing values ({pct_missing:.3f}%)")
    else:
        print("- No missing values found")


    # Infinite values
    infinite_features = [
        col for col in numeric_cols
        if np.isinf(df[col]).any() 
    ]
    if len(infinite_features) > 0:
        print(f"- {len(infinite_features)} columns with infinite values:")
        for f in infinite_features:
            pos_inf = np.isposinf(df[f]).sum()
            neg_inf = np.isneginf(df[f]).sum()

            pct_pos_inf = 100 * pos_inf / len(df)
            pct_neg_inf = 100 * neg_inf / len(df)

            print(f"  - {f}: +inf={pos_inf} ({pct_pos_inf:.3f}%) / -inf={neg_inf} ({pct_neg_inf:.3f}%)")
    else:
        print("- No infinite values found")

    # Constant columns    
    constant_features = [
        col for col in df.columns 
        if df[col].nunique() <= 1
    ]
    if len(constant_features) > 0:
        print(f"- {len(constant_features)} constant columns:")
        for f in constant_features:
            print(f"  - {f}")
    else:
        print("- No constant features found")

    # Plausibity Check
    negative_features = [
            col for col in numeric_cols
            if (df[col] < 0).sum()  
    ]
    if len(negative_features) > 0:
        print(f"- {len(negative_features)} columns with negative values:")
        for f in negative_features:
            n_neg = (df[f] < 0).sum()
            pct_n_neg = 100 * n_neg / len(df)
            print(f"  - {f}: {n_neg} negative values ({pct_n_neg:.3f}%)")
    else:
        print("- No negative values found")

    report = {
        "missing_features": missing_features,
        "infinite_features": infinite_features,
        "negative_features": negative_features,
        "constant_features": constant_features,
    }
    return report

def clean_dataset(
    report: dict[str, list[str]],
    df: pd.DataFrame,
    invalid_negative_columns: list[str] | None = None,
    categorical_columns: list[str] | None = None,
) -> pd.DataFrame: 
    """Clean a DataFrame using results from assess_data_quality()"""
    intro("Data Cleaning")
    if invalid_negative_columns is None:
        invalid_negative_columns = []
    if categorical_columns is None:
        categorical_columns = []

    # Avoid modifying original data
    df = df.copy()

    # Replace infinite values with NaN
    df = df.replace([np.inf, -np.inf], np.nan)
    print(f"- Infinite values replaced with NaN")

    # Drop rows containing missing values
    rows_before = len(df)
    df = df.dropna()
    rows_dropped = rows_before - len(df)
    print(f"- {rows_dropped} rows with missing values dropped")

    # Remove rows with invalid negative values
    # Only use the ones that exist in the DataFrame
    available_invalid_negative_columns = [
        column
        for column in invalid_negative_columns
        if column in df.columns
    ]
    if len(available_invalid_negative_columns) > 0:
        rows_before = len(df)
        invalid_rows = (df[available_invalid_negative_columns] < 0).any(axis=1)
        df = df.drop(index=df[invalid_rows].index)
        rows_dropped = rows_before - len(df)
        print(f"- {rows_dropped} negative rows dropped")
    else:
        print("- No negative columns found")

    # Drop reported constant columns
    constant_columns = [
        column
        for column in report["constant_features"]
        if column in df.columns
    ]
    df = df.drop(columns=constant_columns)
    print(f"- {len(constant_columns)} constant columns dropped")

    # Drop categorical columns
    # Only use the ones that exist in the DataFrame
    available_categorical_columns = [
        column
        for column in categorical_columns
        if column in df.columns
    ]
    df = df.drop(columns=available_categorical_columns)
    print(
        f"- {len(available_categorical_columns)} "
        "categorical features dropped"
    )
    return df

def save(
        dataset_name: str, 
        df_to_save: pd.DataFrame
) -> None:
    """Downcast numeric columns and save a DataFrame as Parquet"""
    
    intro("Saving dataset as .parquet")
    data_dir = 'data/processed'
    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, dataset_name)
    df_to_save = df_to_save.copy()

    # Downcast integer columns and keep floating-point columns at float32 or wider.
    for col in df_to_save.select_dtypes(include=['integer']).columns:
        df_to_save[col] = pd.to_numeric(df_to_save[col], downcast='integer')
    for col in df_to_save.select_dtypes(include=['floating']).columns:
        df_to_save[col] = df_to_save[col].astype('float32')

    df_to_save.to_parquet(path, index=False)
    size_mb = os.path.getsize(path) / 1e6
    print(f"Final Dataset Saved: {path} ({size_mb:.2f} MB) ")

def load_dataset(path: str) -> pd.DataFrame:
    """
    Load a processed dataset from .csv
    """
    return pd.read_parquet(path)

def split_features_target(
    df: pd.DataFrame,
    target_column: str = "Label",
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Separate predictor features (X) from the target variable (y)
    """
    if target_column not in df.columns:
        raise KeyError(f"Target column '{target_column}' was not found in the DataFrame")

    X = df.drop(columns=[target_column])
    y = df[target_column]
    return X, y

def encode_target(y: pd.Series,) -> np.ndarray:
    """
    Encode target labels into numerical values.
    """
    encoder = LabelEncoder()
    return encoder.fit_transform(y)