# TAN — The Agro News

## Especificação Funcional e Estrutural do MVP

**Versão:** 1.0  
**Status:** MVP estático / arquitetura preparada para evolução dinâmica  
**Objetivo:** Definir a estrutura completa do site TAN — The Agro News, um portal editorial de notícias sobre o agronegócio, com publicação diária e arquitetura preparada para processamento de notícias por NLP.

---

# 1. Visão do Produto

## 1.1 Conceito

O **TAN — The Agro News** será um portal de notícias especializado em **agronegócio, agricultura, pecuária, tecnologia, mercado, clima, política agrícola e tendências do setor**.

A proposta editorial é semelhante à de um portal de notícias moderno, porém com foco exclusivo no ecossistema Agro.

O MVP será inicialmente **estático**, utilizando conteúdo mockado, mas toda a estrutura deverá ser organizada para permitir posteriormente:

- ingestão automática de notícias;
- processamento por NLP;
- classificação temática;
- sumarização;
- extração de entidades;
- identificação de eventos;
- agrupamento de notícias relacionadas;
- atualização diária;
- busca;
- filtros;
- analytics;
- CMS ou backend próprio.

---

# 2. Objetivos do MVP

O MVP deverá provar quatro pontos principais:

1. **Consumo:** o usuário consegue descobrir rapidamente o que está acontecendo no Agro.
2. **Organização:** notícias complexas são separadas por temas e apresentadas de forma compreensível.
3. **Curadoria:** o sistema consegue transformar diversas fontes em uma experiência editorial única.
4. **Escalabilidade:** a interface e o modelo de conteúdo não devem depender de textos escritos manualmente.

---

# 3. Público-Alvo

O produto pode atender:

- produtores rurais;
- estudantes;
- profissionais do agronegócio;
- gestores e empresários;
- investidores;
- pesquisadores;
- consultores;
- profissionais de tecnologia agrícola;
- pessoas interessadas em economia e política do Agro.

---

# 4. Arquitetura Geral do Site

## 4.1 Sitemap

```text
/
├── index.html
│   └── Home
│
├── noticias/
│   ├── index.html
│   │   └── Feed diário
│   │
│   └── [slug-da-edicao].html
│       └── Edição diária / agregador de notícias
│
├── noticia/
│   └── [slug].html
│       └── Página individual da notícia
│
├── categorias/
│   ├── agricultura.html
│   ├── pecuaria.html
│   ├── mercado.html
│   ├── tecnologia.html
│   ├── clima.html
│   ├── politica.html
│   └── sustentabilidade.html
│
├── busca.html
│
├── sobre.html
│
├── metodologia.html
│
├── fontes.html
│
└── erro/
    └── 404.html
```

> No MVP estático, os arquivos podem ser HTML independentes ou gerados a partir de um template. Em uma etapa posterior, `[slug]` deverá ser resolvido dinamicamente por backend, CMS ou framework.

---

# 5. Navegação Global

Todas as páginas deverão compartilhar o mesmo sistema de navegação.

## Header

### Elementos obrigatórios

- Logo / nome: **TAN**
- Texto secundário: **The Agro News**
- Link: **Início**
- Link: **Notícias**
- Link: **Categorias**
- Link: **Sobre**
- Campo/ícone de **Busca**
- CTA opcional: **Edição de Hoje**

### Comportamento

O header deve permanecer consistente em todas as páginas.

Desktop:

```text
[TAN] [Início] [Notícias] [Categorias] [Sobre]        [🔍 Buscar]
```

Mobile:

```text
[TAN]                                  [☰]
```

---

# 6. Home — `/`

A Home é a principal página de apresentação e descoberta.

## 6.1 Hero

Deve apresentar rapidamente:

**TAN — The Agro News**

> As principais notícias do agronegócio, organizadas em um único lugar.

Elementos:

- título;
- subtítulo;
- CTA **Ler a edição de hoje**;
- CTA secundário **Explorar notícias**;
- imagem ou composição visual relacionada ao Agro.

### Links

