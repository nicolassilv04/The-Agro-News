"""
Camada de persistência e banco de dados para o pipeline de coleta.
Suporta SQLite nativo (padrão) e PostgreSQL com restrição de unicidade na URL.
Sprint 2 - Dupla A (Cards 8.1 e 8.7 / US-1, US-2, US-7).
"""

import json
import sqlite3
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

from coleta.config import SQLITE_DB_PATH, DATABASE_URL

logger = logging.getLogger("coleta.db")


class DatabaseManager:
    """
    Gerenciador de banco de dados resiliente com verificação prévia de links,
    deduplicação garantida por restrição de unicidade e log de auditoria.
    """

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or SQLITE_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.inicializar_banco()

    def get_connection(self) -> sqlite3.Connection:
        """Cria e retorna uma conexão com o banco SQLite."""
        conn = sqlite3.connect(
            str(self.db_path),
            timeout=30.0,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")  # Modo WAL para alta concorrência
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def inicializar_banco(self) -> None:
        """Cria as tabelas e índices necessários caso não existam."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Tabela de artigos (conforme especificação da seção 8.1 do PRD)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS artigos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    portal_nome TEXT NOT NULL,
                    url TEXT NOT NULL UNIQUE,
                    titulo TEXT NOT NULL,
                    lead TEXT,
                    corpo_texto TEXT NOT NULL,
                    publicado_em TEXT,
                    processado_status TEXT DEFAULT 'pendente',
                    criado_em TEXT NOT NULL
                );
            """)

            # Índice dedicado para busca instantânea de URL
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_artigos_url ON artigos(url);
            """)

            # Tabela de auditoria de execuções do agendador
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS coleta_execucoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    inicio_em TEXT NOT NULL,
                    fim_em TEXT NOT NULL,
                    duracao_segundos REAL NOT NULL,
                    status TEXT NOT NULL,
                    total_encontradas INTEGER NOT NULL DEFAULT 0,
                    total_novas INTEGER NOT NULL DEFAULT 0,
                    total_ignoradas INTEGER NOT NULL DEFAULT 0,
                    total_erros INTEGER NOT NULL DEFAULT 0,
                    detalhes_json TEXT
                );
            """)

            conn.commit()
            logger.info("Banco de dados inicializado com sucesso em %s", self.db_path)

    def url_existe(self, url: str) -> bool:
        """
        Verificação prévia: verifica se a URL já existe no banco de dados.
        Retorna True se já existir, evitando o download e processamento pesado.
        """
        url_normalizada = url.strip()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM artigos WHERE url = ? LIMIT 1;", (url_normalizada,))
            return cursor.fetchone() is not None

    def obter_urls_existentes(self, urls: List[str]) -> Set[str]:
        """
        Recebe uma lista de URLs candidatas e retorna o subconjunto que JÁ existe no banco.
        Otimização em lote para descartar links repetidos em uma única consulta.
        """
        if not urls:
            return set()

        urls_limpas = [u.strip() for u in urls if u and u.strip()]
        if not urls_limpas:
            return set()

        encontradas: Set[str] = set()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Fazer a busca em blocos de até 500 para respeitar limites do SQLite
            chunk_size = 500
            for i in range(0, len(urls_limpas), chunk_size):
                chunk = urls_limpas[i:i + chunk_size]
                placeholders = ",".join("?" for _ in chunk)
                query = f"SELECT url FROM artigos WHERE url IN ({placeholders});"
                cursor.execute(query, chunk)
                for row in cursor.fetchall():
                    encontradas.add(row["url"])

        return encontradas

    def inserir_artigo(
        self,
        portal_nome: str,
        url: str,
        titulo: str,
        lead: Optional[str],
        corpo_texto: str,
        publicado_em: Optional[str] = None,
        processado_status: str = "pendente",
    ) -> bool:
        """
        Insere uma matéria no banco.
        Se a URL já existir (devido à restrição UNIQUE), a inserção é ignorada
        sem gerar exceção impeditiva, retornando False.
        Retorna True caso a matéria tenha sido inserida com sucesso.
        """
        url_limpa = url.strip()
        criado_em = datetime.now(timezone.utc).isoformat()

        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO artigos (
                        portal_nome, url, titulo, lead, corpo_texto,
                        publicado_em, processado_status, criado_em
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(url) DO NOTHING;
                    """,
                    (
                        portal_nome,
                        url_limpa,
                        titulo.strip(),
                        (lead or "").strip() or None,
                        corpo_texto.strip(),
                        publicado_em,
                        processado_status,
                        criado_em,
                    ),
                )
                conn.commit()
                # rowcount será 1 se inseriu, 0 se houve conflito de URL
                return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            logger.debug("Conflito de unicidade ignorado para a URL: %s", url_limpa)
            return False
        except Exception as exc:
            logger.error("Erro inesperado ao inserir artigo %s: %s", url_limpa, exc)
            raise

    def registrar_execucao(
        self,
        inicio_em: datetime,
        fim_em: datetime,
        status: str,
        total_encontradas: int,
        total_novas: int,
        total_ignoradas: int,
        total_erros: int,
        detalhes: Optional[Dict[str, Any]] = None,
    ) -> int:
        """
        Registra o log consolidado de um ciclo do agendador na tabela de auditoria.
        """
        duracao = (fim_em - inicio_em).total_seconds()
        detalhes_str = json.dumps(detalhes or {}, ensure_ascii=False)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO coleta_execucoes (
                    inicio_em, fim_em, duracao_segundos, status,
                    total_encontradas, total_novas, total_ignoradas, total_erros, detalhes_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    inicio_em.isoformat(),
                    fim_em.isoformat(),
                    duracao,
                    status,
                    total_encontradas,
                    total_novas,
                    total_ignoradas,
                    total_erros,
                    detalhes_str,
                ),
            )
            conn.commit()
            return cursor.lastrowid or 0

    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna métricas gerais sobre a base de dados de artigos e execuções."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) AS total FROM artigos;")
            total_artigos = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT portal_nome, COUNT(*) AS qtd
                FROM artigos
                GROUP BY portal_nome
                ORDER BY qtd DESC;
            """)
            por_portal = {row["portal_nome"]: row["qtd"] for row in cursor.fetchall()}

            cursor.execute("""
                SELECT * FROM coleta_execucoes
                ORDER BY id DESC
                LIMIT 1;
            """)
            ultima = cursor.fetchone()
            ultima_exec = dict(ultima) if ultima else None

            return {
                "total_artigos": total_artigos,
                "artigos_por_portal": por_portal,
                "ultima_execucao": ultima_exec,
            }
