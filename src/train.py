import json
import os
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

EVAL_THRESHOLD = 0.70


def _build_model(params: dict):
    model_type = params.get("model_type", "random_forest")
    model_params = {key: value for key, value in params.items() if key != "model_type"}
    if model_type == "random_forest":
        return RandomForestClassifier(**model_params, random_state=42)
    if model_type == "gradient_boosting":
        return GradientBoostingClassifier(**model_params, random_state=42)
    if model_type == "logistic_regression":
        return LogisticRegression(**model_params, random_state=42, max_iter=1000)
    raise ValueError(f"Unsupported model_type: {model_type}")


def train(
    params: dict,
    data_path: str = "data/train_phase1.csv",
    eval_path: str = "data/eval.csv",
) -> float:
    """Train, evaluate, track, and persist the selected classification model."""
    df_train = pd.read_csv(data_path)
    df_eval = pd.read_csv(eval_path)
    if "target" not in df_train or "target" not in df_eval:
        raise ValueError("Both datasets must contain a target column")

    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval = df_eval.drop(columns=["target"])
    y_eval = df_eval["target"]
    model_type = params.get("model_type", "random_forest")
    model = _build_model(params)

    with mlflow.start_run():
        mlflow.log_params({**params, "model_type": model_type})
        model.fit(X_train, y_train)
        predictions = model.predict(X_eval)
        accuracy = float(accuracy_score(y_eval, predictions))
        f1 = float(f1_score(y_eval, predictions, average="weighted"))
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("train_samples", len(df_train))
        mlflow.log_metric("eval_samples", len(df_eval))
        mlflow.sklearn.log_model(model, "model")

        labels = [0, 1, 2]
        matrix = confusion_matrix(y_eval, predictions, labels=labels).tolist()
        precision, recall, _, support = precision_recall_fscore_support(
            y_eval, predictions, labels=labels, zero_division=0
        )
        label_distribution = {
            str(label): float((y_train == label).mean()) for label in labels
        }
        for label, ratio in label_distribution.items():
            if ratio < 0.10:
                print(f"WARNING: class {label} represents only {ratio:.2%} of training data")

        metrics = {
            "accuracy": accuracy,
            "f1_score": f1,
            "model_type": model_type,
            "train_samples": len(df_train),
            "eval_samples": len(df_eval),
            "label_distribution": label_distribution,
            "confusion_matrix": matrix,
            "precision": {str(label): float(value) for label, value in zip(labels, precision)},
            "recall": {str(label): float(value) for label, value in zip(labels, recall)},
            "support": {str(label): int(value) for label, value in zip(labels, support)},
        }
        Path("outputs").mkdir(exist_ok=True)
        Path("models").mkdir(exist_ok=True)
        with open("outputs/metrics.json", "w", encoding="utf-8") as handle:
            json.dump(metrics, handle, indent=2)
        with open("outputs/report.txt", "w", encoding="utf-8") as handle:
            handle.write("Confusion matrix (labels 0, 1, 2):\n")
            handle.write(json.dumps(matrix) + "\n\n")
            handle.write("class,precision,recall,support\n")
            for index, label in enumerate(labels):
                handle.write(
                    f"{label},{precision[index]:.6f},{recall[index]:.6f},{support[index]}\n"
                )
        joblib.dump(model, "models/model.pkl")
        print(f"Accuracy: {accuracy:.4f} | F1: {f1:.4f}")

    return accuracy


if __name__ == "__main__":
    with open("params.yaml", encoding="utf-8") as handle:
        train(yaml.safe_load(handle))