- "Ler a edição de hoje" → `/noticias/`
- "Explorar notícias" → `/noticias/`

---

# 7. Seção "O que é o TAN?"

Breve explicação do produto.

Exemplo:

> O TAN reúne e organiza as principais movimentações do agronegócio em uma experiência editorial simples. Notícias de diferentes fontes são processadas, classificadas e agrupadas para facilitar a compreensão dos acontecimentos relevantes do setor.

Botão:

**Conheça nossa metodologia** → `/metodologia.html`

---

# 8. Edição de Hoje

A Home deve possuir uma seção destacada para a edição atual.

## Estrutura

```text
EDIÇÃO DE HOJE
10 SET 2026

[Notícia principal]

[Notícia] [Notícia] [Notícia]
```

Cada card deve conter:

- categoria;
- título;
- resumo curto;
- horário ou data;
- origem/fonte;
- indicador visual de destaque;
- link.

---

# 9. Categorias em Destaque

Categorias padrão do MVP:

### Agricultura

Soja, milho, trigo, café, algodão, cana etc.

### Pecuária

Bovinos, suínos, aves, leite etc.

### Mercado

Commodities, preços, exportações, importações, câmbio etc.

### Tecnologia

AgTech, IA, sensores, drones, automação, robótica etc.

### Clima

Secas, chuvas, geadas, eventos extremos e previsões.

### Política e Regulação

Ministérios, legislação, crédito rural, tributação, políticas agrícolas.

### Sustentabilidade

ESG, carbono, conservação, rastreabilidade e agricultura regenerativa.

### Internacional

China, EUA, Europa e demais acontecimentos globais com impacto no Agro brasileiro.

Cada categoria deve apontar para sua página própria.

---

# 10. Página de Notícias — `/noticias/`

Esta é a página principal de consumo recorrente.

## Objetivo

Mostrar a produção diária do TAN em ordem cronológica/editorial.

## Estrutura

```text
NOTÍCIAS
As principais movimentações do agronegócio.

[Filtros]

EDIÇÃO DE HOJE
├── Destaque principal
├── Card
├── Card
├── Card
└── Card

EDIÇÕES ANTERIORES
├── 09 SET
├── 08 SET
├── 07 SET
└── ...
```

## Filtros

- Todos
- Agricultura
- Pecuária
- Mercado
- Tecnologia
- Clima
- Política
- Sustentabilidade
- Internacional

Filtros adicionais futuros:

- período;
- cultura;
- estado/região;
- país;
- entidade;
- empresa;
- commodity.

---

# 11. Conceito de Edição Diária

Como o projeto terá aproximadamente **uma publicação principal por dia**, cada publicação pode ser tratada como uma **Edição TAN**.

Exemplo:

```text
TAN — Edição #127
10 de setembro de 2026
```

Uma edição pode conter várias notícias processadas.

## Estrutura conceitual

```text
Edição
│
├── Resumo do dia
│
├── Agricultura
│   ├── Notícia
│   └── Notícia
│
├── Pecuária
│   └── Notícia
│
├── Mercado
│   ├── Notícia
│   └── Notícia
│
├── Tecnologia
│   └── Notícia
│
└── Clima
    └── Notícia
```

---

# 12. Página da Edição — `/noticias/[slug-da-edicao].html`

Exemplo:

```text
/noticias/edicao-10-09-2026.html
```

## Header

```text
TAN — Edição de 10 de setembro de 2026

As principais movimentações do Agro nas últimas 24 horas.
```

## Resumo da edição

Uma introdução curta gerada pelo sistema.

Exemplo genérico:

> O mercado agrícola iniciou o dia com movimentações relevantes nas principais commodities, enquanto novas projeções climáticas influenciam decisões de plantio em diferentes regiões.

Esse bloco futuramente poderá ser gerado automaticamente por NLP.

---

# 13. Organização das Notícias Dentro da Edição

Cada notícia deve possuir:

- tag de categoria;
- título;
- resumo;
- horário;
- fontes;
- entidades relevantes;
- região;
- link para notícia detalhada.

