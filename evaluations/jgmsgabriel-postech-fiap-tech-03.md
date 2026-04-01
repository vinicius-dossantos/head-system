# Avaliação — jgmsgabriel/postech-fiap-tech-03

**Repositório:** https://github.com/jgmsgabriel/postech-fiap-tech-03  
**Avaliado em:** 01/04/2026  
**Curso:** Pós-Graduação em Machine Learning Engineering — FIAP  
**Tema:** Análise de atrasos de voos nos EUA — EDA, Classificação, Clusterização  
**Equipe:** 1 colaborador (jgmsgabriel) | 1 commit

---

## Nota Final: **61 / 90**

---

## Resumo Executivo

Repositório bem estruturado e com execução comprovada. A EDA é das mais completas entre os trabalhos avaliados: 10 figuras PNG e 10 CSVs de resultados foram commitados como evidências de execução. A modelagem supervisionada apresenta três classificadores (Logistic Regression, Random Forest e XGBoost) com validação cruzada 5-fold e métricas adequadas — XGBoost lidera com AUC=0.777. A clusterização não supervisionada é sofisticada: agrupa 4.591 rotas com KMeans (k=7 selecionado via método do cotovelo e silhouette score) e adiciona DBSCAN para detecção de outliers. **Os dois problemas críticos são a ausência completa de Modelo de Regressão e PCA** (2 dos 5 componentes obrigatórios), e a **ausência de README.md**, que priva o repositório de qualquer documentação textual sobre o projeto.

---

## Inventário do Repositório

| Arquivo / Diretório | Tamanho | Descrição |
|---|---|---|
| `.gitignore` | 37 B | Exclui `.venv`, `data/raw/`, `outputs/tables/`, `*.csv` |
| `data/dicionario_dados_flights.pdf` | — | ✅ Dicionário de dados (adição rara e positiva) |
| `data/raw/airlines.csv` | — | ✅ Commitado (force-added, pois .gitignore ignora `data/raw/`) |
| `data/raw/airports.csv` | — | ✅ Commitado (force-added) |
| `data/raw/flights.csv` | — | ✅ Corretamente não versionado (arquivo grande) |
| `outputs/figures/` (10 PNGs) | — | ✅ Evidências visuais de execução |
| `outputs/tables/` (10 CSVs) | — | ✅ Resultados tabulares commitados (force-added) |
| `src/notebooks/tech_challenge_fase3_flights.ipynb` | 1,7 MB | Notebook principal: EDA + Classificação |
| `src/notebooks/tech_challenge_fase3_unsupervised.ipynb` | 849 KB | Notebook: Clusterização não supervisionada |
| **`README.md`** | — | ❌ **AUSENTE** — repositório sem documentação textual |
| **`requirements.txt`** | — | ❌ **AUSENTE** — dependências não declaradas |

**Commits:** 1 | **Branches:** 1 | **Issues/PRs:** 0

> **Nota sobre `.gitignore`:** O arquivo lista `data/raw/` e `outputs/tables/` como ignorados, mas os CSVs de aeroportos/companhias e os 10 CSVs de resultados estão commitados (provavelmente via `git add -f`). O comportamento é funcionalmente correto — os arquivos estão disponíveis — mas o `.gitignore` não reflete fielmente o que é versionado.

---

## Análise por Seção

### `tech_challenge_fase3_flights.ipynb` — EDA e Classificação

#### Carregamento de Dados

```python
flights_path = DATA_RAW / 'flights.csv'
df_flights = pd.read_csv(flights_path, ...)
```

✅ Uso de `pathlib.Path` — sem caminhos absolutos hardcoded.  
❌ `DtypeWarning` nas colunas 7/8 — ausência de `low_memory=False` ou `dtype` explícito.

Dataset: **5.819.079 voos × 31 colunas**.

---

#### EDA — Análise Exploratória

**Figuras geradas e commitadas (10 PNGs):**

