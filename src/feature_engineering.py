import ipaddress

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, StandardScaler

from src.utils import intro

def categorize_port_number(port: int | float) -> str:
    """
    Categorize a TCP/UDP port number
    """

    if 0 <= port <= 1023:
        return "Well-known"
    if 1024 <= port <= 49151:
        return "Registered"
    if 49152 <= port <= 65535:
        return "Dynamic"
    
    raise ValueError(f"Invalid port number: {port}")
    
def ipv4_to_int(ip: str) -> int:
    """
    Convert an IPv4 address to integer representation
    """
    return int(ipaddress.IPv4Address(ip))

def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Encode IP addresses, protocols, and port numbers
    """

    intro("Encoding Categorical Features")
    # Avoid modifying original data
    df = df.copy()

    print("- Encoding Source/Destination IP")
    ip_columns = ["Source IP", "Destination IP"]
    for column in ip_columns:
        df[column] = df[column].apply(ipv4_to_int)
    scaler = MinMaxScaler(feature_range=(0, 1))
    df[ip_columns] = scaler.fit_transform(df[ip_columns])

    print("- Encoding Protocol")
    protocol_column  = 'Protocol'
    encoder = OneHotEncoder(sparse_output=False)
    protocol_encoded = encoder.fit_transform( df[[protocol_column]])
    protocol_columns = [f"is_{protocol}" for protocol in encoder.categories_[0]]
    protocol_df = pd.DataFrame(
        protocol_encoded,           
        index=df.index,             
        columns=protocol_columns    
    )
    df = pd.concat([df, protocol_df],axis=1)
    df = df.drop(columns=[protocol_column])

    print("- Encoding Source/Destination Port")
    port_columns = ['Source Port', 'Destination Port']
    for col in port_columns:
        df[col] = df[col].apply(categorize_port_number)
    encoder = OneHotEncoder(sparse_output=False)
    port_encoded = encoder.fit_transform(df[port_columns])
    encoded_port_columns = encoder.get_feature_names_out(port_columns)

    port_df = pd.DataFrame(
        port_encoded,                            
        index=df.index,             
        columns=encoded_port_columns                       
    )
    df = pd.concat( [df, port_df],axis=1)
    df = df.drop(columns=['Source Port', 'Destination Port'])
    n = 3
    print("- Sample of scaled '{Source, Destination} IP':")
    print(df[ip_columns].sample(n))
    print("- Sample of new protocol column:")
    print(df[protocol_columns].sample(n))
    print("- Sample of encoded '{Source, Destination} Port':")
    print(df[encoded_port_columns].sample(n))
    return df

def apply_log_transform(
    df: pd.DataFrame,
    features: list[str],
) -> pd.DataFrame:
    """Apply log1p transformation to selected features"""
    intro("Applying log(1+x) transformation")
    df = df.copy()
    df[features] = np.log1p(df[features])
    return df

def scale_data(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame | None = None,
    scaler_type: str = "standard",
)-> tuple[np.ndarray, np.ndarray | None, StandardScaler]:
    """
    Scale features using parameters learned only from X_train to avoid data leakage
    """
    if scaler_type == "standard":
        scaler = StandardScaler()
    else:
        raise ValueError("scaler_type must be 'standard'")

    # Fit only on training data
    X_train_scaled = scaler.fit_transform(X_train)

    X_test_scaled = None
    if X_test is not None:
        X_test_scaled = scaler.transform(X_test)

    return (
        X_train_scaled,
        X_test_scaled,
        scaler,
    )
