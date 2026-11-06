"""
Configurações da automação de coleta de notícias do TAN (The Agro News).
Sprint 2 - Dupla A (Card 8.7 / US-7).
"""

import os
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Banco de dados
# Permite PostgreSQL via DATABASE_URL ou SQLite local por padrão
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATA_DIR / 'tan_news.db'}")
SQLITE_DB_PATH = DATA_DIR / "tan_news.db"

# Logs
LOG_FILE_PATH = LOGS_DIR / "coleta.log"
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB por arquivo
LOG_BACKUP_COUNT = 5              # 5 arquivos de histórico rotativo

# Agendador
INTERVALO_HORAS_PADRAO = 3        # Disparo a cada 3 horas
MISFIRE_GRACE_TIME = 300          # 5 minutos de tolerância caso o sistema hiberne/atrase

# Scraping e requisições HTTP
DEFAULT_TIMEOUT = 15              # segundos por requisição
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 (The Agro News Ingestion Bot)"
)
REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

# 5 Portais oficiais definidos no PRD
PORTAIS_CONFIG = {
    "TheAgriBiz": {
        "url_base": "https://theagribiz.com",
        "feed_url": "https://theagribiz.com/feed/",
    },
    "AgFeed": {
        "url_base": "https://agfeed.com.br",
        "feed_url": "https://agfeed.com.br/feed/",
    },
    "Agrolink": {
        "url_base": "https://www.agrolink.com.br",
        "feed_url": "https://www.agrolink.com.br/rss/noticias.xml",
    },
    "Canal Rural": {
        "url_base": "https://www.canalrural.com.br",
        "feed_url": "https://www.canalrural.com.br/feed/",
    },
    "Notícias Agrícolas": {
        "url_base": "https://www.noticiasagricolas.com.br",
        "feed_url": "https://www.noticiasagricolas.com.br/rss/",
    },
}
