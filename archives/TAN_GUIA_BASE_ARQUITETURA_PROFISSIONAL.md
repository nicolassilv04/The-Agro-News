# TAN — The Agro News

## Guia Base de Arquitetura Profissional — Frontend Estático Pré-Modelo

**Versão:** 1.0  
**Status:** Documento normativo para refatoração arquitetural  
**Projeto-alvo:** `tan_project.zip`  
**Objetivo desta versão:** entregar um site editorial estático, visualmente refinado, tecnicamente sólido, rápido, acessível, indexável e preparado para integração futura com o modelo/NLP/API.

---

## 0. Regra-mestra

Esta versão do TAN **não deve implementar a plataforma inteligente futura**.

O objetivo atual é construir uma base de frontend profissional e sustentável sobre a qual, posteriormente, serão conectados:

```text
Fontes → ingestão → normalização → NLP/modelo → dados editoriais → frontend TAN
```

Na versão atual:

- dados mockados são aceitáveis;
- conteúdo pode continuar estático;
- comportamentos complexos do modelo não devem ser inventados;
- nenhuma API de produção deve ser criada apenas para “simular” a integração futura;
- nenhuma funcionalidade futura deve ser adicionada sem necessidade arquitetural;
- o frontend deve, entretanto, possuir contratos de dados claros para receber esses dados no futuro.

**Princípio central:** o site deve parecer e se comportar como um produto editorial profissional, mesmo que o conteúdo ainda seja mockado.

---

# 1. Objetivo técnico

Transformar a implementação atual, que combina HTML manual, JSON local e renderização client-side, em uma arquitetura de publicação estática profissional.

### Estado atual simplificado

```text
HTML manual
   +
JSON local
   +
JavaScript client-side
   +
innerHTML
   +
URLs com ?id=
   +
sitemap manual
```

### Estado-alvo

```text
Conteúdo estruturado
        ↓
Validação de dados
        ↓
Build determinístico
        ↓
Templates + componentes
        ↓
HTML pré-renderizado
        ↓
CSS/JS otimizados
        ↓
SEO + sitemap + RSS + metadata
        ↓
Deploy estático
```

A arquitetura deve permitir que o conteúdo mockado de hoje seja substituído por uma fonte de dados futura sem exigir uma reconstrução completa do frontend.

---

# 2. Escopo desta versão

## 2.1 Incluído

- refatoração arquitetural;
- migração para SSG moderno, preferencialmente Astro;
- componentes reutilizáveis;
- layouts e templates;
- conteúdo estruturado;
- URLs semânticas;
- HTML pré-renderizado;
- SEO técnico;
- Open Graph e Twitter/X metadata;
- Schema.org/NewsArticle;
- sitemap automático;
- robots.txt;
- RSS quando aplicável;
- busca estática eficiente;
- acessibilidade;
- performance;
- imagens e fontes otimizadas;
- estados de loading/empty/error/404;
- responsividade real;
- validação de dados;
- lint/format/build;
- estrutura de CI/CD preparada;
- documentação técnica mínima;
- organização de projeto adequada a evolução futura.

## 2.2 Explicitamente fora de escopo

Não implementar nesta etapa:

- backend editorial;
- autenticação;
- painel administrativo;
- banco de dados de produção;
- crawler real;
- coleta real de notícias;
- integração com LLM/API de produção;
- pipeline NLP real;
- recomendação inteligente real;
- personalização por usuário;
- sistema de contas;
- newsletter funcional;
- analytics de produção obrigatório;
- pagamentos;
- notificações;
- infraestrutura distribuída;
- microserviços.

Qualquer uma dessas necessidades deve ser tratada como etapa posterior.

---

# 3. Benchmark arquitetural

O projeto deve adotar padrões comuns a sites editoriais estáticos profissionais, especialmente os demonstrados por projetos públicos de referência como:

- **AstroPaper:** https://github.com/satnaing/astro-paper
- **Eleventy Base Blog:** https://github.com/11ty/eleventy-base-blog
- **Documentação Astro:** https://docs.astro.build/
- **Documentação Eleventy:** https://www.11ty.dev/docs/
- **Schema Article/NewsArticle do Google:** https://developers.google.com/search/docs/appearance/structured-data/article

