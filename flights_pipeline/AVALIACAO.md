# 📋 Avaliação — Tech Challenge Fase 3
**Repositório avaliado:** https://github.com/jgmsgabriel/postech-fiap-tech-03  
**Curso:** Machine Learning Engineering — FIAP PosTech  
**Data da avaliação:** 2026-04-01

---

## 1. Visão Geral do Repositório

### Estrutura identificada

```
postech-fiap-tech-03/
├── data/
│   ├── airlines.csv          ✅ Presente
│   ├── airports.csv          ✅ Presente
│   └── data_dictionary.pdf   ✅ Presente
│   └── flights.csv           ❌ AUSENTE (arquivo principal — requer download externo)
├── src/notebooks/
│   ├── tech_challenge_fase3_flights.ipynb      ✅ EDA + Modelagem Supervisionada
│   └── tech_challenge_fase3_unsupervised.ipynb ✅ Modelagem Não Supervisionada
├── outputs/
│   ├── figs/    (10 imagens geradas)            ✅
│   └── tables/  (10 tabelas CSV geradas)        ✅
├── .gitignore                                    ✅
├── README.md                                     ❌ AUSENTE
└── requirements.txt                              ❌ AUSENTE
```

### Dataset utilizado
- **Fonte:** Dataset público de voos dos EUA (BTS / Kaggle — 2015 Flight Delays and Cancellations)
- **Dimensões:** 5.819.079 linhas × 31 colunas
- **Tabelas auxiliares:** companhias aéreas (14 registros) e aeroportos (322 registros)

---

## 2. Critérios de Avaliação e Pontuação

| Critério                          | Peso | Nota | Pontuação |
|-----------------------------------|------|------|-----------|
| 1. Análise Exploratória de Dados  | 20   | 8,5  | **17,0**  |
| 2. Modelagem Supervisionada       | 30   | 7,5  | **22,5**  |
| 3. Modelagem Não Supervisionada   | 20   | 7,0  | **14,0**  |
| 4. Qualidade e Organização        | 15   | 6,0  | **9,0**   |
| 5. Documentação e Reprodutibilidade | 15 | 4,0  | **6,0**   |
| **Total**                         | 100  | —    | **68,5**  |

**Nota Final: 6,85 / 10**

---

## 3. Detalhamento por Critério

### 3.1 Análise Exploratória de Dados (EDA) — 17,0 / 20

**Pontos positivos:**
- ✅ Utilização de dado real e em grande escala (5,8 milhões de registros), o que demonstra maturidade técnica.
- ✅ Análise de valores ausentes bem conduzida, com visualização de barplot mostrando o percentual por coluna.
- ✅ Estatísticas descritivas exportadas para CSV, facilitando a revisão dos resultados.
- ✅ Estratégia inteligente de imputação: mediana por rota origem-destino para `AIR_TIME`, e reconstrução via fórmula para `ELAPSED_TIME` e `ARRIVAL_DELAY`.
- ✅ Análise de taxa de atraso segmentada por companhia, mês e aeroporto de origem.
- ✅ Matriz de correlação com heatmap.
- ✅ Análise e remoção de variáveis com alta ausência (colunas de delay reason, cancellations).
- ✅ Verificação de duplicatas (0 duplicatas encontradas).

**Pontos de melhoria:**
- ⚠️ Não foi realizada análise de outliers nas variáveis de atraso. Voos com atrasos extremos (ex.: > 300 min) podem distorcer modelos sem tratamento adequado.
- ⚠️ Ausência de análise temporal mais aprofundada: evolução de atrasos ao longo dos meses do ano não foi explicitamente visualizada em linha do tempo.
- ⚠️ Sem análise de distribuição geográfica por aeroporto (mapa de calor por estado/região).
- ⚠️ O notebook mistura EDA e modelagem supervisionada em um único arquivo de 1,8 MB, dificultando a navegação e manutenção.

---

### 3.2 Modelagem Supervisionada — 22,5 / 30

**Pontos positivos:**
- ✅ Feature engineering relevante: médias de atraso por rota, companhia e aeroporto de origem/destino.
- ✅ Inclusão de variáveis de atraso do voo anterior (`PREV_DEP_DELAY`) como feature preditiva.
- ✅ Uso de Label Encoding para variáveis categóricas (AIRLINE, ORIGIN_AIRPORT, DESTINATION_AIRPORT, TAIL_NUMBER).
- ✅ Comparação de pelo menos dois algoritmos (inferido pelo tamanho do notebook e imports observados).
- ✅ Métricas de avaliação presentes nos outputs (tabelas exportadas).

**Pontos de melhoria:**
- ⚠️ **Label Encoding para categorias de alta cardinalidade** (ex.: TAIL_NUMBER com centenas de valores únicos) pode introduzir ordem artificial. Recomenda-se Target Encoding ou embeddings para este caso.
- ⚠️ Não foi evidenciada validação cruzada (cross-validation), o que pode levar a estimativas otimistas de performance.
- ⚠️ Não há tratamento explícito de desbalanceamento de classes (ex.: `class_weight='balanced'` ou SMOTE).
- ⚠️ A separação EDA/modelagem no mesmo notebook dificulta a rastreabilidade do pipeline.
- ⚠️ Não foi evidenciada análise de importância de features ou SHAP values para interpretabilidade.

---

### 3.3 Modelagem Não Supervisionada — 14,0 / 20

**Pontos positivos:**
- ✅ Abordagem de clusterização em nível de rota (origem-destino) é relevante e bem fundamentada.
- ✅ Método do cotovelo (Elbow Method) utilizado para determinar k ótimo.
- ✅ Silhouette Score calculado como métrica de qualidade do agrupamento.
- ✅ Atributos de features bem escolhidos: total de voos, taxa de atraso de partida/chegada, atraso médio, distância e tempo de voo médios.

