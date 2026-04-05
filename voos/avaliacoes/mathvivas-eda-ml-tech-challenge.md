# Avaliação Acadêmica — FIAP EML Tech Challenge Fase 3: Atrasos de Voos

**Repositório avaliado:** [Mathvivas/pos-tech-fiap-alura — eda-ml-tech-challenge](https://github.com/Mathvivas/pos-tech-fiap-alura/tree/main/eda-ml-tech-challenge)  
**Data de avaliação:** 2026-04-04  
**Avaliador:** Copilot (agente automatizado)

---

## 📝 Avaliação Geral

O projeto se destaca em engenharia de dados: a arquitetura Medallion (Bronze → Silver → Gold) implementada com PySpark no Databricks demonstra maturidade técnica rara neste desafio, sendo a escolha correta para um dataset de 5,8 milhões de registros. A organização em notebooks sequenciais com outputs visíveis comprova que o código foi efetivamente executado.

No entanto, o projeto sofre de dois problemas críticos e estruturais que comprometem toda a validade dos modelos supervisionados:

1. **Data leakage severo nas features**: as variáveis usadas no VectorAssembler incluem DEPARTURE_DELAY, ARRIVAL_DELAY, DEPARTURE_TIME, TAXI_OUT, WHEELS_OFF, ELAPSED_TIME, AIR_TIME, WHEELS_ON, TAXI_IN e ARRIVAL_TIME — todas informações operacionais que só existem **depois que o voo aconteceu**. ARRIVAL_DELAY é literalmente uma das parcelas da própria variável alvo (TOTAL_DELAY = DEPARTURE_DELAY + ARRIVAL_DELAY).

2. **Target encoding calculado sobre o dataset completo antes do split**: as colunas `route_delay_rate` e `tail_delay_rate` são calculadas com `df.groupBy(...)` antes do `randomSplit`, contaminando o conjunto de teste com informações do treino.

Com esses dois problemas, o AUC de 0.8292 reportado para Regressão Logística não mede capacidade preditiva real — mede a capacidade do modelo de explorar leakage. A EDA, embora operacionalmente correta, é superficial e não produz os insights necessários para uma boa seleção de features.

---

## ✅ Pontos Positivos

1. **Arquitetura Medallion com PySpark no Databricks:** A divisão em Bronze (dados brutos), Silver (limpeza e transformação) e Gold (feature engineering + modelagem) é a abordagem correta para um dataset de 5,8M de registros. O uso de PySpark em vez de pandas evita o colapso de memória que afeta outros projetos deste desafio. Essa escolha técnica demonstra conhecimento de engenharia de dados em escala real.

2. **Raciocínio correto sobre ORIGIN/DESTINATION:** O notebook `gold.ipynb` justifica explicitamente que aeroportos de origem e destino têm cardinalidade alta demais para OneHotEncoding, e propõe como alternativa calcular a taxa média de atraso por rota (`route_delay_rate`) e por aeronave (`tail_delay_rate`). O conceito de **target encoding** para variáveis de alta cardinalidade é tecnicamente correto e demonstra compreensão além do básico — mesmo que a execução sofra do problema de leakage citado acima.

3. **Uso de Spark ML Pipeline com StandardScaler:** A modelagem usa corretamente `VectorAssembler → StandardScaler → LogisticRegression` encapsulados num `Pipeline`, que é a forma idiomática do Spark ML. Isso garante que o scaler seja ajustado apenas no treino durante o `pipeline.fit(train_df)`, e que a inferência em produção seja feita de forma consistente.

---

## ❌ Pontos de Melhoria

1. **Data leakage estrutural nas features — invalida todos os resultados supervisionados:** O `VectorAssembler` no `gold.ipynb` inclui as seguintes colunas no vetor de features:
   - **DEPARTURE_DELAY** — atraso real na partida, só medido após o voo sair
   - **ARRIVAL_DELAY** — atraso real na chegada; é **uma das parcelas do target** (TOTAL_DELAY = DEPARTURE_DELAY + ARRIVAL_DELAY)
   - **DEPARTURE_TIME** — horário real de partida (diferente de SCHEDULED_DEPARTURE)
   - **TAXI_OUT** — tempo real de taxiamento até a decolagem
   - **WHEELS_OFF** — instante real de decolagem
   - **ELAPSED_TIME** — tempo total real de voo
   - **AIR_TIME** — tempo real em voo
   - **WHEELS_ON** — instante real de pouso
   - **TAXI_IN** — tempo real até o portão após o pouso
   - **ARRIVAL_TIME** — horário real de chegada

   Nenhuma dessas variáveis está disponível no momento em que se deseja prever se um voo vai atrasar (antes da partida). O modelo aprende a reconstruir ARRIVAL_DELAY — que está praticamente embutido no próprio target — a partir de colunas que são versões do mesmo sinal. O AUC=0.8292 é uma ilusão estatística, não uma capacidade preditiva real.

2. **Data leakage no target encoding de rota e aeronave:** `route_delay_rate` e `tail_delay_rate` são calculados com:
   ```python
   route_stats = df.groupBy('ORIGIN_AIRPORT', 'DESTINATION_AIRPORT').agg(F.avg('TOTAL_DELAY')...)
   df = df.join(route_stats, ...)
   train_df, test_df = df.randomSplit([0.8, 0.2], seed=174)
   ```
   O join ocorre **antes** do split, portanto a média de atraso de cada rota é calculada incluindo os voos que vão para o conjunto de teste. Isso viola o princípio básico de que o conjunto de teste deve ser tratado como "desconhecido" durante o treino. A solução correta seria calcular as estatísticas apenas no `train_df` e depois fazer o join no `test_df`.

3. **Definição problemática do target — TOTAL_DELAY e limiar incorretos:**
   - `TOTAL_DELAY = DEPARTURE_DELAY + ARRIVAL_DELAY` é uma métrica sem sentido operacional claro. Se um voo sai 30 min atrasado mas chega apenas 10 min atrasado (compensou em voo), o TOTAL_DELAY seria 40 min. Isso não representa nem o atraso de partida nem o de chegada de forma limpa.
   - O limiar `DELAY = TOTAL_DELAY > 0` classifica como "atrasado" qualquer voo com soma positiva de atraso de partida + chegada, mesmo que seja 1 minuto. O padrão da aviação civil (FAA/IATA) é **ARRIVAL_DELAY ≥ 15 minutos**.
   - Essa definição não convencional não é justificada em nenhum lugar do projeto.

4. **EDA superficial, sem análise do target nem dos padrões temporais:** O notebook `flights-bronze-to-silver.ipynb` realiza: (a) contagem de nulos; (b) análise de atraso médio e mediana por companhia aérea. Faltam completamente:
   - Distribuição do ARRIVAL_DELAY (o target real): quais % dos voos chegam com ≥15 min de atraso?
   - Padrões temporais: atraso por mês, dia da semana, hora do dia (estudos mostram que voos após as 17h têm atraso crescente por efeito cascata)
   - Análise de aeroportos de origem e destino: quais são os mais congestionados?
   - Matriz de correlação entre variáveis numéricas
   - Análise das colunas de causa de atraso (AIR_SYSTEM_DELAY, WEATHER_DELAY, etc.) para entender o que mais causa atrasos
   - Discussão sobre o que significa "voo atrasado" e qual threshold usar

   Os insights gerados na EDA (NK tem maior atraso médio de partida) não são aproveitados nas decisões de feature engineering da modelagem.

---

## 📊 Avaliação por Critério

### EDA: 4/10
O notebook de EDA usa corretamente PySpark para inspecionar 5,8M de registros, identifica nulos em todas as colunas (incluindo o padrão correto: colunas de causa de atraso são nulas para voos não atrasados) e produz uma análise de atraso médio/mediano por companhia aérea com outputs visíveis. O notebook `silver-to-gold.ipynb` inclui um histograma de TOTAL_DELAY. A nota não é superior porque: (1) não há análise da variável alvo — qual é a taxa de voos "atrasados" segundo o critério escolhido?; (2) sem análise temporal (hora, mês, dia da semana) — que é fundamental para entender atrasos de voo; (3) sem análise de aeroportos de origem/destino — que são explicitamente mencionados no rubric; (4) sem correlações entre features; (5) sem discussão do critério de definição de "atraso" e do porquê da escolha de `TOTAL_DELAY > 0`; (6) os insights da EDA não informam a seleção de features para os modelos.

### Modelagem Supervisionada: 2/10
O projeto implementa Regressão Logística (classificação) e Random Forest Regressor com Spark ML Pipeline, StandardScaler e split 80/20. A estrutura técnica com Pipeline é correta. Contudo, a nota é mínima pelos seguintes motivos: (1) data leakage severo com features pós-evento (ARRIVAL_DELAY, DEPARTURE_DELAY, TAXI_OUT, ELAPSED_TIME, etc.) invalida completamente os resultados — AUC=0.8292 é artificial; (2) data leakage no target encoding (calculado antes do split); (3) o target TOTAL_DELAY > 0 é não convencional e não justificado; (4) FLIGHT_NUMBER e TAIL_NUMBER (via tail_delay_rate) são incluídos como features, mas `route_delay_rate` calculada com leakage é o principal preditor; (5) não há métricas além de AUC (sem Precision, Recall, F1, matriz de confusão); (6) não há análise dos coeficientes do modelo (feature importance); (7) nenhuma iteração ou melhoria do modelo após os primeiros resultados.

### Modelagem Não Supervisionada: 5/10
O notebook implementa KMeans com PCA via Spark ML (`pyspark.ml.clustering.KMeans`, `pyspark.ml.feature.PCA`). O uso de PCA antes do KMeans para redução de dimensionalidade é tecnicamente correto e demonstra conhecimento acima da média. O uso de `ClusteringEvaluator` para avaliação é correto. A nota não é superior porque: (1) as features usadas no KMeans incluem as mesmas variáveis com leakage (ARRIVAL_DELAY etc.), contaminando também os clusters; (2) não há justificativa para o número de clusters escolhido (sem Elbow Method); (3) os clusters não são interpretados — quem são os voos no cluster X? O que eles têm em comum?; (4) sem visualização dos clusters (scatter plots, distribuição das features por cluster); (5) sem análise de Silhouette Score como métrica adicional.

### Análise Crítica: 2/10
Praticamente inexistente. O notebook `gold.ipynb` apresenta resultados (AUC, tabela de previsões) sem qualquer análise do que significam, por que são assim, e o que poderiam indicar sobre o modelo. O problema mais grave do projeto — o data leakage severo — não é mencionado em nenhum lugar. Não há comparativo entre os modelos supervisionado e não supervisionado. Não há discussão de limitações (dataset de apenas 2015, apenas voos domésticos americanos, ausência de dados meteorológicos reais). Não há próximos passos propostos. Não há resposta estruturada às perguntas de negócio do rubric.

### Engenharia/Organização: 7/10
Ponto muito positivo: arquitetura Medallion (Bronze/Silver/Gold) com PySpark no Databricks, demonstrando maturidade de engenharia de dados. Os notebooks são bem nomeados e sequenciais (a ordem de execução está clara no README). O código usa Spark corretamente: DataFrames PySpark, funções `F.*`, `Window`, `Pipeline`, `VectorAssembler`. O README inclui um vídeo de demonstração. Pontos negativos: sem `requirements.txt` ou instruções de configuração do ambiente Databricks; os notebooks só funcionam em Databricks (com os volumes montados), tornando o projeto não-reproduzível fora desse ambiente; sem testes; commits com mensagens genéricas.

---

## 🎯 Nota Final

**4.0 / 10**

O projeto demonstra excelente maturidade em engenharia de dados — a escolha do PySpark, a arquitetura Medallion e o uso de Spark ML Pipeline são diferenciais técnicos genuínos. No entanto, esses pontos positivos são completamente ofuscados pelo data leakage que permeia toda a modelagem supervisionada e pelo target mal definido. Um modelo que usa ARRIVAL_DELAY (parte da própria variável alvo) como feature não aprende a prever atrasos — aprende a fazer aritmética sobre o próprio label. O AUC de 0.83 não representa nenhuma capacidade preditiva real.

Uma reformulação que: (1) restrinja as features apenas a informações disponíveis antes da partida (MONTH, DAY_OF_WEEK, SCHEDULED_DEPARTURE, DISTANCE, AIRLINE, ORIGIN, DESTINATION); (2) corrija o target para ARRIVAL_DELAY ≥ 15 min; (3) calcule o target encoding de rotas apenas no conjunto de treino; e (4) adicione análise crítica dos resultados — transformaria este projeto de 4.0 para facilmente 7.5+, dado o diferencial técnico da infraestrutura já implementada.
