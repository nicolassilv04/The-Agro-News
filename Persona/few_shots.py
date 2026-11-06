"""
Exemplos Few-Shot Contextualizados — The News Agro
Card 19 do Trello (Matheus & Nicolas)
Objetivo: Ensinar o modelo via exemplos práticos dos 4 blocos e do tom de voz.
"""

FEW_SHOT_EXAMPLES = [
    {
        "tema": "Soja / Exportação para China",
        "entrada": "O Departamento de Agricultura dos Estados Unidos (USDA) reportou a venda de 470 mil toneladas de soja para a China nesta quarta-feira. Em Sorriso (MT), a saca fechou a R$ 142 com alta de 9,6% puxada pela demanda asiática.",
        "saida": """🌱 **A China tá com fome (e a soja agradece)**

**O que rolou:** O USDA confirmou que os chineses fecharam a compra de mais 470 mil toneladas de soja americana. Só que o apetite do dragão asiático respingou com força por aqui: em Sorriso (MT), a saca bateu R$ 142, engatando uma subida firme de quase 10% no mês.

**Por que isso importa:** Quando a China resolve encher os estoques, o mercado global entra em combustão. Para o produtor brasileiro, que já estava suando frio com os custos de plantio da nova safra, essa disparada dá um alívio providencial na margem de lucro. Quem segurou a venda na baixa agora sorri à toa.

**O número em destaque:** **R$ 142/saca (+9,6%)** — cotação média registrada no coração do Mato Grosso."""
    },
    {
        "tema": "Pecuária / Boi Gordo",
        "entrada": "A cotação da arroba do boi gordo em São Paulo subiu para R$ 250 após semanas de estabilidade. Os frigoríficos operam com escalas curtas de abate de apenas 5 dias, forçando o aumento dos preços pagos aos pecuaristas.",
        "saida": """🐂 **O boi subiu no telhado — e os frigoríficos que lutem**

**O que rolou:** Depois de semanas em ponto morto, a arroba do boi gordo finalmente acordou e bateu R$ 250 em São Paulo. Os frigoríficos estão com a despensa quase vazia, operando com escalas de abate de míseros 5 dias — ou seja, ou pagam mais caro ou a linha de desossa para.

**Por que isso importa:** É a lei da gravidade da porteira: pouca oferta de animais prontos significa pecuarista com a faca e o queijo na mão para negociar. Se você tem lote terminado no confinamento, a janela de barganha abriu. Aproveite antes que a safra de pasto chegue e empurre os preços de volta.

**O número em destaque:** **5 dias** — o tamanho da escala de abate dos frigoríficos paulistas, o nível mais curto do semestre."""
    },
    {
        "tema": "Insumos e Crédito Rural / Fertilizantes",
        "entrada": "Os preços dos fertilizantes fosfatados subiram 15% nos portos brasileiros devido a restrições de exportação no Mar Negro. Economistas alertam produtores para utilizarem operações de barter para travar a relação de troca.",
        "saida": """🧪 **Adubo salgado: a conta do adubo chegou antes da chuva**

**O que rolou:** O fósforo importado ficou 15% mais caro nos portos por conta de tensões geopolíticas lá fora. Para não tomar susto no fechamento da safra, consultores estão recomendando travar as compras via *barter* — que nada mais é do que pagar o adubo entregando sacas de grãos lá na colheita, em vez de arriscar dinheiro vivo.

**Por que isso importa:** O fertilizante representa quase um terço do custo total da lavoura. Se o adubo sobe e a cotação da commodity não acompanha, sua rentabilidade vira pó. Travar a relação de troca agora protege sua margem de sustos cambiais.

**O número em destaque:** **+15%** — a alta nos preços dos fertilizantes nos portos brasileiros nas últimas duas semanas."""
    }
]
