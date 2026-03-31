# Avaliação — maria-c2003/FIAP-FASE-3

**Repositório:** https://github.com/maria-c2003/FIAP-FASE-3  
**Avaliado em:** 31/03/2026  
**Curso:** Pós-Graduação em Machine Learning Engineering — FIAP  
**Tema:** Análise de atrasos de voos nos EUA — Classificação, Regressão, Clusterização, PCA  
**Equipe:** 1 colaborador (maria-c2003)

---

## Nota Final: **52 / 90**

---

## Resumo Executivo

O repositório entrega um único script Python (`tech_challenge.py`, 744 linhas) que implementa EDA, classificação binária, clusterização de aeroportos e PCA em um pipeline coeso, executável via linha de comando. A abordagem técnica é sólida: uso de DuckDB para carga de dados em larga escala, `sklearn.pipeline.Pipeline` com transformadores customizados, argparse CLI com seed configurável e geração automática de relatórios (CSV + PNGs).

**Ponto crítico:** o modelo de **regressão está completamente ausente** (nenhuma predição de atraso em minutos), sendo o único requisito do enunciado não implementado. Além disso, a ausência de `requirements.txt`, README e de outputs versionados compromete a reprodutibilidade e a documentação do trabalho.

---

## Inventário do Repositório

| Arquivo | Tamanho | Descrição |
|---|---|---|
| `tech_challenge.py` | 25,6 KB / 744 linhas | Script principal do pipeline |
| `.gitattributes` | — | Gerado pelo GitHub (auto) |
| `.mplconfig/fontlist-v390.json` | 124 KB | Cache de fontes Matplotlib (acidental) |

**Commits:** 2 (`Initial commit` + `create project`)  
**Branches:** 1 (`main`) | **Issues/PRs:** 0  

---

## Análise do Código — `tech_challenge.py`

### Estrutura Geral

```
tech_challenge.py
├── _set_plot_style()           — configuração visual seaborn/matplotlib
├── _hhmm_to_minutes()          — converte HHMM → minutos (robusto a NaN)
├── _minutes_to_hour_bucket()   — classifica período do dia (manhã/tarde/noite/madrugada)
├── FrequencyEncoder            — transformer sklearn customizado (log1p freq encoding)
├── SupervisedMetrics           — dataclass de métricas de classificação
├── _evaluate_binary()          — ROC-AUC, PR-AUC, F1, precision, recall, best threshold
├── _supervised_sample()        — amostragem via DuckDB com fallback
├── run_eda()                   — análise exploratória (4 gráficos + 3 CSVs)
├── run_supervised()            — classificação (LogReg + HistGBT)
├── run_unsupervised()          — KMeans (k=3..8, silhouette) + PCA 2D
└── main() + parse_args()       — CLI com argparse
```

### Módulo EDA (`run_eda`)

**O que produz:**
- `eda_overview.csv` — totais de cancelamentos, desvios e atrasos nulos
- `eda_arrival_delay_hist.png` — histograma de atraso (amostra de 250 k voos)
- `eda_by_airline.csv` + `eda_top_airlines_delay_rate.png` — ranking de companhias por taxa de atraso
- `eda_by_origin_airport.csv` + `eda_top_origin_airports_delay_rate.png` — ranking de aeroportos
- `eda_heatmap_day_hour.png` — heatmap dia-da-semana × hora-de-partida

**Pontos positivos:**
- Usa `TRY_CAST` no DuckDB para tolerância a dados sujos
- Filtra cancelados e desviados antes de qualquer agregação
- Frequência normalizada com `PercentFormatter`
- Heatmap com granularidade de hora (0–23) e dia, pivot correto

**Pontos negativos:**
- Sem análise temporal por mês/sazonalidade
- Sem correlação entre features numéricas
- Sem boxplot de atraso por companhia/aeroporto (apenas taxa binária)

### Módulo Classificação (`run_supervised`)

**Features usadas:**

| Tipo | Features |
|---|---|
| Numéricas | `MONTH`, `DAY`, `DAY_OF_WEEK`, `SCHEDULED_TIME`, `DISTANCE`, `sched_dep_hour` |
| Categóricas | `AIRLINE`, `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT`, `periodo_dia` |

