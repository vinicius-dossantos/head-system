# Avaliação — guipignatari/Tech-Challenge-ML-3

**Repositório:** https://github.com/guipignatari/Tech-Challenge-ML-3  
**Avaliado em:** 31/03/2026  
**Curso:** Pós-Graduação em Machine Learning Engineering — FIAP  
**Tema:** Análise e previsão de atrasos de voos nos EUA — EDA, Classificação, Clusterização, Bônus Geográfico  
**Equipe:** 1 colaborador (guipignatari) | 1 commit

---

## Nota Final: **55 / 90**

---

## Resumo Executivo

Trabalho sólido e bem estruturado para um único contribuidor. O pipeline está todo contido em um notebook (`pipeline.ipynb`) com **28 células executadas**, todas com outputs preservados e 6 imagens PNG embeds. A limpeza de dados é correta e bem comentada, a análise exploratória tem profundidade adequada (5 charts + heatmap de correlação), e a clusterização usa `StandardScaler` com comentário explícito justificando a padronização — ponto técnico importante. Há também um mapa geográfico de aeroportos como bônus. **Os dois principais pontos de penalização são:** (1) ausência completa de **Modelo de Regressão** e **PCA** (2 dos 5 componentes obrigatórios); e (2) os modelos de classificação **não tratam o desbalanceamento**, resultando em Recall ≈ 0% para a classe de interesse (atrasos), tornando-os inutilizáveis na prática.

---

## Inventário do Repositório

| Arquivo | Tamanho | Descrição |
|---|---|---|
| `pipeline.ipynb` | 458 KB | Notebook principal — único artefato de código |
| `readme.md` | 2,4 KB | Documentação do projeto |
| `.gitignore` | 5 B | Exclui apenas `*.csv` |
| `.DS_Store` | 6,1 KB | ❌ Arquivo macOS commitado por engano |

**Datasets:** Corretamente não versionados (excluídos pelo `.gitignore`); link Google Drive no README ✅

---

## Estrutura do Notebook (28 células)

| Seção | Células | Status |
|---|---|---|
| EDA | 1–8 (markdown + 7 code) | ✅ Executado, com outputs |
| Modelagem Supervisionada | 9–16 (markdown + 7 code) | ⚠️ Executado, mas recall≈0% |
| Modelagem Não Supervisionada | 17–24 (markdown + 7 code) | ✅ Executado, com outputs |
| Bônus — Análise Geográfica | 25–28 (markdown + 3 code) | ✅ Executado, mapa PNG |
| **Regressão** | — | ❌ **AUSENTE** |
| **PCA** | — | ❌ **AUSENTE** |

---

## Análise por Seção

### EDA (Células 1–8)

**Carregamento:**
```python
df_flights = pd.read_csv('flights.csv')
```
⚠️ `DtypeWarning` — colunas 7, 8 com tipos mistos; faltou `low_memory=False` ou `dtype` explícito.

**Limpeza — exemplar:**
```python
df_voos = df_flights[(df_flights['CANCELLED'] == 0) & (df_flights['DIVERTED'] == 0)].copy()
df_voos[colunas_motivos] = df_voos[colunas_motivos].fillna(0)
df_voos.dropna(subset=['ARRIVAL_DELAY', 'DEPARTURE_DELAY'], inplace=True)
```
- `.copy()` antes das atribuições ✅
- `fillna(0)` correto para colunas de **motivos de atraso** (NULL = "não houve esse tipo de atraso") ✅
- `dropna(subset=['ARRIVAL_DELAY'])` ao invés de `fillna(0)` nos delays reais ✅ (prática mais correta)

**Variável alvo:**
```python
df_voos['ATRASO_15MIN'] = df_voos['ARRIVAL_DELAY'].apply(lambda x: 1 if x > 15 else 0)
```
Threshold correto de 15 minutos (padrão da indústria) ✅

**Visualizações geradas (5 gráficos):**
1. Countplot — proporção voos atrasados × no horário ✅
2. Barplot — atraso médio por companhia aérea (ordenado) ✅
3. Heatmap de correlação (`DEPARTURE_DELAY`, `TAXI_OUT`, `DISTANCE`, `ARRIVAL_DELAY`) ✅