### Características desejáveis observadas nesses ecossistemas

```text
conteúdo separado da apresentação
componentização
layouts
build reproduzível
páginas estáticas
SEO gerado
sitemap automático
conteúdo tipado/validado
busca indexada
CI/deploy reproduzível
```

O TAN deve adaptar esses princípios ao próprio produto, e não copiar a estrutura visual de qualquer benchmark.

---

# 4. Diagnóstico do projeto atual

O ZIP de origem apresenta uma base visual coerente e um bom modelo conceitual de dados, porém possui dívida arquitetural para produção.

## 4.1 Pontos positivos a preservar

- design system já iniciado;
- separação entre `variables.css`, `reset.css`, `global.css`, `components.css` e `responsive.css`;
- modelo de notícia rico;
- modelo de edição;
- categorização;
- conceito de NLP separado do frontend;
- páginas institucionais já concebidas;
- navegação global;
- estados de interface previstos na especificação original;
- identidade editorial própria.

## 4.2 Problemas prioritários identificados

### A. Conteúdo depende excessivamente do JavaScript

Páginas de notícia usam hidratação client-side para montar conteúdo.

Problema:

```text
crawler/browser
   ↓
HTML quase vazio
   ↓
JavaScript
   ↓
conteúdo
```

Alvo:

```text
crawler/browser
   ↓
HTML completo
   ↓
JavaScript apenas para interações necessárias
```

### B. URLs com query string

Atual:

```text
/noticia/index.html?id=news-001
```

Alvo:

```text
/noticia/soja-movimentacao-mercado-internacional/
```

### C. Datas/links estruturais hardcoded

A data da edição atual aparece diretamente no código em vários lugares.

Alvo:

```text
fonte única de dados
        ↓
slug/URL
        ↓
todas as páginas
```

### D. Sitemap manual e incompleto

O sitemap deve ser gerado a partir das páginas realmente produzidas pelo build.

### E. Ausência de pipeline formal de build

O projeto precisa de scripts determinísticos para:

```bash
npm run dev
npm run build
npm run preview
npm run lint
npm run format
```

### F. Busca client-side baseada no carregamento integral do JSON

Para crescimento do acervo, usar uma busca estática/indexada, preferencialmente Pagefind ou solução equivalente.

### G. Uso indiscriminado de `innerHTML`

Renderização de conteúdo deve ser segura, previsível e, quando possível, derivada de templates do SSG.

### H. SEO incompleto

Cada documento deve gerar metadata específica e consistente.

### I. Sistema editorial de imagens ainda insuficiente

Notícias devem possuir um modelo de imagem principal e texto alternativo.

### J. Analytics atual é apenas mock

A estrutura deve ser tratada como camada futura/telemetria, e não como implementação real.

---

# 5. Arquitetura alvo

## 5.1 Stack recomendada

### Obrigatório

- Astro;
- TypeScript;
- CSS organizado;
- dados estruturados em JSON/Markdown/MDX conforme necessidade;
- ferramenta de build integrada ao Astro;
- ESLint ou equivalente;
- Prettier ou equivalente;
- validação de conteúdo.

### Recomendado

- Zod ou mecanismo equivalente para schema validation;
- Pagefind para busca estática;
- `@astrojs/sitemap` ou equivalente;
- RSS quando adequado;
- formatos modernos de imagem como WebP/AVIF;
- Playwright para smoke tests ou ferramenta equivalente.

### Evitar

- React para partes que podem permanecer em Astro puro;
- estado global sem necessidade;
- bibliotecas de UI pesadas;
- dependências que resolvam tarefas triviais já suportadas pela plataforma;
- frameworks múltiplos no mesmo frontend sem motivo técnico.

---

# 6. Estrutura de diretórios alvo

Uma estrutura recomendada:

