# Avaliação Acadêmica — FIAP EML Tech Challenge Fase 3: Atrasos de Voos

**Repositório avaliado:** [jessycalunna/postech-proj-fase3](https://github.com/jessycalunna/postech-proj-fase3)  
**Data de avaliação:** 2026-04-02  
**Avaliador:** Copilot (agente automatizado)

---

## 📝 Avaliação Geral

O projeto se destaca pela **escolha tecnológica adequada à escala do problema**: utiliza PySpark no Databricks para processar os ~5,8 milhões de registros do dataset real de 2015, integra MLflow para rastreamento de experimentos, e persiste resultados em tabelas Delta no Unity Catalog. A análise exploratória é cuidadosa e responde diretamente às perguntas do rubric. O maior diferencial técnico é o notebook 04, que executa K-Means com elbow + Silhouette Score de forma exemplar, identificando 3 perfis distintos de aeroportos com boa interpretação de negócio. As principais fraquezas são a **domínio quase total de `DEPARTURE_DELAY` como feature preditiva** (limita a utilidade real do modelo supervisionado), a ausência de PCA ou qualquer redução de dimensionalidade, e uma **engenharia de repositório muito fraca**: README praticamente vazio, sem `requirements.txt`, sem `.gitignore`, estrutura plana e dependência exclusiva do Databricks.

---

## ✅ Pontos Positivos

1. **PySpark + MLflow + Delta Lake — stack de produção real:** O projeto não usa pandas/sklearn em notebook local, mas sim PySpark MLlib com `Pipeline`, `StringIndexer`, `VectorAssembler`, `StandardScaler` e `ClusteringEvaluator`. Todos os experimentos são rastreados no MLflow com parâmetros, métricas e modelos versionados, e as saídas dos modelos (previsões e clusters) são salvas como tabelas Delta reutilizáveis. Isso demonstra maturidade técnica acima da média em trabalhos acadêmicos.

2. **EDA orientada a responder o rubric:** O notebook 02 constrói uma tabela de conclusões (seção 11) que responde explicitamente às perguntas exigidas: aeroportos mais críticos (ASE ~15.5 min, EGE ~12.5 min), piores companhias (Spirit: 29% atrasados, Frontier: 25%), piores dias (quinta, segunda) e meses (junho, fevereiro), e causa principal (LATE_AIRCRAFT_DELAY ~24 min). A correlação entre DEPARTURE_DELAY e ARRIVAL_DELAY (0.94) é documentada com clareza.

3. **K-Means com validação dupla (Elbow + Silhouette) e interpretação de negócio:** O notebook 04 avalia k de 2 a 10 com WSSSE e Silhouette Score simultâneos, escolhendo k=3 (Silhouette = 0.4594) por critério quantitativo, não arbitrário. Os 3 clusters são nomeados e interpretados com perfis numéricos detalhados (39 mega hubs com taxi_out de 17.4 min e 19.5% de atrasados vs. 161 aeroportos eficientes com atraso médio de -0.7 min), e o heatmap normalizado complementa os scatter plots. A MLflow loga os artefatos visuais dentro da execução do experimento.

---

## ❌ Pontos de Melhoria

1. **`DEPARTURE_DELAY` domina com 96% da importância — modelo supervisionado com utilidade prática limitada:** O Random Forest identifica que o atraso na partida explica praticamente toda a variação do atraso na chegada (0.94 de correlação, 96% de importância). O modelo resultante aprende essencialmente a regra "se saiu atrasado, vai chegar atrasado". O notebook 05 reconhece essa limitação, mas não propõe nem executa uma versão do modelo **sem** `DEPARTURE_DELAY`, que seria o experimento comparativo mais importante para demonstrar capacidade de predição antecipada — que é o cenário de negócio relevante.

2. **Ausência de PCA ou qualquer redução de dimensionalidade:** O rubric menciona explicitamente "Redução de dimensionalidade (ex.: PCA)" como abordagem não supervisionada. Nenhum dos 5 notebooks aplica PCA, t-SNE, UMAP ou equivalente. O notebook 05 cita PCA apenas como "próximo passo" proposto. A infraestrutura de dados (tabelas Delta com múltiplas features numéricas) estava disponível para aplicar PCA antes do K-Means ou como análise independente das features do modelo supervisionado.

3. **Engenharia de repositório insuficiente:** O README contém apenas o título `# postech-proj-fase3` — sem descrição, sem instruções de execução, sem dicionário de dados. Não há `requirements.txt` (bibliotecas como `mlflow`, `matplotlib`, `seaborn` e `pandas` são necessárias). Não há `.gitignore`. A estrutura é plana (5 arquivos `.py` na raiz) sem organização em pastas. O repositório tem apenas 2 commits de um único autor com a mensagem genérica "Add files via upload" — sem histórico de desenvolvimento, sem ramificações, sem pull requests. A reprodução exige acesso ao workspace Databricks pessoal da autora e ao Unity Catalog `jessyca_oliveira.default`.

---

## 📊 Avaliação por Critério

### EDA: 8/10
O notebook de EDA (02) demonstra análise rigorosa dos 5,8M de registros usando PySpark distribuído. Cobre distribuição do atraso (média 4.4 min, mediana -5 min, 17.9% acima de 15 min), padrões por dia da semana, mês, top 15 aeroportos de origem (com filtro de ≥1.000 voos para relevância estatística), análise por companhia com join nos dados de airlines, matriz de correlação e análise das causas de atraso. A tabela de conclusões (seção 11) responde objetivamente às perguntas do rubric. A perda de pontos vem da ausência de: análise por hora do dia, mapas geográficos de rotas/atrasos, análise sazonal explícita (apenas mensal), e saídas estáticas commitadas no repositório (o notebook depende de execução no Databricks para visualizar os gráficos).

### Modelagem Supervisionada: 7/10
Dois algoritmos comparados (Regressão Logística + Random Forest) com boa configuração: feature selection anti-leakage (apenas variáveis disponíveis antes do pouso), undersampling para balanceamento de classes (2:1), pipeline com `StandardScaler`, e rastreamento via MLflow. Os resultados são sólidos: RF com 89.9% de acurácia e AUC-ROC ~0.93. A penalização principal é a concentração de 96% da importância em `DEPARTURE_DELAY` — o modelo aprende uma tautologia operacional em vez de um padrão preditivo antecipado. Também pesam: apenas 2 algoritmos (sem Gradient Boosting, XGBoost ou LightGBM), ausência de validação cruzada, nenhum gráfico de ROC ou matriz de confusão visualizado, e nenhuma iteração de otimização de hiperparâmetros.

### Modelagem Não Supervisionada: 7/10
O K-Means aplicado a aeroportos é bem executado: 8 features de agregação por aeroporto, `Pipeline` com `VectorAssembler` + `StandardScaler`, elbow + Silhouette Score para k de 2 a 10, k=3 selecionado por critério quantitativo (Silhouette = 0.4594), clusters interpretados com perfis numéricos e heatmap normalizado, MLflow logando métricas e artefatos visuais. Os 3 clusters (Mega Hubs congestionados / Regionais moderados / Eficientes e pontuais) são bem delimitados e interpretáveis. A nota não é superior porque PCA está completamente ausente — o rubric menciona redução de dimensionalidade como abordagem esperada — e porque os resultados da clusterização não foram integrados como feature no modelo supervisionado (o que elevaria consideravelmente o nível técnico).

### Análise Crítica: 8/10
O notebook 05 é o ponto mais forte em termos de reflexão. Consolida resultados de todas as etapas, documenta 6 limitações em tabela estruturada com justificativa de impacto para o negócio (incluindo o reconhecimento honesto do problema de DEPARTURE_DELAY), e propõe 4 próximas etapas concretas e tecnicamente fundamentadas (incluir clima NOAA, testar sem DEPARTURE_DELAY, usar XGBoost/LightGBM, DBSCAN, Model Serving no Databricks). O painel 2×2 de resultados visuais consolida as conclusões de forma executiva. A penalização é pela ausência de tabela comparativa de métricas dos dois modelos (a célula de MLflow search pode não funcionar sem o experiment_id correto) e pela falta de discussão explícita sobre por que o RF supera a LR (além das métricas brutas).

### Engenharia/Organização: 4/10
O pior aspecto do projeto. O README contém apenas o título, sem qualquer instrução, contexto ou dicionário de dados. Não há `requirements.txt`, `.gitignore` ou estrutura de pastas. Os 5 arquivos `.py` são exports do Databricks com marcadores `# MAGIC %md` — legíveis, mas não executáveis localmente sem o ambiente Databricks. O repositório tem 2 commits, 1 autor, mensagem genérica ("Add files via upload"), sem histórico de desenvolvimento. A reprodução completa é impossível sem acesso ao workspace Databricks pessoal e às credenciais do Unity Catalog. A nota (4 e não menos) reconhece que o código é bem estruturado internamente (numeração lógica dos notebooks, seções bem delimitadas, boas práticas de PySpark e MLflow dentro do ambiente Databricks).

---

## 🎯 Nota Final

**6.6 / 10**

O projeto entrega análise técnica competente com stack de produção real (PySpark, MLflow, Delta Lake) e responde satisfatoriamente ao rubric em EDA, modelagem supervisionada e não supervisionada. A nota é limitada pela combinação de: modelo supervisionado que aprende uma tautologia (DEPARTURE_DELAY → ARRIVAL_DELAY) sem explorar o cenário de predição antecipada, ausência de PCA/redução de dimensionalidade, e engenharia de repositório muito deficiente. Com um README completo, `requirements.txt`, uma versão do modelo sem `DEPARTURE_DELAY`, e a adição de PCA, este projeto poderia facilmente alcançar 8.0+.
