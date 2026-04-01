"""
preprocessing.py
----------------
Funções utilitárias de pré-processamento e engenharia de features
para o pipeline de voos.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer


CATEGORICAL_FEATURES = ["airline", "origin", "destination"]
NUMERICAL_FEATURES = [
    "departure_hour",
    "day_of_week",
    "month",
    "distance_km",
    "dep_delay_min",
    "weather_delay",
    "carrier_delay",
]
TARGET = "is_delayed"


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata valores ausentes:
    - Numéricas: preenche com a mediana
    - Categóricas: preenche com a moda
    """
    df = df.copy()
    num_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=["object", "category"]).columns

    for col in num_cols:
        if df[col].isna().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)

    for col in cat_cols:
        if df[col].isna().any():
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)

    return df


def build_preprocessor() -> ColumnTransformer:
    """
    Constrói e retorna o ColumnTransformer com:
    - Pipeline numérico: imputação + normalização
    - Pipeline categórico: imputação + one-hot encoding
    """
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERICAL_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )

    return preprocessor


def split_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """
    Separa o DataFrame em conjuntos de treino e teste.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset completo contendo features e target.
    test_size : float, optional
        Proporção do conjunto de teste (padrão: 0.2).
    random_state : int, optional
        Semente para reprodutibilidade (padrão: 42).

    Returns
    -------
    X_train, X_test, y_train, y_test
    """
    feature_cols = CATEGORICAL_FEATURES + NUMERICAL_FEATURES
    X = df[feature_cols]
    y = df[TARGET]
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
