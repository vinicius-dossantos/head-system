"""
Módulo de treinamento, avaliação e comparação de modelos.
"""
from __future__ import annotations

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    accuracy_score,
)


def get_models(random_state: int = 42) -> dict:
    """Retorna um dicionário com os modelos a comparar."""
    return {
        "Regressão Logística": LogisticRegression(max_iter=1000, random_state=random_state),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=random_state),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=random_state),
    }


def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    """Calcula métricas de avaliação para um modelo já treinado."""
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_proba) if y_proba is not None else None,
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "classification_report": classification_report(y_test, y_pred),
    }
    return metrics


def train_and_evaluate(
    models: dict,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> pd.DataFrame:
    """Treina todos os modelos e retorna um DataFrame com as métricas comparativas."""
    results = []
    trained = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        trained[name] = model
        metrics = evaluate_model(model, X_test, y_test)
        results.append(
            {
                "Modelo": name,
                "Acurácia": round(metrics["accuracy"], 4),
                "Precisão": round(metrics["precision"], 4),
                "Recall": round(metrics["recall"], 4),
                "F1-Score": round(metrics["f1"], 4),
                "ROC-AUC": round(metrics["roc_auc"], 4) if metrics["roc_auc"] else "-",
            }
        )
    return pd.DataFrame(results).set_index("Modelo"), trained


def get_feature_importance(model, feature_names: list[str]) -> pd.Series:
    """Retorna importância das features para modelos baseados em árvores."""
    if hasattr(model, "feature_importances_"):
        return (
            pd.Series(model.feature_importances_, index=feature_names)
            .sort_values(ascending=False)
        )
    if hasattr(model, "coef_"):
        import numpy as np
        return (
            pd.Series(abs(model.coef_[0]), index=feature_names)
            .sort_values(ascending=False)
        )
    raise ValueError("Modelo não suporta importância de features.")
