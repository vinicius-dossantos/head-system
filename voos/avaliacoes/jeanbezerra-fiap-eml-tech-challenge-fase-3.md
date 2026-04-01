# Avaliação Acadêmica — FIAP EML Tech Challenge Fase 3: Atrasos de Voos

**Repositório avaliado:** [jeanbezerra/fiap-eml-tech-challenge-fase-3](https://github.com/jeanbezerra/fiap-eml-tech-challenge-fase-3)  
**Data de avaliação:** 2026-04-01  
**Avaliador:** Copilot (agente automatizado)

---

## 📝 Avaliação Geral

O trabalho se destaca como o melhor exemplo de **engenharia de ML** entre os projetos avaliados neste desafio. A estrutura de pastas, a automação do pipeline completo (download → normalização → curadoria → features → modelagem), o logging de auditoria com ISO 8601, a detecção de drift com KS-Test e PSI, e o cálculo de VIF são práticas de produção raras em trabalhos acadêmicos. A grande fraqueza — e penalização significativa — é a **ausência completa da modelagem não supervisionada**, que é um requisito mínimo explícito do desafio. O desempenho dos modelos supervisionados também permanece fraco (Random Forest com overfitting severo não resolvido), mas os mecanismos de diagnóstico automático que o projeto implementa reconhecem e documentam esses problemas com clareza.

---

## ✅ Pontos Positivos

1. **Pipeline de produção end-to-end automatizado:** O projeto implementa um pipeline completo e reprodutível em Python puro, com camadas explícitas de dados (`raw → normalized → curated → features`), scripts modularizados por responsabilidade (`data-download`, `data-normalization`, `feature-engineering`, `modeling`), automação via `run.cmd`, e dados hospedados em AWS S3 público. Qualquer pessoa pode reproduzir o projeto do zero com um único comando.

2. **MLOps avançado com auditoria, drift e multicolinearidade:** O script `flights-modeling.py` implementa, além das métricas padrão, diagnóstico automático de overfitting/underfitting, OOB Score, cálculo de VIF para multicolinearidade, KS-Test e PSI para drift entre treino e teste, e Isolation Forest para anomalias. Os logs de auditoria com timestamp ISO 8601 foram efetivamente executados e commitados no repositório, provando que o pipeline funciona.

3. **Feature engineering anti-leakage rigorosa:** O script `build_features.py` define explicitamente uma lista `LEAKAGE_COLUMNS` (19 colunas pós-voo removidas) e implementa `AIRLINE_HIST_DELAY_RATE` e `ROUTE_HIST_DELAY_RATE` via cumulative sum temporal (sem leakage), codificação cíclica de horários com sin/cos, `PERIOD_OF_DAY`, e `IS_WEEKEND` — demonstrando domínio sólido de boas práticas em feature engineering para séries temporais.

---

## ❌ Pontos de Melhoria

1. **Modelagem não supervisionada completamente ausente:** O rubric exige explicitamente "mínimo uma abordagem" de aprendizado não supervisionado (clusterização ou redução de dimensionalidade). Não existe nenhum notebook, script ou saída de K-Means, PCA, DBSCAN ou qualquer outra técnica no repositório. Este é o gap mais crítico e impacta fortemente a nota.

2. **Overfitting severo do Random Forest não resolvido:** O log de auditoria registra `Gap_F1=0.6839` (treino F1=0.997, teste F1=0.31), diagnóstico `OVERFITTING`, e dois alertas automáticos. Apesar do diagnóstico correto, nenhuma iteração de melhoria foi realizada (regularização, limitação de profundidade, subsampling, GridSearch). O modelo final entregue à produção seria a Regressão Logística com F1=0.33 — desempenho insatisfatório para o negócio.

3. **Perguntas do rubric não respondidas explicitamente nos notebooks:** O rubric lista perguntas de negócio concretas (quais aeroportos são mais críticos? atrasos são mais comuns em certos dias da semana?). Os notebooks de EDA realizam análise descritiva, mas não apresentam conclusões explícitas respondendo essas perguntas de forma consolidada e orientada ao negócio.

---

## 📊 Avaliação por Critério

### EDA: 8/10
O projeto possui 4 notebooks de EDA (`0_data_normalization_check`, `1_EDA`, `2_EDA`, `3_EDA`) que demonstram análise rigorosa. O notebook `0` valida a normalização. Os notebooks `1–3` cobrem distribuições, análise temporal, padrões por companhia e aeroporto, e análise regional. O README documenta o dicionário de dados completo com 31 variáveis. A ausência de mapas geográficos, análise sazonal explícita, e respostas diretas às perguntas do rubric impedem a nota máxima.

### Modelagem Supervisionada: 7/10
Dois algoritmos foram comparados (Logistic Regression + Random Forest), com `class_weight='balanced'`, threshold customizado (0.30), estratificação no split, e OOB score. O audit log prova execução real com 5,3M de linhas. A penalização vem do overfitting severo do RF (Gap=0.68) não tratado, ausência de algoritmos baseados em boosting (que teriam performance superior neste dataset), e F1 final de 0.33 (LR) / 0.31 (RF) — ambos insatisfatórios. Nenhum GridSearch ou ajuste de hiperparâmetros foi realizado.

### Modelagem Não Supervisionada: 2/10
**Requisito não atendido.** Não existe nenhuma evidência de modelagem não supervisionada no repositório — nenhum notebook, nenhum script, nenhuma saída ou log. A nota mínima (2) reconhece que a infraestrutura de dados criada no projeto seria perfeitamente adequada para realizar K-Means em aeroportos ou PCA nas features, mas isso não foi executado.

### Análise Crítica: 8/10
Este é um ponto forte. Os logs de auditoria implementam automaticamente: diagnóstico de overfitting/underfitting com `Gap_F1`, alertas de recall baixo, VIF com classificação HIGH/MODERATE/LOW, KS-Test com status DRIFT/STABLE, PSI com classificação HIGH_DRIFT/MODERATE_DRIFT/LOW_DRIFT, e Isolation Forest com status de anomalia. O README explica em linguagem de negócio o que cada métrica significa e como agir em cada cenário. A penalização é pela ausência de análise crítica narrativa no formato de notebook (os insights ficam espalhados em logs técnicos), e pela falta de discussão sobre por que os modelos falharam e quais melhorias seriam priorizadas.

### Engenharia/Organização: 10/10
Nota máxima. O projeto entrega:
- `requirements.txt` com versões pinadas para 14 dependências
- `.gitignore` bem configurado (exclui dados, modelos, `.venv`, cache)
- Dados hospedados em AWS S3 público (não no repositório)
- Estrutura de pastas clara por camada e por responsabilidade
- `run.cmd` para automação do pipeline completo no Windows
- `run_to_modeling.cmd` para execução parcial até a modelagem
- `data/README.md` com dicionário de dados completo
- `ide/README.md` com instruções de configuração do ambiente
- Logs de auditoria com ISO 8601 commitados como evidência de execução
- Contribuição de múltiplos membros do time via branches e PRs

---

## 🎯 Nota Final

**7.0 / 10**

O projeto entrega engenharia de nível profissional que supera qualquer outro trabalho avaliado neste desafio. No entanto, a ausência da modelagem não supervisionada — um requisito mínimo explícito do rubric — e o desempenho insatisfatório dos modelos supervisionados sem iteração de melhoria limitam a nota. Se a modelagem não supervisionada fosse entregue e o Random Forest tivesse ao menos uma iteração de regularização, este projeto alcançaria facilmente 9.0+.
