"""
Módulo de scrapers para os 5 portais agro de referência:
- TheAgriBiz
- AgFeed
- Agrolink
- Canal Rural
- Notícias Agrícolas

Sprint 2 - Dupla A (Cards 8.1 e 8.7 / US-1, US-7, US-13).
"""

import re
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin, urlparse

import requests
import feedparser
import trafilatura
from bs4 import BeautifulSoup

from coleta.config import REQUEST_HEADERS, DEFAULT_TIMEOUT, PORTAIS_CONFIG

logger = logging.getLogger("coleta.scrapers")


class ArticleCandidate:
    """Representa um link de matéria descoberto na etapa preliminar."""

    def __init__(self, portal_nome: str, url: str, titulo_sugerido: str = "", publicado_em: Optional[str] = None):
        self.portal_nome = portal_nome
        self.url = url.strip()
        self.titulo_sugerido = titulo_sugerido.strip()
        self.publicado_em = publicado_em

    def __repr__(self) -> str:
        return f"<ArticleCandidate {self.portal_nome}: {self.url}>"


class ScrapedArticle:
    """Representa uma matéria com conteúdo extraído e sanitizado."""

    def __init__(
        self,
        portal_nome: str,
        url: str,
        titulo: str,
        lead: Optional[str],
        corpo_texto: str,
        publicado_em: Optional[str] = None,
    ):
        self.portal_nome = portal_nome
        self.url = url.strip()
        self.titulo = titulo.strip()
        self.lead = (lead or "").strip() or None
        self.corpo_texto = corpo_texto.strip()
        self.publicado_em = publicado_em

    def __repr__(self) -> str:
        return f"<ScrapedArticle {self.portal_nome}: {self.titulo[:30]}... ({len(self.corpo_texto)} chars)>"


