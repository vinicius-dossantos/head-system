"""
Módulo de geração e carregamento de dados sintéticos de voos.
"""
import numpy as np
import pandas as pd


# Reprodutibilidade
RNG = np.random.default_rng(42)

CARRIERS = ["GOL", "LATAM", "Azul", "Avianca", "TAM"]
AIRPORTS = ["GRU", "CGH", "GIG", "BSB", "SSA", "FOR", "REC", "POA", "CWB", "MAO"]
WEATHER = ["clear", "cloudy", "rain", "storm"]
WEATHER_PROBS = [0.55, 0.25, 0.15, 0.05]

# Distâncias aproximadas entre alguns pares de aeroportos (km)
DISTANCES = {
    ("GRU", "GIG"): 357,
    ("GRU", "BSB"): 873,
    ("GRU", "SSA"): 1947,
    ("GRU", "FOR"): 2368,
    ("GRU", "REC"): 2125,
    ("GRU", "POA"): 1100,
    ("GRU", "CWB"): 408,
    ("GRU", "MAO"): 2695,
    ("CGH", "GIG"): 354,
    ("CGH", "BSB"): 866,
    ("CGH", "SSA"): 1943,
    ("GIG", "BSB"): 928,
    ("GIG", "SSA"): 1650,
    ("GIG", "FOR"): 2817,
    ("BSB", "SSA"): 1080,
    ("BSB", "FOR"): 1692,
    ("BSB", "REC"): 1650,
    ("SSA", "FOR"): 1093,
    ("FOR", "REC"): 800,
    ("POA", "CWB"): 552,
}


def _get_distance(origin: str, destination: str) -> int:
    key = (origin, destination)
    rev = (destination, origin)
    if key in DISTANCES:
        return DISTANCES[key]
    if rev in DISTANCES:
        return DISTANCES[rev]
    return int(RNG.integers(300, 3000))


def generate_flight_data(n_samples: int = 10_000, save_path: str | None = None) -> pd.DataFrame:
    """Gera um dataset sintético de voos com n_samples registros.

    Parameters
    ----------
    n_samples:
        Número de registros a gerar.
    save_path:
        Se fornecido, salva o CSV neste caminho.

    Returns
    -------
    pd.DataFrame com os dados de voos.
    """
    origins = RNG.choice(AIRPORTS, size=n_samples)
    destinations = RNG.choice(AIRPORTS, size=n_samples)

    # Garante que origem != destino
    same = origins == destinations
    while same.any():
        destinations[same] = RNG.choice(AIRPORTS, size=same.sum())
        same = origins == destinations

    carriers = RNG.choice(CARRIERS, size=n_samples)
    months = RNG.integers(1, 13, size=n_samples)
    days_of_week = RNG.integers(1, 8, size=n_samples)
    hours = RNG.integers(0, 24, size=n_samples)

    weather = RNG.choice(WEATHER, size=n_samples, p=WEATHER_PROBS)

    distances = np.array([_get_distance(o, d) for o, d in zip(origins, destinations)])

    # Atraso base: influenciado por clima, hora do dia e distância
    base_delay = (
        RNG.normal(5, 15, size=n_samples)  # ruído
        + (weather == "rain") * RNG.normal(20, 10, size=n_samples)
        + (weather == "storm") * RNG.normal(60, 20, size=n_samples)
        + (hours >= 17) * RNG.normal(10, 5, size=n_samples)  # rush noturno
        + (days_of_week >= 5) * RNG.normal(8, 4, size=n_samples)  # fim de semana
    )

    departure_delay = np.clip(base_delay, -30, 300).astype(int)
    arrival_delay = (departure_delay + RNG.normal(0, 8, size=n_samples)).astype(int)

    # Introduz valores ausentes realistas (~2%)
    mask_dep = RNG.random(n_samples) < 0.02
    mask_arr = RNG.random(n_samples) < 0.02
    dep_delay_series = departure_delay.astype(float)
    arr_delay_series = arrival_delay.astype(float)
    dep_delay_series[mask_dep] = np.nan
    arr_delay_series[mask_arr] = np.nan

    df = pd.DataFrame(
        {
            "flight_id": range(1, n_samples + 1),
            "origin": origins,
            "destination": destinations,
            "carrier": carriers,
            "month": months,
            "day_of_week": days_of_week,
            "hour": hours,
            "distance_km": distances,
            "weather": weather,
            "departure_delay_min": dep_delay_series,
            "arrival_delay_min": arr_delay_series,
        }
    )

    # Variável alvo: atrasado se atraso na chegada >= 15 min
    df["is_delayed"] = (df["arrival_delay_min"] >= 15).astype("Int8")

    if save_path:
        df.to_csv(save_path, index=False)

    return df


def load_or_generate(path: str, n_samples: int = 10_000) -> pd.DataFrame:
    """Carrega dados do disco ou gera se não existir."""
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        df = generate_flight_data(n_samples=n_samples, save_path=path)
        return df
