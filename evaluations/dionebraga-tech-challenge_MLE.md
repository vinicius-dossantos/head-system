# Avaliação — dionebraga/tech-challenge_MLE

**Repositório:** https://github.com/dionebraga/tech-challenge_MLE  
**Avaliado em:** 31/03/2026  
**Curso:** Pós-Graduação em Machine Learning Engineering — FIAP  
**Tema:** API RESTful de Livros com Web Scraping, Dashboard e Deploy em Produção  
**Equipe:** 1 colaborador (dionebraga) | 20 commits

---

## Nota Final: **72 / 90**

---

## Resumo Executivo

Projeto ambicioso e funcional. Trata-se de uma **API FastAPI completa** com scraping do site *Books to Scrape*, persistência em CSV/SQLite/PostgreSQL, dashboard HTML dinâmico com Plotly (4 tipos de gráficos + galeria de livros), e **deploy funcional no Render** documentado no README. A qualidade de execução e a profundidade das funcionalidades superam a maioria dos trabalhos avaliados nesta turma. Os principais pontos de penalização são: inconsistências internas entre camadas (modelos SQLAlchemy ativos mas API usando apenas CSV; `livros_repository.py` com imports absolutos quebrados); ausência de testes automatizados; e um segredo de banco de dados PostgreSQL commitado diretamente no README. O deploy em produção e o dashboard são diferencias positivos relevantes.

---

## Inventário do Repositório

| Arquivo / Pasta | Tamanho | Descrição |
|---|---|---|
| `tech_challenge_books_api/main.py` | 4,8 KB | Entry point FastAPI — bem estruturado |
| `tech_challenge_books_api/routers/scraping.py` | 5,0 KB | Scraping incremental (40 livros/run) |
| `tech_challenge_books_api/routers/relatorios.py` | 14,5 KB | Dashboard + 4 tipos de gráficos Plotly |
| `tech_challenge_books_api/routers/stats.py` | 4,3 KB | 3 endpoints de estatísticas |
| `tech_challenge_books_api/routers/livros.py` | 2,0 KB | CRUD de livros (via CSV) |
| `tech_challenge_books_api/routers/categorias.py` | 6,0 KB | CRUD de categorias + visualização HTML |
| `tech_challenge_books_api/routers/saude.py` | 0,35 KB | Healthcheck |
| `tech_challenge_books_api/infra/database.py` | 1,1 KB | Camada de dados (apenas CSV) |
| `tech_challenge_books_api/models/livro_model.py` | 0,67 KB | ORM SQLAlchemy (Livro) |
| `tech_challenge_books_api/models/categoria_model.py` | 0,26 KB | ORM SQLAlchemy (Categoria) |
| `tech_challenge_books_api/schemas/livro_schema.py` | 1,0 KB | Pydantic schemas (Livro) |
| `tech_challenge_books_api/schemas/schemas.py` | 0,67 KB | Schemas legados com `orm_mode` |
| `tech_challenge_books_api/repositories/livros_repository.py` | 1,25 KB | Repository (imports absolutos quebrados) |
| `tech_challenge_books_api/scripts/scraper_books.py` | 13,2 KB | Scraper standalone completo |
| `tech_challenge_books_api/scripts/scraping.py` | 3,1 KB | Scraper auxiliar |
| `tech_challenge_books_api/infra/books.db` | 57 KB | ❌ Banco SQLite binário commitado |
| `books.db` | 28 KB | ❌ Banco SQLite duplicado na raiz |
| `books.csv` | 18 KB | ✅ CSV de exemplo (dados reais de scraping) |
| `requirements.txt` | 0,85 KB | Dependências com versões fixas |
| `Procfile` | 79 B | Configuração Heroku-style |
| `tech_challenge_books_api/render.yaml` | 0,46 KB | Configuração Render |
| `BooksAPI.postman_collection.json` | 4,4 KB | Coleção Postman |
| `books_api_collection.json` | 11,7 KB | Coleção Postman ampliada |
| `links_tech_challenge_MLE.txt` | 0,55 KB | Links do projeto |
| `README.md` | 6,1 KB | Documentação completa |
| `TODO.md` | 0,44 KB | Checklist de tarefas concluídas |
| `.pylintrc` | 0,27 KB | Configuração do pylint |
| `pyrightconfig.json` | 0,56 KB | Configuração do Pyright |