```text
TAN/
├── public/
│   ├── fonts/
│   ├── images/
│   ├── icons/
│   ├── favicon.svg
│   └── robots.txt
│
├── src/
│   ├── components/
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   ├── NewsCard.astro
│   │   ├── NewsGrid.astro
│   │   ├── Breadcrumb.astro
│   │   ├── SourceList.astro
│   │   ├── RelatedNews.astro
│   │   ├── NlpSummary.astro
│   │   ├── EditionCard.astro
│   │   └── SearchInterface.astro
│   │
│   ├── content/
│   │   ├── news/
│   │   ├── editions/
│   │   └── categories/
│   │
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   ├── NewsLayout.astro
│   │   └── EditionLayout.astro
│   │
│   ├── pages/
│   │   ├── index.astro
│   │   ├── busca.astro
│   │   ├── sobre.astro
│   │   ├── metodologia.astro
│   │   ├── fontes.astro
│   │   ├── noticias/
│   │   │   ├── index.astro
│   │   │   └── [...slug].astro
│   │   ├── noticia/
│   │   │   └── [...slug].astro
│   │   └── categorias/
│   │       ├── index.astro
│   │       └── [...slug].astro
│   │
│   ├── styles/
│   │   ├── variables.css
│   │   ├── reset.css
│   │   ├── global.css
│   │   ├── components.css
│   │   └── responsive.css
│   │
│   ├── lib/
│   │   ├── content.ts
│   │   ├── seo.ts
│   │   ├── urls.ts
│   │   └── formatting.ts
│   │
│   └── types/
│       └── content.ts
│
├── scripts/
├── tests/
├── astro.config.ts
├── tsconfig.json
├── eslint.config.js
├── prettier.config.js
├── package.json
└── README.md
```

A estrutura pode variar tecnicamente, mas as responsabilidades devem permanecer separadas.

---

# 7. Princípios arquiteturais obrigatórios

## 7.1 Single Source of Truth

Informações como:

- nome de categoria;
- slug;
- edição atual;
- data;
- título;
- resumo;
- fontes;
- tags;
- entidades;
- metadata;

não devem ser duplicadas manualmente em múltiplos arquivos quando podem ser derivadas do conteúdo.

## 7.2 Conteúdo desacoplado da apresentação

O componente visual não deve possuir conhecimento rígido do mecanismo futuro de ingestão/NLP.

Exemplo:

```ts
interface NewsItem {
  id: string;
  slug: string;
  title: string;
  summary: string;
  content: string;
  category: string;
  publishedAt: string;
  updatedAt?: string;
  sources: Source[];
  tags: string[];
  entities?: Entity[];
  nlp?: NlpData;
}
```

A fonte poderá mudar de:

```text
JSON local
```

para:

```text
API / banco / CMS
```

sem alterar o contrato visual principal.

## 7.3 Progressive Enhancement

A página deve continuar útil como HTML mesmo sem JavaScript, especialmente para conteúdo editorial.

JavaScript é reservado a:

- menu móvel;
- filtros interativos quando necessários;
- busca;
- pequenas interações;
- telemetria futura;
- enhancements visuais.

## 7.4 Zero duplicação estrutural desnecessária

Evitar ter:

```text
12 páginas HTML quase iguais
```

quando podem ser geradas por um template.

## 7.5 Build determinístico

A mesma entrada deve produzir a mesma saída, salvo elementos explicitamente dinâmicos.

---

# 8. Sistema de conteúdo

## 8.1 Formato recomendado

Preferência:

- Markdown/MDX para corpo editorial;
- frontmatter para metadados;
- JSON apenas onde fizer sentido para dados estruturados ou fixtures.

Exemplo:

```yaml
---
title: 'Soja registra nova movimentação no mercado internacional'
slug: 'soja-movimentacao-mercado-internacional'
category: 'mercado'
publishedAt: '2026-09-10T08:30:00-03:00'
updatedAt: '2026-09-10T09:20:00-03:00'
summary: 'Resumo editorial da notícia.'
heroImage: '/images/news/soja.webp'
heroAlt: 'Descrição objetiva da imagem'
tags:
  - soja
  - mercado
sourcesCount: 4
---
Conteúdo editorial...
```

## 8.2 Validação

Nenhuma notícia deve entrar no build se campos obrigatórios estiverem inválidos.

Campos mínimos:

```text
title
slug
summary
content
category
publishedAt
```

Campos recomendados:

```text
updatedAt
heroImage
heroAlt
author
sources
tags
entities
nlp
```

---

# 9. Routing e URLs