Exemplo:

```text
MERCADO

Soja registra nova movimentação no mercado internacional

Mercados externos apresentam novas oscilações e aumentam a atenção sobre os próximos embarques brasileiros.

09:42 · Mercado

[LER NOTÍCIA]
```

---

# 14. Página Individual da Notícia — `/noticia/[slug].html`

Esta página é importante para SEO, compartilhamento e aprofundamento.

## Estrutura

```text
Breadcrumb

Categoria

Título

Subtítulo / resumo

Data + hora

Fonte(s)

Conteúdo principal

Resumo automático

Principais pontos

Entidades citadas

Notícias relacionadas

Fontes originais

Compartilhar
```

---

# 15. Breadcrumb

Exemplo:

```text
Início / Notícias / Mercado / Soja registra nova movimentação...
```

Cada nível deverá ser clicável.

---

# 16. Cabeçalho da Notícia

Elementos:

- categoria;
- título;
- subtítulo;
- data;
- horário;
- autor/editoria;
- status da informação;
- fonte principal.

Exemplo:

```text
MERCADO

Soja registra nova movimentação no mercado internacional

Movimentos recentes nos mercados externos alteram expectativas para exportadores brasileiros.

10 de setembro de 2026 · 09:42

Fonte: Exemplo Agência
```

---

# 17. Conteúdo Principal

No MVP, o corpo pode conter texto genérico.

Entretanto, o HTML deve separar semanticamente:

```html
<article>
  <header>...</header>

  <section class="article-summary">...</section>

  <section class="article-content">...</section>

  <section class="article-analysis">...</section>

  <section class="article-sources">...</section>
</article>
```

Isso facilitará futuras alterações automáticas.

---

# 18. Bloco "Resumo TAN"

Como o site utilizará NLP, cada notícia deverá ter uma área reservada para um resumo automatizado.

Exemplo:

### Resumo TAN

- O mercado apresentou nova movimentação;
- produtores acompanham as projeções;
- exportadores avaliam os próximos embarques;
- cenário internacional continua sendo relevante.

Este bloco poderá ser produzido por modelos de sumarização.

---

# 19. Bloco "Principais pontos"

Um segundo resultado de NLP pode gerar:

```text
PRINCIPAIS PONTOS

• O que aconteceu?
• Quem foi impactado?
• Onde aconteceu?
• Qual é a possível consequência?
• O que observar nos próximos dias?
```

Essa estrutura ajuda a transformar uma notícia longa em informação rapidamente consumível.

---

# 20. Entidades Extraídas por NLP

Deverá existir uma seção preparada para entidades.

Exemplo:

```text
ENTIDADES

Empresas
[Empresa A] [Empresa B]

Pessoas
[Nome A]

Organizações
[Organização X]

Locais
[Mato Grosso] [Brasil]

Produtos
[Soja] [Milho]

Commodities
[Soja]
```

Cada entidade poderá futuramente possuir uma página própria.

Exemplo:

```text
/categorias/soja.html
/entidades/empresa-a.html
/regioes/mato-grosso.html
```

---

# 21. Classificação NLP

Cada notícia pode possuir metadados calculados automaticamente:

```json
{
  "category": "mercado",
  "subcategory": "commodities",
  "topics": ["soja", "exportação", "China"],
  "entities": ["Brasil", "China", "Empresa X"],
  "regions": ["Mato Grosso"],
  "sentiment": "neutral",
  "importance": 0.87
}
```

Esses dados não precisam aparecer integralmente para o usuário no MVP, mas a interface deve ser preparada para utilizá-los.

---

# 22. Score Editorial

O sistema poderá calcular uma pontuação de relevância.

Exemplo:

```text
importance_score = 0.87
```

Esse score pode ajudar a decidir:

- notícia principal;
- ordem dos cards;
- destaque da Home;
- seleção das notícias da edição;
- geração dos resumos.

---

# 23. Agrupamento de Notícias

Uma capacidade importante do NLP será evitar a repetição de notícias.

Exemplo:

```text
Fonte A
"Preço da soja sobe nesta manhã"

Fonte B
"Soja avança nos mercados internacionais"

Fonte C
"Mercado registra alta da soja"

                ↓ NLP

GRUPO DE EVENTO

"Soja registra alta no mercado internacional"
```

A página deverá permitir mostrar:

```text
Fontes relacionadas: 3
```

Isso cria uma experiência mais próxima de uma plataforma de inteligência editorial.

---

# 24. Fontes

Página:

```text
/fontes.html
```

Objetivo: explicar de onde vêm as informações.

Estrutura:

```text
FONTES DO TAN

O TAN utiliza diferentes fontes públicas e jornalísticas para acompanhar o agronegócio.

[Fonte A]
[Fonte B]
[Fonte C]

Como selecionamos e processamos as informações
```

Cada notícia deverá manter a referência da fonte original.

---

# 25. Metodologia — `/metodologia.html`

Esta página explica a operação editorial/tecnológica.

## Seções

### Coleta

Como as notícias são obtidas.

### Normalização

Como títulos, datas e textos são padronizados.

### Classificação

Como as notícias recebem categorias.

### NLP

Como são produzidos:

- resumos;
- entidades;
- tópicos;
- agrupamentos;
- relevância.

### Revisão

Caso exista etapa humana, explicar que conteúdos podem passar por revisão editorial.

### Transparência

Explicar claramente que o TAN é uma camada de organização e informação e deve manter referência às fontes originais.

---

# 26. Sobre — `/sobre.html`

Conteúdo institucional.

## Estrutura

```text
SOBRE O TAN

O que somos

Por que existimos

Como ajudamos o leitor

Nossa visão

Contato
```

Exemplo:

> O TAN nasceu com a proposta de tornar o fluxo de informações do agronegócio mais simples de acompanhar, conectando notícias, contexto e tecnologia em uma única experiência.

---

# 27. Busca — `/busca.html`

A busca deve permitir encontrar:

- notícias;
- categorias;
- entidades;
- commodities;
- regiões.

Interface:

```text
[ Digite sua busca... ] [Buscar]

RESULTADOS

12 resultados encontrados

[Card]
[Card]
[Card]
```

No MVP estático, pode funcionar apenas visualmente.

Em uma versão dinâmica, a busca poderá utilizar:

- índice textual;
- Elasticsearch/OpenSearch;
- banco de dados;
- busca semântica;
- embeddings.

---

# 28. Categorias

Cada categoria deve possuir uma landing page.

Exemplo:

```text
/categorias/agricultura.html
```

Estrutura:

```text
AGRICULTURA

Descrição da categoria

Destaque

Últimas notícias

Mais relevantes

Subcategorias
```

Subcategorias futuras:

```text
Soja
Milho
Café
Algodão
Trigo
Cana
```

---

# 29. Cards de Notícias

Todos os cards devem seguir um componente reutilizável.

## Estrutura

```text
[CATEGORIA]

Título da notícia em até duas ou três linhas.

Resumo curto opcional.

10 SET · 09:42
Fonte

→ Ler notícia
```

Classes/componentes sugeridos:

```text
.news-card
.news-card__category
.news-card__title
.news-card__summary
.news-card__meta
.news-card__source
```

---

# 30. Notícias Relacionadas

Em cada notícia individual:

```text
NOTÍCIAS RELACIONADAS

[Notícia A]
[Notícia B]
[Notícia C]
```

A relação poderá posteriormente ser calculada por NLP usando:

- embeddings;
- similaridade semântica;
- tópicos;
- entidades;
- categoria;
- proximidade temporal.

---

# 31. Layout Responsivo

O site deverá funcionar em:

- desktop;
- notebook;
- tablet;
- celular.

Breakpoints sugeridos:

```text
mobile: < 768px
tablet: 768–1023px
desktop: >= 1024px
```

No celular:

- cards em uma coluna;
- navegação compacta;
- imagens responsivas;
- títulos reduzidos;
- filtros em menu/dropdown.

---

# 32. Design System

## Identidade