**Análises ausentes na EDA:**
- Sem análise de sazonalidade (atraso por mês)
- Sem análise por dia da semana
- Sem distribuição de `ARRIVAL_DELAY` (histograma/boxplot)
- Sem análise por aeroporto de origem

---

### Modelagem Supervisionada — Classificação (Células 9–16)

**Features usadas (pré-voo — sem data leakage):**
```python
features = ['MONTH', 'DAY_OF_WEEK', 'SCHEDULED_DEPARTURE', 'DISTANCE', 'AIRLINE']
```
✅ Correto — todas as variáveis são conhecidas antes do voo.

**Pré-processamento:**
```python
le = LabelEncoder()
X['AIRLINE'] = le.fit_transform(X['AIRLINE'])
```
⚠️ LabelEncoder atribui valores ordinais (0, 1, 2...) às companhias, o que pode introduzir relação ordinal falsa.

**Divisão:** 70% treino / 30% teste, `random_state=42` ✅

**Resultados:**

| Modelo | Accuracy | Precision (cl.1) | Recall (cl.1) | F1 (cl.1) |
|---|---|---|---|---|
| Regressão Logística | 82% | 0.00 | **0.00** | 0.00 |
| Árvore de Decisão (`max_depth=10`) | 82% | 0.48 | **0.01** | 0.01 |

> **Problema crítico:** Sem `class_weight='balanced'` (ou outra técnica de balanceamento), ambos os modelos ignoram quase completamente a classe positiva (atrasos). O Recall de 0% na Regressão Logística e 1% na Árvore significa que o modelo **não detecta atrasos** na prática. A accuracy de 82% é ilusória — corresponde à proporção de voos não atrasados na base.

**`max_depth=10`** na Árvore de Decisão ✅ — boa prática para evitar overfitting.

---

### Modelagem Não Supervisionada — KMeans (Células 17–24)

**Preparação dos dados:**
```python
df_cia_metricas = df_voos.groupby('AIRLINE')[['ARRIVAL_DELAY', 'DEPARTURE_DELAY', 'DISTANCE']].mean().reset_index()
```
Resultado: 14 companhias aéreas como registros para o clustering.

**Padronização — ponto positivo com comentário explícito:**
```python
# Como Distância (milhas) e Atraso (minutos) têm escalas muito diferentes, 
# precisamos padronizar os dados para que o algoritmo não dê peso extra para a distância.
scaler = StandardScaler()
X_cluster = scaler.fit_transform(df_cia_metricas[['ARRIVAL_DELAY', 'DISTANCE']])
```
`StandardScaler` ✅ + `n_init=10` ✅ + `random_state=42` ✅

**k=3 fixo sem justificativa metodológica** ❌ — não usa elbow method nem Silhouette Score.

**Resultado dos clusters (14 companhias):**

| Cluster | Companhias | Perfil |
|---|---|---|
| 0 | American, Alaska, JetBlue, Delta, United, US Airways, Virgin America | Longas distâncias, atraso moderado (−1 a 7 min) |
| 1 | Atlantic Southeast, Hawaiian, American Eagle, SkyWest, Southwest | Rotas curtas/médias, atraso moderado (2–7 min) |
| 2 | Frontier, Spirit | Maior atraso médio (12–14 min) |

> ⚠️ Nota: clustering sobre apenas 14 pontos é estatisticamente questionável. K-Means com k=3 sobre 14 registros tem elevada sensibilidade a variações mínimas nos dados.

---

### Bônus — Análise Geográfica (Células 25–28)

Mapa de scatter usando coordenadas `LATITUDE`/`LONGITUDE` com:
- Tamanho do ponto proporcional ao volume de voos (`TOTAL_VOOS`)
- Cor representando `MEDIA_ATRASO` (paleta `YlOrRd`)
- Limites geográficos corretos para os EUA continentais (-130 a -65, 24 a 50)
- Legenda detalhada

✅ Boa visualização geográfica — identifica aeroportos-gargalo visualmente.

---

## Critérios de Avaliação

### 1. Aderência ao Problema (13/25)

| Requisito | Status | Evidência |
|---|---|---|
| EDA | ✅ | 5 gráficos, heatmap de correlação, limpeza correta, variável alvo |
| Modelo de Classificação | ⚠️ | 2 modelos (LR + DT), executados, mas recall≈0% sem balanceamento |
| **Modelo de Regressão** | ❌ | **Completamente ausente** |
| Clusterização | ✅ | KMeans k=3 com StandardScaler, 3 grupos de companhias |
| **PCA** | ❌ | **Completamente ausente** |
| Bônus Geográfico | ✅ | Mapa de atrasos por aeroporto com lat/lon |

