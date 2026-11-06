"""
Motor de Geração — The News Agro
Integra o System Prompt, Few-Shot e API Gemini para gerar matérias
no formato editorial oficial (Card 19 / US-3).
"""

import os
import json
import re
import argparse
from datetime import date
from pathlib import Path
from typing import Optional, Dict, Any

from google import genai
from google.genai import types

from Persona.system_prompt import (
    SYSTEM_PROMPT,
    FEW_SHOT_CORPUS,
    NewsletterArticle,
)

# ==============================================================================
# CONFIGURAÇÃO DA API
# ==============================================================================

DEFAULT_MODEL = "gemini-2.5-flash"
NEWS_DIR = Path(__file__).resolve().parents[1] / "src" / "content" / "news"


# ==============================================================================
# BUILDER DE PROMPT: injeta few-shot + entrada do usuário
# ==============================================================================

def build_user_message(
    cluster: str,
    centroide: str,
    relacionadas: list[str],
    data: Optional[str] = None,
) -> str:
    """Monta a mensagem de usuário com exemplos few-shot e a notícia a processar."""

    msg = "=== EXEMPLOS DE REFERÊNCIA (siga este formato à risca) ===\n"

    for ex in FEW_SHOT_CORPUS:
        s = ex["saida"]
        msg += f"\nCLUSTER: {ex['cluster']}\n"
        msg += f"NOTÍCIA PRINCIPAL: {ex['entrada']['centroide']}\n"
        msg += f"SAÍDA ESPERADA:\n"
        msg += f"**{s['titulo']}**\n"
        msg += f"_{s['resumao']}_\n\n"
        msg += f"**O que aconteceu**\n{s['o_que_aconteceu']}\n\n"
        msg += f"**O que isso muda pra você**\n{s['o_que_muda_pra_voce']}\n"
        if s.get("e_agora"):
            msg += f"\n**E agora?**\n{s['e_agora']}\n"
        if s.get("fechamento"):
            msg += f"\n{s['fechamento']}\n"
        msg += "\n---\n"

    hoje = data or date.today().strftime("%d/%m/%Y")
    rel_text = "\n".join(f"- {r}" for r in relacionadas) if relacionadas else "(sem notícias relacionadas)"

    msg += f"""
=== TAREFA DE PRODUÇÃO ===

CLUSTER: {cluster}
DATA: {hoje}
NOTÍCIA PRINCIPAL (centroide): {centroide}
NOTÍCIAS RELACIONADAS (contexto): 
{rel_text}

Agora escreva a matéria para a newsletter seguindo RIGOROSAMENTE o formato dos exemplos acima.
Use a notícia principal como base. Use as relacionadas só para confirmar fatos e identificar tendência.
Responda em JSON com as chaves: titulo, resumao, o_que_aconteceu, o_que_muda_pra_voce, e_agora (null se não houver ação concreta), fechamento (null se não couber).
"""
    return msg


# ==============================================================================
# GERAÇÃO COM A API GEMINI
# ==============================================================================

def gerar_materia(
    cluster: str,
    centroide: str,
    relacionadas: Optional[list[str]] = None,
    data: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Envia a notícia para o Gemini e devolve o artigo validado.
    Retorna um dict com 'artigo' (NewsletterArticle) e 'auditoria' (métricas).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "A variável GEMINI_API_KEY não está definida. Configure sua chave da API do Gemini no ambiente antes de executar."
        )

    relacionadas = relacionadas or []
    user_msg = build_user_message(cluster, centroide, relacionadas, data)

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=os.environ.get("GEMINI_MODEL", DEFAULT_MODEL),
        contents=user_msg,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
            max_output_tokens=4096,
            response_mime_type="application/json",
        ),
    )

    raw = (response.text or "").strip()
    if not raw:
        raise RuntimeError("O Gemini retornou uma resposta vazia.")

    try:
        data_dict = json.loads(raw)
    except json.JSONDecodeError as error:
        raise ValueError("O Gemini não retornou um JSON válido.") from error

    if not isinstance(data_dict, dict):
        raise ValueError("A resposta do Gemini precisa ser um objeto JSON.")

    artigo = NewsletterArticle(**data_dict)
    auditoria = _auditar(artigo)
    return {"artigo": artigo, "auditoria": auditoria, "raw_response": raw}