**Target:** `delayed = (ARRIVAL_DELAY > delay_threshold)` — padrão 15 min

**Modelo 1 — Regressão Logística:**
- Pré-processamento: `SimpleImputer(median)` + `StandardScaler` para numéricas; `SimpleImputer(most_frequent)` + `OneHotEncoder(handle_unknown='ignore')` para categóricas
- `class_weight='balanced'` ✅ — trata desbalanceamento
- `solver='saga'`, `max_iter=2000` — adequado para dataset grande
- `sklearn.pipeline.Pipeline` completo ✅

**Modelo 2 — HistGradientBoostingClassifier:**
- Pré-processamento: `SimpleImputer(median)` + `FrequencyEncoder` customizado
- `FrequencyEncoder`: codifica frequência logarítmica (`log1p(freq/total)`) por categoria — técnica válida, evita alta esparsidade do OHE
- `learning_rate=0.08`, `max_depth=6`, `max_iter=250` — hiperparâmetros razoáveis
- **Sem `class_weight`** ❌ — desbalanceamento não tratado no HGB

**Métricas calculadas:**
- ROC-AUC, PR-AUC, F1@0.5, Precision@0.5, Recall@0.5, Best-F1 + threshold ótimo
- Matrizes de confusão com anotação de `n` e `%` por linha (real)
- Análise de coeficientes da LogReg exportada para CSV

**Problemas técnicos:**
- `FrequencyEncoder` armazena mapas por índice de coluna (`maps[i]`) em vez de por nome — frágil se `feature_cols_cat` mudar de ordem
- Sem validação cruzada — único split 75%/25%
- Modelos não são serializados (`joblib.dump`) — impossível reutilizar sem re-treinar
- Fallback em `_supervised_sample` (quando amostra é menor que `sample_size`) não aplica `random_state` → não reprodutível nesse caso

### Módulo Clusterização + PCA (`run_unsupervised`)

**Features por aeroporto (7):** `n_flights_total`, `cancel_rate`, `divert_rate`, `avg_arrival_delay`, `pct_delayed`, `latitude`, `longitude`

**Pipeline:**
1. `SimpleImputer(median)` + `StandardScaler`
2. Busca de k ótimo (k=3..8) por `silhouette_score` ✅
3. KMeans final com melhor k
4. PCA 2D para visualização dos clusters ✅

**Outputs:**
- `unsup_airport_features.csv` — features por aeroporto com cluster
- `unsup_airport_clusters.csv` — idem
- `unsup_pca_clusters.png` — scatter PCA colorido por cluster
- `unsup_silhouette_by_k.png` — curva silhouette por k

**Pontos positivos:**
- Seleção automática de k por silhouette — sem escolha arbitrária ✅
- `np.clip(X, -20, 20)` após `nan_to_num` — proteção contra outliers extremos ✅
- PCA 2D com `random_state` para reprodutibilidade ✅
- Latitude/longitude como features geoespaciais — diferencial interessante ✅

**Pontos negativos:**
- Variância explicada pelos componentes PCA não é reportada
- Sem tabela de caracterização dos clusters (médias por cluster)
- Sem método do cotovelo (elbow) complementando o silhouette

---

## Critérios de Avaliação

### 1. Aderência ao Problema (20/25)

| Requisito | Status | Evidência |
|---|---|---|
| EDA | ✅ | `run_eda()` — 4 gráficos + 3 CSVs |
| Classificação | ✅ | LogReg + HistGBT com métricas completas |
| **Regressão** | ❌ | **Completamente ausente** |
| Clusterização | ✅ | KMeans com silhouette selection, k=3..8 |
| PCA | ✅ | PCA 2D como visualização dos clusters |

Regressão não implementada (predição de `ARRIVAL_DELAY` como valor contínuo). **−5 pts.**

### 2. Reprodutibilidade (7/15)

| Item | Status | Detalhe |
|---|---|---|
| Código presente | ✅ | `tech_challenge.py` funcional |
| `--seed` parametrizado | ✅ | `argparse`, padrão 42 |
| `stratify=y` no split | ✅ | Linha 492 |
| `requirements.txt` | ❌ | Dependências não declaradas (duckdb, sklearn, seaborn…) |
| README / instruções de uso | ❌ | Nenhuma documentação de como executar |
| Modelos salvos | ❌ | Nenhum `.pkl` / `joblib.dump` |
| Fallback sem seed | ⚠️ | `_supervised_sample` fallback sem `random_state` |

