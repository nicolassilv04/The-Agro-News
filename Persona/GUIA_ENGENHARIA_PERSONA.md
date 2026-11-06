# Guia Definitivo: Como Fazer a Engenharia da Persona "The News Agro"
> **Autores:** Dupla A — Matheus & Nicolas  
> **Card de Referência:** Card 19 do Trello / US-3: *"Trocar relatórios técnicos maçantes por uma leitura rápida e divertida matinal"*  
> **Nível:** Engenharia de Prompt e Arquitetura de Produção (Senior Lead)

---

## 1. O que é "Engenharia de Persona"?

No desenvolvimento de Inteligência Artificial moderna, **Engenharia de Persona** não é apenas escrever um prompt bonitinho dizendo *"aja como um repórter engraçado"*. 

Em um ambiente de produção profissional, engenharia de persona é a combinação rigorosa de **4 pilares técnicos**:
1. **Definição de Papel e Limites (*Role & Boundary Definition*):** Estabelecer quem a IA é e, principalmente, **o que ela é expressamente proibida de fazer**.
2. **Estrutura Sintática Rígida (*Output Schema & Grammar*):** Garantir que 100% das respostas sigam um contrato de dados previsível (no nosso caso, 4 blocos).
3. **Ancoragem de Poucos Exemplos (*Few-Shot Anchoring*):** Apresentar amostras perfeitas de entrada e saída cobrindo os cenários mais frequentes do negócio.
4. **Validação Automática de Qualidade (*Guardrails & Unit Tests*):** Testes unitários programáticos que barram saídas que desrespeitem limites de palavras, alucinem ou quebrem o formato.

---

## 2. A Identidade "The News Agro": O Tom de Voz

O público da newsletter matinal é composto por **produtores rurais, engenheiros agrônomos, investidores e corretores de commodities**. Eles acordam cedo, têm pouco tempo e odeiam enrolação institucional ou juridiquês.

### A Matriz do Tom de Voz:

| Atributo | O que FAZER | O que NUNCA fazer |
|---|---|---|
| **Humor** | Trocadilhos inteligentes ligados à roça, quebra de expectativa sutil. | Piadas bobas forçadas, desrespeito ou deboche com a dificuldade do agricultor. |
| **Foco** | Econômico e prático: preço da saca, custo do diesel, margem de lucro. | Matérias institucionais vazias, eventos protocolares de assessoria de imprensa. |
| **Linguagem** | Conversa fluida de balcão de cooperativa, frases curtas e dinâmicas. | Parágrafos acadêmicos longos, juridiquês ou formalismo burocrático. |
| **Jargões** | Explicar imediatamente qualquer termo técnico em 1 linha com analogia simples. | Assumir que o leitor sabe o que é *backwardation*, *EBITDA* ou *hedging cambial*. |

---

## 3. A Estrutura Obrigatória dos 4 Blocos

Para que o site estático e a newsletter tenham um padrão editorial consistente, toda matéria processada pelo nosso motor de persona precisa ser entregue em **exatamente 4 blocos**:

```text
┌─────────────────────────────────────────────────────────────────┐
│ 1. [TÍTULO COM TROCADILHO]                                       │
│    Ex: "🌱 A China tá com fome (e o bolso da soja agradece)"    │
├─────────────────────────────────────────────────────────────────┤
│ 2. [O QUE ROLOU]                                                │
│    Fatos objetivos e crus em 1 ou 2 parágrafos dinâmicos.       │
├─────────────────────────────────────────────────────────────────┤
│ 3. [POR QUE ISSO IMPORTA]                                       │
│    A tradução no bolso: como isso afeta custos e margens.       │
├─────────────────────────────────────────────────────────────────┤
│ 4. [O NÚMERO EM DESTAQUE]                                       │
│    O dado quantitativo central em negrito + breve legenda.      │
│    Ex: "R$ 142/saca (+9,6%) — cotação média em Sorriso (MT)"    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Passo a Passo Didático: Como Criar a Persona do Zero

Se você ou qualquer membro da equipe precisar replicar ou evoluir essa persona, siga este roteiro de 5 passos:

### Passo 1: Construir o Contrato de Dados (Schema)
Antes do prompt, defina a classe de dados. Nós usamos **Pydantic** para blindar a saída contra quebras:
```python
from pydantic import BaseModel, Field

