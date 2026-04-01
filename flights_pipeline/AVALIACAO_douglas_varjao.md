# 📋 Avaliação — Tech Challenge Fase 3: Atrasos de Voos
**Repositório avaliado:** https://github.com/douglas-varjao/TechChallenge-Fase3-AtrasosVoos  
**Curso:** Machine Learning Engineering — FIAP PosTech  
**Data da avaliação:** 2026-04-01  
**Idioma da resposta:** Português do Brasil

---

## 1. Visão Geral do Repositório

### Estrutura identificada

```
TechChallenge-Fase3-AtrasosVoos/
├── README.md                            ✅ Presente e completo
├── Tc3_Analise_exploratoria.ipynb       ✅ Notebook dedicado à EDA (2,2 MB)
└── TechChallenge_Fase3_AtrasosVoos.ipynb ✅ Pipeline de ML completo (1,2 MB)
```

**Arquivos ausentes:**
- ❌ `requirements.txt` — dependências não documentadas
- ❌ `flights.csv` / `airlines.csv` / `airports.csv` — hospedados no Google Drive (link fornecido)
- ❌ `clima_2015.csv` — gerado via API Open-Meteo, sem script de coleta versionado

### Dataset utilizado
- **Fonte:** Dataset público de voos domésticos dos EUA — BTS/Kaggle 2015
- **Dimensões:** 5.819.079 linhas × 31 colunas (após limpeza: 5.712.660 registros)
- **Tabelas auxiliares:** `airlines.csv` (14 registros) e `airports.csv` (322 registros)
- **Dados externos:** `clima_2015.csv` coletado via API Open-Meteo com dados reais de 2015

---

## 2. Critérios de Avaliação e Pontuação

| Critério                              | Peso | Nota | Pontuação |
|---------------------------------------|------|------|-----------|
| 1. Análise Exploratória de Dados (EDA)| 20   | 9,0  | **18,0**  |
| 2. Modelagem Supervisionada           | 30   | 8,7  | **26,0**  |
| 3. Modelagem Não Supervisionada       | 20   | 8,5  | **17,0**  |
| 4. Qualidade e Organização do Código  | 15   | 7,3  | **11,0**  |
| 5. Documentação e Reprodutibilidade   | 15   | 6,7  | **10,0**  |
| **Total**                             | 100  | —    | **82,0**  |

**Nota Final: 8,2 / 10**

---

## 3. Detalhamento por Critério

### 3.1 Análise Exploratória de Dados (EDA) — 18,0 / 20

**Pontos positivos:**
- ✅ **Notebook EDA dedicado** (`Tc3_Analise_exploratoria.ipynb`): separação adequada entre exploração e modelagem, com 5 seções bem estruturadas (Configuração, Carregamento, Dicionário, EDA e Perguntas de Negócio).
- ✅ **Dicionário de dados completo** com todas as 31 colunas, tipos, descrições e identificação da variável-alvo, apresentado com estilo visual (destaque em amarelo para `ARRIVAL_DELAY`).
- ✅ **Análise de causas de atraso** com detalhe por companhia, mês, aeroporto de origem e tipo de causa (clima, sistema, cascata, segurança, companhia).
- ✅ **Tratamento explícito de nulos**: colunas de causa de atraso preenchidas com 0 (comportamento esperado documentado).
- ✅ **Paleta visual consistente** (`COR_PRINCIPAL`, `COR_ALERTA`, `COR_OK`, `COR_NEUTRO`) utilizada em todos os gráficos ao longo dos dois notebooks.
- ✅ **Volume de dados real e em grande escala** (5,8 milhões de registros) demonstra maturidade técnica e habilidade de trabalhar com datasets de produção.
- ✅ **Perguntas de negócio explícitas**: análise orientada a problemas reais (quais companhias atrasam mais? Quais rotas são críticas?).
- ✅ Uso de `sns.set_theme` e padronização de `plt.rcParams` garante uniformidade visual.

**Pontos de melhoria:**
- ⚠️ A análise temporal (evolução mensal dos atrasos) não foi explicitamente representada em gráfico de linha evolutiva ao longo do ano.
- ⚠️ Não há análise geográfica (mapa de calor dos estados com maior concentração de atrasos), o que enriqueceria a narrativa.
- ⚠️ O limiar de 600 minutos (10 horas) para remoção de outliers, embora justificado, não foi validado com análise de distribuição (boxplot/histogram) antes e depois do corte.

---

### 3.2 Modelagem Supervisionada — 26,0 / 30

