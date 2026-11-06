# Persona "The News Agro" — Dupla A (Matheus & Nicolas)

Este módulo implementa a **Engenharia da Persona "The News Agro" (Sprint 1 - Card 19 / US-3)**.

## 🎯 Objetivo
Transformar matérias agrícolas burocráticas, relatórios maçantes e cotações sonolentas em uma leitura matinal ágil, informativa e descontraída, com sarcasmo na medida certa e foco no bolso do produtor rural.

---

## 🏗️ Estrutura de Arquivos

```text
Persona/
├── system_prompt.py  # System Prompt oficial com regras de tom e voz
├── few_shots.py      # Exemplos de referência contextualizados no Agro (Few-Shot)
└── test_persona.py   # Script de validação automática dos critérios de aceite
```

---

## 📐 Estrutura Obrigatória dos 4 Blocos
Cada notícia reescrita pelo modelo obedece rigorosamente à seguinte divisão:
1. **[TÍTULO COM TROCADILHO]** — Criativo, espirituoso e direto.
2. **[O QUE ROLOU]** — O fato em 1 ou 2 parágrafos curtos.
3. **[POR QUE ISSO IMPORTA]** — A tradução prática: como isso mexe com o bolso do produtor.
4. **[O NÚMERO EM DESTAQUE]** — O dado quantitativo central da matéria.

---

## ✅ Critérios de Aceite Atendidos
- **100% de conformidade com os 4 blocos.**
- **Limite rigoroso de 180 palavras por matéria** (leitura em menos de 1 minuto).
- **Tradução de jargões técnicos** (*barter*, *hedge*, *backwardation*) em linguagem simples e analogias do cotidiano rural.

---

## 🧪 Como Testar a Validação

Para rodar a bateria de testes de validação dos critérios de aceite:

```bash
python -m Persona.test_persona
```

## Gerar uma matéria com Gemini

Instale as dependências Python e configure uma chave da Gemini API no ambiente. A chave não deve ser colocada no código nem enviada ao navegador:

```powershell
pip install -r requirements.txt
$env:GEMINI_API_KEY = "sua-chave"
python -m Persona.gerar_materia --news-id news-001
```

O comando usa os textos da notícia e das notícias relacionadas já existentes em `src/content/news/`, solicita a matéria ao Gemini e só a salva se passar pela auditoria editorial. O resultado fica no campo `persona` do JSON da notícia e aparece na respectiva página do site; como o site é estático, o build/deploy deve ser atualizado para publicar a alteração. O modelo padrão é `gemini-2.5-flash`; é possível escolher outro com a variável `GEMINI_MODEL`.

O scraper não é obrigatório: este fluxo usa as notícias já cadastradas. Para publicar uma matéria gerada, configure a variável de ambiente também no ambiente de build e execute o comando antes do build.