O visual deve combinar:

- jornalismo;
- tecnologia;
- agronegócio;
- credibilidade.

Evitar estética excessivamente "fazenda/rústica".

Preferir:

- layout editorial;
- tipografia forte;
- bastante espaço em branco;
- cards limpos;
- elementos de dados;
- detalhes visuais inspirados em mapas, linhas e gráficos.

## Componentes

Criar componentes reutilizáveis:

```text
Header
Footer
Button
Badge
NewsCard
FeaturedNews
CategoryCard
EditionCard
Breadcrumb
FilterBar
SearchBar
Tag
SourceBadge
EntityTag
RelatedNews
Pagination
```

---

# 33. Footer

Todas as páginas devem conter:

```text
TAN — The Agro News

Notícias
Categorias
Sobre
Metodologia
Fontes

Contato

© TAN — The Agro News
```

Links adicionais futuros:

- Termos de uso;
- Política de privacidade;
- Política editorial;
- Correções.

---

# 34. Rodapé Editorial

Como o projeto trabalha com notícias processadas por tecnologia, é recomendável deixar claro:

> Conteúdo organizado e processado com apoio de tecnologia. Consulte as fontes originais para informações completas.

Isso reforça transparência.

---

# 35. Modelo de Dados

Mesmo no site estático, o conteúdo deve seguir uma estrutura de dados consistente.

## Exemplo de objeto de notícia

```json
{
  "id": "news-0001",
  "slug": "soja-registra-nova-movimentacao-no-mercado",
  "title": "Soja registra nova movimentação no mercado",
  "subtitle": "Mercados externos apresentam novas oscilações",
  "summary": "Resumo curto da notícia.",
  "content": "Texto da notícia...",
  "category": "mercado",
  "subcategory": "commodities",
  "published_at": "2026-09-10T09:42:00-03:00",
  "updated_at": "2026-09-10T10:05:00-03:00",
  "source": {
    "name": "Fonte Exemplo",
    "url": "https://example.com"
  },
  "tags": ["soja", "mercado", "exportação"],
  "entities": ["Brasil", "China"],
  "regions": ["Mato Grosso"],
  "nlp": {
    "importance_score": 0.87,
    "sentiment": "neutral",
    "topics": ["commodities", "exportação"]
  },
  "related_news": ["news-0007", "news-0014"],
  "edition_id": "edition-2026-09-10"
}
```

---

# 36. Modelo de Edição

```json
{
  "id": "edition-2026-09-10",
  "slug": "edicao-10-09-2026",
  "title": "TAN — Edição de 10 de setembro de 2026",
  "date": "2026-09-10",
  "summary": "Resumo geral da movimentação do Agro no dia.",
  "featured_news": "news-0001",
  "news": ["news-0001", "news-0002", "news-0003", "news-0004"]
}
```

---

# 37. Estrutura de Pastas Recomendada

Para o MVP:

```text
tan-agro-news/
│
├── index.html
├── noticias/
│   ├── index.html
│   └── edicao-10-09-2026.html
│
├── noticia/
│   ├── soja-movimentacao.html
│   └── mercado-milho.html
│
├── categorias/
│   ├── agricultura.html
│   ├── pecuaria.html
│   ├── mercado.html
│   ├── tecnologia.html
│   ├── clima.html
│   ├── politica.html
│   └── sustentabilidade.html
│
├── busca.html
├── sobre.html
├── metodologia.html
├── fontes.html
├── 404.html
│
├── assets/
│   ├── css/
│   │   ├── reset.css
│   │   ├── variables.css
│   │   ├── global.css
│   │   ├── components.css
│   │   └── responsive.css
│   │
│   ├── js/
│   │   ├── main.js
│   │   ├── navigation.js
│   │   ├── search.js
│   │   └── filters.js
│   │
│   └── images/
│
└── data/
    ├── editions.json
    └── news.json
```

---

# 38. Arquitetura Preparada para NLP

O front-end não deve depender diretamente de como o NLP funciona.

O fluxo futuro recomendado:

```text
Fontes
   ↓
Coleta
   ↓
Limpeza / Normalização
   ↓
NLP
   ├── Classificação
   ├── Sumarização
   ├── Entidades
   ├── Tópicos
   ├── Similaridade
   └── Relevância
   ↓
Banco / API
   ↓
Frontend TAN
```

O front-end deve apenas consumir um modelo de conteúdo padronizado.

---

# 39. Pipeline Futuro de NLP

Exemplo:

```text
RAW ARTICLE
      ↓
Language Detection
      ↓
Text Cleaning
      ↓
Deduplication
      ↓
Named Entity Recognition
      ↓
Topic Classification
      ↓
Summarization
      ↓
Event Clustering
      ↓
Importance Scoring
      ↓
Editorial Output
```

---

# 40. Estrutura de Dados para o NLP

É importante separar os dados editoriais dos dados derivados.

### Dados originais

```text
source
url
title
content
published_at
```

### Dados normalizados

```text
normalized_title
normalized_content
language
```

### Dados NLP

```text
summary
entities
topics
sentiment
importance_score
embedding
cluster_id
```

### Dados editoriais

```text
category
featured
edition_id
display_order
```

Isso facilita alterar o modelo de NLP sem quebrar a camada visual.

---

# 41. Recursos que Podem Entrar no MVP

Além das páginas básicas, o MVP deve deixar espaços preparados para:

### Newsletter

```text
Receba a edição do TAN por e-mail.
[seu@email.com] [Assinar]
```

### Compartilhamento

- WhatsApp;
- LinkedIn;
- copiar link;
- compartilhar nativamente no mobile.

### Bookmark

Futuramente:

```text
☆ Salvar notícia
```

### Indicadores

Exemplo:

```text
+12% interesse
4 fontes relacionadas
7 notícias sobre soja hoje
```

---

# 42. SEO

Cada notícia deve possuir:

```html
<title>
<meta name="description">
<link rel="canonical">
```

Também é recomendável implementar futuramente:

- Open Graph;
- Twitter/X Cards;
- Schema.org `NewsArticle`;
- sitemap.xml;
- robots.txt;
- URLs semânticas.

Exemplo:

```text
https://tan.agro/noticia/soja-registra-nova-movimentacao
```

---

# 43. Performance

Como o MVP será estático:

- imagens comprimidas;
- lazy loading;
- CSS enxuto;
- JavaScript modular;
- fontes otimizadas;
- evitar dependências desnecessárias.

Priorizar carregamento rápido da Home e da página de notícias.

---

# 44. Acessibilidade

Requisitos mínimos:

- HTML semântico;
- contraste adequado;
- `alt` nas imagens;
- navegação por teclado;
- foco visível;
- hierarquia correta de títulos;
- botões com labels claros;
- áreas clicáveis adequadas no mobile.

---

# 45. Analytics

A estrutura deve prever eventos como:

```text
page_view
news_open
category_open
search
source_click
share_click
edition_open
newsletter_signup
```

Isso permitirá descobrir:

- quais temas possuem maior interesse;
- quais notícias performam melhor;
- quais categorias geram retenção;
- quais termos são mais buscados.

---

# 46. Estados de Interface

Cada tela deverá prever:

## Loading

Skeleton cards.

## Empty State

Exemplo:

> Nenhuma notícia encontrada para este filtro.

## Error State

Exemplo:

> Não foi possível carregar as notícias.

## 404

Exemplo:

> Esta notícia não existe ou foi removida.

Botão:

**Voltar para o TAN**

---

# 47. Interligação das Páginas

Fluxo principal:

```text
HOME
 │
 ├──→ Edição de Hoje
 │       │
 │       ├──→ Notícia A
 │       ├──→ Notícia B
 │       └──→ Notícia C
 │
 ├──→ Notícias
 │       └──→ Edições
 │
 ├──→ Categorias
 │       ├──→ Agricultura
 │       ├──→ Pecuária
 │       ├──→ Mercado
 │       ├──→ Tecnologia
 │       ├──→ Clima
 │       └──→ Política
 │
 ├──→ Sobre
 │
 └──→ Metodologia
```