---

### 2. Reprodutibilidade (10/15)

| Item | Status | Detalhe |
|---|---|---|
| `random_state=42` consistente | ✅ | LR, DT, KMeans, train_test_split |
| Notebook com outputs executados | ✅ | Todas as 28 células executadas |
| Imagens PNG preservadas | ✅ | 6 imagens embed no `.ipynb` |
| Caminhos relativos | ✅ | Lê `'flights.csv'` da pasta atual |
| Link para dados (Google Drive) | ✅ | Pasta com 3 CSVs |
| `requirements.txt` | ❌ | Ausente — `pip install pandas seaborn scikit-learn` não documentado formalmente |
| `low_memory=False` ou `dtype` | ❌ | `DtypeWarning` ao carregar `flights.csv` |

---

### 3. Qualidade Técnica do Código (16/25)

| Item | Status | Detalhe |
|---|---|---|
| Sem data leakage | ✅ | Features são exclusivamente pré-voo |
| `StandardScaler` no KMeans | ✅ | Com comentário explicando a necessidade |
| `n_init=10` no KMeans | ✅ | Evita ótimo local |
| `max_depth=10` no DT | ✅ | Limita overfitting |
| `.copy()` antes de modificar subsets | ✅ | `df_voos = df_flights[...].copy()` |
| `dropna` em delays reais | ✅ | Correto — não substitui NaN por 0 nos atrasos |
| `fillna(0)` em colunas de motivo | ✅ | Semanticamente correto |
| **Sem `class_weight='balanced'`** | ❌ | Recall ≈ 0% — modelos não detectam atrasos |
| **k=3 fixo sem justificativa** | ❌ | Sem elbow method ou Silhouette Score |
| LabelEncoder para AIRLINE | ⚠️ | Ordinalidade artificial |
| Sem cross-validation | ❌ | Única divisão train/test |
| Seaborn FutureWarnings | ⚠️ | `palette` sem `hue` — API depreciada |
| `DtypeWarning` | ⚠️ | `low_memory=False` ausente |

---

### 4. Documentação (7/10)

| Item | Status | Detalhe |
|---|---|---|
| README claro e estruturado | ✅ | Objetivos, tecnologias, conclusões, como executar |
| README menciona desbalanceamento | ✅ | Documentado como "principal desafio" |
| README menciona próximos passos | ✅ | SMOTE, APIs meteorológicas |
| Células markdown no notebook | ✅ | 4 headers de seção (EDA, Supervisionada, Não Supervisionada, Bônus) |
| Comentários inline no código | ✅ | Cada bloco de código tem comentário explicativo |
| Limitações documentadas no notebook | ⚠️ | Apenas no README; notebook não discute falha dos modelos |
| Interpretação dos clusters | ⚠️ | Scatter plot gerado mas clusters não têm nomes/interpretação semântica no notebook |

---

### 5. Evidências de Execução (8/10)

| Item | Status | Detalhe |
|---|---|---|
| Notebook executado | ✅ | Todos os cells têm output |
| Imagens PNG embedded | ✅ | 6 gráficos preservados |
| `describe()` com estatísticas | ✅ | Cell 5: shape + describe completo |
| `classification_report` | ✅ | Cells 14–15: precision/recall/F1 para ambos modelos |
| Tabela de clusters | ✅ | Cell 24: 14 companhias com cluster atribuído |
| Mapa geográfico | ✅ | Cell 28: scatter lat/lon executado |
| Métricas de Regressão | ❌ | Ausente (componente não implementado) |
| Evidências de PCA | ❌ | Ausente |

---

### 6. Critérios Não Funcionais (1/5)

| Item | Status | Detalhe |
|---|---|---|
| `.gitignore` presente | ✅ | Exclui `*.csv` |
| `.gitignore` completo | ❌ | Não exclui `.DS_Store`, `__pycache__/`, `.ipynb_checkpoints/` |
| `.DS_Store` commitado | ❌ | Arquivo macOS de 6KB no repositório |
| `requirements.txt` | ❌ | Ausente |
| Estrutura organizada | ✅ | Notebook único bem estruturado |

