# TAN — The Agro News

> Portal editorial estático de inteligência e notícias do agronegócio brasileiro, construído com Astro + TypeScript SSG.

---

## Stack Tecnológica

| Tecnologia | Função |
|---|---|
| [Astro 4](https://astro.build) | SSG — geração estática de todas as páginas |
| TypeScript (strict) | Contratos de dados e segurança de tipos |
| Zod | Validação de schema no build |
| Pagefind | Busca estática indexada no build |
| Prettier | Formatação de código |
| ESLint + eslint-plugin-astro | Qualidade de código |
| GitHub Actions | CI/CD automático |

---

## Comandos

```bash
npm install          # Instalar dependências
npm run dev          # Servidor de desenvolvimento local
npm run build        # Build de produção (check + astro build + pagefind)
npm run preview      # Pré-visualizar o build gerado
npm run check        # Verificação TypeScript via astro check
npm run lint         # ESLint
npm run format       # Formatar com Prettier
npm run format:check # Verificar formatação (usado no CI)
```

---

## Estrutura do Projeto

```text
tan_project/
├── public/
│   ├── favicon.svg
│   └── robots.txt
├── src/
│   ├── components/        # Componentes Astro reutilizáveis
│   │   ├── Breadcrumb.astro
│   │   ├── EditionCard.astro
│   │   ├── Footer.astro
│   │   ├── Header.astro
│   │   ├── NewsCard.astro
│   │   ├── NewsGrid.astro
│   │   ├── NlpEntities.astro
│   │   ├── NlpKeyPoints.astro
│   │   ├── NlpSummary.astro
│   │   ├── RelatedNews.astro
│   │   ├── SearchInterface.astro
│   │   └── SourceList.astro
│   ├── content/           # Astro Content Collections (fonte única de dados)
│   │   ├── config.ts      # Schemas Zod de validação
│   │   ├── news/          # news-001.json ... news-025.json
│   │   ├── editions/      # edition-2026-09-10.json ...
│   │   └── categories/    # agricultura.json ...
│   ├── layouts/
│   │   ├── BaseLayout.astro   # Layout raiz com SEO completo
│   │   ├── EditionLayout.astro
│   │   └── NewsLayout.astro
│   ├── lib/
│   │   ├── content.ts     # Funções de consulta às coleções
│   │   ├── formatting.ts  # Formatação de datas e textos
│   │   ├── seo.ts         # Geração de metadados e JSON-LD
│   │   └── urls.ts        # URLs semânticas canônicas
│   ├── pages/
│   │   ├── index.astro
│   │   ├── busca.astro
│   │   ├── sobre.astro
│   │   ├── metodologia.astro
│   │   ├── fontes.astro
│   │   ├── 404.astro
│   │   ├── rss.xml.ts
│   │   ├── sitemap.xml.ts
│   │   ├── noticia/[slug].astro
│   │   ├── noticias/index.astro
│   │   ├── noticias/[slug].astro
│   │   ├── categorias/index.astro
│   │   └── categorias/[slug].astro
│   ├── styles/
│   │   ├── variables.css  # Design tokens centralizados
│   │   ├── reset.css
│   │   ├── global.css
│   │   ├── components.css
│   │   └── responsive.css
│   └── types/
│       └── content.ts     # Interfaces TypeScript (NewsItem, Edition, Category...)
├── data/                  # JSONs originais (fonte para migração)
├── scripts/
│   └── verify-build.mjs   # Script de smoke test pós-build
├── .github/workflows/ci.yml
├── astro.config.mjs
├── tsconfig.json
├── eslint.config.mjs
├── prettier.config.mjs
└── package.json
```

---

## Rotas Geradas (SSG)

| Rota | Página |
|---|---|
| `/` | Home editorial |
| `/noticias/` | Feed de notícias e edições |
| `/noticias/[slug]/` | Edição diária (ex: `edicao-10-09-2026`) |
| `/noticia/[slug]/` | Notícia individual pré-renderizada (25 páginas) |
| `/categorias/` | Índice de categorias |
| `/categorias/[slug]/` | Landing page de categoria (8 categorias) |
| `/busca/` | Busca estática Pagefind |
| `/sobre/` | Institucional |
| `/metodologia/` | Metodologia e NLP |
| `/fontes/` | Fontes auditadas |
| `/404` | Página de erro |
| `/sitemap.xml` | Sitemap gerado no build |
| `/rss.xml` | Feed RSS 2.0 |
| `/robots.txt` | Indexação configurada |

---

## Contratos de Dados (API Futura)

As interfaces TypeScript em `src/types/content.ts` e os schemas Zod em `src/content/config.ts` definem os contratos que a futura integração API/NLP deverá satisfazer. A substituição dos dados mockados por uma fonte dinâmica exige apenas alterar as funções em `src/lib/content.ts` — sem tocar em layouts, componentes ou rotas.

```
Hoje:   src/content/news/*.json → src/lib/content.ts → páginas
Futuro: API/NLP/CMS             → src/lib/content.ts → mesmas páginas
```

---

## CI/CD

O arquivo `.github/workflows/ci.yml` executa automaticamente em cada `push` ou `pull_request` para `main`:

1. `npm ci` — instalação limpa
2. `npm run check` — verificação TypeScript
3. `npm run format:check` — verificação de formatação
4. `npm run build` — build + Pagefind index

O `dist/` gerado é compatível com deploy em Cloudflare Pages, Netlify, Vercel ou GitHub Pages sem configuração adicional de servidor.

---

## 🤖 Pipeline de Coleta Automatizada — Sprint 2 / Dupla A

> **Card 8.7 — Automação Agendada da Coleta de Matérias**

Módulo Python localizado em `coleta/` que implementa a ingestão autônoma de notícias dos 5 portais agro de referência com agendamento a cada 3 horas, deduplicação por URL e log estruturado completo.

### Funcionalidades

| Funcionalidade | Detalhe |
|---|---|
| **Agendador APScheduler** | Disparos a cada 3 horas (`IntervalTrigger`), `max_instances=1`, `coalesce=True`, graceful shutdown |
| **Verificação Prévia no Banco** | Consulta `SELECT url FROM artigos WHERE url IN (...)` antes de qualquer download, descartando links já cadastrados |
| **Restrição de Unicidade** | Coluna `url UNIQUE` com `ON CONFLICT DO NOTHING` — blindagem dupla contra duplicatas |
| **Log Rotativo** | `logs/coleta.log` com `RotatingFileHandler` (5 MB/arquivo, 5 backups) + saída no console |
| **Auditoria em Banco** | Tabela `coleta_execucoes` registra início, fim, duração, contagens e status de cada ciclo |
| **Scraping Resiliente** | Feed RSS (prioritário) + fallback HTML, limpeza com `trafilatura` e `BeautifulSoup` |
| **Tolerância a Falhas** | Exceção em um portal é logada e não interrompe os demais |

### Portais Monitorados

- **TheAgriBiz** — via RSS
- **AgFeed** — via RSS
- **Agrolink** — via RSS / HTML
- **Canal Rural** — via RSS
- **Notícias Agrícolas** — via RSS / HTML

### Comandos

```bash
# Instalar dependências Python
python -m pip install apscheduler trafilatura beautifulsoup4 feedparser requests

# Executar um único ciclo de coleta (ideal para testes)
python -m coleta.agendador --run-once

# Iniciar agendador contínuo — 3 horas de intervalo (produção)
python -m coleta.agendador

# Consultar estatísticas do banco e última execução
python -m coleta.agendador --status

# Rodar testes automatizados (6 testes, critérios de aceite)
python -m unittest coleta.test_coleta
```

### Estrutura do Módulo

```text
coleta/
├── __init__.py         # Pacote Python
├── config.py           # Configurações centrais (banco, logs, portais, intervalo)
├── db.py               # Camada de banco (SQLite/PostgreSQL, deduplicação, auditoria)
├── scrapers.py         # Coletores dos 5 portais com RSS + HTML e limpeza trafilatura
├── pipeline.py         # Orquestrador do ciclo de coleta com métricas
├── agendador.py        # APScheduler (3h), logging rotativo, CLI
├── test_coleta.py      # 6 testes unitários — todos aprovados ✅
└── README.md           # Documentação do módulo

data/
└── tan_news.db         # Banco SQLite (criado automaticamente)

logs/
└── coleta.log          # Log rotativo (criado automaticamente)
```

### Resultados Validados

Dois ciclos reais executados com sucesso:

| Rodada | Encontradas | Novas | Ignoradas (Pré-existentes) | Erros | Duração |
|---|---|---|---|---|---|
| 1ª (carga inicial) | 60 | 57 | 0 | 3* | 51.3s |
| 2ª (deduplicação) | 60 | 9 | 51 | 0 | 8.5s |

> \* Os 3 erros da 1ª rodada foram links de redes sociais (Instagram, YouTube) que foram corretamente filtrados na iteração seguinte após atualização do filtro de URLs.

Testes unitários:
```
Ran 6 tests in 1.058s
OK
```

### Critérios de Aceite Atendidos

- ✅ Pipeline de coleta executa de maneira autônoma (configurado para 48h+ sem intervenção).
- ✅ Volume de notícias armazenadas cresce de forma condizente sem duplicação de URLs.