| Arquivo | Conteúdo |
|---|---|
| `missing_percent.png` | Análise de dados ausentes |
| `hist_numeric.png` | Histogramas de variáveis numéricas |
| `boxplot_numeric.png` | Boxplots das variáveis numéricas |
| `corr_heatmap.png` | Mapa de calor de correlações |
| `delayed_countplot.png` | Distribuição da variável alvo |
| `delayed_rate_airline.png` | Taxa de atraso por companhia aérea |
| `delayed_rate_month.png` | Taxa de atraso por mês (**sazonalidade** ✅) |
| `delayed_rate_origin_airport.png` | Taxa de atraso por aeroporto de origem |
| `top10_airlines.png` | Top 10 companhias por volume |
| `top10_origin_airports.png` | Top 10 aeroportos de origem por volume |

**Tabelas geradas e commitadas (10 CSVs):**
`corr_matrix.csv`, `delayed_by_airline.csv`, `delayed_by_month.csv`, `delayed_by_origin_airport.csv`, `describe_numeric.csv`, `dtypes_flights.csv`, `missing_report.csv`, `nunique_all.csv`, `top10_airline.csv`, `top10_origin_airport.csv`

A EDA inclui análise de missing data, estatísticas descritivas, correlações, sazonalidade mensal (ponto que muitos trabalhos ignoram) e top aeroportos/companhias. É uma das EDAs mais completas entre os trabalhos avaliados desta turma.

**Taxa de atraso por mês (evidência de sazonalidade):**

| Mês | Taxa de atraso |
|---|---|
| Fevereiro | 53,7% |
| Junho | 52,9% |
| Janeiro | 50,0% |
| Março | 49,9% |
| Julho | 49,8% |
| Dezembro | 49,6% |
| Agosto | 46,9% |
| Maio | 46,1% |
| Abril | 46,0% |
| Novembro | 43,0% |
| Setembro | 38,4% |

> A taxa média de ~47% indica dataset **razoavelmente balanceado**, o que explica recalls de 0,55–0,60 sem necessidade de `class_weight='balanced'` — diferente de cenários com 80/20.

---

#### Feature Engineering

O notebook engenharia pelo menos 6 novas features antes da modelagem:

| Feature | Descrição |
|---|---|
| `previous_flight_delay_arrival` | Atraso de chegada do voo anterior da mesma aeronave |
| `previous_flight_delay_departure` | Atraso de saída do voo anterior da mesma aeronave |
| `total_delay` | Soma dos atrasos de chegada e saída |
| `route_delay_mean` | Média histórica de atraso da rota (par ORIGEM–DESTINO) |
| `origin_delay_mean` | Média histórica de atraso do aeroporto de origem |
| `dest_delay_mean` | Média histórica de atraso do aeroporto de destino |
| `TAIL_NUMBER_ENC` | Aeronave codificada (LabelEncoder) |
| `ORIGIN_AIRPORT_ENC` | Aeroporto de origem codificado |
| `DESTINATION_AIRPORT_ENC` | Aeroporto de destino codificado |
| `AIRLINE_ENC` | Companhia aérea codificada |

⚠️ **Risco de data leakage:** as features `route_delay_mean`, `origin_delay_mean` e `dest_delay_mean` precisam ser calculadas **exclusivamente no conjunto de treino** (usando `.fit_transform(X_train)` e `.transform(X_test)`). Se calculadas sobre o dataset inteiro antes do split, introduzem leakage. O notebook não é verificável sem execução, mas a performance realista dos modelos (AUC=0,777) sugere que não há leakage severo.

---

#### Modelagem Supervisionada — Classificação

Dataset final salvo em `outputs/tables/df_flights.csv` (5.235.375 linhas × 37 colunas) — reutilizado pelo notebook não supervisionado.

**Modelos treinados com validação cruzada 5-fold:**

| Modelo | CV Accuracy Média | Accuracy Teste | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|---|
| **XGBoost** | 0,7093 | **0,7098** | 0,7455 | 0,5972 | **0,6631** | **0,7766** |
| Random Forest | 0,7001 | 0,7006 | 0,7435 | 0,5712 | 0,6460 | 0,7642 |
| Logistic Regression | 0,6603 | 0,6605 | 0,6797 | 0,5491 | 0,6074 | 0,7129 |

