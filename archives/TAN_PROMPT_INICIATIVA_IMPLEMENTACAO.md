# Prompt de Iniciativa — Transformação Profissional do TAN

> **Documento-base obrigatório:** `TAN_GUIA_BASE_ARQUITETURA_PROFISSIONAL.md`

---

## PROMPT

Atue como um **Staff/Principal Frontend Engineer especializado em sites editoriais, SSG, arquitetura web, SEO técnico, acessibilidade, performance e engenharia de frontend de produção**.

Você recebeu um projeto chamado **TAN — The Agro News**.

O arquivo `TAN_GUIA_BASE_ARQUITETURA_PROFISSIONAL.md` é o **documento normativo principal desta tarefa**. Leia-o integralmente antes de modificar qualquer código.

O projeto também possui uma especificação funcional/editorial existente (`TAN_The_Agro_News_Especificacao_MVP.md`). Essa especificação define a intenção do produto e deve ser preservada, mas este documento prevalece quando a decisão envolver arquitetura, qualidade de código, build, SEO, acessibilidade, performance e manutenção.

---

# 1. OBJETIVO DA INICIATIVA

Transformar o projeto atual em uma **base de frontend estático extremamente profissional, organizada, otimizada, eficiente e pronta para deploy**, mantendo a identidade visual e a intenção editorial do TAN.

### Importante

Esta etapa **NÃO é a implementação do modelo/NLP/API**.

O site deve permanecer baseado em **dados mockados/estáticos**, porém a arquitetura deve ser preparada para que uma futura integração substitua a fonte de dados sem exigir reconstrução do frontend.

Em outras palavras:

```text
AGORA
conteúdo mockado
      ↓
SSG / build
      ↓
site estático profissional

FUTURO
modelo/API
      ↓
mesmo contrato de dados
      ↓
frontend TAN
```

Não invente funcionalidades futuras apenas para tornar o projeto “mais completo”. Nesta fase, qualidade arquitetural é mais importante que quantidade de recursos.

---

# 2. DOCUMENTO DE AUTORIDADE

Use `TAN_GUIA_BASE_ARQUITETURA_PROFISSIONAL.md` como um **contrato técnico de implementação**.

Você deve obedecer especialmente:

- escopo e fora de escopo;
- arquitetura-alvo;
- estrutura de pastas;
- princípios de desacoplamento;
- regras de routing;
- SEO;
- performance;
- acessibilidade;
- segurança;
- contratos de dados;
- fases de implementação;
- Definition of Done;
- regras de atuação do executor.

Não contradiga o documento-base sem apresentar uma justificativa técnica forte.

---

# 3. ANTES DE CODIFICAR: AUDITORIA OBRIGATÓRIA

Primeiro inspecione o projeto inteiro.

Mapeie pelo menos:

```text
arquivos
páginas
CSS
JS
dados
links internos
rotas
metadados
sitemap
robots
dependências
scripts
padrões repetidos
hardcodes
uso de innerHTML
hidratação client-side
```

Leia também a especificação funcional existente e identifique o que deve ser preservado.

### Não faça uma migração cega.

Produza primeiro um diagnóstico técnico curto contendo:

1. arquitetura atual;
2. principais problemas;
3. o que será preservado;
4. o que será substituído;
5. arquitetura-alvo;
6. ordem de execução.

Depois comece a implementação.

---

# 4. DIREÇÃO TECNOLÓGICA

Adote **Astro + TypeScript** como arquitetura preferencial, salvo se uma limitação objetiva do projeto tornar isso inviável.

O resultado deve usar Astro principalmente como **gerador estático de conteúdo**, e não como uma SPA.

### Regra fundamental

Não transportar a arquitetura atual de:

```text
HTML vazio → JS → innerHTML → conteúdo
```

para dentro do Astro.

O objetivo é obter:

```text
conteúdo → build → HTML completo
```

JavaScript deve existir somente quando uma interação realmente exigir JavaScript.

---

# 5. EXECUTE EM FASES

Execute exatamente nesta ordem lógica.

## FASE 0 — Inventário

- analisar o repositório;
- mapear páginas;
- mapear dados;
- mapear componentes;
- mapear dependências;
- identificar duplicações;
- identificar hardcodes;
- identificar falhas de SEO;
- identificar gargalos de performance;
- identificar problemas de acessibilidade.

### Entrega da fase

Um diagnóstico curto no seu relatório de execução.

---

## FASE 1 — Fundação do projeto

Criar/ajustar:

```text
package.json
Astro
TypeScript
configuração global
lint
Prettier
estrutura src/public
```

Criar scripts equivalentes a:

```bash
npm run dev
npm run build
npm run preview
npm run lint
npm run format
npm run format:check
```

### Critério de passagem

```text
npm install
npm run build
```

