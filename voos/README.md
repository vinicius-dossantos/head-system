# Dados de Voos — Pipeline de Ciência de Dados

Pipeline completo de ciência de dados aplicado a dados de voos, desenvolvido como Tech Challenge para o curso de Machine Learning Engineering.

## Estrutura do Projeto

```
voos/
├── data/               # Diretório para datasets (gerados pelos notebooks)
├── notebooks/
│   ├── 01_eda.ipynb                  # Análise Exploratória de Dados
│   ├── 02_supervised_modeling.ipynb  # Modelagem Supervisionada
│   └── 03_unsupervised_modeling.ipynb # Modelagem Não Supervisionada
├── src/
│   ├── __init__.py
│   ├── data_loader.py      # Geração e carregamento de dados
│   ├── preprocessing.py    # Pré-processamento e feature engineering
│   ├── models.py           # Treinamento e avaliação de modelos
│   └── visualization.py    # Funções de visualização
└── requirements.txt
```

## Objetivo

Construir um pipeline de análise de dados de voos que inclui:

1. **EDA** — estatísticas descritivas, tratamento de valores ausentes e geração de insights visuais
2. **Modelagem Supervisionada** — classificação binária de atrasos (≥ 15 min) com comparação entre Regressão Logística e Random Forest
3. **Modelagem Não Supervisionada** — clusterização com K-Means e redução de dimensionalidade com PCA

## Dados

Os dados são gerados sinteticamente dentro dos notebooks para garantir reproducibilidade sem dependência de fontes externas. O dataset simula operações reais de voos com:

- Companhias aéreas, rotas e distâncias
- Atrasos de partida e chegada
- Condições climáticas
- Padrões temporais (mês, dia da semana, hora)

## Como Executar

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar Jupyter
jupyter notebook notebooks/
```

Execute os notebooks na ordem numérica:
1. `01_eda.ipynb`
2. `02_supervised_modeling.ipynb`
3. `03_unsupervised_modeling.ipynb`

## Requisitos

- Python 3.10+
- Ver `requirements.txt` para as bibliotecas necessárias
