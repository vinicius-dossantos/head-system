# ✈️ Pipeline de Ciência de Dados — Dados de Voos

Este projeto implementa um pipeline completo de ciência de dados utilizando dados de voos, como parte do Tech Challenge da FIAP.

## 🎯 Objetivo

Analisar dados de voos para identificar padrões de atrasos, construir modelos preditivos e segmentar voos por comportamento operacional.

## 📁 Estrutura do Repositório

```
flights_pipeline/
├── README.md
├── requirements.txt
├── data/                        # Dados gerados sinteticamente
├── src/
│   ├── data_generation.py       # Geração do dataset sintético de voos
│   └── preprocessing.py         # Pré-processamento e feature engineering
└── notebooks/
    └── flight_data_pipeline.ipynb  # Notebook principal com todo o pipeline
```

## 🔧 Como Executar

### 1. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 2. Abrir o notebook

```bash
jupyter notebook notebooks/flight_data_pipeline.ipynb
```

### 3. Executar todas as células

No menu do Jupyter: **Kernel → Restart & Run All**

## 📊 Conteúdo do Pipeline

### 1. Exploração de Dados (EDA)
- Estatísticas descritivas do dataset
- Análise de valores ausentes e tratamento
- Distribuição dos atrasos por companhia aérea, aeroporto e horário
- Matriz de correlação e insights

### 2. Modelagem Supervisionada
- **Problema:** Classificação binária — prever se um voo terá atraso (> 15 min)
- **Modelos treinados:**
  - Regressão Logística
  - Random Forest
  - Gradient Boosting
- **Métricas:** Accuracy, Precision, Recall, F1-Score, ROC-AUC
- Comparação entre os modelos com tabela e curvas ROC

### 3. Modelagem Não Supervisionada
- **K-Means Clustering** com método do cotovelo (Elbow Method)
- **PCA** (Análise de Componentes Principais) para redução de dimensionalidade
- Visualização e interpretação dos clusters

### 4. Análise Crítica
- Conclusões sobre os modelos e os dados
- Limitações identificadas
- Sugestões de melhorias futuras

## 📦 Dependências Principais

| Biblioteca | Uso |
|-----------|-----|
| `pandas` | Manipulação de dados |
| `numpy` | Operações numéricas |
| `matplotlib` / `seaborn` | Visualizações |
| `scikit-learn` | Modelos de ML |
| `jupyter` | Execução do notebook |

## 📝 Dataset

O dataset é gerado sinteticamente dentro do próprio notebook, simulando 50.000 registros de voos com as seguintes features:

- `airline`: Companhia aérea (6 companhias)
- `origin` / `destination`: Aeroportos de origem/destino (8 aeroportos)
- `departure_hour`: Hora de partida (0–23)
- `day_of_week`: Dia da semana (0=Segunda, 6=Domingo)
- `month`: Mês do ano (1–12)
- `distance_km`: Distância do voo em km
- `dep_delay_min`: Atraso na partida (minutos)
- `arr_delay_min`: Atraso na chegada (minutos)
- `weather_delay`: Atraso por condições climáticas
- `carrier_delay`: Atraso por operação da companhia
- `is_delayed`: Target — 1 se atraso > 15 min, 0 caso contrário
