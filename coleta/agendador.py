"""
Agendador de Tarefas em Background (APScheduler) com disparos a cada 3 horas.
Inclui logging estruturado com rotação de arquivos e suporte a execução autônoma.
Sprint 2 - Dupla A (Card 8.7 / US-7, US-15).
"""

import sys
import signal
import logging
import argparse
from logging.handlers import RotatingFileHandler
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from coleta.config import (
    INTERVALO_HORAS_PADRAO,
    MISFIRE_GRACE_TIME,
    LOG_FILE_PATH,
    LOG_MAX_BYTES,
    LOG_BACKUP_COUNT,
)
from coleta.pipeline import PipelineColeta
from coleta.db import DatabaseManager


def configurar_logging(nivel: int = logging.INFO) -> logging.Logger:
    """
    Configura o sistema de log registrando em arquivo rotativo (logs/coleta.log)
    e simultaneamente na saída padrão do console (stdout).
    """
    LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

    formato = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(nivel)

    # Evita duplicação de handlers se chamada múltiplas vezes
    if not any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
        file_handler = RotatingFileHandler(
            filename=str(LOG_FILE_PATH),
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setFormatter(formato)
        file_handler.setLevel(nivel)
        root_logger.addHandler(file_handler)

    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formato)
        stream_handler.setLevel(nivel)
        root_logger.addHandler(stream_handler)

    return logging.getLogger("coleta.agendador")


class AgendadorColeta:
    """
    Encapsula o APScheduler com tarefas a cada 3 horas e proteção contra concorrência.
    """

    def __init__(
        self,
        intervalo_horas: int = INTERVALO_HORAS_PADRAO,
        intervalo_minutos: int = 0,
        db_manager: DatabaseManager = None,
    ):
        self.intervalo_horas = intervalo_horas
        self.intervalo_minutos = intervalo_minutos
        self.db = db_manager or DatabaseManager()
        self.pipeline = PipelineColeta(db=self.db)
        self.scheduler = BlockingScheduler()
        self.logger = logging.getLogger("coleta.agendador")

    def executar_tarefa_agendada(self) -> None:
        """Invólucro seguro para a execução da tarefa no agendador."""
        self.logger.info("Disparando tarefa agendada de coleta periódica...")
        try:
            metricas = self.pipeline.executar_ciclo()
            self.logger.info(
                "Ciclo concluído com sucesso. Novas matérias: %d | Ignoradas: %d | Erros: %d",
                metricas["total_novas"],
                metricas["total_ignoradas"],
                metricas["total_erros"],
            )
        except Exception as exc:
            self.logger.exception("Exceção não tratada durante o ciclo de coleta: %s", exc)

    def iniciar(self, executar_na_inicializacao: bool = True) -> None:
        """
        Inicia o agendador em modo contínuo (autonomia de 48h+).
        """
        configurar_logging()

        # Determina o gatilho de intervalo
        if self.intervalo_minutos > 0:
            trigger = IntervalTrigger(minutes=self.intervalo_minutos)
            descricao_intervalo = f"{self.intervalo_minutos} minutos"
        else:
            trigger = IntervalTrigger(hours=self.intervalo_horas)
            descricao_intervalo = f"{self.intervalo_horas} horas"

        self.scheduler.add_job(
            func=self.executar_tarefa_agendada,
            trigger=trigger,
            id="job_coleta_agro",
            name="Coleta de Notícias do Agronegócio",
            replace_existing=True,
            coalesce=True,
            max_instances=1,
            misfire_grace_time=MISFIRE_GRACE_TIME,
        )

        # Captura de sinais para finalização limpa (Graceful Shutdown)
        def _handle_exit(signum, frame):
            self.logger.info("Sinal de encerramento recebido (%s). Finalizando agendador...", signum)
            if self.scheduler.running:
                self.scheduler.shutdown(wait=False)
            sys.exit(0)

        try:
            signal.signal(signal.SIGINT, _handle_exit)
            signal.signal(signal.SIGTERM, _handle_exit)
        except (ValueError, AttributeError):
            # Em alguns ambientes Windows com threads subordinadas pode não ser possível
            pass

        self.logger.info(
            "Agendador inicializado. Disparos configurados a cada %s. Pressione Ctrl+C para encerrar.",
            descricao_intervalo,
        )

        if executar_na_inicializacao:
            self.logger.info("Executando rodada inicial antes de aguardar o próximo disparo...")
            self.executar_tarefa_agendada()

        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("Agendador parado pelo usuário.")


def main():
    parser = argparse.ArgumentParser(
        description="Agendador em Background da Coleta de Notícias - The Agro News"
    )
    parser.add_argument(
        "--run-once",
        action="store_true",
        help="Executa um único ciclo de coleta imediatamente e encerra.",
    )
    parser.add_argument(
        "--interval-hours",
        type=int,
        default=INTERVALO_HORAS_PADRAO,
        help=f"Intervalo entre disparos em horas (padrão: {INTERVALO_HORAS_PADRAO}h).",
    )
    parser.add_argument(
        "--interval-minutes",
        type=int,
        default=0,
        help="Intervalo entre disparos em minutos (para testes).",
    )
    parser.add_argument(
        "--no-run-on-start",
        action="store_true",
        help="Não executa a coleta imediatamente ao iniciar, apenas aguarda o primeiro intervalo.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Exibe as estatísticas do banco de dados e da última execução de coleta.",
    )

    args = parser.parse_args()
    logger = configurar_logging()

    db = DatabaseManager()

    if args.status:
        stats = db.obter_estatisticas()
        print("\n=== ESTATÍSTICAS DO BANCO DE DADOS TAN ===")
        print(f"Total de Artigos Armazenados: {stats['total_artigos']}")
        print("Artigos por Portal:")
        for portal, total in stats["artigos_por_portal"].items():
            print(f"  - {portal}: {total}")
        print("\nÚltima Execução:")
        if stats["ultima_execucao"]:
            u = stats["ultima_execucao"]
            print(f"  - Início: {u['inicio_em']}")
            print(f"  - Término: {u['fim_em']} ({u['duracao_segundos']}s)")
            print(f"  - Status: {u['status']}")
            print(f"  - Novas: {u['total_novas']} | Ignoradas: {u['total_ignoradas']} | Erros: {u['total_erros']}")
        else:
            print("  Nenhuma execução registrada até o momento.")
        return

    if args.run_once:
        logger.info("Modo --run-once acionado. Executando um único ciclo de coleta...")
        pipeline = PipelineColeta(db=db)
        metricas = pipeline.executar_ciclo()
        print("\n=== RESUMO DO CICLO CONCLUÍDO ===")
        print(f"Início: {metricas['inicio_em']}")
        print(f"Fim:    {metricas['fim_em']} (Duração: {metricas['duracao_segundos']}s)")
        print(f"Status: {metricas['status']}")
        print(f"Matérias Encontradas: {metricas['total_encontradas']}")
        print(f"Novas Inseridas:      {metricas['total_novas']}")
        print(f"Ignoradas (Já no BD): {metricas['total_ignoradas']}")
        print(f"Erros/Falhas:         {metricas['total_erros']}")
        return

    agendador = AgendadorColeta(
        intervalo_horas=args.interval_hours,
        intervalo_minutos=args.interval_minutes,
        db_manager=db,
    )
    agendador.iniciar(executar_na_inicializacao=not args.no_run_on_start)


if __name__ == "__main__":
    main()