## 9.1 Notícias

Padrão:

```text
/noticia/[slug]/
```

## 9.2 Edições

Padrão:

```text
/noticias/[slug-da-edicao]/
```

Exemplo:

```text
/noticias/edicao-10-09-2026/
```

## 9.3 Categorias

Padrão:

```text
/categorias/agricultura/
/categorias/pecuaria/
```

## 9.4 Regras

- sem `?id=` para conteúdo editorial;
- slugs estáveis;
- URLs legíveis;
- URLs canônicas únicas;
- evitar IDs internos expostos na URL;
- não criar URLs duplicadas para o mesmo conteúdo.

---

# 10. SEO técnico

Cada página pública deve gerar metadata adequada ao tipo de documento.

## 10.1 Base

```html
<title>...</title>
<meta name="description" content="..." />
<link rel="canonical" href="..." />
```

## 10.2 Open Graph

```text
og:title
og:description
og:url
og:type
og:image
og:site_name
```

Para notícia:

```text
article:published_time
article:modified_time
article:section
```

## 10.3 Twitter/X

Usar metadata equivalente e imagem adequada.

## 10.4 Structured Data

Notícias devem gerar `NewsArticle`/`Article` de forma server/build-time.

Estrutura mínima:

```json
{
  "@context": "https://schema.org",
  "@type": "NewsArticle",
  "headline": "...",
  "description": "...",
  "image": ["..."],
  "datePublished": "...",
  "dateModified": "...",
  "author": {
    "@type": "Organization",
    "name": "TAN — The Agro News"
  },
  "publisher": {
    "@type": "Organization",
    "name": "TAN — The Agro News"
  },
  "mainEntityOfPage": "..."
}
```

Não injetar esses dados apenas no client-side quando eles podem ser gerados durante o build.

## 10.5 Sitemap

Gerado automaticamente a partir das rotas reais.

Nunca manter uma lista manual de URLs editoriais como fonte principal.

## 10.6 Robots

Deve existir e refletir a estratégia real de indexação.

## 10.7 RSS

Considerar feed de notícias/edições, desde que sua estrutura seja coerente com o produto editorial.

---

# 11. Performance

## 11.1 Metas qualitativas

O site deve:

- carregar rapidamente em desktop e mobile;
- minimizar JavaScript enviado;
- evitar dependências pesadas;
- não bloquear conteúdo principal com scripts desnecessários;
- não carregar o acervo inteiro apenas para renderizar uma página;
- otimizar imagens;
- usar fontes de forma econômica.

## 11.2 Imagens

Preferir:

```text
AVIF/WebP
responsive images
width/height definidos
lazy loading fora do conteúdo crítico
fetchpriority adequado para hero quando aplicável
alt textual correto
```

## 11.3 JavaScript

Regra:

> Se uma informação puder ser produzida durante o build, não enviar JavaScript para produzi-la no navegador.

---

# 12. Acessibilidade

Objetivo mínimo: WCAG 2.2 AA como referência de qualidade.

Obrigatório:

- HTML semântico;
- hierarquia de headings coerente;
- labels/accessible names claros;
- navegação por teclado;
- foco visível;
- `aria-expanded` e `aria-controls` onde necessários;
- skip link;
- contraste adequado;
- `alt` descritivo em imagens informativas;
- textos de links significativos;
- estados de erro acessíveis;
- não depender apenas de cor para transmitir significado.

Menu mobile deve possuir estado acessível, por exemplo:

```html
<button aria-expanded="false" aria-controls="mobile-navigation">Menu</button>
```

---

# 13. Design System

A identidade atual deve ser preservada e refinada, não descaracterizada.

Centralizar:

```text
cores
spacing
radius
shadows
font sizes
line heights
breakpoints
containers
z-index
```

Evitar estilos inline repetidos.

Exemplo ruim:

```html
<a style="font-size:0.85rem; color:..."></a>
```

Preferir:

```html
<a class="section-link"></a>
```

com estilo centralizado.

---

# 14. Componentização

Componentes devem representar responsabilidades reais.

Exemplos:

```text
Header
Footer
NewsCard
NewsList
EditionCard
Breadcrumb
NewsMeta
SourceList
RelatedNews
NlpSummary
NlpEntities
SearchInterface
```

