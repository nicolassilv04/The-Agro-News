import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from Persona import gerar_materia as generator
from Persona.system_prompt import FEW_SHOT_CORPUS, NewsletterArticle


class GeminiIntegrationTests(unittest.TestCase):
    def test_generation_requires_api_key(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(generator.genai, "Client") as client:
                with self.assertRaisesRegex(RuntimeError, "GEMINI_API_KEY"):
                    generator.gerar_materia("Mercado", "Notícia")
        client.assert_not_called()

    def test_approved_article_is_saved_to_news_json(self):
        article = NewsletterArticle(**FEW_SHOT_CORPUS[0]["saida"])
        audit = generator._auditar(article)
        self.assertEqual(audit["status"], "[APROVADO]")

        with tempfile.TemporaryDirectory() as temp_dir:
            news_path = Path(temp_dir) / "news-test.json"
            original = {
                "id": "news-test",
                "title": "Notícia original",
                "summary": "Resumo original",
                "content": "Texto de origem",
                "category": "mercado",
                "published_at": "2026-10-15T09:00:00-03:00",
                "related_news": [],
            }
            news_path.write_text(json.dumps(original), encoding="utf-8")

            with patch.object(
                generator,
                "gerar_materia",
                return_value={"artigo": article, "auditoria": audit},
            ):
                generator.gerar_para_noticia(news_path)

            saved = json.loads(news_path.read_text(encoding="utf-8"))

        self.assertEqual(saved["title"], original["title"])
        self.assertEqual(saved["persona"]["titulo"], article.titulo)
        self.assertEqual(saved["persona"]["o_que_muda_pra_voce"], article.o_que_muda_pra_voce)

    def test_rejected_article_is_not_saved(self):
        article = NewsletterArticle(**FEW_SHOT_CORPUS[0]["saida"])
        rejected_audit = {"status": "[REPROVADO]", "checks": {"word_count": False}}

        with tempfile.TemporaryDirectory() as temp_dir:
            news_path = Path(temp_dir) / "news-test.json"
            original = {
                "id": "news-test",
                "title": "Notícia original",
                "summary": "Resumo original",
                "content": "Texto de origem",
                "category": "mercado",
                "published_at": "2026-10-15T09:00:00-03:00",
                "related_news": [],
            }
            original_text = json.dumps(original)
            news_path.write_text(original_text, encoding="utf-8")

            with patch.object(
                generator,
                "gerar_materia",
                return_value={"artigo": article, "auditoria": rejected_audit},
            ):
                with self.assertRaisesRegex(ValueError, "não foi salva"):
                    generator.gerar_para_noticia(news_path)

            self.assertEqual(news_path.read_text(encoding="utf-8"), original_text)


if __name__ == "__main__":
    unittest.main()