devem funcionar sem erros estruturais.

---

## FASE 2 — Migrar e organizar o Design System

Preserve a identidade atual do TAN.

Não redesenhe a marca sem necessidade.

Centralize:

```text
cores
typography
spacing
radius
shadow
breakpoints
container widths
```

Remova estilos inline repetidos quando a substituição puder ser feita de forma limpa.

Transforme elementos repetidos em componentes reutilizáveis.

### Critério de passagem

Comparar visualmente antes/depois e corrigir regressões evidentes.

---

## FASE 3 — Conteúdo e contratos de dados

Migrar os dados existentes para uma estrutura adequada ao SSG.

Criar tipos/interfaces para:

```text
NewsItem
Edition
Category
Source
Entity
NlpData
```

Criar validação de schema.

O build deve falhar quando dados obrigatórios estiverem inválidos.

### Importante

Não alterar arbitrariamente o conteúdo editorial.

Não apagar campos úteis ao modelo futuro.

Não acoplar o frontend à futura API.

---

## FASE 4 — Templates e páginas

Criar layouts e rotas para:

```text
/
/noticias/
/noticias/[slug]/
/noticia/[slug]/
/categorias/
/categorias/[slug]/
/busca/
/sobre/
/metodologia/
/fontes/
/404
```

As páginas individuais de notícia precisam existir como **HTML real no resultado final do build**.

### Corrigir obrigatoriamente

Trocar:

```text
/noticia/index.html?id=news-001
```

por:

```text
/noticia/slug-da-noticia/
```

Não use IDs internos como mecanismo principal de navegação editorial.

---

# 6. ELIMINAR DUPLICAÇÕES E HARDCODES

Procure e remova padrões como:

```text
edicao-10-09-2026
```

espalhados por HTML/JS.

Datas, slugs, títulos e URLs devem ser derivados da fonte de dados.

### Regra

Se uma informação existe no conteúdo estruturado, não copie manualmente a mesma informação para vários arquivos.

---

# 7. SEO DE PRODUÇÃO

Implemente metadata por página e por notícia.

Cada conteúdo público relevante deve gerar:

```text
title
description
canonical
Open Graph
Twitter/X
structured data
```

Notícias devem gerar `NewsArticle`/`Article` no HTML final/build-time.

Não depender de `document.title` ou de injeção client-side para SEO básico.

Sitemap deve ser gerado automaticamente a partir das rotas reais.

Robots.txt deve ser coerente com o ambiente.

Adicionar RSS quando tecnicamente apropriado.

---

# 8. PERFORMANCE

O resultado deve ser static-first.

### Não fazer

```text
baixar todo o acervo para abrir a home
baixar todo o conteúdo para abrir uma notícia
usar JS onde HTML resolve
usar biblioteca pesada para componente simples
```

### Fazer

```text
pré-rendering
bundle mínimo
imagens otimizadas
fontes bem controladas
CSS enxuto
lazy loading contextual
```

Avaliar Pagefind para busca estática.

---

# 9. ACESSIBILIDADE

Use HTML semântico e referência WCAG 2.2 AA.

Verifique:

```text
headings
landmarks
keyboard navigation
focus-visible
skip link
aria-expanded
aria-controls
accessible names
alt text
contraste
```

O menu mobile deve ter estado acessível.

Nenhuma interação crítica pode depender exclusivamente de hover.

---

# 10. SEGURANÇA

Revise o uso de:

```text
innerHTML
dados externos
links
URLs
scripts
```

Evite renderização insegura de conteúdo.

Nenhuma chave, token ou segredo deve ser inserido no frontend.

Não crie uma API falsa apenas para justificar arquitetura.

---

# 11. BUSCA

A busca desta etapa deve trabalhar sobre o conteúdo estático existente.

Priorize uma solução de busca indexada e compatível com SSG, preferencialmente Pagefind.

Não transforme a busca em um sistema de IA.

Isso pertence à etapa futura.

---

# 12. IMAGENS E CONTEÚDO EDITORIAL

Criar um modelo consistente para:

```text
hero image
thumbnail
alt text
```

Quando existirem imagens reais/adequadas no projeto, integrá-las corretamente.

Quando não existirem, não inventar uma biblioteca visual enorme.

O importante nesta fase é preparar a arquitetura.

---

# 13. ESTADOS DE INTERFACE

Revisar:

```text
loading
empty
error
404
```

Não adicionar estados artificiais onde não existe carregamento assíncrono real.

---

# 14. CI/CD

Criar uma configuração mínima de CI para:

```text
install
lint
format check
build
```

Preparar o projeto para deploy estático.

Não acoplar a arquitetura a um provedor sem necessidade.

---

# 15. VALIDAÇÃO OBRIGATÓRIA APÓS A IMPLEMENTAÇÃO