---

## Estrutura e Arquitetura

```
tech_challenge_books_api/
├── main.py                       ✅ Entry point bem estruturado
├── index.html                    ✅ Página inicial customizada
├── infra/
│   ├── database.py               ✅ Abstração CSV
│   ├── books.db                  ❌ Binário commitado
│   └── data/                     ✅ Diretório de dados dinâmicos
├── routers/
│   ├── scraping.py               ✅ Scraping incremental
│   ├── relatorios.py             ✅ Dashboard Plotly (4 gráficos + galeria)
│   ├── stats.py                  ✅ 3 endpoints de estatísticas
│   ├── livros.py                 ✅ (modo CSV — CRUD parcial)
│   ├── categorias.py             ✅ Listagem + visualização HTML
│   └── saude.py                  ✅ Healthcheck
├── models/                       ⚠️ ORM definido mas não usado pela API
├── schemas/                      ⚠️ Dois arquivos de schema divergentes
├── repositories/                 ❌ Imports absolutos quebrados
└── scripts/
    ├── scraper_books.py          ✅ Scraper standalone (mais completo)
    └── scraping.py               ⚠️ Versão auxiliar (duplicação)
```

---

## Análise por Componente

### 1. Entry Point — `main.py`

**Pontos positivos:**
- Estrutura limpa com separação de responsabilidades
- Middleware CORS configurado (com comentário alertando para produção) ✅
- Scraping automático no startup via variável de ambiente `STARTUP_SCRAPING` ✅
- Página inicial com HTML customizado e fallback ✅
- Custom OpenAPI schema ✅

**Pontos de atenção:**
```python
@app.on_event("startup")
async def startup_scraping_auto():
```
⚠️ `@app.on_event("startup")` foi depreciado no FastAPI em favor de `lifespan`. Funciona mas gerará avisos no FastAPI ≥ 0.93.

```python
# 🌐 Middleware CORS
allow_origins=["*"]  # ⚠️ Permite qualquer origem
```
⚠️ `allow_origins=["*"]` combinado com `allow_credentials=True` causa erro no FastAPI/Starlette — credenciais e wildcard são mutuamente exclusivos.

---

### 2. Scraping — `routers/scraping.py`

**Pontos positivos:**
- Scraping **incremental** — não baixa livros já existentes no CSV ✅
- Controle de limite (40 livros/run) com early stopping ✅
- Tratamento de erros por página (try/except individual) ✅
- Codificação UTF-8-BOM no CSV (`utf-8-sig`) ✅
- Deduplicação final com `drop_duplicates(subset=["titulo"])` ✅

**Pontos de atenção:**
```python
for pagina in range(1, 51):
    ...
    detalhe = requests.get(link_livro, timeout=10)  # requisição síncrona dentro de router assíncrono
```
⚠️ Usando `requests.get` (síncrono) dentro de um endpoint FastAPI — correto funcionar mas bloqueia o event loop. Deveria usar `httpx.AsyncClient` ou `asyncio.to_thread`.

- Sem paginação nos endpoints GET de livros — retorna todos os livros de uma vez ❌
- Sem autenticação nos endpoints de scraping — qualquer pessoa pode disparar o scraping ❌

---

### 3. Dashboard — `routers/relatorios.py`

**Ponto mais forte do projeto.** Dashboard com:
- **4 tipos de gráficos Plotly**: barras por categoria, rating médio por categoria, boxplot de preços, scatter preço × rating ✅
- **Galeria de livros** com cards HTML por categoria ✅
- `include_plotlyjs="cdn"` apenas no primeiro gráfico (os demais usam `False`) — economiza banda ✅
- Tratamento de imagens quebradas com `onerror` no HTML ✅
- Função `_carregar_df()` centralizada com verificações de colunas ✅
- Limpeza de preço robusta (`_clean_price_series`) — trata `Â`, `£`, vírgula/ponto ✅

