# Avaliação — gabrieljesus-pixel/Tech3

**Repositório:** https://github.com/gabrieljesus-pixel/Tech3  
**Avaliado em:** 31/03/2026  
**Curso:** Pós-Graduação em Machine Learning Engineering — FIAP  
**Tema:** Análise de atrasos de voos nos EUA — EDA, Classificação, Clusterização  
**Equipe:** 1 colaborador (gabrieljesus-pixel)

---

## Nota Final: **26 / 90**

---

## Resumo Executivo

O repositório entrega 4 scripts Python de EDA e clusterização, mas **o componente central do trabalho — o arquivo `modelagem_supervisionada.py` — está completamente ausente do repositório**, apesar de ser mencionado nominalmente no README. Com isso, os modelos de Classificação, Regressão e PCA simplesmente não existem. A EDA é superficial (cada script isolado, sem análise de distribuição de atrasos, sem correlações, sem sazonalidade mensal). A clusterização é simples mas funcional. O ponto crítico de reprodutibilidade é o **caminho absoluto hardcoded** no `analise_aeroporto.py`, que impossibilita a execução em qualquer máquina que não seja o computador original do autor. Nenhuma evidência de execução foi commitada.

---

## Inventário do Repositório

| Arquivo | Tamanho | Descrição |
|---|---|---|
| `README.md` | 1,1 KB | Documentação do projeto |
| `analise_aeroporto.py` | 2,9 KB | EDA de aeroportos |
| `analise_airlines.py` | 2,9 KB | EDA de companhias aéreas |
| `analise_flights.py` | 2,8 KB | EDA de voos (simplificada) |
| `clusterizacao_aeroportos.py` | 2,1 KB | KMeans — clusterização de aeroportos |
| `airports.csv` | 23,9 KB | Dataset de aeroportos (versionado ✅) |
| `airlines.csv` | 359 B | Dataset de companhias (versionado ✅) |
| **`modelagem_supervisionada.py`** | — | ❌ **NÃO EXISTE** (mencionado no README) |

**Commits:** 4 | **Branches:** 1 (`main`) | **Issues/PRs:** 0

> **`flights.csv`:** Corretamente não versionado (excede o limite do GitHub); link para Google Drive fornecido no README.

---

## Análise do Código

### `analise_aeroporto.py` — EDA de Aeroportos

**Bug crítico de reprodutibilidade:**
```python
def analisar_aeroportos(caminho_arquivo):
    # O parâmetro 'caminho_arquivo' é recebido mas NUNCA usado
    df = pd.read_csv('C:\\Users\\DELL CORE i7\\Desktop\\Machine Learning\\Tech3\\airports.csv')
```
O parâmetro `caminho_arquivo` é ignorado; o arquivo é lido de um **caminho absoluto Windows hardcoded**. Este script é executável apenas na máquina original do autor.

**Visualizações produzidas:**
- Distribuição de aeroportos por estado (barplot) ✅
- Mapa geográfico por lat/lon (scatterplot) ✅ com anotação do Alasca
- Distribuição do comprimento dos nomes dos aeroportos (histplot) ✅

**`plt.show()` em todos os gráficos** — não funciona em execução headless/servidor.

---

### `analise_airlines.py` — EDA de Companhias Aéreas

Estrutura funcional: parâmetro de caminho usado corretamente.

**Análises:**
- Comprimento dos nomes das companhias (`nome_comprimento`) ✅
- Quantidade de palavras por nome (`qtd_palavras`) ✅
- Top 10 termos mais frequentes (via `Counter + re.findall`) ✅
- Tratamento de valores ausentes com `dropna()` ✅

**Problema:** A análise de comprimento de nomes de companhias aéreas é uma métrica de utilidade questionável para o objetivo do Tech Challenge (análise de atrasos). Faltam análises relevantes como proporção de atrasos por companhia.

---

### `analise_flights.py` — EDA Principal de Voos

**Carregamento com `usecols`** — seletivo e eficiente para CSV grande ✅

**Tratamento de dados:**
- Filtra voos cancelados: `df[df['CANCELLED'] == 0]` ✅
- `fillna(0)` em `DEPARTURE_DELAY` e `ARRIVAL_DELAY` ⚠️ — preencher NaN com 0 pode introduzir viés; para voos não cancelados com ARRIVAL_DELAY nulo, seria mais correto fazer `dropna()`