Execute tudo o que estiver disponível, pelo menos:

```bash
npm run lint
npm run format:check
npm run build
```

Depois faça uma revisão de smoke test das principais rotas.

Valide também:

```text
links internos
sitemap
robots
metadata
canonical
JSON-LD
404
responsividade
menu mobile
busca
```

Se algo falhar, **corrija antes de considerar a fase encerrada**.

---

# 16. REGRA DE QUALIDADE

Não aceite uma solução apenas porque “funciona”.

Use estas perguntas:

### Arquitetura

- O conteúdo está separado da apresentação?
- O build gera páginas reais?
- Existe fonte única dos dados?
- Há duplicação desnecessária?
- O frontend está desacoplado do backend futuro?

### SEO

- O conteúdo está presente no HTML?
- Cada página tem metadata própria?
- O sitemap reflete as rotas reais?
- Há canonical consistente?

### Performance

- O JS enviado é realmente necessário?
- O conteúdo principal bloqueia o carregamento?
- As imagens estão adequadas?

### Acessibilidade

- A página pode ser usada por teclado?
- O foco é perceptível?
- O markup é semântico?

### Manutenção

- Alterar uma edição exige editar 10 arquivos manualmente?
- Adicionar uma nova categoria exige duplicar HTML?
- Adicionar 100 notícias exige criar 100 templates?

Se a resposta for “sim”, a arquitetura ainda não está pronta.

---

# 17. COMPORTAMENTO ESPERADO DURANTE A EXECUÇÃO

Trabalhe de forma incremental.

Após cada fase:

```text
1. resumir alteração;
2. validar build/testes;
3. registrar problemas encontrados;
4. corrigir regressões;
5. avançar somente quando a fase estiver estável.
```

Não faça uma grande reescrita opaca sem validações intermediárias.

---

# 18. RESTRIÇÕES IMPORTANTES

### Não implementar agora

```text
❌ integração real com IA
❌ API de produção
❌ banco
❌ login
❌ CMS
❌ crawler
❌ recomendação inteligente
❌ personalização
❌ microserviços
❌ infraestrutura complexa
```

### Implementar agora

```text
✅ arquitetura
✅ SSG
✅ conteúdo estruturado
✅ componentes
✅ rotas
✅ SEO
✅ performance
✅ acessibilidade
✅ busca estática
✅ validação
✅ build
✅ CI
✅ documentação
```

---

# 19. Definition of Done

Não encerre a iniciativa até que seja possível marcar:

```text
[ ] Projeto com arquitetura SSG profissional
[ ] Astro configurado
[ ] TypeScript configurado
[ ] Conteúdo estruturado
[ ] Schemas/validação
[ ] Layouts/componentes reutilizáveis
[ ] URLs semânticas
[ ] Notícias pré-renderizadas
[ ] SEO completo
[ ] JSON-LD build-time
[ ] Sitemap automático
[ ] Robots configurado
[ ] Busca preparada para crescimento
[ ] Design preservado/refinado
[ ] Responsividade revisada
[ ] Acessibilidade revisada
[ ] Imagens tratadas arquiteturalmente
[ ] Sem hardcodes editoriais críticos
[ ] Sem dependência de JS para conteúdo principal
[ ] Lint funcionando
[ ] Format check funcionando
[ ] Build funcionando
[ ] Smoke test das rotas principais
[ ] CI preparada
[ ] README atualizado
[ ] Nenhuma integração futura inventada
```

---

# 20. FORMATO DO RELATÓRIO FINAL

Ao concluir, responda com:

## A. Resumo executivo

Explique em poucas linhas o que mudou.

## B. Arquitetura anterior → arquitetura final

Mostre a transformação de forma objetiva.

## C. Principais problemas corrigidos

Liste os problemas mais importantes e como foram resolvidos.

## D. Estrutura final

Mostre a árvore principal do projeto.

## E. Validações executadas

Mostre os comandos usados e seus resultados.

## F. Débitos técnicos restantes

Somente problemas reais que ainda existirem.

## G. Preparação para o modelo futuro

Explique quais contratos/interfaces estão prontos para receber API/NLP posteriormente.

Não inclua novas funcionalidades apenas como “ideias legais”.

---

# 21. DECISÃO FINAL

Sua missão não é transformar o TAN no maior sistema possível.

Sua missão é transformar o TAN em uma **base editorial estática profissional, rápida, semântica, acessível, indexável, testável, manutenível e pronta para deploy**, sem criar dívida técnica desnecessária.

A futura integração do modelo deve entrar por uma fronteira clara de dados.

Use esta regra durante toda a implementação:

> **Hoje: construir a melhor casca editorial possível. Amanhã: conectar inteligência a essa casca sem precisar reconstruí-la.**
