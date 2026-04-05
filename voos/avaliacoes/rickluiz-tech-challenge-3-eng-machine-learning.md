# Avaliação Acadêmica — FIAP EML Tech Challenge Fase 3: Atrasos de Voos

**Repositório avaliado:** [RickLuiz/Tech-Challenge---3---Eng.-Machine-Learning](https://github.com/RickLuiz/Tech-Challenge---3---Eng.-Machine-Learning)  
**Data de avaliação:** 2026-04-02  
**Avaliador:** Copilot (agente automatizado)

---

## 📝 Avaliação Geral

O projeto apresenta uma estrutura organizada (3 notebooks numerados + README detalhado) e executa com outputs visíveis, provando que o código foi efetivamente rodado. A EDA é razoável e apresenta insights relevantes, incluindo uma análise de atraso por período do dia (manhã/tarde/noite) que demonstra compreensão do efeito cumulativo dos atrasos. O ponto crítico e mais grave é a modelagem supervisionada: os dois primeiros modelos treinados (Regressão Logística e Random Forest sem ajuste de classes) **falham completamente** em identificar a classe de interesse (voos atrasados), obtendo Recall = 0 para a classe 1, e essa falha **não é reconhecida nem discutida** pelos autores — eles apenas imprimem os resultados e seguem em frente. O modelo final com `class_weight='balanced'` é marginalmente melhor (F1=0.36), mas ainda insatisfatório e sem iteração de melhoria. A modelagem não supervisionada usa K-Means com apenas 3 features, sem validação por Silhouette Score e com ausência de evidência de normalização, limitando a qualidade dos clusters.

---

## ✅ Pontos Positivos

1. **README claro e estruturado:** O README explica o objetivo do projeto, descreve cada um dos 3 notebooks com seus propósitos e processos, lista as tecnologias usadas, fornece instruções de execução e apresenta as principais conclusões do desafio em linguagem de negócio. É um dos READMEs mais completos entre os projetos avaliados neste desafio.

2. **Feature selection anti-leakage no modelo supervisionado:** As features escolhidas para o modelo de classificação (MONTH, DAY_OF_WEEK, AIRLINE_CODE, ORIGIN_AIRPORT, DESTINATION_AIRPORT, SCHEDULED_DEPARTURE, DISTANCE) são todas informações disponíveis antes do voo acontecer, demonstrando que os autores entenderam o problema de data leakage. Isso é correto do ponto de vista metodológico e diferencia o projeto de outros que incluem DEPARTURE_DELAY como preditor.

3. **Análise de atraso por período do dia:** O notebook de EDA inclui uma análise do atraso por faixa horária (manhã, tarde, noite) que identifica o efeito cumulativo dos atrasos ao longo do dia — voos noturnos são os mais afetados porque carregam os atrasos acumulados de toda a cadeia operacional. Este é um insight genuinamente útil para o negócio que vai além da análise padrão de dia da semana/mês.

---

## ❌ Pontos de Melhoria

1. **Falha completa dos dois primeiros modelos supervisionados sem reconhecimento ou discussão:** A Regressão Logística e o Random Forest (sem `class_weight`) obtêm Recall = 0 para a classe positiva (voos atrasados) — os modelos nunca preveem um atraso. Isso é uma falha crítica que deveria ser o ponto central de análise do notebook, levando à discussão sobre desbalanceamento de classes, suas causas e soluções. Em vez disso, os autores apenas imprimem o `classification_report` e imediatamente treinam o próximo modelo sem comentário algum. O Random Forest sem ajuste obteve Precision = 1.00 e Recall = 0.00 — um resultado que matematicamente demonstra que o modelo aprendeu a nunca prever atrasos — e isso não foi nem mencionado.

2. **Modelagem não supervisionada com apenas 3 features e sem normalização evidente:** O notebook 03 agrupa 533 aeroportos usando K-Means com apenas 3 métricas (total de voos, atraso médio, taxa de atraso). Outros atributos operacionalmente relevantes disponíveis no dataset (TAXI_OUT médio, DISTANCE média, distribuição por dia da semana) foram ignorados. Mais grave: o código importa `StandardScaler` mas não há evidência clara de que a normalização foi aplicada antes do KMeans — se as features foram usadas em escala bruta (TOTAL_VOOS em milhares vs TAXA_ATRASO entre 0 e 1), o KMeans terá sido dominado pela feature de maior variância, comprometendo a qualidade dos clusters. Além disso, não há Silhouette Score para validar a qualidade da separação.

3. **Ausência de análise crítica e conclusões consolidadas:** Não existe um notebook ou seção dedicada a comparar os modelos, discutir limitações, propor próximos passos ou responder às perguntas de negócio do rubric de forma estruturada. As conclusões críticas aparecem apenas no README em linguagem de negócio, mas sem profundidade técnica. Não há discussão sobre por que os modelos iniciais falharam, o que significam os clusters identificados para a operação aérea, ou quais melhorias concretas poderiam ser feitas (e.g., features de contexto histórico, modelos baseados em boosting, validação cruzada).

---

## 📊 Avaliação por Critério

### EDA: 7/10
O notebook de EDA carrega os 3 datasets (5.8M voos, companhias e aeroportos), realiza o merge e limpeza de forma correta, cria a variável alvo IS_DELAYED, e produz visualizações sobre atraso por companhia aérea, distribuição do ARRIVAL_DELAY, padrões por dia da semana, mês, período do dia e causas de atraso. A análise de período do dia (manhã/tarde/noite) demonstra um entendimento acima da média do problema. As principais conclusões são documentadas no final do notebook. A nota não é superior porque: (1) faltam análises por aeroporto de origem (quais são os mais críticos?) — que é uma pergunta explícita do rubric; (2) a tabela de correlação entre variáveis numéricas está presente mas não é discutida profundamente; (3) as perguntas de negócio do rubric não são respondidas de forma explícita e consolidada.

### Modelagem Supervisionada: 4/10
Feature selection correta (sem leakage). O notebook executa 3 versões do modelo: LR base, RF sem ajuste e RF com `class_weight='balanced'`. O resultado final (RF balanceado: Precision=0.25, Recall=0.63, F1=0.36 para classe 1) é melhor que os primeiros, mas ainda insatisfatório. A penalização severa vem de: (1) os dois primeiros modelos falham completamente (Recall=0) e isso **não é discutido** — uma falha crítica de análise; (2) nenhuma métrica de AUC-ROC foi computada; (3) o dataset tem 5.7M linhas mas apenas 500k foram usadas para modelagem, sem justificativa técnica (podia usar mais ou explicar por que não); (4) não há validação cruzada; (5) nenhum algoritmo de boosting foi testado; (6) não há discussão sobre o trade-off Precision/Recall ou sobre threshold customizado.

### Modelagem Não Supervisionada: 5/10
K-Means com Elbow Method para seleção de k (k=3), com interpretação dos clusters em linguagem de negócio. Os 3 clusters identificados (grandes hubs eficientes, aeroportos regionais pontuais, aeroportos com gargalos) são razoavelmente interpretáveis. A penalização vem de: (1) apenas 3 features utilizadas, deixando de lado informações operacionalmente relevantes disponíveis no próprio dataset; (2) ausência de evidência clara de normalização — crítico para KMeans, cujo resultado é sensível à escala das variáveis; (3) sem Silhouette Score para validação quantitativa da qualidade dos clusters; (4) sem PCA ou qualquer outra técnica de redução de dimensionalidade; (5) análise dos clusters superficial, sem visualização gráfica dos clusters (scatter plots) e sem identificação dos aeroportos mais representativos de cada grupo.

### Análise Crítica: 4/10
A análise crítica está dispersa e é superficial. O README apresenta conclusões de negócio concisas, mas não há reflexão técnica aprofundada. As falhas mais óbvias (Recall=0 nos primeiros modelos) não são mencionadas em lugar algum. Não há discussão de limitações do dataset (apenas 2015, apenas domésticos, ausência de dados de clima). Não há comparativo explícito entre modelos com tabela de métricas. Não há próximos passos propostos. A análise de feature importance do Random Forest (revelando SCHEDULED_DEPARTURE como a feature mais importante) é o único elemento de análise genuinamente interpretativo, mas não é aprofundado.

### Engenharia/Organização: 6/10
O projeto possui `.gitignore`, README detalhado, notebooks numerados com nomes descritivos, e um pipeline claro onde o notebook 01 gera um `.pkl` que é consumido pelos notebooks 02 e 03. As dependências (pandas, numpy, matplotlib, seaborn, scikit-learn) são listas no README. Pontos negativos: sem `requirements.txt` formal com versões pinadas; 6 commits com mensagens genéricas ("first commit", "deploy" x4, "readme"), sem histórico de desenvolvimento iterativo; aparentemente apenas 1 contribuidor ativo (Henrique Capristano), diferente do dono do repositório (RickLuiz); sem instruções sobre como criar o ambiente virtual.

---

## 🎯 Nota Final

**5.5 / 10**

O projeto demonstra organização básica e um bom entendimento do problema de negócio, especialmente no README e na EDA. No entanto, a modelagem supervisionada tem problemas críticos que não são reconhecidos nem discutidos — dois modelos que falham completamente em prever a classe de interesse deveriam ser o ponto de partida para uma análise aprofundada sobre desbalanceamento de classes, não apenas algo para "superar" adicionando `class_weight`. A modelagem não supervisionada, embora funcional, é superficial. A ausência de uma análise crítica estruturada e de uma discussão de limitações e próximos passos impede o projeto de se destacar. Com a adição de análise crítica aprofundada dos resultados, mais features na clusterização, e ao menos uma iteração adicional de melhoria dos modelos supervisionados, este projeto poderia alcançar facilmente 7.0+.
