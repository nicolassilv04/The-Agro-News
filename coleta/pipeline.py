"""
Pipeline de execução do ciclo de coleta de notícias.
Orquestra a descoberta preliminar, a verificação prévia no banco contra duplicatas,
a extração limpa e o registro de métricas e auditoria.
Sprint 2 - Dupla A (Card 8.7 / US-1, US-2, US-7).
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

from coleta.db import DatabaseManager
from coleta.scrapers import AgroScraper
from coleta.config import PORTAIS_CONFIG

logger = logging.getLogger("coleta.pipeline")


class PipelineColeta:
    """
    Executa o ciclo de coleta com verificação prévia no banco e registro de métricas.
    """

    def __init__(self, db: Optional[DatabaseManager] = None, scraper: Optional[AgroScraper] = None):
        self.db = db or DatabaseManager()
        self.scraper = scraper or AgroScraper()

    def executar_ciclo(self, limite_por_portal: int = 15) -> Dict[str, Any]:
        """
        Executa uma rodada completa de coleta nos 5 portais.
        Retorna o resumo estatístico da rodada.
        """
        inicio_em = datetime.now(timezone.utc)
        logger.info("=== INÍCIO DO CICLO DE COLETA: %s ===", inicio_em.isoformat())

        metricas: Dict[str, Any] = {
            "inicio_em": inicio_em.isoformat(),
            "fim_em": None,
            "duracao_segundos": 0.0,
            "status": "SUCESSO",
            "total_encontradas": 0,
            "total_novas": 0,
            "total_ignoradas": 0,
            "total_erros": 0,
            "portais": {},
        }

        portais_alvo = list(PORTAIS_CONFIG.keys())

        for portal_nome in portais_alvo:
            portal_stats = {
                "encontradas": 0,
                "ignoradas_preexistentes": 0,
                "novas_inseridas": 0,
                "erros": 0,
            }
            logger.info("[%s] Iniciando verificação de matérias...", portal_nome)

            try:
                # 1. Descoberta de candidatos
                candidatos = self.scraper.descobrir_candidatos(portal_nome, limite=limite_por_portal)
                portal_stats["encontradas"] = len(candidatos)
                metricas["total_encontradas"] += len(candidatos)

                if not candidatos:
                    logger.warning("[%s] Nenhum link candidato encontrado nesta rodada.", portal_nome)
                    metricas["portais"][portal_nome] = portal_stats
                    continue

                # 2. VERIFICAÇÃO PRÉVIA NO BANCO (Deduplicação antes da extração pesada)
                urls_candidatas = [c.url for c in candidatos]
                urls_existentes = self.db.obter_urls_existentes(urls_candidatas)

                candidatos_novos = [c for c in candidatos if c.url not in urls_existentes]
                qtd_ignoradas = len(candidatos) - len(candidatos_novos)

                portal_stats["ignoradas_preexistentes"] = qtd_ignoradas
                metricas["total_ignoradas"] += qtd_ignoradas

                logger.info(
                    "[%s] Triagem prévia no banco: %d links encontrados, %d já cadastrados (ignorados), %d novos a extrair.",
                    portal_nome,
                    len(candidatos),
                    qtd_ignoradas,
                    len(candidatos_novos),
                )

                # 3. Extração e gravação somente das matérias novas
                for candidato in candidatos_novos:
                    try:
                        artigo = self.scraper.extrair_artigo(candidato)
                        if not artigo:
                            portal_stats["erros"] += 1
                            metricas["total_erros"] += 1
                            continue

                        inserido = self.db.inserir_artigo(
                            portal_nome=artigo.portal_nome,
                            url=artigo.url,
                            titulo=artigo.titulo,
                            lead=artigo.lead,
                            corpo_texto=artigo.corpo_texto,
                            publicado_em=artigo.publicado_em,
                        )

                        if inserido:
                            portal_stats["novas_inseridas"] += 1
                            metricas["total_novas"] += 1
                            logger.debug("[%s] Matéria inserida com sucesso: %s", portal_nome, artigo.titulo[:50])
                        else:
                            # Caso tenha sido inserida concorrentemente
                            portal_stats["ignoradas_preexistentes"] += 1
                            metricas["total_ignoradas"] += 1

                    except Exception as err_artigo:
                        logger.error(
                            "[%s] Exceção ao processar artigo %s: %s",
                            portal_nome,
                            candidato.url,
                            err_artigo,
                            exc_info=True,
                        )
                        portal_stats["erros"] += 1
                        metricas["total_erros"] += 1

            except Exception as err_portal:
                logger.error(
                    "[%s] Exceção crítica ao coletar portal: %s",
                    portal_nome,
                    err_portal,
                    exc_info=True,
                )
                portal_stats["erros"] += 1
                metricas["total_erros"] += 1

            metricas["portais"][portal_nome] = portal_stats
            logger.info(
                "[%s] Concluído: %d novas inseridas, %d ignoradas, %d erros.",
                portal_nome,
                portal_stats["novas_inseridas"],
                portal_stats["ignoradas_preexistentes"],
                portal_stats["erros"],
            )

        # 4. Finalização e registro de métricas
        fim_em = datetime.now(timezone.utc)
        duracao = (fim_em - inicio_em).total_seconds()
        metricas["fim_em"] = fim_em.isoformat()
        metricas["duracao_segundos"] = round(duracao, 2)

        if metricas["total_erros"] > 0:
            metricas["status"] = "ERRO_PARCIAL" if metricas["total_novas"] > 0 else "FALHA"
        else:
            metricas["status"] = "SUCESSO"

        # Persistir auditoria no banco
        try:
            self.db.registrar_execucao(
                inicio_em=inicio_em,
                fim_em=fim_em,
                status=metricas["status"],
                total_encontradas=metricas["total_encontradas"],
                total_novas=metricas["total_novas"],
                total_ignoradas=metricas["total_ignoradas"],
                total_erros=metricas["total_erros"],
                detalhes=metricas["portais"],
            )
        except Exception as err_audit:
            logger.error("Falha ao registrar auditoria no banco: %s", err_audit, exc_info=True)

        logger.info(
            "=== FIM DO CICLO DE COLETA: %s | Duração: %.2fs | Novas: %d | Ignoradas: %d | Erros: %d | Status: %s ===",
            fim_em.isoformat(),
            duracao,
            metricas["total_novas"],
            metricas["total_ignoradas"],
            metricas["total_erros"],
            metricas["status"],
        )

        return metricas
