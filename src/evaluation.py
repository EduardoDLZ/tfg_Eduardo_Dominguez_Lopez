from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score,precision_score, recall_score


def save_results(
    results: pd.DataFrame,
    output_dir: str | Path = "output",
    filename: str = "results.json",
) -> None:
    """
    Save evaluation results as a JSON file
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / filename
    results.to_json(output_file,orient="split",indent=4,)
    print(f"Results saved to: {output_file.resolve()}")

def compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> dict[str, float | int]:
    """
    Compute binary classification metrics
    """

    tn, fp, fn, tp = confusion_matrix(y_true,y_pred,labels=[0, 1]).ravel()
    return {
        "BENIGN": int(np.sum(y_true == 0)),
        "DDoS": int(np.sum(y_true == 1)),
        "FP": int(fp),
        "FN": int(fn),
        "TP": int(tp),
        "TN": int(tn),
        "FP Rate": (fp / (fp + tn) if (fp + tn) > 0 else 0),
        "Accuracy": accuracy_score(y_true, y_pred),
        "F1": f1_score(y_true,y_pred,average="weighted"),
    }


def evaluate_models(saved: dict) -> pd.DataFrame:
    """
    Load saved models and test data, generate predictions,
    and calculate evaluation metrics.
    """
    results = []
    for (model_name, feature_set), values in saved.items():
        print(f"Evaluating {model_name} on {feature_set}...")

        model = joblib.load(values["model"])
        data = np.load(values["test"],allow_pickle=True)

        X_test = data["X_test"]
        y_test = data["y_test"]
        X_test = pd.DataFrame(X_test, columns=data["feature_names"])
        y_pred = model.predict(X_test)

        metrics = compute_metrics(y_test,y_pred)
        result = {
            "Model": model_name,
            "Feature Set": feature_set,
            "Features Count": values["n_features"],
            "Train Time": values["train_time"],
            "Train Accuracy": values["train_accuracy"],
            "Train F1": values["train_f1"],
            **metrics,
            "Features Names": values["feature_names"]
        }
        results.append(result)
    return pd.DataFrame(results)