class AgroScraper:
    """
    Coletor unificado para os portais do setor do agronegócio.
    Implementa descoberta rápida por RSS/HTML e extração de conteúdo limpo.
    """

    def __init__(self, timeout: int = DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(REQUEST_HEADERS)

    def descobrir_candidatos(self, portal_nome: str, limite: int = 20) -> List[ArticleCandidate]:
        """
        Descobre links recentes no portal via feed RSS (preferencial) ou varredura de links da home.
        Retorna uma lista de ArticleCandidate para triagem preliminar no banco.
        """
        config = PORTAIS_CONFIG.get(portal_nome)
        if not config:
            logger.warning("Configuração não encontrada para o portal: %s", portal_nome)
            return []

        candidatos: List[ArticleCandidate] = []
        urls_vistas = set()

        # 1. Tentativa via Feed RSS
        feed_url = config.get("feed_url")
        if feed_url:
            try:
                resp = self.session.get(feed_url, timeout=self.timeout)
                if resp.status_code == 200:
                    parsed_feed = feedparser.parse(resp.content)
                    for entry in parsed_feed.entries[:limite]:
                        link = entry.get("link")
                        if link and link not in urls_vistas and self._is_valid_article_url(portal_nome, link):
                            urls_vistas.add(link)
                            titulo = entry.get("title", "")
                            pub_date = entry.get("published", entry.get("updated"))
                            candidatos.append(ArticleCandidate(portal_nome, link, titulo, pub_date))
                    if candidatos:
                        logger.info("[%s] %d links descobertos via RSS", portal_nome, len(candidatos))
                        return candidatos
            except Exception as exc:
                logger.warning("[%s] Falha ao coletar feed RSS (%s): %s", portal_nome, feed_url, exc)

        # 2. Fallback: Varredura HTML da página inicial
        base_url = config["url_base"]
        try:
            resp = self.session.get(base_url, timeout=self.timeout)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, "html.parser")
                for a_tag in soup.find_all("a", href=True):
                    href = a_tag["href"].strip()
                    full_url = urljoin(base_url, href)
                    if full_url not in urls_vistas and self._is_valid_article_url(portal_nome, full_url):
                        urls_vistas.add(full_url)
                        titulo = a_tag.get_text(strip=True)
                        candidatos.append(ArticleCandidate(portal_nome, full_url, titulo))
                        if len(candidatos) >= limite:
                            break
                logger.info("[%s] %d links descobertos via HTML da home", portal_nome, len(candidatos))
        except Exception as exc:
            logger.error("[%s] Falha ao varrer HTML da home (%s): %s", portal_nome, base_url, exc)

        return candidatos

    def extrair_artigo(self, candidato: ArticleCandidate) -> Optional[ScrapedArticle]:
        """
        Faz o download e a extração limpa do conteúdo da matéria.
        Remove anúncios, menus, rodapés e scripts.
        """
        url = candidato.url
        portal_nome = candidato.portal_nome

        try:
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code != 200:
                logger.warning("[%s] HTTP %d ao acessar %s", portal_nome, resp.status_code, url)
                return None

            html_content = resp.text

            # 1. Extração profissional com Trafilatura
            texto_extraido = trafilatura.extract(
                html_content,
                url=url,
                include_comments=False,
                include_tables=False,
                no_fallback=False,
            )

            # Metadata via trafilatura
            meta = trafilatura.extract_metadata(html_content, default_url=url)
            titulo = (meta.title if meta and meta.title else "") or candidato.titulo_sugerido
            publicado_em = (meta.date if meta and meta.date else "") or candidato.publicado_em

            # 2. Fallback com BeautifulSoup se trafilatura não extraiu texto suficiente
            lead = ""
            if not texto_extraido or len(texto_extraido) < 120:
                soup = BeautifulSoup(html_content, "html.parser")

                # Remove tags espúrias
                for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
                    tag.decompose()

                if not titulo:
                    title_tag = soup.find("h1") or soup.find("title")
                    if title_tag:
                        titulo = title_tag.get_text(strip=True)

                paragrafos = [p.get_text(strip=True) for p in soup.find_all("p") if len(p.get_text(strip=True)) > 40]
                if paragrafos:
                    lead = paragrafos[0]
                    texto_extraido = "\n\n".join(paragrafos)

            if not texto_extraido or len(texto_extraido.strip()) < 80:
                logger.debug("[%s] Matéria com texto insuficiente descartada: %s", portal_nome, url)
                return None

            # Limpar rodapés comuns de "Leia mais", "Inscreva-se", "Copyright"
            texto_limpo = self._limpar_ruido_editorial(texto_extraido)
            if not lead:
                linhas = [l.strip() for l in texto_limpo.split("\n") if l.strip()]
                lead = linhas[0] if linhas else ""

            if not titulo:
                titulo = candidato.titulo_sugerido or (lead[:80] + "...")

            return ScrapedArticle(
                portal_nome=portal_nome,
                url=url,
                titulo=titulo,
                lead=lead,
                corpo_texto=texto_limpo,
                publicado_em=publicado_em or datetime.now(timezone.utc).isoformat(),
            )

        except Exception as exc:
            logger.error("[%s] Erro ao extrair conteúdo de %s: %s", portal_nome, url, exc)
            return None

    def _is_valid_article_url(self, portal_nome: str, url: str) -> bool:
        """Filtra URLs que são páginas estruturais, categorias ou arquivos estáticos."""
        parsed = urlparse(url)
        path = parsed.path.lower()

        # Ignorar recursos estáticos
        if any(path.endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".css", ".js"]):
            return False

        # Ignorar páginas institucionais e navegação
        termos_bloqueados = [
            "/categoria/", "/tag/", "/author/", "/autor/", "/contato", "/sobre",
            "/anuncie", "/termos", "/privacidade", "/page/", "/login", "/assine",
            "/newsletter", "#", "whatsapp.com", "facebook.com", "twitter.com",
            "youtube.com", "instagram.com", "linkedin.com", "tiktok.com"
        ]
        if any(termo in url.lower() for termo in termos_bloqueados):
            return False

        # Validação específica de domínio
        netloc = parsed.netloc.lower()
        if portal_nome == "TheAgriBiz" and "theagribiz.com" in netloc:
            return len(path) > 5 and not path.endswith("/feed/")
        elif portal_nome == "AgFeed" and "agfeed.com.br" in netloc:
            return len(path) > 5 and not path.endswith("/feed/")
        elif portal_nome == "Agrolink" and "agrolink.com.br" in netloc:
            return "/noticias/" in path
        elif portal_nome == "Canal Rural" and "canalrural.com.br" in netloc:
            return len(path) > 10 and not path.endswith("/feed/")
        elif portal_nome == "Notícias Agrícolas" and "noticiasagricolas.com.br" in netloc:
            return "/noticias/" in path

        # Padrão genérico se couber no domínio
        return bool(path and len(path) > 8)

    def _limpar_ruido_editorial(self, texto: str) -> str:
        """Remove links 'leia também', avisos de cookies e rodapés institucionais."""
        padroes_ruido = [
            r"Leia também:.*$",
            r"Veja mais:.*$",
            r"Clique aqui e receba as notícias.*$",
            r"Inscreva-se na nossa newsletter.*$",
            r"Todos os direitos reservados.*$",
            r"Siga o .* nas redes sociais.*$",
        ]
        texto_limpo = texto
        for padrao in padroes_ruido:
            texto_limpo = re.sub(padrao, "", texto_limpo, flags=re.IGNORECASE | re.MULTILINE)

        # Normalizar quebras de linha excessivas
        texto_limpo = re.sub(r"\n{3,}", "\n\n", texto_limpo).strip()
        return texto_limpo