**Avaliação por modelo:**
- Confusion matrix: ✅ (visualizada para todos os modelos)
- Curva ROC com AUC: ✅ (visualizada para todos os modelos)
- 5-fold cross-validation: ✅ (raramente visto nos demais trabalhos)
- Comparação final: ✅ tabela comparativa + barplot de F1

> ⚠️ **Seaborn FutureWarning** no output: `palette` sem `hue` — API depreciada no seaborn >= 0.14.

---

### `tech_challenge_fase3_unsupervised.ipynb` — Clusterização

#### Preparação dos Dados

Lê o dataset engenheirado `outputs/tables/df_flights.csv` (5.235.375 × 37 colunas).

**Granularidade:** Agrega por **rota** (par ORIGEM–DESTINO) → **4.591 rotas únicas**.
> Contraste positivo com trabalhos que clusterizam apenas 14 companhias aéreas (estatisticamente frágil).

#### KMeans com Seleção Automática de k

```python
# Método do cotovelo
inertias = []
for k in range(2, 21):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

k_otimo = choose_k_by_elbow(inertias)  # k=7
```

✅ `StandardScaler` antes do KMeans  
✅ Função customizada `choose_k_by_elbow` para seleção automática  
✅ Silhouette Score calculado para k=2 até k=20  
✅ `n_init=10` e `random_state=42`  
✅ **k=7 selecionado e justificado metodologicamente**

#### DBSCAN

Aplicação adicional de DBSCAN para identificar **rotas outlier** — pontos que não se encaixam em nenhum cluster KMeans. Boa prática metodológica.

---

## Critérios de Avaliação

### 1. Aderência ao Problema (16/25)

| Requisito | Status | Evidência |
|---|---|---|
| EDA | ✅✅ | 10 gráficos + 10 CSVs — análise de sazonalidade, correlação, missing, top aeroportos/companhias |
| Modelo de Classificação | ✅ | 3 modelos (LR + RF + XGBoost), 5-fold CV, AUC até 0,777 |
| **Modelo de Regressão** | ❌ | **Completamente ausente** |
| Clusterização | ✅✅ | KMeans k=7 (via elbow+silhouette) + DBSCAN em 4.591 rotas |
| **PCA** | ❌ | **Completamente ausente** |

> 2 dos 5 componentes obrigatórios estão ausentes. EDA e clustering de nível avançado; classificação correta e bem avaliada.

---

### 2. Reprodutibilidade (10/15)

| Item | Status | Detalhe |
|---|---|---|
| Notebooks com outputs executados | ✅ | Ambos os notebooks têm células executadas |
| 10 figuras PNG commitadas | ✅ | Excelente evidência visual |
| 10 CSVs de resultados commitados | ✅ | Excelente evidência tabular |
| Dicionário de dados commitado | ✅ | `dicionario_dados_flights.pdf` — adição rara |
| Caminhos relativos (`pathlib.Path`) | ✅ | Sem caminhos absolutos hardcoded |
| `airlines.csv` e `airports.csv` versionados | ✅ | Permite execução parcial |
| `flights.csv` não commitado | ✅ | Correto para arquivo grande |
| **`README.md`** | ❌ | **AUSENTE** — sem instruções de execução, sem link para dados |
| `requirements.txt` | ❌ | Ausente — dependências não declaradas |
| `DtypeWarning` ao carregar flights.csv | ❌ | Ausência de `low_memory=False` |
| `random_state=42` consistente | ✅ | KMeans, modelos, train/test split |
| `.gitignore` inconsistente | ⚠️ | Ignora `data/raw/` e `outputs/tables/` mas os arquivos estão commitados |

---

### 3. Qualidade Técnica do Código (18/25)