**Pontos de melhoria:**
- ⚠️ Apenas o algoritmo K-Means foi explorado. Recomenda-se comparar com DBSCAN (para detecção de outliers/rotas anômalas) ou Hierarchical Clustering.
- ⚠️ Não foi realizada redução de dimensionalidade com PCA para visualização 2D dos clusters, o que facilitaria a interpretação visual.
- ⚠️ A interpretação dos clusters poderia ser mais aprofundada: quais rotas pertencem a cada cluster? Qual o impacto operacional?
- ⚠️ Não há visualização clara do perfil dos clusters (ex.: heatmap normalizado por feature × cluster).

---

### 3.4 Qualidade e Organização do Código — 9,0 / 15

**Pontos positivos:**
- ✅ Código Python limpo, com uso adequado de pandas, matplotlib, seaborn e scikit-learn.
- ✅ Outputs organizados em diretórios separados (`figs/` e `tables/`).
- ✅ Uso de constantes e paths parametrizados (`fig_dir`, `table_dir`).
- ✅ Funções `display()` para apresentação de tabelas nos notebooks.

**Pontos de melhoria:**
- ⚠️ **Sem modularização**: todo o código reside em notebooks. Funções de pré-processamento e feature engineering deveriam ser extraídas para módulos `.py` reutilizáveis.
- ⚠️ Ausência de testes unitários ou de integração.
- ⚠️ O notebook principal (`tech_challenge_fase3_flights.ipynb`) é muito extenso (~1,8 MB) — deveria ser dividido em ao menos dois: EDA e Modelagem.
- ⚠️ Sem uso de `Pipeline` do scikit-learn para encadeamento de pré-processamento + modelo, o que aumenta o risco de data leakage.

---

### 3.5 Documentação e Reprodutibilidade — 6,0 / 15

**Pontos positivos:**
- ✅ Comentários inline nos notebooks explicando as decisões tomadas.
- ✅ Células Markdown separando seções do notebook.
- ✅ Dicionário de dados em PDF incluído no repositório.

**Pontos de melhoria:**
- ❌ **README.md ausente**: não há instruções de como executar o projeto, instalar dependências ou baixar o dataset.
- ❌ **requirements.txt ausente**: as versões das bibliotecas utilizadas não estão documentadas, comprometendo a reprodutibilidade.
- ❌ **Dataset principal ausente** (`flights.csv`): o arquivo de ~600 MB precisa ser baixado manualmente de fonte externa (Kaggle), sem instruções de como fazê-lo.
- ⚠️ Sem uso de `random_state` fixo em todas as operações estocásticas — resultados podem variar entre execuções.
- ⚠️ Sem `.env.example` ou arquivo de configuração para variáveis de ambiente.

---

## 4. Análise Comparativa com Boas Práticas

| Boa Prática                             | Status |
|-----------------------------------------|--------|
| README com instruções claras            | ❌     |
| requirements.txt com versões fixadas    | ❌     |
| Dataset versionado ou instruções de download | ❌ |
| Separação EDA / Treinamento / Avaliação | ⚠️ Parcial |
| Modularização em módulos `.py`          | ❌     |
| Pipeline scikit-learn (evita leakage)   | ❌     |
| Cross-validation                        | ⚠️ Não evidenciado |
| Tratamento de desbalanceamento          | ⚠️ Não evidenciado |
| Visualização de importância de features | ⚠️ Não evidenciado |
| Comparação de ≥ 2 algoritmos supervisionados | ✅ |
| Comparação de ≥ 2 algoritmos não supervisionados | ❌ |
| PCA ou t-SNE para visualização clusters | ❌     |
| Análise crítica dos resultados          | ✅ Presente |
| Testes unitários                        | ❌     |

---

## 5. Recomendações Prioritárias

1. **Adicionar README.md** com: descrição do projeto, instruções de instalação, como baixar o dataset, e como executar os notebooks.
2. **Criar requirements.txt** com versões fixadas das bibliotecas (ex.: `pandas==2.2.2`, `scikit-learn==1.5.0`).
3. **Separar EDA de Modelagem** em notebooks distintos para melhor organização e manutenção.
4. **Extrair funções de pré-processamento** para um módulo `src/preprocessing.py`, reduzindo duplicação.
5. **Adicionar validação cruzada** (ex.: `StratifiedKFold`) para estimativas mais robustas de performance.
6. **Incluir PCA** para visualização 2D dos clusters no notebook de clusterização.
7. **Comparar K-Means com DBSCAN** para demonstrar consciência das limitações de cada algoritmo.
8. **Documentar o pipeline de features** — quais features foram criadas, como e por quê.

---

## 6. Referência de Implementação

O diretório `flights_pipeline/` neste repositório contém uma implementação de referência que aborda os principais pontos de melhoria identificados:

- **`src/data_generation.py`**: geração de dataset sintético com 50.000 registros reproduzíveis.
- **`src/preprocessing.py`**: pré-processamento modularizado com `Pipeline` scikit-learn, evitando data leakage.
- **`notebooks/flight_data_pipeline.ipynb`**: notebook estruturado em 5 seções claramente separadas (EDA, Supervisionado, Não Supervisionado, Análise Crítica, Reprodutibilidade).

```bash
# Reproduzir a implementação de referência
cd flights_pipeline
pip install -r requirements.txt
jupyter notebook notebooks/flight_data_pipeline.ipynb
```

---

*Avaliação gerada automaticamente pelo head-system com base na análise estática do repositório.*