**Pontos de atenção:**
```python
fig_rat = px.bar(..., include_plotlyjs=False, full_html=False)  # Correto
```
✅ Evita duplicar o JS do Plotly.

```python
div_rat = pio.to_html(fig_rat, include_plotlyjs=False, full_html=False)
```
⚠️ Porém o HTML final não tem `<script src="cdn">` explícito para os gráficos com `include_plotlyjs=False` — funciona porque o primeiro gráfico carrega o CDN e os demais reutilizam.

- Dashboard não tem paginação na galeria — pode ser lento com muitos livros ❌
- Dashboard sem data de última atualização do scraping (apenas data de geração) ⚠️

---

### 4. Estatísticas — `routers/stats.py`

**Bom.** 3 endpoints distintos:
1. `/stats/summary` — contagem de livros e categorias
2. `/stats/categories` — preço médio e rating médio por categoria
3. `/stats/ratings` — distribuição de livros por nota

```python
warnings.filterwarnings("ignore", category=FutureWarning)
```
⚠️ Suprime warnings globalmente no módulo — melhor seria isolar no bloco específico.

```python
stats = (
    df["rating"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "rating", "rating": "quantidade"})
)
```
⚠️ `.rename(columns={"index": "rating", "rating": "quantidade"})` está incorreto no Pandas ≥ 2.0 — `value_counts().reset_index()` retorna colunas `["rating", "count"]`, não `["index", "rating"]`. Este bug não aparece porque há um `FutureWarning` suprimido.

---

### 5. Routers de Livros e Categorias

**`livros.py` — modo CSV explícito:**
```python
@router.post("/", summary="Criar Livro 🚫")
def criar_livro():
    raise HTTPException(status_code=405, detail="Criação de livro não permitida em modo CSV")
```
✅ Decisão arquitetural declarada explicitamente — endpoints retornam `405` com mensagem.

⚠️ `router = APIRouter(prefix="/api/v1/livros", tags=["📘 Livros"])` — o prefix `/api/v1` é definido aqui **e** em `main.py` (via `app.include_router(livros.router, prefix="/api/v1")`). Isso resulta no path duplicado `/api/v1/api/v1/livros`. **Bug de roteamento.**

**`categorias.py` — destaque positivo:**
- Detecção automática de base URL (Vercel/Render/local) via variável de ambiente ✅
- Visualização HTML com links para todos os gráficos ✅

---

### 6. Inconsistência de Camadas (Problema Estrutural)

O projeto tem **duas camadas de dados em conflito**:

| Camada | Status | Usada? |
|---|---|---|
| `infra/database.py` (CSV) | ✅ Funcional | ✅ Sim — toda a API usa esta camada |
| `models/` (SQLAlchemy ORM) | ✅ Definido | ❌ Não — nenhum router usa ORM |
| `repositories/` (Repository Pattern) | ❌ Imports quebrados | ❌ Não — imports absolutos sem pacote |
| `schemas/schemas.py` (`orm_mode=True`) | ⚠️ Legado Pydantic v1 | ❌ Não — não usado |

O `livros_repository.py` usa:
```python
from models.livro_model import Livro  # ❌ Import absoluto quebrado
from livro_schema import LivroCreate   # ❌ Import absoluto quebrado
```
Estes imports funcionariam apenas se executado como script standalone, não como módulo do pacote.

O `schemas/schemas.py` usa `orm_mode = True` (Pydantic v1) enquanto `schemas/livro_schema.py` corretamente usa `from_attributes = True` (Pydantic v2). Há duplicação com divergência de versão.

---

### 7. Segurança — Credencial em Código

