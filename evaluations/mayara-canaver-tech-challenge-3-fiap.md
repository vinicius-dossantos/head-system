# Avaliação — mayara-canaver/tech-challenge-3-fiap

**Repositório:** https://github.com/mayara-canaver/tech-challenge-3-fiap  
**Avaliado em:** 31/03/2026  
**Curso:** Pós-Graduação em Machine Learning Engineering — FIAP  
**Tema:** Análise de atrasos de voos nos EUA — Classificação, Clusterização e Dashboard  
**Equipe:** 2 colaboradores (mayara-canaver + eduardohenrik)

---

## Nota Final: **62 / 90**

---

## Resumo Executivo

Trabalho de equipe com boa qualidade técnica no que foi entregue, mas com **dois requisitos obrigatórios ausentes: Regressão e PCA**. O ponto mais positivo é a entrega de um **dashboard Streamlit interativo** (`app.py`) — artefato além do escopo básico — que demonstra domínio técnico e preocupação com usabilidade. A EDA é detalhada com boas análises e insights. Os modelos de classificação (Random Forest + XGBoost) apresentam recall de 63% na classe positiva com tratamento correto de desbalanceamento. A clusterização K-Means usa elbow method com justificativa para k=5. O módulo `helpers.py` mostra boa separação de responsabilidades, reutilizado em notebooks e app. Os principais pontos a melhorar são: implementar regressão e PCA (requisitos faltantes), usar mais features no modelo (apenas 3 das 7 preparadas foram incluídas em X), e corrigir avisos (SettingWithCopyWarning, FutureWarnings).

---

## Critérios de Avaliação

### 1. Aderência ao Problema (15/25)

| Requisito | Status | Evidência |
|---|---|---|
| EDA | ✅ | `eda_geral.ipynb` + seção EDA em `analise_atraso.ipynb`: sazonalidade, dia da semana, horário, companhias, distância, risco por aeroporto |
| Modelo de Classificação | ✅ | `analise_atraso.ipynb`: Random Forest (recall=0.63) + XGBoost (recall=0.63); class_weight='balanced' / scale_pos_weight |
| Modelo de Regressão | ❌ | **Ausente** — nenhum notebook ou seção de regressão encontrada |
| Clusterização | ✅ | `k_means_atraso_voo.ipynb`: K-Means com elbow method, k=5 escolhido com justificativa |
| PCA | ❌ | **Ausente** — redução de dimensionalidade não implementada |
| **Bônus** Streamlit Dashboard | ✅ | `app.py`: 3 abas (Tendências, Companhias, K-Means), filtros na sidebar, Plotly, caching, KMeans ao vivo |

> **Nota:** A ausência de Regressão e PCA representa 2 dos 5 componentes obrigatórios do Tech Challenge 3. O Dashboard Streamlit é um extra significativo mas não substitui os requisitos faltantes.

---

### 2. Reprodutibilidade (11/15)

| Item | Status | Detalhe |
|---|---|---|
| `random_state=7` consistente | ✅ | Usado em todos os modelos RF, XGBoost, KMeans e no app |
| Notebooks com outputs | ✅ | Células executadas; algumas saídas são "Figure size X with Y Axes" (imagens não renderizadas no IPynb) |
| Modelos salvos como `.pkl` | ✅ | `modelo_random_forest.pkl` (19 MB) e `modelo_xgb.pkl` (734 KB) versionados |
| `requirements.txt` presente | ✅ | Todas as dependências listadas |
| `random_state` no `train_test_split` | ⚠️ | `train_test_split(X, y, test_size=0.1, random_state=7)` — OK nesta linha |
| Instruções de execução no README | ✅ | Ordem de execução dos notebooks especificada |
| Caminho de dados relativo | ✅ | `os.path.join("data", 'flights.csv')` — sem hardcode absoluto |
| NaN em ARRIVAL_DELAY no notebook | ⚠️ | `analise_atraso.ipynb` não faz `dropna(subset=['ARRIVAL_DELAY'])` explicitamente; o `app.py` faz. Voos cancelados são filtrados mas NaN residuais em ARRIVAL_DELAY podem ser tratados silenciosamente pelo `np.where` como 0 |

---

### 3. Qualidade Técnica do Código (16/25)

