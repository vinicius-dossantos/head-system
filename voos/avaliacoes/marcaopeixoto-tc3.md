# Avaliação Acadêmica — FIAP EML Tech Challenge Fase 3: Atrasos de Voos

**Repositório avaliado:** [MarcaoPeixoto/TC3](https://github.com/MarcaoPeixoto/TC3)  
**Data de avaliação:** 2026-04-02  
**Avaliador:** Copilot (agente automatizado)

---

## 📝 Avaliação Geral

O projeto entrega os três pilares solicitados (EDA, modelagem supervisionada e não supervisionada) com código que roda completamente, resultados visíveis nos outputs dos notebooks e uma estrutura limpa. Há pontos criativos genuínos: o uso de **MiniBatchKMeans** para lidar eficientemente com 4.6M de linhas, a **codificação cíclica (sin/cos)** de horários em minutos para a regressão Ridge e para o clustering, e a aplicação correta de `StandardScaler` no modelo não supervisionado. Contudo, o projeto é gravemente comprometido por um problema de **data leakage** que permeia toda a modelagem supervisionada e parcialmente a não supervisionada: as features utilizadas incluem variáveis medidas apenas durante ou após o voo (DEPARTURE_DELAY, TAXI_OUT, WHEELS_OFF, ELAPSED_TIME, AIR_TIME, WHEELS_ON, TAXI_IN), tornando trivial a tarefa de classificação e inflando artificialmente as métricas. Adicionalmente, a variável alvo BOL_DELAYED foi definida com um limiar não convencional (ARRIVAL_DELAY > 0 minutos, ao invés dos 15 minutos padrão da aviação civil). Esses dois erros metodológicos fundamentais, associados à remoção de todas as features categóricas pré-voo (AIRLINE, ORIGIN_AIRPORT, DESTINATION_AIRPORT, MONTH, DAY_OF_WEEK) que seriam as mais úteis numa predição real, comprometem substancialmente a validade dos resultados.

---

## ✅ Pontos Positivos

1. **MiniBatchKMeans e codificação cíclica de horários:** O notebook de clustering usa `MiniBatchKMeans`, escolha tecnicamente correta para um dataset de 4.6M linhas (drasticamente mais rápido que o KMeans convencional sem perda significativa de qualidade). A codificação sin/cos para converter horários HHMM em representação cíclica (para que 2359 seja "próximo" de 0000) é uma técnica de engenharia de features sofisticada e bem-aplicada, especialmente num modelo linear como RidgeCV. Isso demonstra conhecimento acima da média de engenharia de features temporais.

2. **Pipeline de limpeza de dados correto e bem documentado:** O notebook de EDA remove corretamente os voos cancelados antes de qualquer análise (justificando que ARRIVAL_DELAY é NaN para voos cancelados), examina as colunas de causa de atraso para entender sua estrutura, e toma decisões documentadas sobre quais colunas remover. O raciocínio de que "as colunas de causa de atraso só aparecem quando o voo está atrasado" é correto e bem verificado no código.

3. **Validação cruzada e `StandardScaler` aplicados:** O modelo KNN utiliza `cross_val_score` com 5 folds e split estratificado, demonstrando preocupação com a generalização do modelo. O RidgeCV com `cv=5` e busca de alpha via `np.logspace(-3, 3, 13)` mostra conhecimento de regularização. No notebook não supervisionado, `StandardScaler` é aplicado corretamente antes do KMeans (obrigatório para esse algoritmo, e ausente em vários outros projetos avaliados neste desafio).

---

## ❌ Pontos de Melhoria

1. **Data leakage severo em toda a modelagem supervisionada:** O dataset `flights_limpas.csv` usado nos modelos contém 12 colunas: SCHEDULED_DEPARTURE, **DEPARTURE_DELAY**, **TAXI_OUT**, **WHEELS_OFF**, **ELAPSED_TIME**, **AIR_TIME**, DISTANCE, **WHEELS_ON**, **TAXI_IN**, SCHEDULED_ARRIVAL, ARRIVAL_DELAY, BOL_DELAYED. As 7 features destacadas em negrito são informações que só existem *durante* ou *depois* que o voo acontece — nenhuma delas está disponível no momento em que se faz a previsão (antes do voo partir). DEPARTURE_DELAY sozinho é quase determinístico para prever ARRIVAL_DELAY: se o voo saiu atrasado, muito provavelmente chegará atrasado. As métricas do KNN (Accuracy 94%, F1 0.88) não refletem aprendizado genuíno de padrões preditivos, mas simplesmente exploração de informação que, na prática, seria impossível ter antes do evento.

2. **Remoção de todas as features categóricas pré-voo:** O processo de limpeza da EDA descarta AIRLINE, ORIGIN_AIRPORT, DESTINATION_AIRPORT, MONTH e DAY_OF_WEEK — precisamente as features que estariam disponíveis antes da partida e que têm maior valor preditivo real (diferentes companhias têm taxas de atraso muito distintas; diferentes rotas e dias da semana têm padrões históricos identificáveis). A análise da EDA até demonstra isso explicitamente (NK tem 29.15% de atraso, versus AS com ~13%), mas essa informação é descartada antes da modelagem. Um modelo real deveria **usar** essas features, não removê-las.

3. **Definição não convencional de BOL_DELAYED e ausência de análise crítica dos resultados:** A variável BOL_DELAYED é definida como ARRIVAL_DELAY > 0 (qualquer atraso positivo, mesmo de 1 minuto), enquanto a convenção da indústria de aviação civil dos EUA é ≥ 15 minutos. Isso não é discutido em lugar algum. No geral, os notebooks apresentam código e resultados, mas praticamente não há análise crítica: o F1 de 0.1872 no modelo não supervisionado (clustering) é apresentado sem qualquer comentário sobre sua inadequação, não há comparativo entre modelos, não há discussão de por que o R² do RidgeCV é 0.69 (baixo, mesmo com leakage), e não há menção ao aviso `LinAlgWarning: Ill-conditioned matrix` que aparece repetidamente no treinamento do RidgeCV, indicando multicolinearidade severa.

---

## 📊 Avaliação por Critério

### EDA: 5/10
O notebook de EDA carrega corretamente o dataset completo (5.8M linhas), remove voos cancelados com justificativa, analisa as colunas de causa de atraso, e produz tabelas de percentual de atraso por companhia e aeroporto (ex: NK com 29.15% de atraso vs. outras companhias). Há visualizações incluídas. A nota não é superior porque: (1) BOL_DELAYED é definido com limiar incorreto (>0 ao invés de ≥15 minutos); (2) todas as features categóricas informativas são descartadas sem justificativa técnica; (3) as colunas de causa de atraso (AIR_SYSTEM_DELAY, etc.) são removidas sem aproveitamento do insight que elas trazem; (4) não há análise temporal (por mês, hora do dia), correlação entre features, ou análise por aeroporto de origem/destino além das tabelas de frequência; (5) o insight gerado (NK é a companhia com maior taxa de atraso) não é utilizado na modelagem.

### Modelagem Supervisionada: 3/10
O projeto implementa corretamente duas tarefas: classificação (KNN) e regressão (RidgeCV). Há boas práticas técnicas: cross-validation, split estratificado, pipeline com StandardScaler para o Ridge, busca automática de alpha. A codificação cíclica de horários é um diferencial técnico positivo. Contudo, a nota é severamente penalizada pelo data leakage: as features incluem DEPARTURE_DELAY e todas as variáveis operacionais pós-partida, tornando a tarefa trivialmente solucionável por qualquer modelo. A F1=0.88 do KNN não é um resultado válido porque não representa capacidade preditiva real. O R²=0.69 do RidgeCV é, curiosamente, modesto mesmo com leakage — o que indica multicolinearidade severa (confirmada pelos avisos LinAlgWarning) que o modelo não consegue resolver. Nada disso é discutido.

### Modelagem Não Supervisionada: 5/10
O notebook usa MiniBatchKMeans (k=10) com normalização via StandardScaler, codificação cíclica e um threshold baseado na taxa de atraso por cluster para classificação. O resultado (F1=0.1872 para classe 1) é consistente com o esperado para um método não supervisionado: o clustering não consegue separar bem atrasados de não-atrasados mesmo com features contaminadas por leakage (DEPARTURE_DELAY ainda está presente aqui). A nota é moderada porque: (1) não há Elbow Method nem Silhouette Score para justificar k=10; (2) os clusters não são interpretados (quem são os voos no cluster 2 com 74.9% de atraso? Qual padrão eles representam?); (3) não há visualização dos clusters; (4) ainda inclui features de leakage. O balanced accuracy de 0.5476 (ligeiramente acima do chance level de 0.5) mostra que o clustering mal supera uma classificação aleatória para o problema de interesse.

### Análise Crítica: 3/10
A análise crítica é quase inexistente. O README apresenta os resultados principais de forma concisa (KNN: Accuracy 0.9425, F1 0.88; Ridge: MAE 4.39, R² 0.69; KMeans: Accuracy 0.7703, F1 0.1872) e conclui que "modelos supervisionados tiveram melhor desempenho para previsão de atraso". Não há: discussão do data leakage (o principal problema), comparativo técnico detalhado entre modelos, análise de limitações, interpretação dos clusters, discussão do porquê das métricas obtidas, ou proposta de próximos passos. Os avisos do RidgeCV (LinAlgWarning) são completamente ignorados. A observação sobre "BOL_DELAYED" não é justificada em nenhum lugar.

### Engenharia/Organização: 4/10
Ponto positivo: o dataset `flights.csv` (25MB) está incluído na pasta `data/`, tornando o projeto reproduzível sem dependências externas. O README tem estrutura clara. Ponto negativo: apenas 3 commits com mensagens genéricas ("Initial commit", "Add files via upload" ×2) — o projeto foi criado diretamente via upload no GitHub, sem histórico de desenvolvimento iterativo. Não há `requirements.txt`, os notebooks não são numerados (a ordem de execução está apenas no README), e não há evidência de que o fluxo `exploracao.ipynb → flights_limpas.csv → supervisionado.ipynb` esteja automatizado ou documentado na forma de dependência explícita.

---

## 🎯 Nota Final

**4.5 / 10**

O projeto demonstra domínio técnico em algumas áreas específicas (MiniBatchKMeans, codificação cíclica, RidgeCV com pipeline), mas é comprometido por um data leakage que invalida todos os resultados supervisionados. Ironicamente, o projeto realizou uma análise exploratória que **demonstra** quais features pré-voo são informativas (taxa de atraso por companhia, por aeroporto), mas essas features foram descartadas antes da modelagem — e as features ilegítimas (pós-partida) foram mantidas. Uma reformulação que: (1) use apenas features pré-voo (MONTH, DAY_OF_WEEK, AIRLINE, ORIGIN, DESTINATION, SCHEDULED_DEPARTURE, DISTANCE); (2) corrija o limiar de BOL_DELAYED para ≥15 minutos; e (3) adicione análise crítica dos resultados — transformaria este projeto de 4.5 para facilmente 7.0+.
