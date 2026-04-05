# Avaliação Acadêmica — FIAP EML Tech Challenge Fase 3: Atrasos de Voos

**Repositório avaliado:** [arthurtcm/fiap-mlet-techchallenge3](https://github.com/arthurtcm/fiap-mlet-techchallenge3)  
**Data de avaliação:** 2026-04-05  
**Avaliador:** Copilot (agente automatizado)

---

## 📝 Avaliação Geral

O projeto entrega um notebook único (`tc3.ipynb`) com 10 células de código executadas sobre o dataset completo de voos de 2015. O maior acerto técnico do projeto é a ausência de data leakage nas features supervisionadas: o modelo usa apenas `MONTH`, `DAY_OF_WEEK`, `AIRLINE`, `ORIGIN_AIRPORT` e `DESTINATION_AIRPORT` — informações genuinamente disponíveis antes da partida. Isso contrasta positivamente com outros projetos do mesmo desafio que incluem `DEPARTURE_DELAY` e inflam artificialmente as métricas.

No entanto, o projeto tem duas falhas críticas não identificadas nem discutidas: (1) a **Regressão Logística produz um classificador degenerado** — prevê **100% das observações como "Não Atrasado"** (Confusion Matrix: 959.170 TN, 204.646 FN, 0 TP, 0 FP), sem que isso seja percebido ou comentado. O modelo responde ao desbalanceamento de classes (82% negativos) fazendo a previsão trivial; (2) o **Random Forest "base"** tem Recall=0.06 para voos atrasados (identifica apenas 6% dos atrasos), o que o torna praticamente inútil na prática, mas também não é discutido. Apenas o Random Forest com `class_weight='balanced'` (terceira versão) alcança resultados minimamente aceitáveis (Recall=0.62), com Precision baixa (0.24).

A parte não supervisionada é o ponto mais forte: dois agrupamentos independentes (por companhia e por aeroporto) com Elbow Method, Silhouette Score e interpretação detalhada dos clusters. A organização do projeto, porém, é muito precária: sem README, sem requirements.txt, sem células de markdown para estruturar a narrativa, e com avisos de deprecação no código não tratados.

---

## ✅ Pontos Positivos

1. **Features supervisionadas sem data leakage:** O modelo de classificação usa exclusivamente `MONTH`, `DAY_OF_WEEK`, `AIRLINE`, `ORIGIN_AIRPORT` e `DESTINATION_AIRPORT` — todas variáveis disponíveis no momento da reserva ou do check-in. Isso representa a escolha metodologicamente correta: o modelo está fazendo previsão pré-voo, não retroativamente. Nenhuma coluna operacional pós-partida (DEPARTURE_DELAY, TAXI_OUT, ELAPSED_TIME etc.) foi incluída.

2. **Dois agrupamentos distintos na análise não supervisionada:** O projeto implementa clusterização separada para companhias aéreas (14 objetos, k=3) e para aeroportos de origem (301 objetos com >1000 voos, k=3). A escolha de criar entidades com métricas de negócio (taxa de atraso, taxa de cancelamento, volume de voos, distância média) é uma abordagem madura, e a interpretação final dos clusters inclui a listagem das companhias e aeroportos de cada grupo, tornando os resultados acionáveis.

3. **Uso correto de Elbow Method + Silhouette Score:** Para ambos os agrupamentos, o notebook calcula inércia e Silhouette Score para k de 2 a 7, visualiza as curvas e justifica a escolha do k antes de treinar o modelo final. Esse processo é exatamente o esperado para seleção de hiperparâmetro em KMeans.

4. **Target correto e variável combinada delay+cancel:** `is_delayed = (ARRIVAL_DELAY > 15)` segue o padrão FAA/IATA, e a criação de `delay_plus_cancel = is_delayed | is_cancelled` como métrica auxiliar é uma decisão de negócio interessante: reflete o impacto real para o passageiro, que enfrenta tanto atrasos quanto cancelamentos.

5. **Reconhecimento do desbalanceamento de classes:** A tentativa de corrigir o desbalanceamento com `class_weight='balanced'` na versão aprimorada do Random Forest demonstra que o problema foi identificado. O estudante percebeu que a Accuracy isolada é uma métrica enganosa e tentou melhorar o Recall para a classe minoritária.

---

## ❌ Pontos de Melhoria

1. **Regressão Logística completamente degenerada — não identificada:** A Confusion Matrix da Regressão Logística mostra `[[959170, 0], [204646, 0]]` — o modelo classifica 100% dos exemplos como "Não Atrasado" e tem Precision=0.00, Recall=0.00, F1=0.00 para a classe positiva. O aviso `UndefinedMetricWarning: Precision is ill-defined` aparece no output, mas não há nenhuma análise ou comentário sobre esse resultado. Incluir um modelo completamente degenerado como segunda "alternativa" no relatório final, sem discutir por que ele falhou e o que isso significa, é uma lacuna crítica de análise.

2. **Ausência total de uma tarefa de regressão:** O desafio pede tanto classificação ("vai atrasar?") quanto regressão ("quanto vai atrasar?"). O projeto implementa apenas classificação. Uma tarefa de regressão com `ARRIVAL_DELAY` como target contínuo (Ridge, Lasso ou Random Forest Regressor com MAE/RMSE/R²) completaria o escopo e forneceria insights adicionais sobre a magnitude dos atrasos.

3. **EDA sem análise descritiva básica:** O notebook não apresenta `flights.shape`, `flights.describe()`, análise de valores ausentes nem a distribuição de `ARRIVAL_DELAY`. Os dados são carregados com um DtypeWarning sobre colunas (7, 8) com tipos mistos — o que indica problema na leitura do CSV — sem que isso seja investigado. A EDA começa diretamente nas visualizações sem caracterizar minimamente o dataset (5,8M de linhas, 31 colunas, taxa de atrasos).

4. **Sem PCA e sem análise de correlação:** A redução de dimensionalidade com PCA é esperada no componente não supervisionado e não foi implementada. Adicionalmente, não há matriz de correlação entre as variáveis numéricas — o que seria particularmente útil para entender, por exemplo, a relação entre `DEPARTURE_DELAY` e `ARRIVAL_DELAY` (mesmo que DEPARTURE_DELAY não seja usada nos modelos, entender a correlação entre as variáveis orienta a análise).

5. **Organização muito precária — sem README, sem estrutura de markdown:** O notebook tem 10 células, todas de código, sem nenhuma célula de markdown para nomear seções, contextualizar objetivos ou interpretar resultados entre as análises. Não há README no repositório (só o notebook e a pasta `bases/`). Não há `requirements.txt`. Essa ausência de estrutura narrativa torna o projeto difícil de avaliar e demonstra pouca atenção à comunicação dos resultados.

---

## 📊 Avaliação por Critério

### EDA: 5/10
O notebook define corretamente o target (`is_delayed = ARRIVAL_DELAY > 15`), cria a variável auxiliar `delay_plus_cancel` e enriquece os dados com nomes de companhias e estados dos aeroportos. Produz 8 visualizações distribuídas em duas figuras 2×2: volume de voos por aeroporto no tempo, timeline mensal de atrasos e cancelamentos, proporção de atrasos por companhia, tempo médio de atraso por companhia, percentual de atrasos+cancelamentos por companhia e por aeroporto, e total de voos por companhia e por aeroporto. Inclui análise de aeroportos, que é um requisito explícito do desafio. A nota não é superior porque: (1) não há `describe()` nem `shape` — o leitor não sabe o tamanho do dataset; (2) sem análise de valores ausentes; (3) sem distribuição do `ARRIVAL_DELAY`; (4) sem análise por dia da semana nem por hora do dia (os padrões temporais são fundamentais para previsão de atrasos); (5) sem matriz de correlação entre variáveis numéricas; (6) os insights da EDA não são conectados às decisões de feature engineering.

### Modelagem Supervisionada: 3/10
As features estão corretas (sem data leakage), o StandardScaler é aplicado, o split é 80/20, e há reconhecimento do desbalanceamento com `class_weight='balanced'`. Porém: (1) a Regressão Logística é completamente degenerada (Recall=0.00, prevê apenas a classe majoritária) e isso não é identificado nem discutido; (2) o Random Forest base tem Recall=0.06 para voos atrasados — identifica apenas 1 em 16 atrasos; (3) o Random Forest melhorado ainda tem Precision=0.24 (76% de falsos positivos); (4) sem tarefa de regressão; (5) sem curvas ROC/PR; (6) sem cross-validação; (7) sem feature importance; (8) sem análise comparativa das três versões do modelo nem justificativa para as escolhas de hiperparâmetros (max_depth=15, min_samples_split=50 etc.).

### Modelagem Não Supervisionada: 6/10
Ponto mais forte do projeto. Dois agrupamentos distintos (companhias e aeroportos) com features de negócio relevantes, StandardScaler corretamente aplicado antes do KMeans, Elbow Method e Silhouette Score para seleção do k, visualizações claras (elbow, silhouette, scatter) e interpretação detalhada dos clusters com rótulos de negócio ("HIGH-RISK", "HIGH-PERFORMANCE", "HIGH-TRAFFIC"). A nota não é 8+ porque: (1) sem PCA; (2) os aeroportos do Cluster 2 têm IDs numéricos (10140, 10299...) em vez de códigos IATA — indicando que parte dos aeroportos não fez merge com o arquivo `airports.csv` —, o que não é investigado; (3) a escolha de k=3 para companhias com apenas 14 objetos é discutível (com 14 pontos, k=3 significa 4–6 objetos por cluster); (4) o Silhouette Score numérico de cada k poderia ser explicitado em texto para facilitar a comparação objetiva.

### Análise Crítica: 2/10
Não há seção dedicada a conclusões, limitações ou próximos passos. A falha mais grave — a Regressão Logística prevendo 100% de negativos — passa completamente despercebida. O péssimo Recall=0.06 do Random Forest base não é comentado. Não há comparativo estruturado entre as três versões do classificador, nem resposta explícita à pergunta de negócio: "este modelo é útil para prever atrasos?". Os outputs são apresentados sem interpretação.

### Engenharia/Organização: 3/10
O notebook roda e produz outputs visíveis ✅. Há um vídeo de demonstração (`tech3.mp4`, 71MB) ✅. Mas: sem README; sem requirements.txt; sem células de markdown para estruturar o notebook; sem comentários explicando as escolhas de modelagem; DtypeWarning na leitura do CSV não tratado; warning de deprecação do Seaborn (`palette` sem `hue`) não tratado; todo o código em 10 células monolíticas sem separação clara de responsabilidades.

---

## 🎯 Nota Final

**4.0 / 10**

O projeto acerta em dois pontos importantes: features supervisionadas sem data leakage e análise de clusterização com metodologia adequada. No entanto, é prejudicado severamente pela ausência de análise crítica — a Regressão Logística que prevê 100% de negativos sem que isso seja notado é o sintoma mais claro de que os resultados não foram interpretados. A falta de regressão (metade do escopo supervisionado), de PCA, de README e de estrutura narrativa completam o quadro de um projeto executado mas não analisado.

Com três melhorias específicas o projeto alcançaria facilmente 7+: (1) identificar e discutir a falha da Regressão Logística, propondo soluções como SMOTE, ajuste de threshold ou algoritmos resistentes a desbalanceamento; (2) adicionar a tarefa de regressão com pelo menos um algoritmo e as métricas MAE/RMSE/R²; (3) estruturar o notebook com células de markdown, README e requirements.txt. A base técnica (target correto, features sem leakage, clusterização dupla) é sólida o suficiente para sustentar um trabalho muito melhor.
