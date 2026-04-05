# Avaliação Acadêmica — TechChallenge Fase 3: Atrasos de Voos

**Repositório avaliado:** [douglas-varjao/TechChallenge-Fase3-AtrasosVoos](https://github.com/douglas-varjao/TechChallenge-Fase3-AtrasosVoos/tree/main)  
**Data de avaliação:** 2026-04-01  
**Avaliador:** Copilot (agente automatizado)

---

## 📝 Avaliação Geral

O trabalho apresenta uma abordagem técnica sólida e bem estruturada para o problema de classificação de atrasos de voos domésticos dos EUA em 2015. O aluno demonstra domínio de técnicas avançadas de ML, incluindo modelos baseados em árvores (XGBoost, LightGBM), redes neurais (MLP) e análise de explicabilidade (SHAP). Destaca-se a integração inteligente entre a etapa não supervisionada (K-Means em aeroportos) e a supervisionada (feature `CLUSTER_AERO`), além da análise de erros com SHAP Waterfall. A principal deficiência do projeto está na organização de engenharia: ausência de `requirements.txt`, estrutura plana de arquivos, sem modularização do código e dependência de ambiente externo (Google Colab + Google Drive) para reprodução.

---

## ✅ Pontos Positivos

1. **Integração sofisticada entre aprendizado não supervisionado e supervisionado:** O resultado do K-Means (perfil de risco operacional de aeroportos) foi convertido em uma feature `CLUSTER_AERO` e injetado diretamente nos modelos preditivos, demonstrando pensamento sistêmico e domínio de domínio.

2. **Análise de erros orientada ao negócio com SHAP:** O projeto não para no F1-Score — vai além ao dissecar os falsos negativos com SHAP Waterfall Plots, identificando um padrão sistêmico específico (Delta Airlines no hub de Atlanta, ATL), entregando um diagnóstico concreto e acionável.

3. **Enriquecimento externo de dados com API de clima:** A integração da API Open-Meteo para adicionar variáveis meteorológicas reais de 2015 (`chuva_mm`, `vento_kmh`, `temperatura_max`) eleva consideravelmente a qualidade do dataset, indo além dos dados brutos disponíveis no Kaggle.

---

## ❌ Pontos de Melhoria

1. **Ausência de `requirements.txt` e gestão de ambiente:** O projeto não possui nenhum arquivo de dependências (pip, conda ou similar), tornando a reprodução do código dependente de tentativa e erro. Isso é uma falha grave de engenharia e prejudica diretamente a reprodutibilidade.

2. **Estrutura de repositório flat e ausência de modularização:** Todo o código está concentrado em dois notebooks Colab (`Tc3_Analise_exploratoria.ipynb` e `TechChallenge_Fase3_AtrasosVoos.ipynb`) sem separação em módulos Python reutilizáveis (ex: `preprocessing.py`, `models.py`). Isso dificulta manutenção, testes e colaboração.

3. **Reprodutibilidade limitada e dependência de ambiente proprietário:** Os dados originais estão hospedados no Google Drive pessoal do autor, exigindo que o avaliador recrie atalhos no próprio Drive. A execução é exclusivamente no Google Colab, sem opção local. Não há `.gitignore`, `Dockerfile` ou qualquer mecanismo alternativo de execução.

---

## 📊 Avaliação por Critério

### EDA: 8/10
O notebook de EDA (`Tc3_Analise_exploratoria.ipynb`, ~2,2 MB com outputs ricos) demonstra uma exploração cuidadosa dos dados. O README documenta as decisões de limpeza em formato tabular com justificativas de negócio (ex.: remoção de cancelados/desviados, tratamento de outliers > 600 min), o que evidencia pensamento analítico maduro. O feature engineering com médias móveis (`rolling(7)`), flags de feriados, contagem diária de voos e dados climáticos externos é exemplar. A ausência de visualizações acessíveis diretamente no repositório (apenas via Colab) e de análises estatísticas formais como testes de normalidade impedem a nota máxima.

### Modelagem Supervisionada: 9/10
A abordagem é robusta: três algoritmos comparados (XGBoost, LightGBM, MLP), tratamento explícito do desbalanceamento de classes (~18% de atrasos) com `stratify` e `scale_pos_weight`, ajuste de threshold (0.4) com justificativa orientada ao negócio (redução de falsos negativos), e uso de SHAP para explicabilidade global e local. O LightGBM foi escolhido com base em F1-Score e velocidade. A única ressalva é que as métricas completas (tabela comparativa de acurácia, precisão, recall, F1, AUC-ROC entre os três modelos) não são visíveis no README — apenas inferíveis pela narrativa.

### Modelagem Não Supervisionada: 9/10
Excelente execução. O K-Means foi aplicado em aeroportos usando métricas de causa de atraso, gerando 4 clusters com nomes de negócio interpretáveis (Eficientes, Críticos, Efeito Cascata, Sensíveis ao Clima). O PCA em 2D foi usado para validação visual da separação matemática. O ponto alto é a injeção do resultado como feature nos modelos supervisionados — uma decisão de design avançada que agrega valor real ao pipeline. A leve penalização se deve à ausência de análise de sensibilidade ao número de clusters (curva do cotovelo, silhouette score) explicitamente documentada.

### Análise Crítica: 9/10
A análise crítica é uma das partes mais fortes do trabalho. O autor identifica um padrão de falha sistêmica específico (falsos negativos concentrados na Delta Airlines no hub ATL), propõe três melhorias concretas e mensuráveis para próximas iterações (clima horário, clusterização dinâmica por estação, feature cruzada [Companhia + Aeroporto + Mês]), e fundamenta tudo com SHAP Waterfall. A nota não é 10 apenas porque a limitação sobre dados temporais (uso de dados de 2015 para um modelo que seria implantado no futuro) não é discutida.

### Engenharia/Organização: 5/10
Este é o ponto mais fraco do projeto. O repositório contém apenas três arquivos na raiz (dois notebooks + README), todos gerados via Google Colab ("Criado usando o Colab" em todas as mensagens de commit). Não há `requirements.txt`, `.gitignore`, estrutura de pastas organizada, módulos Python reutilizáveis ou testes. A reprodução depende inteiramente de acesso ao Google Drive do autor e ao ambiente Colab. O README é bem escrito e documenta o processo, mas isso não compensa a ausência de boas práticas de engenharia de software.

---

## 🎯 Nota Final

**7.8 / 10**

O projeto entrega conteúdo técnico de alta qualidade, com abordagem sofisticada que supera o mínimo exigido em EDA, modelagem supervisionada e não supervisionada, e análise crítica. A nota é penalizada significativamente pela engenharia e organização deficientes — ausência de requirements, estrutura plana, sem modularização e reprodutibilidade frágil — que são aspectos fundamentais de um Tech Challenge de Machine Learning Engineering.
