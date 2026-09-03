from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression

def get_baseline_models():
    """Return the baseline classification models."""
    return {
        "Logistic Regression": LogisticRegression(
            random_state=42,
            n_jobs=-1,
            max_iter=1000,
        ),
        "SVC": SVC(
            C=1.0,
            kernel="rbf",
        ),
        "MLP": MLPClassifier(
            hidden_layer_sizes=(100,),
            activation="relu",
            solver="adam",
            alpha=0.0001,
            max_iter=200,
            random_state=42,
        ),
    }

def get_full_dataset_models():
    """Return baseline models plus tree-based models."""
    return {
        **get_baseline_models(),
        "Decision Tree": DecisionTreeClassifier(
            criterion="gini",
            random_state=42,
        ),
    }
