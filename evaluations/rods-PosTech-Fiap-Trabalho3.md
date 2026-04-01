# Avaliação — rods/PosTech-Fiap-Trabalho3

**Repositório:** https://github.com/rods/PosTech-Fiap-Trabalho3  
**Avaliado em:** 31/03/2026  
**Curso:** Pós-Graduação em Machine Learning Engineering — FIAP  
**Tema:** Análise e previsão de atrasos de voos nos EUA (Dataset: 2015 Flight Delays, Kaggle)

---

## Nota Final: **83 / 90**

---

## Resumo Executivo

Trabalho de alta qualidade que atende completamente ao escopo da fase 3. O repositório é bem organizado, o código é limpo e bem documentado (funções com docstrings e type hints), todas as células do notebook foram executadas com saídas preservadas, e dois arquivos HTML foram gerados como evidências (`analysis_completo.html` e `analysis_resumo.html`). **Não há vazamento de dados (data leakage)** nos modelos preditivos — apenas features pré-voo são usadas. Os resultados dos modelos são honestos e bem interpretados, reconhecendo explicitamente as limitações causadas pela ausência de dados externos (clima, tráfego aéreo).

---

## Critérios de Avaliação

### 1. Aderência ao Problema (25/25)

| Requisito | Status | Evidência |
|---|---|---|
| EDA completa | ✅ | Seção 3: estatísticas, distribuição de atrasos, padrões temporais, top aeroportos/companhias, matriz de correlação |
| Modelo de Classificação | ✅ | Seção 4: LR + RF para prever IS_DELAYED (binário, threshold 15 min) |
| Modelo de Regressão | ✅ | Seção 5: LinearRegression + RF Regressor para estimar minutos de atraso |
| Clusterização | ✅ | Seção 6: KMeans com k=2..10, seleção por Silhouette Score (k=6, score=0.34), 628 aeroportos |
| PCA | ✅ | Seção 7: 6 → 2 dimensões, 77.4% da variância preservada; PC1=54.8% (tamanho), PC2=22.6% (rotas/cancelamentos) |

---

### 2. Reprodutibilidade (15/15)

| Item | Status | Detalhe |
|---|---|---|
| RANDOM_STATE global | ✅ | `RANDOM_STATE = 42` definido como constante e usado em todos os modelos |
| `np.random.seed` | ✅ | Aplicado na configuração inicial |
| Notebook com outputs | ✅ | Todas as células executadas, outputs visíveis no `.ipynb` |
| HTML como evidência | ✅ | `analysis_completo.html` (1.6 MB) + `analysis_resumo.html` (18 KB) |
| Instruções de setup | ✅ | README claro: criar virtualenv, `pip install -r requirements.txt`, download do dataset Kaggle, executar `jupyter notebook` |
| `data/` com `.gitkeep` | ✅ | Diretório reservado; README explica como baixar os CSVs; CSV não versionado (correto, 592 MB) |
| Caminhos sem hardcode | ✅ | `DATA_PATH = '../data'` como constante editável |

---

### 3. Qualidade Técnica do Código (22/25)

| Item | Status | Detalhe |
|---|---|---|
| Sem data leakage | ✅ | Features: MONTH, DAY_OF_WEEK, HOUR_OF_DAY, AIRLINE, ORIGIN_AIRPORT, DESTINATION_AIRPORT, SCHEDULED_TIME, DISTANCE, IS_WEEKEND — todas pré-voo |
| Funções com docstrings e type hints | ✅ | `load_datasets`, `merge_datasets`, `handle_missing_values`, `create_temporal_features`, `create_delay_flag`, etc. |
| Validações com `assert` | ✅ | Validação pós-merge (contagem de linhas), validação de features derivadas |
| Otimização de memória | ✅ | `dtypes` otimizados para `flights.csv` (592 MB): `int8/int16/float32/category` em vez de `int64/float64` |
| Tratamento de erros | ✅ | `FileNotFoundError` e `MemoryError` tratados em `load_datasets` com mensagens orientativas |
| Tratamento de missing values | ✅ | Estratégias `'drop'` e `'impute'` implementadas; apenas 1.81% removido |
| Encoding categórico | ⚠️ | Label Encoding para AIRLINE, ORIGIN_AIRPORT, DESTINATION_AIRPORT — pode introduzir relação ordinal falsa; Target Encoding ou OHE seria mais adequado |
| Tuning de hiperparâmetros | ⚠️ | RandomForest com `n_estimators=100` (padrão); sem busca de hiperparâmetros |
| Validação cruzada | ⚠️ | Única divisão train/test (80/20); cross-validation aumentaria robustez |

---

### 4. Documentação (10/10)

| Item | Status | Detalhe |
|---|---|---|
| README principal | ✅ | Descrição do projeto, estrutura, dataset, setup passo a passo, opção Colab |
| `data/README.md` | ✅ | Tabela com arquivos, tamanhos, link Kaggle e instrução de download |
| `notebooks/README.md` | ✅ | Identifica o notebook principal |
| `analysis_resumo.html` | ✅ | Explicação em linguagem acessível de cada seção (o que o código faz e por quê) |
| Índice no notebook | ✅ | Seções claramente tituladas com âncoras |
| Células markdown | ✅ | Cada seção tem markdown explicativo antes do código |

---

### 5. Evidências de Execução e Validação (8/10)