### 3. Qualidade Técnica do Código (19/25)

| Aspecto | Avaliação |
|---|---|
| `sklearn.pipeline.Pipeline` correto | ✅ +5 |
| `FrequencyEncoder` sklearn-compatível (fit/transform) | ✅ +3 |
| DuckDB para leitura eficiente de CSV grandes | ✅ +3 |
| `@dataclass SupervisedMetrics` | ✅ +2 |
| CLI completo via argparse | ✅ +2 |
| Matriz de confusão com % por linha | ✅ +2 |
| Silhouette selection para KMeans | ✅ +2 |
| `class_weight='balanced'` na LogReg | ✅ +1 |
| **HGB sem tratamento de desbalanceamento** | ❌ −2 |
| **FrequencyEncoder indexado por posição, não nome** | ❌ −1 |
| **Sem validação cruzada (k-fold)** | ❌ −2 |
| Sem serialização dos modelos treinados | ❌ −1 |
| Fallback não-reprodutível em `_supervised_sample` | ❌ −1 |

### 4. Documentação (2/10)

| Item | Status |
|---|---|
| README com instruções de uso | ❌ |
| Docstrings nas funções | ❌ |
| Comentários no código | ⚠️ Mínimo (apenas mensagens de argparse) |
| Descrições de variáveis / features | ❌ |

O `argparse` provê descrições mínimas dos argumentos CLI, mas não há documentação de alto nível.

### 5. Evidências de Execução (0/10)

| Item | Status |
|---|---|
| Outputs (PNGs, CSVs) versionados | ❌ |
| Exemplo de métricas do modelo | ❌ |
| Screenshots / demonstração | ❌ |

O script gera outputs em pasta local (`outputs/run_YYYYMMDD_HHMMSS/`), mas nenhum resultado foi commitado ao repositório.

### 6. Critérios Não Funcionais (4/5)

| Item | Status |
|---|---|
| `.gitignore` | ❌ `.mplconfig/` foi commitado por acidente |
| `requirements.txt` | ❌ |
| Código modular e reutilizável | ✅ |
| `MPLBACKEND=Agg` (headless) | ✅ adequado para execução em servidor |
| `MPLCONFIGDIR` configurado via env | ✅ |
| Pasta de output com timestamp (`run_YYYYMMDD_HHMMSS`) | ✅ |

---

## Resumo de Pontuação

| Critério | Obtido | Máximo |
|---|---|---|
| 1. Aderência ao Problema | 20 | 25 |
| 2. Reprodutibilidade | 7 | 15 |
| 3. Qualidade Técnica | 19 | 25 |
| 4. Documentação | 2 | 10 |
| 5. Evidências de Execução | 0 | 10 |
| 6. Critérios Não Funcionais | 4 | 5 |
| **Total** | **52** | **90** |

---

## Pontos de Destaque Positivos

1. **DuckDB como engine de dados** — escolha inteligente para processar o dataset de voos (5+ milhões de linhas) sem carregar tudo em memória
2. **`FrequencyEncoder` sklearn-compatível** — transformer customizado com `fit`/`transform` corretos, integrável em pipeline de produção
3. **Dois modelos distintos** com pré-processamentos diferentes (OHE para LogReg, Frequency Encoding para HGB)
4. **Seleção automática de k** via silhouette score — sem decisão arbitrária
5. **CLI com argparse** — script executável com parâmetros configuráveis

## Principais Lacunas

1. **Regressão ausente** — predição do atraso em minutos (`ARRIVAL_DELAY` como alvo contínuo) não foi implementada. Seria esperado pelo menos um modelo de `Ridge`, `GradientBoostingRegressor` ou similar com RMSE/MAE
2. **Sem `requirements.txt`** — dependências não declaradas (duckdb, pandas, numpy, scikit-learn, seaborn, matplotlib)
3. **Sem README** — não há instruções de como baixar os dados (Kaggle), instalar dependências e executar o script
4. **Sem outputs versionados** — nenhuma evidência de que o código foi executado com sucesso
5. **`.mplconfig/` commitado** — deveria estar no `.gitignore`