⚠️ **Problema de segurança** no README.md:
```
DATABASE_URL = postgresql://tech_challenge_ofof_user:wgghZ0bq4vHQmjV3eAVIcJoDPLHU3Xfu@dpg-d45341bipnbc73b0idgg-a/tech_challenge_ofof
```
A senha do banco PostgreSQL (`wgghZ0bq4vHQmjV3eAVIcJoDPLHU3Xfu`) está em texto plano no repositório público. Isso é uma violação de segurança — a credencial deve ser revogada e substituída. Em produção, usar variáveis de ambiente (`.env`) e nunca commitá-las.

---

### 8. Testes Automatizados

❌ **Nenhum arquivo de teste encontrado** no repositório. O `TODO.md` lista apenas tarefas de configuração e imports. Ausência de `test_*.py` ou pasta `tests/`.

---

### 9. Deploy e Infraestrutura

**Pontos muito positivos:**
- Deploy funcional no **Render** ✅: `https://tech-challenge-mle.onrender.com/`
- `render.yaml` configurado corretamente (Python 3.13.5, `STARTUP_SCRAPING=true`) ✅
- `Procfile` presente para compatibilidade Heroku-style ✅
- **Duas coleções Postman** commitadas ✅
- `python-dotenv` no requirements, mas sem `.env.example` ❌

**Arquivos binários commitados — deveriam estar no `.gitignore`:**
- `tech_challenge_books_api/infra/books.db` (57 KB) ❌
- `books.db` na raiz (28 KB) ❌

---

## Critérios de Avaliação

### 1. Funcionalidades Implementadas (22/25)

| Funcionalidade | Status | Evidência |
|---|---|---|
| API RESTful com FastAPI | ✅ | 6 routers com prefixos distintos |
| Web Scraping | ✅ | Scraping incremental com BeautifulSoup, paginação, deduplicação |
| Persistência de dados | ✅ | CSV + SQLite (deploy usa PostgreSQL) |
| Dashboard HTML | ✅ | 4 gráficos Plotly + galeria de livros |
| Exportação CSV | ✅ | Endpoint `/api/v1/data/books.csv` via StaticFiles |
| Estatísticas | ✅ | 3 endpoints (`/stats/summary`, `/stats/categories`, `/stats/ratings`) |
| Swagger/Redoc | ✅ | Automático do FastAPI + custom OpenAPI |
| Healthcheck | ✅ | `/api/v1/saude/` |
| Deploy em produção | ✅ | Render funcional |
| Testes automatizados | ❌ | Ausentes |
| Autenticação | ❌ | Sem auth |
| Paginação | ❌ | GET /livros retorna tudo de uma vez |

---

### 2. Qualidade Técnica do Código (17/25)

| Item | Status | Detalhe |
|---|---|---|
| Estrutura modular (routers/models/schemas/repos) | ✅ | Separação clara de responsabilidades |
| FastAPI corretamente configurado | ✅ | Middlewares, mounts, routers |
| Tratamento de erros nos routers | ✅ | HTTPException com status codes corretos |
| Tratamento de erros no scraping | ✅ | try/except por página e por livro |
| Limpeza de dados robusta (preço/rating) | ✅ | `_clean_price_series()` trata encodings e formatos |
| Bug de prefix duplicado em `livros.py` | ❌ | `/api/v1/api/v1/livros` — rota nunca acessível |
| `requests` síncrono em handler FastAPI | ⚠️ | Bloqueia event loop |
| `allow_origins=["*"]` + `allow_credentials=True` | ❌ | Configuração inválida no Starlette |
| `@app.on_event("startup")` depreciado | ⚠️ | Funciona mas deve migrar para `lifespan` |
| ORM definido mas não usado | ⚠️ | Código morto nas camadas models/repositories |
| `orm_mode=True` (Pydantic v1) em `schemas.py` | ❌ | Incompatível com Pydantic v2 em uso |
| `livros_repository.py` com imports absolutos | ❌ | Não funciona como módulo do pacote |
| Bug no `stats_ratings()` (rename columns) | ❌ | Pandas ≥ 2.0: `rename(columns={"index": ...})` incorreto |
| `.pylintrc` e `pyrightconfig.json` presentes | ✅ | Configuração de linters |