| Item | Status | Detalhe |
|---|---|---|
| Sem data leakage | ✅ | Notebook documenta explicitamente as colunas com leakage (DEPARTURE_DELAY, WEATHER_DELAY etc.) e as exclui |
| Features do modelo | ⚠️ | `df_ml` foi preparado com 7 colunas; `X` usa apenas 3 (MONTH, AIRLINE, SCHEDULED_DEPARTURE_HOUR). DAY_OF_WEEK, DIST_TYPE, AIRPORT_RISK_LEVEL foram codificadas mas não incluídas em X |
| Feature engineering avançada | ✅ | Bayesian Smoothing para AIRPORT_SCORE (prior m=100 sobre média global); 6 categorias de risco por qcut |
| `helpers.py` compartilhado | ✅ | Funções `mapping_bts_code_to_iata_code` e `mapping_month_to_season` reutilizadas em notebooks e app |
| `app.py` bem estruturado | ✅ | Uso de pathlib, type hints, `@st.cache_data`, tratamento de FileNotFoundError/ValueError |
| Desbalanceamento tratado | ✅ | RF: `class_weight='balanced'`; XGB: `scale_pos_weight=peso_balanço` calculado do treino |
| Cross-validation | ❌ | Única divisão 90/10; sem k-fold |
| `SettingWithCopyWarning` | ⚠️ | Em `df_ml[col] = le.fit_transform(df_ml[col])` — cópia sem `.copy()` explícito |
| `DtypeWarning` no CSV | ⚠️ | `low_memory=False` ausente nos notebooks (presente no app) |
| Seaborn FutureWarning | ⚠️ | API depreciada (`palette` sem `hue`, parâmetro `ci`) |
| Docstrings em funções | ⚠️ | `helpers.py` tem docstrings; funções inline dos notebooks não têm |

---

### 4. Documentação (7/10)

| Item | Status | Detalhe |
|---|---|---|
| README principal | ✅ | Bem organizado: tabela de artefatos, instrução de dados, setup, execução, sumário de modelagem |
| Células markdown nos notebooks | ✅ | Cada análise tem markdown explicativo com insights (ex: "reset das 5h", efeito cascata) |
| Fluxo entre notebooks | ✅ | README especifica a ordem: `eda_geral → analise_atraso → k_means` |
| `helpers.py` com docstrings | ✅ | Funções documentadas |
| Insights nas conclusões | ✅ | Markdown explicando o que foi encontrado e o que significa (análise de companhias, clustering) |
| Gráficos sem saída renderizada | ⚠️ | Várias células mostram apenas `<Figure size X with Y Axes>` em vez da imagem |
| Sem documentação de limitações | ⚠️ | O app.py tem notas, mas os notebooks não documentam limitações do modelo |

---

### 5. Evidências de Execução (7/10)

| Item | Status | Detalhe |
|---|---|---|
| Notebooks executados | ✅ | Todas as células têm outputs numéricos e textuais |
| Métricas quantitativas | ✅ | `classification_report` completo (precision, recall, f1, support) impresso |
| Imagens dos gráficos | ⚠️ | Mostram `<Figure size...>` em vez de imagens; imagens não estão inline no arquivo `.ipynb` |
| Modelos treinados salvos | ✅ | `.pkl` files presentes e testados no `predicao_classificacao.ipynb` |
| `predicao_classificacao.ipynb` | ✅ | Notebook de inferência funcionando, testa os 2 modelos com novo input |

---

### 6. Critérios Não Funcionais (2/5)

| Item | Status | Detalhe |
|---|---|---|
| `requirements.txt` | ⚠️ | Usa `>=` em vez de versões fixas (`==`) |
| `.gitignore` | ❌ | Ausente — arquivos `.pkl` (19 MB), `__pycache__/`, `.ipynb_checkpoints/` não excluídos |
| Modelos `.pkl` no git | ⚠️ | `modelo_random_forest.pkl` tem 19 MB — deveria estar no `.gitignore` ou usar Git LFS |
| Dois colaboradores | ✅ | mayara-canaver (notebooks principais) + eduardohenrik (dashboard Streamlit e README) |

---

## Resultados dos Modelos

### Classificação — "O voo vai atrasar?" (threshold: ARRIVAL_DELAY ≥ 15 min)