Um componente não deve:

- buscar dados diretamente de uma API futura;
- conhecer detalhes de banco;
- conter regras editoriais irrelevantes à apresentação;
- duplicar markup de outro componente.

---

# 15. Estados de interface

Mesmo com conteúdo mockado, todas as telas relevantes devem prever estados.

## Loading

Usado apenas onde houver carregamento client-side real.

## Empty

Exemplo:

> Nenhuma notícia encontrada para estes filtros.

## Error

Exemplo:

> Não foi possível carregar o conteúdo. Tente novamente.

## 404

Deve possuir página dedicada, consistente com a identidade TAN.

---

# 16. Busca

A busca deve ser preparada para o acervo crescer.

Não usar como solução definitiva:

```text
fetch news.json inteiro
   ↓
filter() em milhares de itens
```

Preferência:

```text
build
 ↓
índice de busca
 ↓
consulta client-side
```

Pagefind é uma opção prioritária para avaliação.

A busca não precisa ser “inteligente” nesta etapa. Ela precisa ser:

- rápida;
- previsível;
- acessível;
- indexada;
- compatível com conteúdo pré-renderizado.

---

# 17. Segurança e integridade de conteúdo

Regras:

- não confiar cegamente em conteúdo externo;
- evitar `innerHTML` com dados não validados;
- sanitizar HTML quando HTML enriquecido for inevitável;
- validar schemas antes do build;
- não expor segredos no frontend;
- nenhuma chave de API deve existir no bundle estático;
- nenhuma credencial deve ser colocada em `.env` público ou commitada.

---

# 18. TypeScript e contratos

Tipos devem existir para os principais objetos editoriais.

Exemplo:

```ts
export interface Source {
  name: string;
  url?: string;
  accessedAt?: string;
}

export interface NewsItem {
  id: string;
  slug: string;
  title: string;
  summary: string;
  content: string;
  category: string;
  publishedAt: string;
  updatedAt?: string;
  tags: string[];
  sources: Source[];
  heroImage?: string;
  heroAlt?: string;
}
```

A modelagem deve suportar os campos de NLP sem acoplá-los à interface.

---

# 19. Configuração e ambiente

Criar configuração central para:

```text
site URL
nome do site
título padrão
descrição padrão
idioma
timezone editorial
prefixos de URL
identidade de publisher
```

Não espalhar `https://tan.agro.br` e outras constantes estruturais por dezenas de arquivos.

---

# 20. Qualidade de código

Obrigatório:

```bash
npm run lint
npm run format:check
npm run build
```

Recomendado:

```bash
npm run test
npm run preview
```

Build deve falhar se houver erro estrutural importante.

---

# 21. CI/CD preparado para produção

Mesmo que o primeiro deploy seja simples, o repositório deve permitir:

```text
push
 ↓
install
 ↓
lint
 ↓
build
 ↓
smoke checks
 ↓
deploy
```

Exemplo de pipeline:

```yaml
name: ci

on:
  push:
    branches: [main]
  pull_request:

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - checkout
      - setup-node
      - npm ci
      - npm run lint
      - npm run format:check
      - npm run build
```

O provedor final pode ser Cloudflare Pages, Netlify, Vercel, GitHub Pages ou infraestrutura equivalente. A arquitetura não deve depender de um provedor específico quando isso não for necessário.

---

# 22. Testes e validações

## 22.1 Build

- build sem warnings críticos;
- todas as páginas geradas;
- nenhum link interno quebrado;
- assets resolvidos.

## 22.2 Rotas

Validar pelo menos:

```text
/
/noticias/
/noticias/[edicao]/
/noticia/[slug]/
/categorias/
/categorias/[slug]/
/busca/
/sobre/
/metodologia/
/fontes/
/404
```

## 22.3 SEO

Validar:

- title;
- description;
- canonical;
- OG;
- Twitter/X;
- JSON-LD;
- sitemap;
- robots.

## 22.4 Conteúdo

Validar:

- títulos corretos;
- datas coerentes;
- slugs únicos;
- categorias existentes;
- fontes válidas;
- imagens existentes;
- alt text preenchido quando necessário.