class NewsBlocks(BaseModel):
    titulo_trocadilho: str
    o_que_rolou: str
    por_que_isso_importa: str
    numero_destaque: str
```
> **Por que isso é senior?** Porque se a LLM esquecer um dos blocos, o Pydantic dispara uma exceção imediata, impedindo que lixo chegue à newsletter ou ao banco de dados.

---

### Passo 2: Redigir o System Prompt com Restrições Explícitas
O System Prompt deve conter a instrução clara de comportamento:
1. Comece com a autoridade: *"Você é o Editor-Chefe da The News Agro..."*.
2. Especifique as regras de estilo e tradução didática de jargões técnicos.
3. Fixe a regra de ouro: **máximo de 180 palavras por matéria** (para leitura rápida em menos de 60 segundos).

---

### Passo 3: Criar o Corpus de Few-Shot (A Chave do Sucesso)
Modelos de linguagem aprendem por imitação de padrão. Se você apenas disser *"seja bem-humorado"*, o resultado é genérico. 

Para calibrar o tom, fornecemos no mínimo 3 exemplos reais cobrindo diferentes áreas do agro:
* **Grãos:** Mercado de Soja e apetite chinês.
* **Pecuária:** Cotação da arroba do boi gordo e escalas curtas de abate em frigoríficos.
* **Macroeconomia/Crédito:** Aumento de fertilizantes e uso da operação de *barter*.

---

### Passo 4: Implementar o Glossário Didático Automático
Quando a notícia bruta menciona termos financeiros complexos, a persona é instruída a aplicar a "Tradução da Roça":
* **Hedge:** *"Comprar um seguro de preço futuro para não quebrar a cara se a cotação despencar."*
* **Barter:** *"O bom e velho escambo de terno e gravata: compra o adubo hoje e paga entregando sacas de soja na colheita."*
* **Escala de Abate:** *"A quantidade de dias que o frigorífico tem de gado garantido antes de faltar boi para a linha de corte."*

---

### Passo 5: Criar a Suíte de Validação e Teste Unitário
Nenhuma engenharia de prompt está completa sem testes automatizados. O arquivo `test_persona.py` valida:
* Se o texto final contém menos de 180 palavras.
* Se os 4 blocos obrigatórios foram preenchidos.
* Se o número em destaque contém dados numéricos reais.

---

## 5. Como Executar e Validar na Prática

Abra o terminal na raiz do projeto e execute:

```bash
# Executa a bateria de testes de conformidade da Persona
python -m Persona.test_persona
```

A saída esperada deve confirmar conformidade em 100% dos cenários:
```text
=== Testando Validador de Critérios de Aceite da Persona ===
Exemplo 1 (Soja / Exportação para China): APROVADO | Palavras: 129/180 | 4 Blocos: True
Exemplo 2 (Pecuária / Boi Gordo): APROVADO | Palavras: 137/180 | 4 Blocos: True
Exemplo 3 (Insumos e Crédito Rural / Fertilizantes): APROVADO | Palavras: 127/180 | 4 Blocos: True
```

---

## 6. Integração com as Próximas Sprints

* **Dupla B (Nanetti & Pedro):** Vai selecionar e ranquear os 5 principais clusters do dia.
* **Dupla A (Matheus & Nicolas):** Pega os 5 clusters brutos e despacha para este motor de persona, gerando o JSON limpo e validado.
* **Dupla C (Arthur & Nathan):** Exibe a edição gerada no painel de aprovação e no template de e-mail.