---

## Resumo de Pontuação

| Critério | Obtido | Máximo |
|---|---|---|
| 1. Aderência ao Problema | 13 | 25 |
| 2. Reprodutibilidade | 10 | 15 |
| 3. Qualidade Técnica | 16 | 25 |
| 4. Documentação | 7 | 10 |
| 5. Evidências de Execução | 8 | 10 |
| 6. Critérios Não Funcionais | 1 | 5 |
| **Total** | **55** | **90** |

---

## Resultados dos Modelos

### Classificação — "O voo vai atrasar?" (threshold: ARRIVAL_DELAY > 15 min)

Dataset: 5.714.008 voos | Divisão: 70% treino / 30% teste | `random_state=42`

| Modelo | Accuracy | Precision (cl.1) | Recall (cl.1) | F1 (cl.1) |
|---|---|---|---|---|
| Regressão Logística | 82% | 0.00 | **0.00** | 0.00 |
| Árvore de Decisão (max_depth=10) | 82% | 0.48 | **0.01** | 0.01 |

> Ambos os modelos predizem quase sempre classe 0 (no horário). Com 82% dos voos no horário, prever sempre "no horário" já entrega 82% de accuracy. Recall de 0–1% significa que o modelo **detecta menos de 1% dos atrasos reais**.

### Clusterização — Companhias Aéreas (KMeans k=3)

Features: `ARRIVAL_DELAY`, `DISTANCE` (após StandardScaler)

| Cluster | Companhias | Atraso Médio | Distância Média |
|---|---|---|---|
| 0 | American, Alaska, JetBlue, Delta, United, US Airways, Virgin America | −1 a 7 min | 854–1.404 mi |
| 1 | Atlantic Southeast, Hawaiian, American Eagle, SkyWest, Southwest | 2–7 min | 422–742 mi |
| 2 | Frontier, Spirit | 12–15 min | 967–986 mi |

---

## Pontos Positivos

1. **Ausência de data leakage** — features exclusivamente pré-voo, ponto mais crítico de ML bem tratado
2. **`StandardScaler` no KMeans com justificativa comentada** — demonstra compreensão do porquê
3. **Limpeza de dados correta** — filtra cancelados e desviados, `dropna` em delays reais, `fillna(0)` correto nos motivos
4. **Notebook inteiramente executado** — todos os outputs e imagens preservados
5. **Mapa geográfico de aeroportos** — visualização bônus de qualidade
6. **README honesto** — documenta limitações do desbalanceamento e propõe melhorias futuras
7. **`random_state=42` consistente** em todos os estimadores

## Oportunidades de Melhoria

1. 🔴 **Implementar Regressão** — prever os minutos de atraso (LinearRegression ou RandomForestRegressor sobre voos atrasados)
2. 🔴 **Implementar PCA** — redução de dimensionalidade, visualização em 2D, variância explicada
3. 🔴 **`class_weight='balanced'`** nos modelos de classificação — sem isso os modelos não detectam atrasos (recall≈0%)
4. 🟠 **Elbow method / Silhouette Score** para justificar k=3 no KMeans
5. 🟠 **`requirements.txt`** — declarar dependências com versões fixas
6. 🟠 **Adicionar `.DS_Store` ao `.gitignore`** — e remover o arquivo já commitado
7. 🟡 **Cross-validation** — uma única divisão train/test é menos robusta que k-fold
8. 🟡 **EDA mais profunda** — adicionar análise por mês, dia da semana, distribuição de atrasos
9. 🟡 **Corrigir Seaborn FutureWarnings** — usar `hue` explicitamente
10. 🟡 **`low_memory=False`** ao ler `flights.csv` para evitar `DtypeWarning`

---

## Conclusão

Trabalho bem estruturado e executado, com boas práticas de limpeza de dados e ausência de data leakage. O ponto técnico mais positivo é o uso correto de `StandardScaler` no KMeans com comentário explicativo. No entanto, a ausência de dois componentes obrigatórios (Regressão e PCA) limita significativamente a nota. O problema mais crítico de ML é a não tratamento do desbalanceamento de classes, que faz os modelos de classificação serem inutilizáveis para detectar atrasos. Com a adição de `class_weight='balanced'`, Regressão e PCA, a nota subiria para a faixa de 76–80 pontos.