## 22.5 Acessibilidade

Executar auditoria automatizada quando possível e uma revisão manual de teclado/foco.

## 22.6 Responsividade

Validar pelo menos:

```text
mobile pequeno
mobile grande
tablet
notebook
monitor largo
```

---

# 23. Critérios de aceite visual

O resultado final deve:

- preservar a identidade TAN;
- não parecer um template genérico de blog;
- manter hierarquia editorial clara;
- apresentar consistência entre Home, Edição, Notícia, Categoria e Institucionais;
- possuir espaçamento e tipografia consistentes;
- apresentar estados de hover/focus coerentes;
- não apresentar overflow horizontal indevido;
- manter legibilidade em telas pequenas;
- não possuir componentes “quebrados” ou sem conteúdo.

---

# 24. Critérios de aceite arquitetural

O projeto será considerado aprovado somente quando:

- conteúdo editorial estiver pré-renderizado;
- não houver necessidade de JavaScript para exibir a notícia principal;
- URLs principais forem semânticas;
- sitemap for automático;
- metadata for derivada do conteúdo;
- conteúdo estiver separado da apresentação;
- componentes estiverem reutilizáveis;
- dados possuírem contratos/tipos;
- build puder ser executado de forma determinística;
- lint/format/build estiverem configurados;
- nenhuma credencial existir no frontend;
- a busca estiver preparada para crescimento;
- futuras integrações de API/NLP puderem substituir a fonte de dados sem redesenhar todo o frontend.

---

# 25. Definition of Done

A tarefa não está concluída porque “o site abre”.

Ela está concluída quando:

```text
[ ] Arquitetura migrada/refatorada
[ ] Conteúdo desacoplado
[ ] Rotas semânticas
[ ] Páginas pré-renderizadas
[ ] SEO completo
[ ] Sitemap automático
[ ] Robots configurado
[ ] Busca adequada ao SSG
[ ] Acessibilidade revisada
[ ] Imagens otimizadas
[ ] Responsividade revisada
[ ] Estados de interface revisados
[ ] TypeScript/tipos
[ ] Schema validation
[ ] Lint
[ ] Format
[ ] Build
[ ] Smoke tests
[ ] CI preparado
[ ] README atualizado
[ ] Sem funcionalidades futuras inventadas
[ ] Sem regressões visuais relevantes
```

---

# 26. Estratégia de implementação em fases

## Fase 0 — Inventário

- ler toda a especificação existente;
- mapear páginas;
- mapear componentes;
- mapear dados;
- identificar duplicações;
- identificar links hardcoded;
- identificar problemas de SEO/acessibilidade.

**Saída:** mapa técnico antes de alterar o projeto.

## Fase 1 — Fundação

- criar `package.json`;
- configurar Astro;
- TypeScript;
- lint;
- format;
- estrutura de diretórios;
- configuração global.

**Gate:** projeto inicializa e builda.

## Fase 2 — Design System

- migrar tokens;
- centralizar componentes;
- remover estilos inline redundantes;
- manter identidade visual.

**Gate:** sem regressão visual relevante.

## Fase 3 — Conteúdo e contratos

- migrar `news.json`;
- `editions.json`;
- `categories.json`;
- criar schemas;
- criar tipos;
- validar dados.

**Gate:** conteúdo inválido bloqueia build.

## Fase 4 — Rotas e templates

- Home;
- Notícias;
- Edições;
- Notícia individual;
- Categorias;
- Institucionais;
- 404.

**Gate:** todas as páginas com HTML real no build.

## Fase 5 — SEO/Discoverability

- title;
- description;
- canonical;
- Open Graph;
- Twitter/X;
- NewsArticle;
- sitemap;
- robots;
- RSS.

**Gate:** validação das principais páginas.

## Fase 6 — Busca e interações mínimas

- busca indexada;
- menu mobile;
- filtros estritamente necessários;
- pequenos enhancements.

**Gate:** JavaScript limitado ao necessário.

## Fase 7 — Performance/A11y

- imagens;
- fontes;
- bundle;
- lazy loading;
- keyboard/focus;
- contraste;
- semântica.

**Gate:** auditoria final.

