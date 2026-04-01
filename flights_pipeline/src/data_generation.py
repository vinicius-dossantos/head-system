"""
data_generation.py
------------------
Gera um dataset sintético de voos com características realistas para uso
no pipeline de ciência de dados.
"""

import numpy as np
import pandas as pd


AIRLINES = ["AA", "DL", "UA", "WN", "B6", "AS"]
AIRPORTS = ["JFK", "LAX", "ORD", "ATL", "DFW", "DEN", "SEA", "BOS"]

# Probabilidades de atraso por companhia (simulando diferenças reais)
AIRLINE_DELAY_PROB = {
    "AA": 0.35,
    "DL": 0.25,
    "UA": 0.38,
    "WN": 0.30,
    "B6": 0.42,
    "AS": 0.22,
}

# Pesos para distâncias típicas entre aeroportos (km)
MEAN_DELAY_MINUTES = 35    # Average delay magnitude for delayed flights (exponential mean)
MIN_DELAY_OFFSET = 15     # Minimum delay threshold to be classified as "delayed"

DISTANCE_PARAMS = {
    ("JFK", "LAX"): (4100, 300),
    ("JFK", "ORD"): (1190, 100),
    ("JFK", "ATL"): (1230, 100),
    ("LAX", "DFW"): (2240, 200),
    ("ORD", "DEN"): (1470, 120),
    ("ATL", "BOS"): (1720, 150),
    ("DEN", "SEA"): (1650, 130),
    ("DFW", "BOS"): (2760, 200),
}


def _get_distance(origin: str, destination: str, rng: np.random.Generator) -> float:
    """Retorna distância estimada (km) entre origin e destination."""
    key = tuple(sorted([origin, destination]))
    if key in DISTANCE_PARAMS:
        mu, sigma = DISTANCE_PARAMS[key]
    else:
        mu, sigma = 1800, 400
    return max(200, rng.normal(mu, sigma))


def generate_flight_dataset(n_samples: int = 50_000, random_state: int = 42) -> pd.DataFrame:
    """
    Gera um DataFrame com n_samples registros de voos sintéticos.

    Parameters
    ----------
    n_samples : int
        Número de registros a gerar.
    random_state : int
        Semente para reprodutibilidade.

    Returns
    -------
    pd.DataFrame
        Dataset de voos com features e target.
    """
    rng = np.random.default_rng(random_state)

    airlines = rng.choice(AIRLINES, size=n_samples, p=[1 / len(AIRLINES)] * len(AIRLINES))
    origins = rng.choice(AIRPORTS, size=n_samples)
    destinations = rng.choice(AIRPORTS, size=n_samples)

    # Evitar origem == destino
    same = origins == destinations
    while same.any():
        destinations[same] = rng.choice(AIRPORTS, size=same.sum())
        same = origins == destinations

    departure_hour = rng.integers(0, 24, size=n_samples)
    day_of_week = rng.integers(0, 7, size=n_samples)
    month = rng.integers(1, 13, size=n_samples)

    distances = np.array([
        _get_distance(origins[i], destinations[i], rng)
        for i in range(n_samples)
    ])

    # Probabilidade base de atraso por companhia
    base_delay_prob = np.array([AIRLINE_DELAY_PROB[a] for a in airlines])

    # Ajustes situacionais
    peak_hour_factor = np.where((departure_hour >= 7) & (departure_hour <= 9), 0.10, 0.0)
    peak_hour_factor += np.where((departure_hour >= 17) & (departure_hour <= 19), 0.12, 0.0)
    weekend_factor = np.where(day_of_week >= 5, 0.05, 0.0)
    winter_factor = np.where((month == 12) | (month == 1) | (month == 2), 0.08, 0.0)
    summer_factor = np.where((month == 6) | (month == 7) | (month == 8), 0.04, 0.0)

    delay_prob = np.clip(
        base_delay_prob + peak_hour_factor + weekend_factor + winter_factor + summer_factor,
        0.0,
        0.95,
    )

    is_delayed = rng.binomial(1, delay_prob).astype(int)

    # Minutos de atraso
    dep_delay_min = np.where(
        is_delayed == 1,
        rng.exponential(MEAN_DELAY_MINUTES, size=n_samples) + MIN_DELAY_OFFSET,
        np.maximum(0, rng.normal(-2, 8, size=n_samples)),
    ).round(1)

    arr_delay_min = dep_delay_min + rng.normal(0, 10, size=n_samples)
    arr_delay_min = arr_delay_min.round(1)

    weather_delay = np.where(
        is_delayed == 1,
        rng.exponential(10, size=n_samples) * rng.binomial(1, 0.3, size=n_samples),
        0.0,
    ).round(1)

    carrier_delay = np.where(
        is_delayed == 1,
        rng.exponential(15, size=n_samples) * rng.binomial(1, 0.5, size=n_samples),
        0.0,
    ).round(1)

    # Introduzir ~3% de valores ausentes em colunas selecionadas
    missing_mask_dep = rng.random(n_samples) < 0.03
    missing_mask_weather = rng.random(n_samples) < 0.03
    dep_delay_min = dep_delay_min.astype(object)
    dep_delay_min[missing_mask_dep] = np.nan
    weather_delay = weather_delay.astype(object)
    weather_delay[missing_mask_weather] = np.nan

    df = pd.DataFrame(
        {
            "airline": airlines,
            "origin": origins,
            "destination": destinations,
            "departure_hour": departure_hour,
            "day_of_week": day_of_week,
            "month": month,
            "distance_km": distances.round(0).astype(int),
            "dep_delay_min": dep_delay_min,
            "arr_delay_min": arr_delay_min,
            "weather_delay": weather_delay,
            "carrier_delay": carrier_delay,
            "is_delayed": is_delayed,
        }
    )

    return df