Dataset: 5.713.008 voos operacionais (cancellados/desviados removidos)  
Divisão: 90% treino (~5.1M) / 10% teste (~571K) | `random_state=7`

| Modelo | Precision (classe 1) | Recall (classe 1) | F1 (classe 1) | Accuracy |
|---|---|---|---|---|
| **Random Forest** | 0.26 | **0.63** | 0.37 | 59% |
| **XGBoost** | 0.26 | **0.63** | 0.37 | 60% |

Features usadas: `MONTH`, `AIRLINE` (label encoded), `SCHEDULED_DEPARTURE_HOUR`

> **Insight do notebook:** "O modelo funciona como um filtro de priorização: identifica voos com alta probabilidade de problemas, permitindo medidas preventivas em 2/3 dos casos reais." A baixa precision (0.26) é esperada dado o desbalanceamento da classe (18.6% de atrasos) e as features limitadas.

### Clusterização de Aeroportos (K-Means, k=5)

Features: taxa média de atraso × volume de voos por aeroporto de origem (StandardScaler)

| Cluster | Perfil | Observação |
|---|---|---|
| Cluster estável (grande) | Mega-hubs com alto volume e perfil estável | ATL, ORD etc. |
| Cluster problemático (pequeno) | Aeroportos pequenos com alta taxa de atraso | Aeroportos regionais |
| Cluster eficiente (médio) | Hubs regionais mais pontuais | — |

> **Insight do notebook:** "O risco não está nos grandes hubs (Cluster 3), que são estáveis, mas sim em aeroportos menores com baixa eficiência (Cluster 2)."

---

## Pontos Positivos

1. **Dashboard Streamlit completo** (`app.py`) — extra significativo com filtros interativos, 3 abas, KMeans ao vivo no recorte filtrado, caching, error handling robusto e type hints
2. **Sem data leakage** — documentado explicitamente no notebook com justificativa
3. **Feature engineering com Bayesian Smoothing** — AIRPORT_SCORE com prior m=100 para estabilizar aeroportos com poucos voos
4. **Tratamento de desbalanceamento** — class_weight e scale_pos_weight corretamente aplicados
5. **helpers.py reutilizável** — separação de responsabilidades entre notebooks e app
6. **Dois modelos de classificação** — RF e XGBoost com métricas comparáveis
7. **Insights contextualizados** — "reset das 5h", efeito cascata, análise de clusters bem explicada
8. **Fluxo de inferência separado** — `predicao_classificacao.ipynb` mostra como carregar e usar os modelos

## Oportunidades de Melhoria

1. 🔴 **Implementar Regressão** — estimar minutos de atraso (LinearRegression ou RandomForestRegressor sobre voos atrasados)
2. 🔴 **Implementar PCA** — redução de dimensionalidade para visualização/interpretação
3. 🟠 **Usar todas as features preparadas** — DAY_OF_WEEK, DIST_TYPE e AIRPORT_RISK_LEVEL foram codificadas mas não incluídas em X
4. 🟠 **Adicionar `.gitignore`** — excluir `*.pkl` (19 MB), `__pycache__/`, `.ipynb_checkpoints/`
5. 🟠 **Corrigir SettingWithCopyWarning** — usar `.copy()` ou `.loc` para evitar cópia implícita
6. 🟡 **Cross-validation** — k-fold para estimativas mais robustas de performance
7. 🟡 **Renderizar imagens nos notebooks** — usar `plt.savefig()` ou garantir que o matplotlib backend gera PNG inline
8. 🟡 **Fixar versões no requirements.txt** — usar `==` em vez de `>=`
9. 🟡 **Atualizar API seaborn depreciada** — remover warnings de `palette` sem `hue` e `ci`

---

## Conclusão

A equipe demonstrou boa capacidade técnica e entregou trabalho de qualidade acima da média — especialmente o dashboard Streamlit, que vai além dos requisitos mínimos. A EDA é detalhada, os modelos são bem configurados e o código do app é profissional. No entanto, a ausência de dois componentes obrigatórios (Regressão e PCA) representa uma lacuna significativa no atendimento ao escopo do Tech Challenge 3. Com a implementação desses componentes, a nota subiria para a faixa de 78–82 pontos.