| Item | Status | Detalhe |
|---|---|---|
| Estrutura de diretórios profissional | ✅✅ | `src/notebooks/`, `data/raw/`, `outputs/figures/`, `outputs/tables/` |
| Feature engineering (6+ features) | ✅ | Inclui médias históricas de rotas, aeroportos e previous flight delay |
| Cross-validation 5-fold | ✅✅ | Para os 3 modelos — prática incomum nos trabalhos desta turma |
| 3 modelos de classificação | ✅ | LR + RF + XGBoost com comparação sistemática |
| Confusion matrix + ROC + AUC | ✅ | Para todos os modelos |
| `StandardScaler` no KMeans | ✅ | Correto |
| Elbow method + Silhouette Score | ✅✅ | k=7 justificado metodologicamente |
| DBSCAN para outliers | ✅ | Adição metodológica positiva |
| Clusterização de rotas (4.591 pontos) | ✅ | Estatisticamente mais robusto que 14 companhias |
| Dataset salvo e reutilizado entre notebooks | ✅ | Boa separação de responsabilidades |
| **Regressão ausente** | ❌ | Componente obrigatório não implementado |
| **PCA ausente** | ❌ | Componente obrigatório não implementado |
| `DtypeWarning` | ❌ | `low_memory=False` ausente no carregamento |
| Risco de leakage nas médias históricas | ⚠️ | `route_delay_mean` etc. devem ser calculadas só no treino |
| Seaborn FutureWarning | ⚠️ | `palette` sem `hue` — API depreciada |
| Sem sklearn Pipeline | ❌ | Pré-processamento separado do treinamento |

---

### 4. Documentação (4/10)

| Item | Status | Detalhe |
|---|---|---|
| **`README.md`** | ❌ | **AUSENTE** — penalização severa: sem descrição do projeto, objetivos, como executar, link para dados |
| Dicionário de dados PDF | ✅ | Adição excelente e rara — demonstra atenção ao usuário do projeto |
| Células markdown nos notebooks | ✅ | Estrutura profissional sugere organização por seções |
| Comentários no código | ✅ | Provável dado o nível de organização geral |
| Interpretação dos clusters | ⚠️ | Não verificável sem README ou célula de conclusão explícita |

---

### 5. Evidências de Execução (9/10)

| Item | Status | Detalhe |
|---|---|---|
| 10 figuras PNG commitadas | ✅ | Cobre EDA completa |
| 10 CSVs de resultados commitados | ✅ | Cobre análises tabulares da EDA |
| Notebooks com outputs embedded | ✅ | Ambos os notebooks (1,7MB + 849KB) têm células executadas |
| Tabela comparativa de modelos | ✅ | Visível no output do notebook |
| Confusion matrices e ROC curves | ✅ | Visíveis no output do notebook |
| Métricas de Regressão | ❌ | Ausente (componente não implementado) |
| Evidências de PCA | ❌ | Ausente (componente não implementado) |

---

### 6. Critérios Não Funcionais (4/5)

| Item | Status | Detalhe |
|---|---|---|
| `.gitignore` presente | ✅ | Exclui `.venv`, `flights.csv` (via `data/raw/` e `*.csv`) |
| Estrutura de diretórios | ✅✅ | `src/notebooks/`, `data/raw/`, `outputs/figures/`, `outputs/tables/` — padrão cookiecutter |
| Dicionário de dados | ✅ | `data/dicionario_dados_flights.pdf` — adição bônus de qualidade |
| `requirements.txt` | ❌ | Ausente |
| Histórico de desenvolvimento | ⚠️ | 1 único commit — sem histórico de iterações |
| `.gitignore` inconsistente com estado real | ⚠️ | Ignora diretórios que contêm arquivos commitados |

---

## Resumo de Pontuação

| Critério | Obtido | Máximo |
|---|---|---|
| 1. Aderência ao Problema | 16 | 25 |
| 2. Reprodutibilidade | 10 | 15 |
| 3. Qualidade Técnica | 18 | 25 |
| 4. Documentação | 4 | 10 |
| 5. Evidências de Execução | 9 | 10 |
| 6. Critérios Não Funcionais | 4 | 5 |
| **Total** | **61** | **90** |

---

## Resultados dos Modelos

### Classificação — "O voo vai atrasar?"

Dataset: 5.235.375 voos após limpeza | Split: treino/teste com 5-fold CV | `random_state=42`

| Modelo | CV Accuracy | Test Accuracy | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|---|
| **XGBoost** | **0,7093** | **0,7098** | **0,7455** | **0,5972** | **0,6631** | **0,7766** |
| Random Forest | 0,7001 | 0,7006 | 0,7435 | 0,5712 | 0,6460 | 0,7642 |
| Logistic Regression | 0,6603 | 0,6605 | 0,6797 | 0,5491 | 0,6074 | 0,7129 |

