"""
Módulo de visualização para EDA e avaliação de modelos.
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay


PALETTE = "Blues_d"
FIG_SIZE = (10, 6)


def set_style():
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({"figure.dpi": 100, "axes.titlesize": 14})


def plot_delay_distribution(df: pd.DataFrame, col: str = "arrival_delay_min"):
    """Histograma da distribuição de atrasos."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    data = df[col].dropna()
    ax.hist(data, bins=60, color="#2196F3", edgecolor="white", alpha=0.85)
    ax.axvline(15, color="red", linestyle="--", label="Limiar de atraso (15 min)")
    ax.set_title(f"Distribuição de {col}")
    ax.set_xlabel("Minutos")
    ax.set_ylabel("Frequência")
    ax.legend()
    plt.tight_layout()
    return fig


def plot_delay_by_category(df: pd.DataFrame, col: str, target: str = "is_delayed"):
    """Taxa de atraso por variável categórica."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    order = (
        df.groupby(col)[target]
        .mean()
        .sort_values(ascending=False)
        .index
    )
    sns.barplot(data=df, x=col, y=target, order=order, palette=PALETTE, ax=ax)
    ax.set_title(f"Taxa de Atraso por {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Taxa de Atraso")
    ax.set_ylim(0, 1)
    plt.tight_layout()
    return fig


def plot_correlation_matrix(df: pd.DataFrame, cols: list[str] | None = None):
    """Heatmap de correlação."""
    cols = cols or df.select_dtypes(include=[np.number]).columns.tolist()
    fig, ax = plt.subplots(figsize=(12, 8))
    corr = df[cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax, linewidths=0.5)
    ax.set_title("Matriz de Correlação")
    plt.tight_layout()
    return fig


def plot_confusion_matrix(model, X_test, y_test, title: str = "Matriz de Confusão"):
    """Plota a matriz de confusão."""
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_estimator(
        model, X_test, y_test, cmap="Blues", ax=ax, colorbar=False
    )
    ax.set_title(title)
    plt.tight_layout()
    return fig


def plot_roc_curves(trained_models: dict, X_test, y_test):
    """Plota curvas ROC para múltiplos modelos."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    for name, model in trained_models.items():
        if hasattr(model, "predict_proba"):
            RocCurveDisplay.from_estimator(model, X_test, y_test, name=name, ax=ax)
    ax.plot([0, 1], [0, 1], "k--", label="Aleatório")
    ax.set_title("Curvas ROC — Comparação de Modelos")
    ax.legend(loc="lower right")
    plt.tight_layout()
    return fig


def plot_feature_importance(importance: pd.Series, title: str = "Importância das Features"):
    """Barplot horizontal de importância das features."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    importance.sort_values().plot(kind="barh", ax=ax, color="#2196F3")
    ax.set_title(title)
    ax.set_xlabel("Importância")
    plt.tight_layout()
    return fig


def plot_elbow(inertias: list[float], k_range: range):
    """Método do cotovelo para K-Means."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(list(k_range), inertias, "o-", color="#2196F3")
    ax.set_title("Método do Cotovelo — K-Means")
    ax.set_xlabel("Número de Clusters (k)")
    ax.set_ylabel("Inércia (WCSS)")
    plt.tight_layout()
    return fig


def plot_pca_variance(explained_variance_ratio: np.ndarray):
    """Variância explicada acumulada pelo PCA."""
    cumulative = np.cumsum(explained_variance_ratio)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio,
           alpha=0.7, color="#2196F3", label="Variância por Componente")
    ax.step(range(1, len(cumulative) + 1), cumulative, where="mid",
            color="red", label="Variância Acumulada")
    ax.axhline(0.95, color="green", linestyle="--", label="95% de variância")
    ax.set_title("Variância Explicada pelo PCA")
    ax.set_xlabel("Componente Principal")
    ax.set_ylabel("Proporção da Variância")
    ax.legend()
    plt.tight_layout()
    return fig


def plot_clusters_2d(X_pca: np.ndarray, labels: np.ndarray, title: str = "Clusters no Espaço PCA"):
    """Scatter plot dos clusters no espaço das 2 primeiras componentes PCA."""
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap="tab10", alpha=0.6, s=10)
    plt.colorbar(scatter, ax=ax, label="Cluster")
    ax.set_title(title)
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    plt.tight_layout()
    return fig
