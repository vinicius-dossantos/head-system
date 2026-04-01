"""
Utilitários para o pipeline de ciência de dados de voos.
Inclui geração de dados sintéticos e funções de pré-processamento.
"""

import numpy as np
import pandas as pd


RANDOM_STATE = 42

AIRLINES = ["LATAM", "GOL", "AZUL", "TAM", "AVIANCA"]
ORIGINS = ["GRU", "GIG", "BSB", "SSA", "FOR", "REC", "CWB", "BEL", "MAO", "CGH"]
DESTINATIONS = ["GRU", "GIG", "BSB", "SSA", "FOR", "REC", "CWB", "BEL", "MAO", "CGH"]
WEATHER_CONDITIONS = ["CLEAR", "RAIN", "FOG", "STORM", "WIND"]


def generate_flight_data(n_samples: int = 5000, random_state: int = RANDOM_STATE) -> pd.DataFrame:
    """
    Gera um dataset sintético de voos domésticos brasileiros.

    Parâmetros
    ----------
    n_samples : int
        Número de registros a serem gerados.
    random_state : int
        Semente para reprodutibilidade.

    Retorna
    -------
    pd.DataFrame
        Dataset de voos com as colunas descritas abaixo.
    """
    rng = np.random.default_rng(random_state)

    airlines = rng.choice(AIRLINES, size=n_samples, p=[0.30, 0.25, 0.25, 0.10, 0.10])
    origins = rng.choice(ORIGINS, size=n_samples)

    destinations = []
    for orig in origins:
        choices = [d for d in DESTINATIONS if d != orig]
        destinations.append(rng.choice(choices))
    destinations = np.array(destinations)

    months = rng.integers(1, 13, size=n_samples)
    day_of_week = rng.integers(0, 7, size=n_samples)
    dep_hour = rng.integers(5, 24, size=n_samples)

    distance_km = rng.integers(300, 5000, size=n_samples)

    weather = rng.choice(WEATHER_CONDITIONS, size=n_samples, p=[0.55, 0.20, 0.10, 0.10, 0.05])

    # Taxiamento (informação operacional, não conta como atraso puro)
    taxi_out = rng.integers(5, 40, size=n_samples).astype(float)
    taxi_in = rng.integers(3, 20, size=n_samples).astype(float)

    # Atraso da companhia (~15% dos voos)
    carrier_delay = np.where(
        rng.random(n_samples) < 0.15,
        rng.integers(5, 60, size=n_samples),
        0
    ).astype(float)

    # Atraso base: clima, dia da semana, sazonalidade e ruído
    is_peak_month = np.isin(months, [12, 1, 7]).astype(float)
    is_weekend = (day_of_week >= 5).astype(float)

    weather_delay = (
        (weather == "STORM") * rng.integers(20, 90, size=n_samples)
        + (weather == "RAIN") * rng.integers(5, 40, size=n_samples)
        + (weather == "FOG") * rng.integers(3, 20, size=n_samples)
        + (weather == "WIND") * rng.integers(2, 15, size=n_samples)
    ).astype(float)

    # Dep delay: ruído gaussiano centrado em -5 (maioria pontual ou adiantado)
    noise = rng.normal(-5, 8, size=n_samples)
    dep_delay = (noise + weather_delay * 0.6 + carrier_delay * 0.5 + is_peak_month * rng.integers(0, 10, size=n_samples) + is_weekend * rng.integers(0, 8, size=n_samples)).astype(float)

    # Arr delay: baseado no dep_delay com recuperação parcial em voo
    recovery = rng.uniform(0, 0.3, size=n_samples) * np.abs(dep_delay)
    arr_delay = (dep_delay - recovery + rng.normal(0, 5, size=n_samples)).astype(float)

    # Cancelamentos: 3% dos voos
    cancelled = (rng.random(n_samples) < 0.03).astype(int)
    dep_delay = np.where(cancelled == 1, np.nan, dep_delay)
    arr_delay = np.where(cancelled == 1, np.nan, arr_delay)

    # Variável alvo binária: atraso na chegada > 15 minutos
    delayed = np.where(cancelled == 1, np.nan, (arr_delay > 15).astype(float))

    df = pd.DataFrame({
        "airline": airlines,
        "origin": origins,
        "destination": destinations,
        "month": months,
        "day_of_week": day_of_week,
        "dep_hour": dep_hour,
        "distance_km": distance_km,
        "weather": weather,
        "dep_delay_min": dep_delay,
        "arr_delay_min": arr_delay,
        "taxi_out_min": taxi_out,
        "taxi_in_min": taxi_in,
        "carrier_delay_min": carrier_delay,
        "cancelled": cancelled,
        "delayed": delayed,
    })

    return df


def preprocess_for_modeling(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica pré-processamento para modelagem:
    - Remove registros cancelados
    - Preenche valores ausentes
    - Codifica variáveis categóricas

    Parâmetros
    ----------
    df : pd.DataFrame
        Dataset bruto de voos.

    Retorna
    -------
    pd.DataFrame
        Dataset pronto para modelagem.
    """
    df_model = df[df["cancelled"] == 0].copy()
    df_model["dep_delay_min"] = df_model["dep_delay_min"].fillna(
        df_model["dep_delay_min"].median()
    )
    df_model["arr_delay_min"] = df_model["arr_delay_min"].fillna(
        df_model["arr_delay_min"].median()
    )
    df_model["delayed"] = df_model["delayed"].fillna(0).astype(int)

    df_model = pd.get_dummies(
        df_model,
        columns=["airline", "origin", "destination", "weather"],
        drop_first=True,
    )

    return df_model


def get_feature_columns(df: pd.DataFrame) -> list:
    """
    Retorna as colunas de features para modelagem (exclui targets e identificadores).
    """
    exclude = {"dep_delay_min", "arr_delay_min", "delayed", "cancelled"}
    return [c for c in df.columns if c not in exclude]