# ==============================================================================
# AUDITORIA DE QUALIDADE (critérios de aceite)
# ==============================================================================

def _auditar(artigo: NewsletterArticle) -> Dict[str, Any]:
    n = artigo.contagem_palavras
    resumao_words = len(re.findall(r'\b\w+\b', artigo.resumao))
    titulo_words  = len(re.findall(r'\b\w+\b', artigo.titulo))

    checks = {
        "titulo_ate_10_palavras":   titulo_words <= 10,
        "resumao_ate_25_palavras":  resumao_words <= 25,
        "tamanho_entre_180_e_300":  artigo.dentro_do_limite,
        "o_que_aconteceu_preenchido": len(artigo.o_que_aconteceu.strip()) > 30,
        "o_que_muda_preenchido":    len(artigo.o_que_muda_pra_voce.strip()) > 30,
    }
    passou = all(checks.values())

    return {
        "status": "[APROVADO]" if passou else "[REPROVADO]",
        "total_palavras": f"{n} palavras",
        "resumao_palavras": f"{resumao_words}/25",
        "titulo_palavras": f"{titulo_words}/10",
        "checks": checks,
    }


def gerar_para_noticia(news_path: Path) -> Dict[str, Any]:
    """Gera, valida e persiste a versão da Persona no JSON da notícia."""
    news = json.loads(news_path.read_text(encoding="utf-8"))
    source_text = "\n\n".join(
        text for text in (
            news.get("title", ""),
            news.get("subtitle", ""),
            news.get("summary", ""),
            news.get("content", ""),
        ) if text
    )
    if not source_text:
        raise ValueError(f"A notícia em {news_path} não contém texto para processar.")

    related_news = news.get("related_news", [])
    related_texts = []
    for related_id in related_news:
        if not re.fullmatch(r"news-\d+", related_id):
            continue
        related_path = NEWS_DIR / f"{related_id}.json"
        if related_path.is_file():
            related = json.loads(related_path.read_text(encoding="utf-8"))
            related_texts.append(
                f"{related.get('title', '')}: {related.get('summary', '')}".strip(": ")
            )

    result = gerar_materia(
        cluster=news.get("category", "Agronegócio"),
        centroide=source_text,
        relacionadas=related_texts,
        data=news.get("published_at", "")[:10] or None,
    )
    article = result["artigo"]
    audit = result["auditoria"]
    if audit["status"] != "[APROVADO]":
        raise ValueError(
            f"A matéria foi reprovada na auditoria e não foi salva: {audit['checks']}"
        )

    news["persona"] = article.model_dump(exclude_none=True)
    temporary_path = news_path.with_suffix(".json.tmp")
    temporary_path.write_text(
        json.dumps(news, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(news_path)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gera uma matéria da Persona para uma notícia já cadastrada no site."
    )
    parser.add_argument(
        "--news-id",
        required=True,
        help="ID do JSON da notícia, por exemplo news-001",
    )
    args = parser.parse_args()

    if not re.fullmatch(r"news-\d+", args.news_id):
        parser.error("--news-id deve ter o formato news-001.")

    news_path = NEWS_DIR / f"{args.news_id}.json"
    if not news_path.is_file():
        parser.error(f"notícia não encontrada: {args.news_id}")

    result = gerar_para_noticia(news_path)
    print("\n--- MATÉRIA GERADA E SALVA ---\n")
    print(result["artigo"].texto_formatado)
    print(f"\nAuditoria: {result['auditoria']['status']} — {result['auditoria']['total_palavras']}")
    print(f"Arquivo atualizado: {news_path}")


if __name__ == "__main__":
    main()
