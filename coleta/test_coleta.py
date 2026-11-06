"""
Bateria de testes automatizados para validação dos critérios de aceite:
1. Agendador em background com disparos a cada 3 horas.
2. Verificação prévia no banco para não reprocessar links já existentes.
3. Sistema de log registrando início, término, volume e exceções.
4. Autonomia e integridade de dados (sem duplicações).
Sprint 2 - Dupla A (Card 8.7).
"""

import os
import shutil
import tempfile
import unittest
import logging
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

from apscheduler.triggers.interval import IntervalTrigger

from coleta.db import DatabaseManager
from coleta.scrapers import ArticleCandidate, ScrapedArticle, AgroScraper
from coleta.pipeline import PipelineColeta
from coleta.agendador import AgendadorColeta, configurar_logging


class TestColetaAgendador(unittest.TestCase):

    def setUp(self):
        # Cria diretório temporário para banco e logs isolados
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_tan.db"
        self.db = DatabaseManager(db_path=self.db_path)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # --------------------------------------------------------------------------
    # 1. TESTES DO AGENDADOR (APScheduler a cada 3 horas)
    # --------------------------------------------------------------------------
    def test_agendador_configurado_para_tres_horas(self):
        """Valida se o agendador configura o intervalo padrão de 3 horas."""
        agendador = AgendadorColeta(intervalo_horas=3, db_manager=self.db)
        self.assertEqual(agendador.intervalo_horas, 3)

        # Simula a adição do job no scheduler
        trigger = IntervalTrigger(hours=agendador.intervalo_horas)
        job = agendador.scheduler.add_job(
            func=agendador.executar_tarefa_agendada,
            trigger=trigger,
            id="job_test",
        )
        self.assertIsNotNone(job)
        self.assertEqual(job.trigger.interval.total_seconds(), 3 * 3600)

    # --------------------------------------------------------------------------
    # 2. TESTES DE VERIFICAÇÃO PRÉVIA E NÃO-DUPLICAÇÃO
    # --------------------------------------------------------------------------
    def test_verificacao_previa_identifica_urls_existentes(self):
        """Valida que o banco e o método de triagem identificam URLs já salvas."""
        url_teste = "https://theagribiz.com/mercado/soja-alta-historica"
        self.assertFalse(self.db.url_existe(url_teste))

        # Insere a matéria
        inserido = self.db.inserir_artigo(
            portal_nome="TheAgriBiz",
            url=url_teste,
            titulo="Soja bate recorde histórico",
            lead="Preços sobem impulsionados pela demanda chinesa",
            corpo_texto="O mercado de grãos registrou movimentação atípica...",
        )
        self.assertTrue(inserido)

        # Verificação prévia agora deve retornar True
        self.assertTrue(self.db.url_existe(url_teste))

        # Teste de busca em lote
        lote_candidato = [
            url_teste,
            "https://theagribiz.com/mercado/milho-exportacoes",
            "https://agfeed.com.br/boi-gordo-valorizacao",
        ]
        existentes = self.db.obter_urls_existentes(lote_candidato)
        self.assertIn(url_teste, existentes)
        self.assertEqual(len(existentes), 1)

    def test_banco_bloqueia_duplicatas_sem_gerar_excecao(self):
        """Valida que reinserir a mesma URL é ignorado sem travar o pipeline."""
        url = "https://agfeed.com.br/noticia-exemplo-01"

        ok1 = self.db.inserir_artigo(
            portal_nome="AgFeed",
            url=url,
            titulo="Primeira versão",
            lead="Lead 1",
            corpo_texto="Corpo 1",
        )
        self.assertTrue(ok1)

        # Tentativa de duplicata: deve retornar False e não estourar erro
        ok2 = self.db.inserir_artigo(
            portal_nome="AgFeed",
            url=url,
            titulo="Segunda versão com mesmo link",
            lead="Lead 2",
            corpo_texto="Corpo 2",
        )
        self.assertFalse(ok2)

        # Total no banco deve ser rigorosamente 1
        stats = self.db.obter_estatisticas()
        self.assertEqual(stats["total_artigos"], 1)

    def test_pipeline_descarta_links_existentes_antes_da_extracao(self):
        """
        Valida que o pipeline faz a triagem prévia: não chama o scraper pesado
        para matérias que já constam no banco de dados.
        """
        url_existente = "https://canalrural.com.br/noticia-1"
        url_nova = "https://canalrural.com.br/noticia-2"

        # Cadastra previamente url_existente no banco
        self.db.inserir_artigo(
            portal_nome="Canal Rural",
            url=url_existente,
            titulo="Notícia 1",
            lead="Lead 1",
            corpo_texto="Corpo 1",
        )

        # Mock do scraper
        mock_scraper = MagicMock(spec=AgroScraper)
        mock_scraper.descobrir_candidatos.return_value = [
            ArticleCandidate("Canal Rural", url_existente, "Notícia 1"),
            ArticleCandidate("Canal Rural", url_nova, "Notícia 2 Nova"),
        ]

        # O scraper só deve ser chamado para extrair a nova!
        mock_scraper.extrair_artigo.return_value = ScrapedArticle(
            portal_nome="Canal Rural",
            url=url_nova,
            titulo="Notícia 2 Nova",
            lead="Lead 2",
            corpo_texto="Texto completo da matéria 2",
        )

        pipeline = PipelineColeta(db=self.db, scraper=mock_scraper)

        with patch("coleta.pipeline.PORTAIS_CONFIG", {"Canal Rural": {}}):
            metricas = pipeline.executar_ciclo()

        # Verificações
        self.assertEqual(metricas["total_encontradas"], 2)
        self.assertEqual(metricas["total_ignoradas"], 1)
        self.assertEqual(metricas["total_novas"], 1)

        # Garantir que extrair_artigo foi chamado apenas 1 vez (para a URL nova)
        self.assertEqual(mock_scraper.extrair_artigo.call_count, 1)
        chamada_arg = mock_scraper.extrair_artigo.call_args[0][0]
        self.assertEqual(chamada_arg.url, url_nova)

    # --------------------------------------------------------------------------
    # 3. TESTES DO SISTEMA DE LOG E AUDITORIA
    # --------------------------------------------------------------------------
    def test_sistema_de_log_registra_horarios_volume_e_status(self):
        """Valida o registro de início, fim, volume de matérias e auditoria."""
        mock_scraper = MagicMock(spec=AgroScraper)
        mock_scraper.descobrir_candidatos.return_value = [
            ArticleCandidate("Agrolink", "https://agrolink.com.br/noticia-a", "A"),
            ArticleCandidate("Agrolink", "https://agrolink.com.br/noticia-b", "B"),
        ]
        mock_scraper.extrair_artigo.side_effect = [
            ScrapedArticle("Agrolink", "https://agrolink.com.br/noticia-a", "A", "Lead A", "Corpo A"),
            ScrapedArticle("Agrolink", "https://agrolink.com.br/noticia-b", "B", "Lead B", "Corpo B"),
        ]

        pipeline = PipelineColeta(db=self.db, scraper=mock_scraper)

        with patch("coleta.pipeline.PORTAIS_CONFIG", {"Agrolink": {}}):
            metricas = pipeline.executar_ciclo()

        self.assertIsNotNone(metricas["inicio_em"])
        self.assertIsNotNone(metricas["fim_em"])
        self.assertGreaterEqual(metricas["duracao_segundos"], 0.0)
        self.assertEqual(metricas["total_novas"], 2)
        self.assertEqual(metricas["status"], "SUCESSO")

        # Verifica auditoria persistida no banco
        stats = self.db.obter_estatisticas()
        ultima = stats["ultima_execucao"]
        self.assertIsNotNone(ultima)
        self.assertEqual(ultima["total_novas"], 2)
        self.assertEqual(ultima["status"], "SUCESSO")

    def test_resiliencia_e_captura_de_excecoes_sem_abortar_pipeline(self):
        """
        Valida que falhas temporárias em um portal são logadas como exceções
        e o pipeline continua executando os demais portais com tolerância a falhas.
        """
        mock_scraper = MagicMock(spec=AgroScraper)

        # Portal 1 falha criticamente com exceção de conexão
        def side_effect_descobrir(portal_nome, limite=15):
            if portal_nome == "PortalComErro":
                raise ConnectionError("Timeout ao conectar ao portal")
            return [ArticleCandidate(portal_nome, f"https://portal.com/n1", "Notícia Normal")]

        mock_scraper.descobrir_candidatos.side_effect = side_effect_descobrir
        mock_scraper.extrair_artigo.return_value = ScrapedArticle(
            "PortalNormal", "https://portal.com/n1", "T", "L", "Texto"
        )

        pipeline = PipelineColeta(db=self.db, scraper=mock_scraper)

        config_portais = {
            "PortalComErro": {},
            "PortalNormal": {},
        }

        with patch("coleta.pipeline.PORTAIS_CONFIG", config_portais):
            metricas = pipeline.executar_ciclo()

        # O pipeline NÃO explodiu, capturou o erro e continuou
        self.assertEqual(metricas["total_erros"], 1)
        self.assertEqual(metricas["total_novas"], 1)
        self.assertEqual(metricas["status"], "ERRO_PARCIAL")

        # Verifica que o erro foi registrado na tabela de auditoria
        stats = self.db.obter_estatisticas()
        self.assertEqual(stats["ultima_execucao"]["total_erros"], 1)
        self.assertEqual(stats["ultima_execucao"]["status"], "ERRO_PARCIAL")


if __name__ == "__main__":
    unittest.main()