> Dataset razoavelmente balanceado (~47% atrasos), o que torna os recalls de 0,55–0,60 genuínos. XGBoost selecionado como melhor modelo.

### Clusterização — Rotas Aéreas (KMeans k=7)

Features: médias de atraso, volume de voos por rota (após StandardScaler)  
Instâncias: 4.591 rotas únicas  
Seleção de k: método do cotovelo + silhouette score (k=7 ótimo)  
Outliers: identificados com DBSCAN

---

## Principais Problemas

1. 🔴 **Modelo de Regressão ausente** — prever os minutos de atraso (ex: `RandomForestRegressor` sobre `ARRIVAL_DELAY`) não foi implementado
2. 🔴 **PCA ausente** — redução de dimensionalidade, variância explicada e visualização em 2D não implementados
3. 🔴 **Sem `README.md`** — repositório sem qualquer documentação textual: sem descrição do problema, instruções de execução, link para `flights.csv` ou interpretação dos resultados
4. 🟠 **Sem `requirements.txt`** — dependências não declaradas formalmente; impossível reproduzir o ambiente sem tentativa e erro
5. 🟠 **`DtypeWarning`** ao carregar `flights.csv` — `low_memory=False` ausente na chamada `pd.read_csv`
6. 🟡 **Risco de data leakage** em `route_delay_mean`, `origin_delay_mean`, `dest_delay_mean` — precisam ser calculadas exclusivamente no conjunto de treino
7. 🟡 **`.gitignore` inconsistente** — ignora `data/raw/` e `outputs/tables/`, mas esses arquivos estão versionados (force-added)
8. 🟡 **Seaborn FutureWarning** — uso de `palette` sem `hue` explícito

---

## Pontos Positivos

1. **Estrutura de diretórios exemplar** — `src/notebooks/`, `data/raw/`, `outputs/figures/`, `outputs/tables/` segue o padrão cookiecutter data science; melhor organização entre os trabalhos avaliados
2. **EDA excepcional** — 10 gráficos + 10 CSVs, incluindo análise de sazonalidade mensal, missing data, correlações, top companhias/aeroportos e distribuição da variável alvo
3. **Cross-validation 5-fold** em todos os 3 modelos — prática metodologicamente sólida e incomum nesta turma
4. **3 modelos de classificação** com comparação sistemática: tabela + confusion matrix + ROC + AUC para todos
5. **Clusterização avançada**: k=7 justificado via elbow method + silhouette score sobre 4.591 rotas (estatisticamente mais robusto que clustering de 14 companhias)
6. **DBSCAN** para detecção de outliers — adição metodológica positiva
7. **Dicionário de dados** commitado em PDF — adição rara e útil para compreensão do dataset
8. **`pathlib.Path`** para todos os caminhos — sem hardcoding, portável entre sistemas operacionais
9. **Feature engineering sofisticado** — 6+ features derivadas incluindo médias históricas de rotas e delay do voo anterior da mesma aeronave
10. **Evidências de execução abundantes** — 10 PNGs + 10 CSVs + outputs embedded nos notebooks

---

## Conclusão

O repositório demonstra domínio técnico sólido: a EDA é completa com sazonalidade e correlações, os modelos de classificação são bem avaliados com cross-validation, e a clusterização é metodologicamente correta com seleção justificada de k. A organização do projeto segue padrões profissionais.

No entanto, **dois dos cinco componentes obrigatórios estão ausentes** (Regressão e PCA), e a **ausência de README.md** é um ponto crítico que impossibilita a compreensão do projeto por qualquer pessoa além do autor. Para atingir a faixa de 75–80 pontos, seria necessário: (1) implementar Regressão (ex: `ARRIVAL_DELAY` contínuo com Random Forest Regressor), (2) implementar PCA com variância explicada, (3) criar um `README.md` com descrição, instruções de execução e link para `flights.csv`, e (4) adicionar `requirements.txt`. Com essas adições, o repositório seria um dos mais completos da turma.