**Pontos positivos:**
- ✅ **Três algoritmos comparados:** XGBoost, LightGBM e Rede Neural (MLP `(128, 64, 32)`), cobrindo paradigmas distintos (boosting baseado em árvore e redes neurais).
- ✅ **Tratamento do desbalanceamento** com `stratify` no split e `scale_pos_weight` nos modelos de boosting — abordagem correta para ~18% de positivos.
- ✅ **Ajuste de threshold para 0.4**, documentado com justificativa de negócio: priorizar Recall (redução de Falsos Negativos) é mais crítico do que Precision para este caso de uso.
- ✅ **Feature Engineering avançado antes da decolagem:**
  - `HIST_ATRASO_ROTA` — média móvel de 7 dias de atrasos da mesma rota (captura efeito cascata).
  - `IS_HOLIDAY`, `IS_WEEKEND` — flags de calendário para feriados federais.
  - `FLUXO_DIARIO` — contagem de voos no aeroporto de origem no dia (proxy de congestionamento).
  - `chuva_mm`, `vento_kmh`, `temperatura_max` — dados reais de clima de 2015 via API Open-Meteo.
  - `CLUSTER_AERO` — perfil operacional do aeroporto (injeção de resultado do K-Means).
- ✅ **SHAP Values** para explicabilidade: Beeswarm (importância global), Dependence Plot (não-linearidade do horário) e Waterfall (diagnóstico individual de Falsos Negativos).
- ✅ **Análise de erros (Falsos Negativos)** com diagnóstico sistêmico identificando padrão na Delta Airlines no aeroporto ATL.
- ✅ Uso de `LabelEncoder` para variáveis categóricas (`AIRLINE`, `ORIGIN_AIRPORT`, `DESTINATION_AIRPORT`, `TAIL_NUMBER`).

