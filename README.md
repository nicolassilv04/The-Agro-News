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
