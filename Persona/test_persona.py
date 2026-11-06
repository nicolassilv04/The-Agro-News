"""
Suíte de Testes Automatizados — Persona "The News Agro"
Valida a conformidade editorial contra o prompt oficial:
- Título: até 10 palavras
- Resumão: até 25 palavras
- Tamanho total: entre 180 e 280 (máx 300) palavras
- Separação de Consequência ("O que isso muda") vs Ação ("E agora?")
"""

import re
from Persona.system_prompt import FEW_SHOT_CORPUS, NewsletterArticle
from Persona.gerar_materia import _auditar

def testar_exemplos_few_shot():
    print("=== Testando Conformidade Editorial dos Exemplos Few-Shot ===")
    todos_aprovados = True
    for i, ex in enumerate(FEW_SHOT_CORPUS, 1):
        artigo = NewsletterArticle(**ex["saida"])
        audit = _auditar(artigo)
        status = audit["status"]
        if "[APROVADO]" not in status:
            todos_aprovados = False
        print(f"\nExemplo {i} [{ex['cluster']}]: {status}")
        print(f"  Titulo ({audit['titulo_palavras']} palavras): '{artigo.titulo}'")
        print(f"  Resumao ({audit['resumao_palavras']} palavras): '{artigo.resumao}'")
        print(f"  Total palavras: {audit['total_palavras']}")
        for check, ok in audit["checks"].items():
            simbolo = "[OK]" if ok else "[FALHOU]"
            print(f"    {simbolo} {check}")
            
    print("\n" + "=" * 50)
    if todos_aprovados:
        print("RESULTADO FINAL: TODOS OS EXEMPLOS ESTAO 100% CONFORMES!")
    else:
        print("RESULTADO FINAL: ALGUNS EXEMPLOS FALHARAM NA AUDITORIA.")

if __name__ == "__main__":
    testar_exemplos_few_shot()