Fluxo da notícia:

```text
Notícia
 │
 ├──→ Categoria
 │
 ├──→ Fonte original
 │
 ├──→ Entidades
 │
 └──→ Notícias relacionadas
          └──→ Outra notícia
```

---

# 48. Exemplo de Conteúdo Mockado

## Edição

**TAN — Edição de 10 de setembro de 2026**

> O agronegócio brasileiro inicia o dia marcado por movimentações nos mercados de commodities, novas projeções climáticas e avanços em soluções tecnológicas para o campo.

### Destaques

**Mercado**  
Soja registra nova movimentação nos mercados internacionais.

**Clima**  
Novas projeções indicam mudanças no padrão de chuvas em regiões produtoras.

**Tecnologia**  
AgTech apresenta solução baseada em inteligência artificial para monitoramento de lavouras.

**Pecuária**  
Mercado acompanha novas perspectivas para os preços do gado.

---

# 49. Exemplo de Notícia Mockada

## Soja registra nova movimentação no mercado internacional

**Mercado · 10 de setembro de 2026 · 09:42**

Os mercados internacionais registraram novas oscilações no comércio de soja nesta quinta-feira. Analistas acompanham o comportamento da demanda e as condições das principais regiões produtoras.

### Resumo TAN

O mercado apresentou novas movimentações e operadores continuam avaliando fatores relacionados à oferta, demanda e exportações.

### Principais pontos

- Mercado internacional apresentou nova oscilação;
- exportadores brasileiros acompanham o cenário;
- demanda externa permanece como fator relevante;
- próximos dados agrícolas podem alterar as expectativas.

### Entidades

**Commodities:** Soja  
**Região:** Brasil  
**Mercado:** Internacional

### Fonte

Fonte Exemplo

> O texto acima é apenas conteúdo demonstrativo para o MVP.

---

# 50. Requisitos Funcionais

## RF01

O usuário deve conseguir acessar a Home.

## RF02

O usuário deve conseguir acessar a edição atual.

## RF03

O usuário deve conseguir abrir notícias individualmente.

## RF04

O usuário deve conseguir navegar entre categorias.

## RF05

O usuário deve conseguir retornar à Home a partir de qualquer página.

## RF06

O usuário deve conseguir acessar fontes originais.

## RF07

O usuário deve conseguir visualizar notícias relacionadas.

## RF08

O usuário deve conseguir utilizar a busca visualmente no MVP.

## RF09

O sistema deve suportar conteúdo organizado por data.

## RF10

A estrutura deve permitir substituir conteúdo estático por API futuramente.

---

# 51. Requisitos Não Funcionais

## RNF01 — Responsividade

Interface adaptável a desktop, tablet e mobile.

## RNF02 — Performance

Carregamento rápido e baixo uso de JavaScript.

## RNF03 — Acessibilidade

HTML semântico e navegação por teclado.

## RNF04 — SEO

URLs, metadata e estrutura semântica compatíveis com indexação.

## RNF05 — Escalabilidade

Conteúdo desacoplado da camada visual.

## RNF06 — Manutenibilidade

Componentes reutilizáveis.

---

# 52. Prioridade de Implementação

## Fase 1 — Fundação

- Header;
- Footer;
- Design system;
- Home;
- página de notícias;
- página individual;
- páginas de categoria.

## Fase 2 — Editorial

- edição diária;
- notícias relacionadas;
- fontes;
- metodologia;
- mock de NLP.

## Fase 3 — Interatividade

- filtros;
- busca;
- compartilhamento;
- newsletter;
- favoritos.

## Fase 4 — Backend/NLP

- API;
- banco de dados;
- ingestão;
- processamento NLP;
- agrupamento;
- classificação;
- sumarização.

---

# 53. Arquitetura Ideal Pós-MVP

