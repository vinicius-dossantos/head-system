"""
Módulo de pré-processamento e feature engineering para dados de voos.
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


CATEGORICAL_COLS = ["origin", "destination", "carrier", "weather"]
NUMERICAL_COLS = ["month", "day_of_week", "hour", "distance_km", "departure_delay_min"]
TARGET_COL = "is_delayed"


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Preenche valores ausentes com a mediana (numérico) ou moda (categórico)."""
    df = df.copy()
    for col in df.select_dtypes(include=[np.number]).columns:
        median = df[col].median()
        df[col] = df[col].fillna(median)
    for col in df.select_dtypes(include=["object", "category"]).columns:
        mode = df[col].mode()[0]
        df[col] = df[col].fillna(mode)
    return df


def encode_categoricals(df: pd.DataFrame, cols: list[str] | None = None) -> pd.DataFrame:
    """Aplica Label Encoding nas colunas categóricas especificadas."""
    df = df.copy()
    cols = cols or CATEGORICAL_COLS
    for col in cols:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    return df


def build_feature_matrix(
    df: pd.DataFrame,
    feature_cols: list[str] | None = None,
    target_col: str = TARGET_COL,
    scale: bool = False,
) -> tuple[pd.DataFrame, pd.Series, StandardScaler | None]:
    """Retorna X, y e (opcionalmente) o scaler ajustado."""
    df = handle_missing_values(df)
    df = encode_categoricals(df)

    feature_cols = feature_cols or (CATEGORICAL_COLS + NUMERICAL_COLS)
    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols].copy()
    y = df[target_col].astype(int)

    scaler = None
    if scale:
        scaler = StandardScaler()
        num_cols_present = [c for c in NUMERICAL_COLS if c in X.columns]
        X.loc[:, num_cols_present] = scaler.fit_transform(X[num_cols_present])

    return X, y, scaler


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Divide dados em treino e teste."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