## Fase 8 — CI e release

- workflow;
- build de produção;
- smoke tests;
- README;
- instruções de deploy.

**Gate final:** Definition of Done completa.

---

# 27. Regras de atuação para o chatbot executor

1. **Não começar codificando imediatamente.** Primeiro inspecionar o repositório.
2. **Não substituir o design sem necessidade.** Refatorar a infraestrutura preservando a linguagem visual existente.
3. **Não criar funcionalidades futuras por iniciativa própria.** Preparar contratos, não implementar o modelo.
4. **Não manter soluções manuais quando o build puder gerá-las.**
5. **Não duplicar dados.** Preferir fonte única e derivação.
6. **Não esconder problemas com hacks.** Resolver a causa arquitetural.
7. **Não introduzir dependências sem justificar o ganho.**
8. **Não alterar conteúdo editorial só para facilitar a implementação.**
9. **Não considerar a tarefa concluída somente após `npm run dev`.** O critério principal é build + validação + qualidade.
10. **Após cada fase, registrar o que foi alterado, validado e o que ainda falta.**
11. **Se houver ambiguidade, escolher a opção mais conservadora e alinhada ao documento, sem inventar requisitos.**
12. **Se uma migração destruir uma funcionalidade visual existente, corrigir a regressão antes de avançar.**

---

# 28. O que não fazer

Evitar explicitamente:

```text
❌ transformar tudo em uma SPA
❌ manter ?id= para notícias
❌ gerar conteúdo principal apenas com JS
❌ manter sitemap manual
❌ espalhar datas em HTML/JS
❌ colocar segredo no frontend
❌ criar API falsa só para parecer “profissional”
❌ instalar dezenas de pacotes sem necessidade
❌ trocar o design inteiro sem justificativa
❌ implementar IA/NLP antes da integração prevista
❌ usar banco de dados para resolver um problema que o SSG resolve
❌ criar microserviços
❌ chamar um MVP estático de “pronto” sem validações
```

---

# 29. Estrutura futura de integração do modelo

A arquitetura deve terminar em algo equivalente a:

```text
                    FUTURO
┌────────────────────────────────────────────┐
│ Fontes externas / ingestão                 │
└──────────────────┬─────────────────────────┘
                   ↓
┌────────────────────────────────────────────┐
│ Normalização / deduplicação                │
└──────────────────┬─────────────────────────┘
                   ↓
┌────────────────────────────────────────────┐
│ Modelo / NLP                               │
│ classificação · resumo · entidades         │
│ relevância · similaridade · clustering     │
└──────────────────┬─────────────────────────┘
                   ↓
┌────────────────────────────────────────────┐
│ Content Store / API / CMS                  │
└──────────────────┬─────────────────────────┘
                   ↓
┌────────────────────────────────────────────┐
│ Contrato de dados TAN                      │
└──────────────────┬─────────────────────────┘
                   ↓
┌────────────────────────────────────────────┐
│ Frontend Astro                             │
└────────────────────────────────────────────┘
```

O frontend atual deve depender somente do **contrato de dados**, não de como o modelo será implementado.

---

# 30. Resultado esperado

Ao final desta etapa, o TAN deve ser um **site editorial estático profissional**, não um protótipo de SPA.

O usuário final deve perceber:

```text
marca editorial
+ conteúdo consistente
+ navegação clara
+ velocidade
+ credibilidade
```

e o desenvolvedor deve perceber:

```text
componentização
+ conteúdo estruturado
+ build reproduzível
+ SEO automático
+ contratos claros
+ baixo acoplamento
+ caminho limpo para API/NLP futura
```

A futura integração do modelo deve parecer uma **substituição da origem dos dados**, e não uma reconstrução do site.

---

# 31. Regra final de decisão

Quando houver duas implementações possíveis, priorizar nesta ordem:

```text
1. Correção arquitetural
2. Conteúdo semanticamente acessível
3. SEO e indexabilidade
4. Performance
5. Acessibilidade
6. Manutenibilidade
7. Consistência visual
8. Complexidade mínima
```

A solução mais profissional não é a que possui mais tecnologias.

É a que resolve o problema com a **menor complexidade necessária e a maior previsibilidade de evolução**.