```text
                 ┌──────────────┐
                 │   FRONTEND   │
                 │   TAN Web    │
                 └──────┬───────┘
                        │
                       API
                        │
              ┌─────────┴─────────┐
              │                   │
         News Service        Search Service
              │                   │
              └─────────┬─────────┘
                        │
                 ┌──────▼──────┐
                 │   DATABASE  │
                 └──────┬──────┘
                        │
                NLP / AI PIPELINE
                        │
          ┌─────────────┼─────────────┐
          │             │             │
      Classificação  Resumo      Clustering
          │             │             │
          └─────────────┼─────────────┘
                        │
                  INGESTÃO DE
                    FONTES
```

---

# 54. Princípio Arquitetural Mais Importante

O TAN não deve ser construído como um simples conjunto de páginas HTML.

Mesmo sendo um MVP estático, ele deve ser construído como se o conteúdo futuramente viesse de uma API.

A regra é:

```text
HTML ≠ conteúdo

HTML = estrutura + apresentação

Conteúdo = dados
```

Por isso, notícias e edições devem ser representadas por objetos JSON ou estruturas equivalentes.

Isso permitirá trocar:

```text
data/news.json
```

por:

```text
GET /api/news
```

sem reconstruir o frontend inteiro.

---

# 55. Resultado Esperado do MVP

Ao finalizar a primeira versão, o usuário deve conseguir:

```text
Entrar no TAN
      ↓
Entender o que é
      ↓
Ver a edição de hoje
      ↓
Encontrar uma notícia
      ↓
Abrir a notícia
      ↓
Ler resumo + principais pontos
      ↓
Ver categoria / entidades / relacionadas
      ↓
Voltar para outras notícias
```

A experiência deve parecer a de um **portal editorial profissional**, e não de uma landing page que apenas lista textos.

---

# 56. Checklist de Implementação

### Estrutura

- [ ] Home
- [ ] Notícias
- [ ] Edição
- [ ] Notícia individual
- [ ] Categorias
- [ ] Busca
- [ ] Sobre
- [ ] Metodologia
- [ ] Fontes
- [ ] 404

### Componentes

- [ ] Header
- [ ] Footer
- [ ] News Card
- [ ] Featured News
- [ ] Category Card
- [ ] Breadcrumb
- [ ] Filter Bar
- [ ] Search Bar
- [ ] Related News
- [ ] Source Block
- [ ] Entity Tags

### Conteúdo

- [ ] Edição mockada
- [ ] Notícias mockadas
- [ ] Resumos
- [ ] Entidades
- [ ] Tags
- [ ] Notícias relacionadas

### Preparação para NLP

- [ ] schema JSON
- [ ] campos NLP
- [ ] score de relevância
- [ ] entidades
- [ ] tópicos
- [ ] agrupamento
- [ ] resumo automático

### Qualidade

- [ ] responsividade
- [ ] SEO
- [ ] acessibilidade
- [ ] performance
- [ ] estados vazios
- [ ] 404
- [ ] analytics preparado

---

# 57. Conclusão

O MVP do TAN deve funcionar como um **portal editorial diário especializado em Agro**, com uma arquitetura visual simples para o usuário, mas tecnicamente preparada para uma camada de inteligência baseada em NLP.

A estrutura recomendada possui três níveis:

```text
1. PORTAL
   Home, categorias, busca e páginas institucionais

2. EDIÇÃO
   Uma publicação diária que organiza os acontecimentos

3. NOTÍCIA
   Conteúdo individual com resumo, entidades, tópicos,
   fontes e notícias relacionadas
```

A decisão arquitetural mais importante é manter **conteúdo e apresentação desacoplados** desde o primeiro protótipo. Isso permite que o MVP seja estático hoje e evolua para uma plataforma alimentada por API + banco + pipeline NLP sem necessidade de reconstruir o produto.

## Próxima etapa recomendada

Implementar primeiro a estrutura visual completa utilizando dados mockados em JSON:

```text
data/news.json
data/editions.json
```

Depois, construir:

```text
Home → Edição → Notícia → Categoria → Relacionadas
```

Somente após esse fluxo estar funcional, conectar o pipeline de NLP e a API real.