**Pontos de melhoria:**
- ⚠️ **Ausência de validação cruzada** (`StratifiedKFold`): a avaliação é feita em um único split, o que pode levar a estimativas de performance mais otimistas do que a realidade.
- ⚠️ **LabelEncoder para `TAIL_NUMBER`** (alta cardinalidade com centenas de registros únicos) introduz ordem artificial. `Target Encoding` seria mais adequado para este caso.
- ⚠️ **Sem uso de `Pipeline` do scikit-learn**: pré-processamento aplicado manualmente fora do pipeline aumenta o risco de data leakage ao fazer ajuste de scaler no conjunto completo antes do split.
- ⚠️ Não foram realizados testes de significância estatística entre os modelos (ex.: McNemar's test) para confirmar se as diferenças de performance são significativas.

---

### 3.3 Modelagem Não Supervisionada — 17,0 / 20

**Pontos positivos:**
- ✅ **K-Means aplicado ao nível de aeroporto** (não de voo individual), com features que capturam o DNA operacional de cada aeroporto: `atraso_medio`, `perc_atrasado_faa`, `log_vol`, `perc_clima`, `perc_cascata`, `perc_cia`, `perc_sistema`.
- ✅ **K=4 validado pelo Silhouette Score** e comentado que foi escolhido com base em análise prévia (boas práticas de justificativa de hiperparâmetros).
- ✅ **PCA 2D** aplicado para validação visual da separação dos clusters.
- ✅ **Radar Chart** (gráfico de teia de aranha) para interpretação visual dos 4 clusters: visualização poderosa que facilita a comunicação dos perfis operacionais.
- ✅ **Nomes interpretáveis para os clusters**: "Eficientes (Baixo Atraso)", "Críticos (Alto Atraso)", "Efeito Cascata", "Sensíveis ao Clima".
- ✅ **Feature injetada nos modelos supervisionados** (`CLUSTER_AERO`): a clusterização não é apenas exploratória — ela enriquece diretamente o pipeline de predição.
- ✅ Filtro por volume mínimo (≥500 voos) antes da clusterização, evitando ruído estatístico em aeroportos pequenos.

**Pontos de melhoria:**
- ⚠️ **Apenas K-Means** foi explorado. Uma comparação com DBSCAN (para detecção de aeroportos operacionalmente anômalos/outliers) ou Hierarchical Clustering enriqueceria a análise.
- ⚠️ A clusterização é estática (1 ano de dados). A proposta de "Clusterização Dinâmica por estação" mencionada nas Limitações seria um avanço significativo.
- ⚠️ Não foi apresentado um heatmap normalizado de features × clusters, que complementaria o Radar Chart com uma visualização mais quantitativa.

---

### 3.4 Qualidade e Organização do Código — 11,0 / 15

**Pontos positivos:**
- ✅ **Dois notebooks distintos**: EDA separada do pipeline de ML, facilitando navegação, manutenção e reutilização.
- ✅ **Código limpo e comentado**: seções numeradas com comentários descritivos (`# ── Seção ──────────`), print statements informativos com emojis e linha separadora.
- ✅ **Tratamento de exceção** no carregamento dos dados (`try/except FileNotFoundError`) com mensagem de erro orientada ao usuário.
- ✅ **Paleta de cores definida como constantes**: `COR_PRINCIPAL`, `COR_ALERTA`, `COR_OK`, garantindo consistência visual e facilitando manutenção.
- ✅ `random_state=42` utilizado no KMeans e nos splits de dados para reprodutibilidade.
- ✅ **Outputs dos notebooks executados** (todas as células têm `outputs` registrados), permitindo revisar os resultados sem re-executar.

**Pontos de melhoria:**
- ⚠️ **Sem modularização em arquivos `.py`**: funções de feature engineering (cascata, calendário, clima, clusterização) estão embutidas nos notebooks e não podem ser importadas ou testadas isoladamente.
- ⚠️ **Sem uso de `Pipeline` do scikit-learn**: os passos de pré-processamento são encadeados manualmente, aumentando o risco de vazamento de dados e dificultando o deploy do modelo.
- ⚠️ **Sem testes unitários ou de integração**: a robustez das funções de feature engineering não é verificada automaticamente.
- ⚠️ A execução depende do Google Colab com `drive.mount`, o que impede a execução em ambiente local sem modificação do código.

---

### 3.5 Documentação e Reprodutibilidade — 10,0 / 15

**Pontos positivos:**
- ✅ **README.md excelente**: inclui descrição do problema, critério FAA, destaques técnicos, índice navegável com links, instruções de acesso aos dados, tabelas de decisão de limpeza e feature engineering, e seções de resultados, limitações e próximos passos.
- ✅ **Instruções de acesso aos dados no Google Drive** com link público e passo a passo para reproduzir o notebook no Google Colab.
- ✅ **Justificativas de negócio documentadas**: cada decisão de limpeza e engenharia de features possui uma justificativa explícita no README e no próprio notebook.
- ✅ **Análise de limitações e próximos passos** documentada de forma honesta e técnica (seção 7 do README).
- ✅ Notebooks abertos no Google Colab com badges de execução direta.

**Pontos de melhoria:**
- ❌ **`requirements.txt` ausente**: não é possível saber as versões exatas de `lightgbm`, `xgboost`, `shap`, `holidays` utilizadas, comprometendo a reprodutibilidade a longo prazo.
- ❌ **Script de coleta do clima (`clima_2015.csv`) não versionado**: um notebook ou script que reproduza a coleta via API Open-Meteo deveria estar no repositório.
- ⚠️ Os caminhos do Google Drive (`drive/MyDrive/TechChallenge_Fase3_AtrasosVoos/database/`) são hardcoded, exigindo adaptação manual por qualquer outro usuário.
- ⚠️ Ausência de `.gitignore` configurado para excluir arquivos de cache e outputs temporários.

---

## 4. Análise Comparativa com Boas Práticas

| Boa Prática                                              | Status         |
|----------------------------------------------------------|----------------|
| README com instruções claras                             | ✅ Completo    |
| Índice navegável no README                               | ✅             |
| Instruções de acesso ao dataset                          | ✅ Google Drive|
| Separação EDA / Treinamento / Avaliação                  | ✅ Dois notebooks|
| Comentários inline e seções nomeadas                     | ✅             |
| Outputs dos notebooks executados                         | ✅             |
| Tratamento de desbalanceamento de classes                | ✅ scale_pos_weight + stratify |
| Comparação de ≥ 2 algoritmos supervisionados             | ✅ 3 modelos   |
| Ajuste de threshold e justificativa                      | ✅             |
| Feature engineering com dados externos (clima)           | ✅             |
| Feature engineering temporal (feriados, dia da semana)  | ✅             |
| Clusterização com K-Means + PCA                         | ✅             |
| Validação de clusters (Silhouette Score)                 | ✅             |
| Explicabilidade com SHAP Values                          | ✅             |
| Análise de erros (Falsos Negativos)                      | ✅ Diagnóstico sistêmico |
| requirements.txt com versões fixadas                     | ❌             |
| Modularização em arquivos `.py`                          | ❌             |
| Pipeline scikit-learn (evita data leakage)               | ❌             |
| Validação cruzada (StratifiedKFold)                      | ❌             |
| Testes unitários                                         | ❌             |
| Script de coleta de dados externos versionado            | ❌             |
| Comparação K-Means vs. DBSCAN                            | ❌             |

---

## 5. Destaques Técnicos Excepcionais

Este repositório apresenta **três elementos que se destacam acima da média** dos projetos do Tech Challenge:

1. **Integração de dados externos reais via API (Open-Meteo):** A coleta de dados climáticos históricos de 2015 para enriquecer o dataset vai além do esperado para o escopo do challenge, demonstrando iniciativa e compreensão do domínio.

2. **Análise de Erros com SHAP Waterfall:** A investigação sistemática dos Falsos Negativos usando SHAP Waterfall Plot não é apenas uma análise de performance — é um diagnóstico operacional. A identificação do padrão na Delta Airlines/ATL como ponto cego do modelo é um resultado de negócio relevante e acionável.

3. **Clusterização como Feature Engineering:** Usar o resultado do K-Means (`CLUSTER_AERO`) como feature de entrada para os modelos supervisionados é uma técnica avançada que demonstra integração real entre aprendizado não supervisionado e supervisionado no mesmo pipeline.

---

## 6. Recomendações Prioritárias

1. **Criar `requirements.txt`** com versões pinadas:
   ```
   pandas==2.x.x
   lightgbm==4.x.x
   xgboost==2.x.x
   shap==0.x.x
   holidays==0.x.x
   scikit-learn==1.x.x
   ```

2. **Versionar o script de coleta de clima** — um arquivo `scripts/coletar_clima_2015.py` que reproduza a chamada à API Open-Meteo é essencial para a reprodutibilidade do projeto.

3. **Adicionar validação cruzada** com `StratifiedKFold` (k=5) para estimativas mais robustas de F1-Score, especialmente dada a natureza desbalanceada do dataset.

4. **Encapsular o pré-processamento em um `Pipeline` do scikit-learn** para eliminar o risco de data leakage e facilitar o deploy do modelo.

5. **Adicionar `.gitignore`** para excluir arquivos de cache do Jupyter (`.ipynb_checkpoints/`), modelos serializados e arquivos temporários.

---

## 7. Comparação com a Implementação de Referência

O diretório `flights_pipeline/` neste repositório implementa o padrão de referência. Em comparação com o projeto avaliado:

| Aspecto                            | douglas-varjao          | Referência (flights_pipeline)     |
|------------------------------------|-------------------------|-----------------------------------|
| Escala dos dados                   | 5,8M registros reais    | 50k registros sintéticos          |
| Separação EDA/Modelagem            | ✅ Dois notebooks       | ✅ Um notebook estruturado        |
| Feature Engineering                | ✅ Avançado (clima+API) | ✅ Básico                         |
| Modelos supervisionados            | ✅ XGBoost, LightGBM, MLP | ✅ LR, RF, GradientBoosting      |
| Explicabilidade (SHAP)             | ✅ Presente             | ⚠️ Apenas importância de features |
| Modularização em .py               | ❌                      | ✅ src/preprocessing.py           |
| Pipeline scikit-learn              | ❌                      | ✅                                |
| requirements.txt                   | ❌                      | ✅                                |

> **Conclusão:** O projeto de douglas-varjao supera a referência em escala, profundidade técnica e explicabilidade, mas fica abaixo nas práticas de engenharia de software (modularização, Pipeline, testes e reprodutibilidade).

---

## 8. Resumo Final

| Dimensão                  | Avaliação |
|---------------------------|-----------|
| **Nível técnico**         | ⭐⭐⭐⭐⭐ Avançado |
| **Qualidade da análise**  | ⭐⭐⭐⭐½ Muito bom |
| **Documentação**          | ⭐⭐⭐⭐ Bom |
| **Reprodutibilidade**     | ⭐⭐⭐ Regular |
| **Engenharia de Software**| ⭐⭐½ Básico |

**Nota Final: 8,2 / 10**

Este é um trabalho de alta qualidade que demonstra domínio de técnicas avançadas de Machine Learning, incluindo modelos de boosting de última geração, explicabilidade com SHAP, integração de dados externos e diagnóstico sistêmico de erros. As principais lacunas estão nas práticas de engenharia de software (ausência de `requirements.txt`, modularização e Pipeline), que são facilmente corrigíveis.

---

*Avaliação realizada pelo head-system com base na análise estática do repositório.*