| Item | Status | Detalhe |
|---|---|---|
| Outputs preservados no `.ipynb` | ✅ | Tabelas, gráficos e prints em todas as células relevantes |
| `analysis_completo.html` | ✅ | Versão completa do notebook executado |
| `analysis_resumo.html` | ✅ | Versão com explicações em linguagem simples |
| Metricas quantitativas reportadas | ✅ | Accuracy, Precision, Recall, F1 (classificação); MAE, RMSE, R² (regressão); Silhouette (clustering) |
| Interpretação dos resultados | ✅ | Análise honesta do porquê os modelos não funcionam bem e o que melhoraria |
| Visualizações commitadas em `docs/` | ⚠️ | Diretório `docs/` existe mas contém apenas um README vazio — imagens poderiam ser salvas separadamente |

---

### 6. Critérios Não Funcionais (3/5)

| Item | Status | Detalhe |
|---|---|---|
| `.gitignore` | ✅ | Exclui `*.csv`, `__pycache__/`, `.venv/`, `.ipynb_checkpoints/`, `.DS_Store` |
| `requirements.txt` | ⚠️ | Usa versões mínimas (`>=`) em vez de versões fixas (`==`) — risco leve de incompatibilidade futura |
| Estrutura de diretórios | ✅ | `data/`, `notebooks/`, `docs/`, `requirements.txt`, `README.md` bem organizados |
| `.kiro/` no repositório | ⚠️ | Diretório de configuração de IDE commitado desnecessariamente |

---

## Resultados dos Modelos

### Classificação — "O voo vai atrasar?"

| Modelo | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| Logistic Regression | 81.4% | ~0% | ~0% | ~0% |
| **Random Forest** | **81.4%** | **68%** | **0.3%** | **0.6%** |

> **Interpretação correta no notebook:** A accuracy de 81.4% é enganosa — como 81.4% dos voos não atrasam, um modelo que sempre prediz "não atrasa" já atinge esse resultado. O Recall de 0.3% indica que o modelo praticamente não detecta atrasos reais. Causa raiz identificada corretamente: **ausência de dados externos** (clima, tráfego aéreo).

### Regressão — "Quantos minutos de atraso?"

| Modelo | MAE | RMSE | R² |
|---|---|---|---|
| Linear Regression | 30.7 min | 52.2 min | 0.01 (1%) |
| **Random Forest** | **30.0 min** | **51.6 min** | **0.03 (3%)** |

> Para voos com mediana de atraso de 15 min, MAE de 30 min é alto. R²=3% indica que o modelo explica apenas 3% da variação — causa raiz idem.

### Clusterização — "Grupos de aeroportos"

| Cluster | Qtd | Voos/ano | Taxa de Atraso | Perfil |
|---|---|---|---|---|
| 0 | 100 | ~7.700 | 13.5% | Médio porte, rotas longas, boa pontualidade |
| 1 | 283 | ~4.800 | 17.5% | Regionais, rotas curtas, atraso moderado |
| 2 | 1 | 9 | 44.4% | Outlier extremo |
| **3** | **27** | **~126.000** | **20.1%** | **Grandes hubs (ATL, ORD, DFW, LAX)** |
| 4 | 198 | ~800 | 9.3% | Pequenos, baixo volume, muito pontuais |
| 5 | 19 | ~880 | 32.2% | Pequenos com problemas crônicos |

> k=6 escolhido por Silhouette Score=0.34. Os grupos são semanticamente significativos.

### PCA

- PC1: 54.8% da variância (tamanho/volume do aeroporto)
- PC2: 22.6% da variância (tipo de rotas e cancelamentos)
- **Total: 77.4% preservados em 2D** — excelente para visualização

---

## Pontos Positivos

1. **Sem data leakage** — único ponto mais crítico de avaliações de ML, tratado corretamente
2. **Código profissional** — funções com docstrings, type hints, constants, assertions
3. **Interpretação honesta dos resultados** — o notebook explica por que os modelos não funcionam bem e propõe melhorias concretas
4. **Evidências sólidas** — dois HTMLs gerados + notebook com outputs
5. **Otimização de memória** — tratamento correto do arquivo de 592 MB
6. **Análise de clustering significativa** — k selecionado metodicamente, grupos com interpretação semântica

## Oportunidades de Melhoria

1. **Encoding categórico**: Label Encoding para aeroportos/companhias introduz ordem artificial. Target Encoding ou OneHotEncoding seriam mais corretos
2. **Cross-validation**: Uma única divisão 80/20 é menos robusta; k-fold cross-validation daria estimativas mais confiáveis
3. **Hiperparâmetros**: Nenhuma busca de hiperparâmetros (`GridSearchCV` ou `RandomizedSearchCV`)
4. **`requirements.txt`**: Usar versões fixas (`==`) em vez de mínimas (`>=`) para garantir reprodutibilidade total
5. **`docs/` vazio**: Salvar imagens dos principais gráficos como arquivos independentes seria um plus
6. **`.kiro/`**: Diretório de IDE não deveria estar no repositório (adicionar ao `.gitignore`)

---

## Conclusão

Este é um trabalho sólido e bem executado para o Tech Challenge Fase 3. A ausência de data leakage é o aspecto mais importante tecnicamente e está correto. O código é de qualidade profissional, bem documentado, e as conclusões são honestas e bem fundamentadas. As oportunidades de melhoria são majoritariamente refinamentos (encoding, cross-validation, tuning) que elevariam a nota para 88-90.