**Visualizações:**
- Atraso médio por hora do dia (lineplot) ✅
- Atraso médio por dia da semana (barplot) ✅

**Ausências graves:**
- Sem histograma de distribuição de `ARRIVAL_DELAY`
- Sem análise de top companhias por atraso
- Sem análise de top aeroportos por atraso
- Sem correlação entre features numéricas
- Sem análise de sazonalidade mensal
- A segunda análise agrega por `ORIGIN_AIRPORT` mas o gráfico do resultado (`atraso_aeroporto`) nunca é plotado

---

### `clusterizacao_aeroportos.py` — KMeans

**Pré-processamento:**
- Agrupa por aeroporto: `atraso_medio` e `total_voos` ✅
- Filtra aeroportos com < 1.000 voos (limpeza razoável) ✅
- **Sem `StandardScaler`** ❌ — `total_voos` (ordem de milhares) e `atraso_medio` (minutos, ~5–30) têm escalas completamente distintas; o KMeans será dominado por `total_voos`, tornando o clustering enviesado

**KMeans:**
- `n_clusters=3`, `random_state=42`, `n_init=10` ✅
- k=3 fixo sem justificativa (sem elbow method, sem silhouette score) ❌

**Visualização:**
- Scatter `total_voos × atraso_medio` colorido por cluster ✅
- Anotações dos 20 primeiros aeroportos com `plt.annotate` ✅

---

## Critérios de Avaliação

### 1. Aderência ao Problema (6/25)

| Requisito | Status | Evidência |
|---|---|---|
| EDA | ⚠️ | Presente mas incompleta — 3 scripts de EDA sem análise de distribuição de atrasos, correlações ou sazonalidade |
| **Modelo de Classificação** | ❌ | **`modelagem_supervisionada.py` AUSENTE** do repositório |
| **Modelo de Regressão** | ❌ | **Completamente ausente** |
| Clusterização | ✅ | `clusterizacao_aeroportos.py` — KMeans k=3 (sem seleção automática) |
| **PCA** | ❌ | **Completamente ausente** |

> 3 dos 5 componentes obrigatórios estão ausentes. A EDA recebe crédito parcial por estar presente mas incompleta.

---

### 2. Reprodutibilidade (3/15)

| Item | Status | Detalhe |
|---|---|---|
| `random_state=42` no KMeans | ✅ | Presente |
| Caminho relativo nos scripts | ❌ | `analise_aeroporto.py` tem caminho Windows absoluto hardcoded |
| `requirements.txt` | ❌ | Ausente — apenas mencionado `pip install pandas scikit-learn seaborn` no README |
| Modelos salvos | ❌ | Nenhum `.pkl` / serialização |
| Outputs versionados | ❌ | Nenhuma imagem ou CSV de resultado |
| `plt.show()` headless | ❌ | Todos os scripts usam `plt.show()` — não funciona sem display |
| Link para dados | ✅ | Google Drive mencionado no README |

---

### 3. Qualidade Técnica do Código (7/25)

| Item | Status | Detalhe |
|---|---|---|
| `usecols` no `read_csv` (flights) | ✅ | Eficiente para arquivo grande |
| `n_init=10` no KMeans | ✅ | Evita ótimo local |
| Filtragem de cancelados | ✅ | `df[df['CANCELLED'] == 0]` |
| **Caminho hardcoded absoluto** | ❌ | `analise_aeroporto.py` inutilizável em outra máquina |
| **Sem `StandardScaler` no KMeans** | ❌ | Escalas incompatíveis comprometem o clustering |
| **`fillna(0)` em delays** | ⚠️ | Para voos não cancelados, NaN em ARRIVAL_DELAY deveria ser `dropna()` |
| Sem sklearn Pipeline | ❌ | Nenhum uso de pipelines |
| Sem validação cruzada | ❌ | (não aplicável por falta de modelo) |
| Sem métricas de avaliação | ❌ | Nenhum classification_report, confusion matrix, etc. |
| Sem seleção de k no KMeans | ❌ | k=3 fixo sem elbow method ou silhouette |
| Análise de `analise_flights.py` incompleta | ⚠️ | `atraso_aeroporto` calculado mas nunca plotado |

---

### 4. Documentação (3/10)

