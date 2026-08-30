from sklearn.metrics import accuracy_score, f1_score 
from sklearn.model_selection import train_test_split
from sklearn.base import clone
from collections import Counter
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
import time

from src.feature_engineering import scale_data
from src.utils import intro

def train_model(model, X_train, y_train):
    """"
    Clone and train model. Compute training time
    """
    # Avoid model overwriting
    model_instance = clone(model)

    start_time = time.perf_counter()
    model_instance.fit(X_train, y_train)
    train_time = time.perf_counter() - start_time

    return model_instance, train_time

def save_artifacts(
    model,
    scaler,
    X_test,
    y_test,
    model_dir: Path,
    feature_set_name: str,
    feature_names,
) -> dict:
    """
    Save the trained model, scaler, and test data
    """

    model_dir.mkdir(parents=True, exist_ok=True)
    model_path = model_dir / f"{feature_set_name}.pkl"
    scaler_path = model_dir / f"{feature_set_name}-scaler.pkl"
    test_path = model_dir / f"{feature_set_name}-test.npz"

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    np.savez(
        test_path,
        X_test=X_test,
        y_test=y_test,
        feature_names=np.asarray(feature_names),
    )

    return {
        "model": model_path,
        "scaler": scaler_path,
        "test": test_path,
    }

def print_class_distribution(labels, dataset_name):
    counts = Counter(labels)
    total = len(labels)
    print(f"{dataset_name} class distribution:")
    for class_label, count in sorted(counts.items(), key=lambda item: str(item[0])):
        percentage = 100 * count / total
        print( f" - Class {class_label}: {count:,} samples ({percentage:.2f}%)")

def split_data(
    X,
    y,
    test_size: float = 0.10,
    random_state: int = 42,
):
    """
     Split data into train and test sets. Stratification preserves the class distribution
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )
    return (
        X_train, 
        X_test, 
        y_train, 
        y_test
    )

def train(X_sets, y_sets, models, dir_name="models", scaler=None, test_size=0.1):
    """
    Train every model on every feature set.
    For every model and feature set, this function:
    1. Splits data into train/test sets.
    2. Fits the scaler only on training data.
    3. Transforms test data.
    4. Trains a cloned model.
    5. Saves the model, scaler, and test data.
    6. Stores training metrics and artifact paths.
    """
    intro("Training models on every feature set")
    models_dir = Path(dir_name)
    models_dir.mkdir(exist_ok=True)
    saved = {}

    for model_name, model in models.items():
        model_dir = models_dir / model_name
        model_dir.mkdir(exist_ok=True)
        print(f"\n{10*"="} {model_name} ({model_dir}) {10*"="}")

        for feature_set_name, X in X_sets.items():
            if feature_set_name not in y_sets:
                raise KeyError(f"No target data found for feature set "f"'{feature_set_name}'.")

            y = y_sets[feature_set_name]
            print( f"\nPreparing {model_name} with {feature_set_name}...")
            feature_names = list(X.columns)
          
            X_train, X_test, y_train, y_test = split_data(X, y, test_size)

            # No scaling requested.
            if scaler is None:
                X_train_processed = X_train
                X_test_processed = X_test
                fitted_scaler = None
            else:
                X_train_scaled, X_test_scaled, fitted_scaler = scale_data(X_train, X_test, scaler_type="standard")
                X_train_processed = pd.DataFrame(X_train_scaled, columns=feature_names)
                X_test_processed = X_test_scaled

            fitted_model, train_time = train_model(model, X_train_processed, y_train)

            train_predictions = fitted_model.predict(X_train_processed)
            train_accuracy = accuracy_score(y_train, train_predictions)
            train_f1 = f1_score(y_train,train_predictions,average="weighted")

            artifact_paths = save_artifacts(
                fitted_model, 
                fitted_scaler, 
                X_test_processed, 
                y_test, 
                model_dir, 
                feature_set_name, 
                X.columns
            )

            saved[(model_name, feature_set_name)] = {
                **artifact_paths,
                "n_features": X.shape[1],
                "feature_names": feature_names,
                "train_time": round(train_time, 3),
                "train_accuracy": train_accuracy,
                "train_f1": train_f1,
            }
            print(f"Train accuracy: {train_accuracy:.4f} | "f"Train F1: {train_f1:.4f}")

    return saved