---

### 3. Reprodutibilidade e Deploy (14/15)

| Item | Status | Detalhe |
|---|---|---|
| `requirements.txt` com versões fixas | ✅ | Todas as 40 dependências pinadas |
| Deploy funcional (Render) | ✅ | `https://tech-challenge-mle.onrender.com/` |
| `render.yaml` correto | ✅ | Python 3.13.5, startup scraping |
| `Procfile` | ✅ | Compatibilidade Heroku-style |
| Instruções de execução local no README | ✅ | Passo a passo completo |
| Link para dados / coleções Postman | ✅ | 2 coleções Postman commitadas + Google Drive |
| Arquivos `.db` commitados | ❌ | `books.db` (28KB + 57KB) no repositório |
| `.env.example` | ❌ | Ausente — apesar de `python-dotenv` no requirements |

---

### 4. Documentação (10/10)

| Item | Status | Detalhe |
|---|---|---|
| README estruturado | ✅ | Estrutura, instalação, endpoints, tecnologias |
| Swagger/Redoc automático | ✅ | FastAPI built-in + custom OpenAPI |
| Tabela de endpoints no README | ✅ | Livros e Categorias documentados |
| Arquitetura de dados documentada | ✅ | Diagrama ASCII no README |
| TODO.md com checklist concluído | ✅ | 8 itens todos marcados como concluídos |
| Diagrama de fluxo (ASCII) | ✅ | `Books.toscrape → Scraper → CSV/DB → FastAPI` |
| Comentários no código | ✅ | Todos os arquivos têm comentários adequados |
| Seção de próximos passos | ✅ | JWT, Streamlit, paginação, ML |

---

### 5. Segurança e Boas Práticas (9/15)

| Item | Status | Detalhe |
|---|---|---|
| `allow_origins=["*"]` | ⚠️ | Permitido com nota no código |
| **Senha PostgreSQL no README** | ❌ | **Violação grave — credencial pública** |
| `.db` binários commitados | ❌ | Devem estar no `.gitignore` |
| Sem autenticação nos endpoints de scraping | ❌ | Qualquer pessoa pode disparar scraping |
| `STARTUP_SCRAPING` via env var | ✅ | Boa prática — não hardcoded |
| `.gitignore` completo | ✅ | Exclui `.env`, `venv`, `__pycache__`, etc. |
| `python-dotenv` para variáveis de ambiente | ✅ | Presente no requirements |

---

## Resumo de Pontuação

| Critério | Obtido | Máximo |
|---|---|---|
| 1. Funcionalidades Implementadas | 22 | 25 |
| 2. Qualidade Técnica | 17 | 25 |
| 3. Reprodutibilidade e Deploy | 14 | 15 |
| 4. Documentação | 10 | 10 |
| 5. Segurança e Boas Práticas | 9 | 15 |
| **Total** | **72** | **90** |

---

## Inventário de Endpoints