| Item | Status | Detalhe |
|---|---|---|
| README presente | ✅ | Descreve o projeto com estrutura e instruções básicas |
| README consistente | ❌ | Cita `modelagem_supervisionada.py` que não existe no repositório |
| Docstrings | ❌ | Nenhuma função tem docstring |
| Comentários no código | ⚠️ | Comentários mínimos (`# 1. Carregando`, `# 2. K-Means`) |
| Markdown cells (notebook) | — | Scripts .py, não notebooks — não aplicável |
| Resultados documentados | ⚠️ | README menciona "RF obteve Recall de 65%" mas o código correspondente não existe |

---

### 5. Evidências de Execução (0/10)

| Item | Status |
|---|---|
| Imagens de gráficos commitadas | ❌ |
| CSVs de resultados | ❌ |
| Outputs de terminal / logs | ❌ |
| Métricas dos modelos | ❌ |
| Notebook com outputs executados | ❌ |

---

### 6. Critérios Não Funcionais (7/5 → 7/5 cap)

| Item | Status | Detalhe |
|---|---|---|
| `requirements.txt` | ❌ | Ausente |
| `.gitignore` | ❌ | Ausente (porém `flights.csv` não foi commitado, o que é correto) |
| `airports.csv` e `airlines.csv` versionados | ✅ | Permite execução parcial sem configuração extra |
| Link externo para `flights.csv` | ✅ | Google Drive — boa prática para arquivo grande |
| Estrutura plana (sem subdiretórios) | ⚠️ | Todos os arquivos na raiz; sem `src/`, `data/`, `outputs/` |

> Pontuação cap a 5 (máximo do critério).

---

## Resumo de Pontuação

| Critério | Obtido | Máximo |
|---|---|---|
| 1. Aderência ao Problema | 6 | 25 |
| 2. Reprodutibilidade | 3 | 15 |
| 3. Qualidade Técnica | 7 | 25 |
| 4. Documentação | 3 | 10 |
| 5. Evidências de Execução | 0 | 10 |
| 6. Critérios Não Funcionais | 7 | 5 |
| **Total** | **26** | **90** |

---

## Principais Problemas

1. 🔴 **`modelagem_supervisionada.py` ausente** — o arquivo de classificação (Random Forest vs. Logistic Regression) mencionado no README não existe no repositório. Este é o componente central do Tech Challenge
2. 🔴 **Regressão e PCA ausentes** — outros 2 dos 5 requisitos obrigatórios não implementados
3. 🔴 **Caminho hardcoded** em `analise_aeroporto.py` — `C:\Users\DELL CORE i7\Desktop\...` — impossibilita execução em qualquer outro ambiente
4. 🟠 **Sem `StandardScaler` no KMeans** — `total_voos` e `atraso_medio` têm escalas incompatíveis; o clustering está matematicamente incorreto
5. 🟠 **Sem evidências de execução** — nenhuma imagem, CSV ou output versionado
6. 🟡 **EDA incompleta** — falta análise de distribuição de `ARRIVAL_DELAY`, top companhias/aeroportos por atraso, correlações, sazonalidade mensal
7. 🟡 **Sem `requirements.txt`** — dependências não declaradas formalmente
8. 🟡 **k=3 fixo** no KMeans sem justificativa metodológica (sem elbow ou silhouette)

## Pontos Positivos

1. **`usecols`** em `analise_flights.py` — leitura seletiva do `flights.csv` é correta para arquivo grande
2. **Filtragem de cancelados** antes de calcular estatísticas de atraso
3. **Anotações no scatter plot** do KMeans — identifica aeroportos por IATA_CODE
4. **Link para dados** no README — resolve o problema do `flights.csv` grande de forma adequada
5. **`n_init=10`** no KMeans — evita convergência para ótimo local

---

## Conclusão

O repositório está incompleto de forma significativa: **3 dos 5 componentes obrigatórios estão ausentes** (Classificação, Regressão, PCA), e o arquivo principal (`modelagem_supervisionada.py`) não foi commitado apesar de constar no README. A EDA existente é básica e com um erro crítico de reprodutibilidade (caminho hardcoded). Para atingir a faixa de 60-70 pontos, seria necessário: (1) commitar `modelagem_supervisionada.py`, (2) adicionar Regressão e PCA, (3) corrigir o caminho hardcoded, (4) adicionar `StandardScaler` ao KMeans e justificar k com elbow/silhouette, e (5) commitar evidências de execução.
