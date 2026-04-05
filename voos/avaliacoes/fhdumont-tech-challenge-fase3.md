# Avaliação Acadêmica — FIAP EML Tech Challenge Fase 3: Atrasos de Voos

**Repositório avaliado:** [FHDumont/tech-challenge-fase3](https://github.com/FHDumont/tech-challenge-fase3)  
**Data de avaliação:** 2026-04-05  
**Avaliador:** Copilot (agente automatizado)

---

## 📝 Avaliação Geral

O projeto entrega um notebook único bem estruturado, rodado com sucesso sobre o dataset completo de 5,8M de registros (SAMPLE_SIZE = None), com outputs visíveis que comprovam a execução real. O ponto de partida é sólido: a variável alvo é corretamente definida como `ARRIVAL_DELAY > 15 min`, seguindo o padrão FAA/IATA, e o notebook cobre todas as etapas exigidas — EDA, classificação, regressão e clusterização + PCA.

O principal problema técnico é a inclusão de **DEPARTURE_DELAY como feature** nos modelos supervisionados. Tecnicamente, o atraso de partida é registrado quando o avião sai do portão — não antes do voo —, o que significa que o modelo não é utilizável como sistema de previsão pré-embarque. Mais importante: DEPARTURE_DELAY tem correlação muito alta com ARRIVAL_DELAY (r ≈ 0.95 em geral), tornando os resultados impressionantemente bons — R² = 0.89 na regressão, F1 = 0.80 na classificação — mas refletindo principalmente essa correlação, e não a capacidade genuína de capturar padrões do problema. O projeto não discute essa limitação de forma explícita.

Há também uma inconsistência interna: as Conclusões mencionam "uso de amostra (300k linhas)" mesmo que o notebook tenha sido efetivamente rodado com o dataset completo (5,8M linhas), indicando que esse texto foi copiado de uma execução anterior sem revisão.

A parte não supervisionada é o ponto mais forte do projeto: StandardScaler aplicado corretamente, Elbow Method + Silhouette Score para escolha do k, k=4 clusters, PCA com gráfico de variância explicada e projeção PC1×PC2 colorida por cluster — tudo correto e bem executado.

---

## ✅ Pontos Positivos

1. **Definição correta do target de classificação:** `DELAYED = (ARRIVAL_DELAY > 15).astype(int)` segue o padrão da aviação civil (FAA/IATA), diferenciando este projeto de outros que usam `ARRIVAL_DELAY > 0` ou targets compostos sem embasamento operacional. A taxa de voos atrasados (17,6%) também é reportada e está coerente com dados históricos de 2015.

2. **Modelagem duplamente supervisionada (classificação + regressão):** O projeto vai além do mínimo ao implementar não só a classificação ("vai atrasar?") como também a regressão ("quanto vai atrasar?"). Cada tarefa usa dois algoritmos distintos (Logistic Regression e Random Forest para classificação; Ridge e Random Forest Regressor para regressão), com métricas adequadas para cada caso (F1/ROC-AUC para classificação; MAE/RMSE/R² para regressão).

3. **Metodologia sólida na modelagem não supervisionada:** A clusterização de aeroportos usa features com sentido de negócio (atraso médio de partida, atraso médio de chegada, volume de voos, distância média), aplica `StandardScaler` corretamente antes do KMeans, usa tanto Elbow Method quanto Silhouette Score para escolha do k, e complementa com PCA (gráfico de variância explicada + projeção bidimensional com clusters coloridos). É a parte mais completa e metodologicamente rigorosa do projeto.

4. **Execução no dataset completo e code quality geral:** SAMPLE_SIZE = None, rodando em Apple Silicon com otimização de threads para NumPy/scikit-learn — o projeto foi testado com os 5,8M de registros reais, não apenas uma amostra. O código tem estilo consistente, imports organizados e células comentadas com blocos numerados.

---

## ❌ Pontos de Melhoria

1. **DEPARTURE_DELAY como feature — contexto de uso não definido e métricas infladas:** A feature mais importante dos modelos é DEPARTURE_DELAY, que está disponível apenas no momento em que o voo já saiu do portão (não antes da viagem). Isso cria dois problemas: (a) o caso de uso real do modelo nunca é discutido — é para previsão pré-embarque? para decisões em tempo real após a partida? (b) DEPARTURE_DELAY tem altíssima correlação com ARRIVAL_DELAY, o que explica mecanicamente os R² = 0.89 e F1 = 0.80, tornando as métricas enganosamente boas. Para um verdadeiro sistema pré-voo, as features devem se restringir ao que se sabe no momento da reserva ou do check-in (mês, dia, horário programado, aeroporto, companhia, distância). O projeto reconhece que DEPARTURE_DELAY é um "preditor forte" nas conclusões, mas não discute a implicação disso para a validade prática do modelo.

2. **Sem cross-validação e sem curva ROC:** O modelo é treinado e avaliado em um único split 75/25 (`train_test_split`), sem nenhuma forma de validação cruzada. Para um dataset de 4,3M de linhas (após limpeza), o custo computacional de um K-Fold seria gerenciável. Adicionalmente, as métricas de ROC-AUC são calculadas mas nunca visualizadas — a curva ROC e a curva de Precisão×Recall são ferramentas padrão em classificação binária desbalanceada (17.6% de positivos) e deveriam estar presentes.

3. **Label Encoding para variáveis de alta cardinalidade — sem discussão de alternativas:** Aeroportos (930 categorias distintas) e companhias aéreas (14) são codificados com `LabelEncoder`, atribuindo arbitrariamente 0–929 a aeroportos sem qualquer relação de ordem. O próprio projeto menciona nas Limitações que "Label encoding para aeroporto/companhia ignora ordem; One-Hot ou embeddings poderiam melhorar" — mas isso não é suficientemente explorado. Com 930 aeroportos, OneHot criaria 930 colunas, mas técnicas como Target Encoding (calculado corretamente, apenas no treino) resolveriam o problema sem criação de features dummy.

4. **Inconsistência nas conclusões sobre tamanho da amostra:** A seção de Limitações afirma "Uso de amostra (300k linhas) para tempo de execução; resultados podem variar no dataset completo", mas o Bloco 3 mostra claramente `SAMPLE_SIZE = None` com saída `Flights: (5819079, 31)`. O modelo foi efetivamente treinado com os 5,8M de registros, não com 300k. Esse texto é remanescente de uma versão anterior e foi esquecido na revisão final.

---

## 📊 Avaliação por Critério

### EDA: 7/10
O notebook define corretamente a variável alvo, reporta a taxa de atrasos (17,6%), analisa valores ausentes com percentuais e produz 5 visualizações: distribuição do ARRIVAL_DELAY, atraso por dia da semana, top 10 companhias por atraso, atraso mediano por mês, e scatter de distância vs. atraso. A análise de período do dia (`PERIOD_DAY`) é uma feature derivada inteligente. A nota não é superior porque: (1) falta análise dos aeroportos de origem — quais são os mais problemáticos? (2) sem matrix de correlação entre variáveis numéricas; (3) não há análise das colunas de causa de atraso (AIR_SYSTEM_DELAY, WEATHER_DELAY, AIRLINE_DELAY, etc.) que poderiam orientar a seleção de features; (4) a EDA não informa explicitamente as decisões de feature engineering da seção 4.

### Modelagem Supervisionada: 6/10
Cobre tanto classificação quanto regressão, com dois algoritmos cada, métricas adequadas para cada tarefa (incluindo ROC-AUC) e split estratificado. A nota é limitada por: (1) inclusão de DEPARTURE_DELAY nas features, que infla artificialmente todas as métricas — R² = 0.89 é excepcional para previsão de atraso de voo, mas é explicado principalmente pela correlação entre DEPARTURE_DELAY e ARRIVAL_DELAY; (2) sem validação cruzada; (3) sem visualização de curvas ROC/PR; (4) sem análise de feature importance para o Random Forest; (5) desbalanceamento de classes (17,6% de positivos) não é endereçado explicitamente — o Recall = 0.71–0.72 sugere que o modelo perde ~28% dos voos atrasados.

### Modelagem Não Supervisionada: 8/10
Ponto mais forte do projeto. Clusterização com 4 features relevantes, StandardScaler corretamente aplicado, Elbow Method + Silhouette Score para seleção de k, escolha de k=4 com justificativa visual, scatter plot de clusters (atraso médio vs. volume), PCA com gráfico de variância explicada e projeção PC1×PC2. A nota não é 9-10 porque: (1) os valores numéricos do Silhouette Score para cada k não são impressos em texto (apenas no gráfico), dificultando a comparação objetiva; (2) os clusters não são interpretados em detalhe — quais aeroportos pertencem a cada cluster? quais são as características médias de cada grupo?

### Análise Crítica: 7/10
Existe uma seção dedicada (Seção 7) com conclusões estruturadas, limitações listadas e próximos passos concretos (XGBoost, SMOTE, threshold ótimo, dashboard, validação temporal). A auto-crítica sobre label encoding e ausência de variáveis externas demonstra consciência das limitações. A nota é limitada por: (1) a limitação mais relevante — DEPARTURE_DELAY como feature — é mencionada apenas indiretamente ("DEPARTURE_DELAY e companhia/aeroporto são preditores fortes"), sem discussão do impacto no caso de uso real; (2) a inconsistência sobre o tamanho da amostra não foi identificada nem corrigida; (3) sem comparativo tabular entre os dois modelos de classificação e os dois de regressão com discussão das diferenças.

### Engenharia/Organização: 8/10
Notebook único com seções claramente numeradas (1–7), células comentadas com blocos numerados, `requirements.txt` com constraints de versão, README detalhado explicando estrutura e como executar, vídeo de apresentação disponível. Otimização de threads para NumPy/Apple Silicon mostra atenção a performance. A nota não é superior por: (1) `requirements.txt` usa `>=` sem versão máxima — uma dependência poderia mudar o comportamento em versões futuras; (2) a inconsistência texto/código nas conclusões indica falta de revisão final; (3) sem comentários explicando a motivação das escolhas de modelagem (por que max_depth=12? por que alpha=1.0?).

---

## 🎯 Nota Final

**7.2 / 10**

O projeto entrega um trabalho completo e executável, com acertos importantes: target correto, cobertura de classificação e regressão, e excelente metodologia de clusterização. A principal melhoria que teria maior impacto seria remover DEPARTURE_DELAY das features e redefinir o problema como previsão pré-embarque — isso exigiria repensar o feature engineering e provavelmente resultaria em métricas mais modestas mas genuinamente preditivas. Com essa mudança e a adição de cross-validação e curvas ROC, este projeto facilmente alcançaria 8.5+, dada a qualidade geral da implementação.