| Método | Endpoint | Descrição | Funcional? |
|---|---|---|---|
| `GET` | `/` | Página inicial HTML | ✅ |
| `GET` | `/docs` | Swagger UI | ✅ |
| `GET` | `/redoc` | Redoc | ✅ |
| `GET` | `/api/v1/saude/` | Healthcheck | ✅ |
| `GET` | `/api/v1/scraping/run` | Executa scraping | ✅ |
| `GET` | `/api/v1/scraping/contagem` | Contagem livros/categorias | ✅ |
| `GET` | `/api/v1/stats/summary` | Resumo geral | ✅ |
| `GET` | `/api/v1/stats/categories` | Stats por categoria | ✅ |
| `GET` | `/api/v1/stats/ratings` | Stats por rating | ⚠️ bug rename |
| `GET` | `/api/v1/relatorios/pizza` | Gráfico pizza | ✅ |
| `GET` | `/api/v1/relatorios/barras` | Gráfico barras | ✅ |
| `GET` | `/api/v1/relatorios/histograma` | Histograma preços | ✅ |
| `GET` | `/api/v1/relatorios/treemap` | Treemap categoria/rating | ✅ |
| `GET` | `/api/v1/relatorios/dashboard` | Dashboard completo | ✅ |
| `GET` | `/api/v1/livros/` | Listar livros | ⚠️ bug prefix |
| `GET` | `/api/v1/livros/{id}` | Buscar por ID | ⚠️ bug prefix |
| `GET` | `/api/v1/livros/search/{titulo}` | Buscar por título | ⚠️ bug prefix |
| `GET` | `/api/v1/categorias/` | Listar categorias | ✅ |
| `GET` | `/api/v1/categorias/visualizar` | Visualização HTML | ✅ |
| `GET` | `/api/v1/data/books.csv` | Download CSV | ✅ |

---

## Pontos Positivos

1. **Deploy funcional em produção** — Render com PostgreSQL, auto-deploy configurado
2. **Dashboard mais rico da turma** — 4 gráficos Plotly interativos + galeria com cards e imagens
3. **Scraping incremental** — não baixa livros duplicados, controle de limite e early stopping
4. **`requirements.txt` completo com versões fixas** — 40 dependências pinadas
5. **Documentação exemplar** — README com estrutura, endpoints, diagrama, próximos passos
6. **2 coleções Postman** commitadas para facilitar testes manuais
7. **Tratamento robusto de encoding** no preço (`£`, `Â`, virgula/ponto)
8. **Detecção automática de base URL** (Vercel/Render/local) nas páginas HTML
9. **Linters configurados** (`.pylintrc` + `pyrightconfig.json`)
10. **TODO.md** com checklist rastreável

## Oportunidades de Melhoria

1. 🔴 **Revogar e remover a senha PostgreSQL do README** — credencial pública é violação de segurança
2. 🔴 **Corrigir o bug de prefix duplo** em `livros.py` — `prefix="/api/v1/livros"` conflita com `main.py`
3. 🔴 **Corrigir imports em `livros_repository.py`** — usar imports relativos para funcionar como módulo
4. 🟠 **Adicionar `.db` ao `.gitignore`** — remover binários SQLite do repositório
5. 🟠 **Corrigir `allow_origins=["*"]` + `allow_credentials=True`** — configuração inválida no Starlette
6. 🟠 **Migrar `@app.on_event("startup")` para `lifespan`** — API depreciada no FastAPI moderno
7. 🟠 **Corrigir bug em `stats_ratings()`** — `rename(columns={"index": "rating"})` incorreto no Pandas ≥ 2.0
8. 🟠 **Adicionar testes automatizados** — ao menos testes de endpoints principais com `TestClient`
9. 🟡 **Usar `httpx.AsyncClient`** no scraping em vez de `requests` síncrono
10. 🟡 **Adicionar paginação** no endpoint `/livros/`
11. 🟡 **Escolher uma camada de dados** — ORM SQLAlchemy ou CSV; eliminar código morto
12. 🟡 **Unificar schemas** — remover `schemas/schemas.py` legado (Pydantic v1 `orm_mode`)
13. 🟡 **Adicionar `.env.example`** para documentar variáveis de ambiente esperadas

---

## Conclusão

O projeto `dionebraga/tech-challenge_MLE` representa o trabalho mais maduro em termos de arquitetura de software avaliado nesta turma. O deploy funcional no Render, a qualidade do dashboard Plotly, o scraping incremental e a documentação detalhada demonstram um nível técnico acima da média. As penalizações são principalmente por inconsistências internas entre camadas (ORM vs CSV), bugs pontuais de roteamento e configuração, ausência de testes e — o ponto mais crítico — credencial de banco de dados exposta publicamente no README. Com as correções identificadas, este projeto teria potencial para atingir 80+ pontos.
