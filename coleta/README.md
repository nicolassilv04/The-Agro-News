# Módulo de Automação de Coleta e Agendamento — The Agro News (TAN)

Este módulo implementa a **Automação Agendada da Coleta de Matérias (Sprint 2 - Card 8.7 / Dupla A)**, integrando agendamento em background com **APScheduler**, verificação prévia no banco contra reprocessamento/duplicação de URLs e sistema completo de auditoria e logs.

---

## 🎯 Funcionalidades Implementadas

1. **Agendador em Background (APScheduler):**
   - Disparos periódicos a cada **3 horas** (`IntervalTrigger(hours=3)`).
   - Configurado com `coalesce=True`, `max_instances=1` e `misfire_grace_time=300` para proteger contra execuções sobrepostas.
   - Tratamento de sinais (`SIGINT`, `SIGTERM`) para encerramento gracioso (*Graceful Shutdown*).

2. **Deduplicação e Verificação Prévia:**
   - **Triagem Prévia:** Antes de realizar o download e o parsing pesado de uma matéria, o sistema consulta se a URL já existe no banco (`SELECT 1 FROM artigos WHERE url = ?`).
   - URLs já cadastradas são descartadas imediatamente, reduzindo o tempo de execução e consumo de rede.
   - **Restrição de Integridade:** Coluna `url UNIQUE` na tabela `artigos` com cláusula `ON CONFLICT(url) DO NOTHING`, garantindo total blindagem contra duplicatas.

3. **Sistema de Log e Auditoria:**
   - Logs em disco com rotação automática (`logs/coleta.log`) com limite de 5MB e até 5 arquivos de histórico (`RotatingFileHandler`).
   - Saída simultânea no console (`stdout`).
   - Registro exato de horários de início e término, duração em segundos, contagem de links encontrados, ignorados, novos inseridos e exceções.
   - Tabela de banco `coleta_execucoes` registrando o histórico de cada ciclo para auditoria.

4. **Scraping Resiliente para os 5 Portais Agro:**
   - TheAgriBiz, AgFeed, Agrolink, Canal Rural e Notícias Agrícolas.
   - Descoberta híbrida (Feed RSS + Fallback HTML da home).
   - Limpeza profissional com `trafilatura` e `BeautifulSoup` (removendo menus, anúncios, scripts e rodapés institucionais).

---

## 🚀 Como Executar

### 1. Instalar dependências
```powershell
python -m pip install apscheduler trafilatura beautifulsoup4 feedparser requests
```

### 2. Executar um único ciclo de coleta imediatamente
Ideal para testes ou cron jobs externos:
```powershell
python -m coleta.agendador --run-once
```

### 3. Iniciar o agendador contínuo (a cada 3 horas)
Executa de forma autônoma e ininterrupta:
```powershell
python -m coleta.agendador
```
*Dica: use `--no-run-on-start` se não desejar executar uma rodada de imediato.*

### 4. Consultar estatísticas e última execução
```powershell
python -m coleta.agendador --status
```

---

## 🧪 Como Rodar a Suíte de Testes

Os testes automatizados validam o intervalo do agendador, a triagem prévia contra links repetidos, o bloqueio de duplicatas e a tolerância a falhas:

```powershell
python -m unittest coleta.test_coleta
```
