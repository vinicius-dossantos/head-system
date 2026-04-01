# Tech Challenge — Pipeline de Ciência de Dados: Análise de Voos

## Descrição

Este projeto implementa um pipeline completo de ciência de dados aplicado a dados de voos domésticos. O objetivo é prever atrasos na chegada (> 15 minutos) e identificar padrões por meio de clusterização.

O dataset utilizado é **sintético e reprodutível**, gerado com semente fixa (`random_state=42`), eliminando a necessidade de downloads externos.

---

## Estrutura do Repositório

```
tech-challenge/
├── README.md                         ← Este arquivo
├── requirements.txt                  ← Dependências do projeto
├── notebooks/
│   ├── 01_eda.ipynb                  ← Análise Exploratória de Dados (EDA)
│   ├── 02_supervised_modeling.ipynb  ← Modelagem Supervisionada (Classificação)
│   └── 03_unsupervised_modeling.ipynb← Modelagem Não Supervisionada (K-Means + PCA)
└── src/
    └── utils.py                      ← Geração de dados e pré-processamento
```

---

## Instalação e Execução

### 1. Criar ambiente virtual (recomendado)

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows
```

### 2. Instalar dependências

```bash
cd tech-challenge
pip install -r requirements.txt
```

### 3. Iniciar o Jupyter Notebook

```bash
jupyter notebook notebooks/
```

Execute os notebooks **na ordem**: `01_eda.ipynb` → `02_supervised_modeling.ipynb` → `03_unsupervised_modeling.ipynb`.

---

## Descrição do Dataset

O dataset é gerado pelo módulo `src/utils.py` e contém **5.000 registros** de voos domésticos brasileiros sintéticos com as seguintes variáveis:

| Variável              | Tipo        | Descrição                                      |
|-----------------------|-------------|------------------------------------------------|
| `airline`             | Categórica  | Companhia aérea (LATAM, GOL, AZUL, TAM, AVIANCA) |
| `origin`              | Categórica  | Aeroporto de origem (código IATA)              |
| `destination`         | Categórica  | Aeroporto de destino (código IATA)             |
| `month`               | Numérica    | Mês do voo (1–12)                              |
| `day_of_week`         | Numérica    | Dia da semana (0=Seg, 6=Dom)                   |
| `dep_hour`            | Numérica    | Hora de partida (5–23)                         |
| `distance_km`         | Numérica    | Distância do voo em km                         |
| `weather`             | Categórica  | Condição climática (CLEAR, RAIN, FOG, STORM, WIND) |
| `dep_delay_min`       | Numérica    | Atraso na partida em minutos                   |
| `arr_delay_min`       | Numérica    | Atraso na chegada em minutos                   |
| `taxi_out_min`        | Numérica    | Tempo de taxiamento na saída em minutos        |
| `taxi_in_min`         | Numérica    | Tempo de taxiamento na chegada em minutos      |
| `carrier_delay_min`   | Numérica    | Atraso atribuído à companhia em minutos        |
| `cancelled`           | Binária     | 1 = voo cancelado, 0 = realizado               |
| `delayed`             | **Alvo**    | 1 = atraso na chegada > 15 min, 0 = pontual    |

---

## Pipeline de Modelagem

### 01 — Análise Exploratória de Dados (EDA)
- Estatísticas descritivas
- Análise e tratamento de valores ausentes (voos cancelados)
- Distribuição da variável alvo
- Visualizações: histogramas, boxplots, heatmap de correlação
- Insights: impacto do clima, dia da semana e horário nos atrasos

### 02 — Modelagem Supervisionada
- **Algoritmos**: Regressão Logística (baseline) e Random Forest (modelo principal)
- **Pré-processamento**: padronização com `StandardScaler`, one-hot encoding
- **Métricas**: Acurácia, Precisão, Recall, F1-Score, AUC-ROC, Matriz de Confusão
- **Validação**: divisão treino/teste (80/20) + validação cruzada estratificada (5-fold)
- **Análise**: importância das features no Random Forest

### 03 — Modelagem Não Supervisionada
- **PCA**: análise de variância explicada, scree plot, loadings das componentes
- **K-Means**: método do cotovelo + Silhouette Score para seleção de k
- **Visualização**: clusters projetados no espaço PCA 2D
- **Interpretação**: perfil médio dos clusters, distribuição climática e por companhia

---

## Reprodutibilidade

Todos os experimentos utilizam `random_state=42`. O dataset é gerado deterministicamente pela função `generate_flight_data()` em `src/utils.py`, garantindo reprodutibilidade completa sem dependências externas de dados.

---

## Tecnologias Utilizadas

| Biblioteca     | Versão  | Uso                                |
|----------------|---------|-------------------------------------|
| pandas         | 2.2.2   | Manipulação de dados                |
| numpy          | 1.26.4  | Operações numéricas                 |
| matplotlib     | 3.9.0   | Visualizações                       |
| seaborn        | 0.13.2  | Visualizações estatísticas          |
| scikit-learn   | 1.5.0   | Modelagem e métricas                |
| jupyter        | 1.0.0   | Ambiente de notebooks               |
| scipy          | 1.13.1  | Análise estatística                 |
