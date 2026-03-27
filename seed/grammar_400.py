"""
300 A1 European Portuguese grammar questions.
Each dict: question_text, option_a/b/c/d, correct_answer, topic
"""

GRAMMAR: list[dict] = [

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: ser (to be — permanent)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Eu ___ português.",
     "option_a": "sou", "option_b": "és", "option_c": "é", "option_d": "somos",
     "correct_answer": "sou", "topic": "ser"},

    {"question_text": "Tu ___ estudante?",
     "option_a": "sou", "option_b": "és", "option_c": "é", "option_d": "são",
     "correct_answer": "és", "topic": "ser"},

    {"question_text": "Ela ___ médica.",
     "option_a": "sou", "option_b": "é", "option_c": "somos", "option_d": "são",
     "correct_answer": "é", "topic": "ser"},

    {"question_text": "Nós ___ de Lisboa.",
     "option_a": "são", "option_b": "somos", "option_c": "sou", "option_d": "é",
     "correct_answer": "somos", "topic": "ser"},

    {"question_text": "Eles ___ professores.",
     "option_a": "somos", "option_b": "sou", "option_c": "são", "option_d": "é",
     "correct_answer": "são", "topic": "ser"},

    {"question_text": "O João ___ engenheiro.",
     "option_a": "sou", "option_b": "és", "option_c": "é", "option_d": "somos",
     "correct_answer": "é", "topic": "ser"},

    {"question_text": "Vocês ___ irmãos?",
     "option_a": "são", "option_b": "sou", "option_c": "somos", "option_d": "é",
     "correct_answer": "são", "topic": "ser"},

    {"question_text": "O gato ___ pequeno.",
     "option_a": "sou", "option_b": "és", "option_c": "é", "option_d": "são",
     "correct_answer": "é", "topic": "ser"},

    {"question_text": "Eu e a Ana ___ amigas.",
     "option_a": "são", "option_b": "somos", "option_c": "é", "option_d": "sou",
     "correct_answer": "somos", "topic": "ser"},

    {"question_text": "De onde ___ tu?",
     "option_a": "sou", "option_b": "és", "option_c": "é", "option_d": "somos",
     "correct_answer": "és", "topic": "ser"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: estar (to be — temporary / state)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Eu ___ em casa.",
     "option_a": "estou", "option_b": "estás", "option_c": "está", "option_d": "estamos",
     "correct_answer": "estou", "topic": "estar"},

    {"question_text": "Tu ___ cansado?",
     "option_a": "estou", "option_b": "estás", "option_c": "está", "option_d": "estão",
     "correct_answer": "estás", "topic": "estar"},

    {"question_text": "Ela ___ doente hoje.",
     "option_a": "estou", "option_b": "estás", "option_c": "está", "option_d": "estão",
     "correct_answer": "está", "topic": "estar"},

    {"question_text": "Nós ___ no restaurante.",
     "option_a": "estão", "option_b": "estamos", "option_c": "estou", "option_d": "está",
     "correct_answer": "estamos", "topic": "estar"},

    {"question_text": "Eles ___ em Portugal.",
     "option_a": "estamos", "option_b": "estou", "option_c": "estão", "option_d": "está",
     "correct_answer": "estão", "topic": "estar"},

    {"question_text": "O café ___ fechado.",
     "option_a": "estou", "option_b": "estás", "option_c": "está", "option_d": "estamos",
     "correct_answer": "está", "topic": "estar"},

    {"question_text": "Vocês ___ bem?",
     "option_a": "estão", "option_b": "estou", "option_c": "está", "option_d": "estamos",
     "correct_answer": "estão", "topic": "estar"},

    {"question_text": "Eu ___ com fome.",
     "option_a": "estás", "option_b": "está", "option_c": "estou", "option_d": "estamos",
     "correct_answer": "estou", "topic": "estar"},

    {"question_text": "Onde ___ o hospital?",
     "option_a": "estou", "option_b": "estás", "option_c": "está", "option_d": "estamos",
     "correct_answer": "está", "topic": "estar"},

    {"question_text": "O tempo ___ bom hoje.",
     "option_a": "estou", "option_b": "estás", "option_c": "está", "option_d": "estão",
     "correct_answer": "está", "topic": "estar"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: ser vs. estar
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "A Maria ___ alta. (permanent characteristic)",
     "option_a": "está", "option_b": "é", "option_c": "estou", "option_d": "sou",
     "correct_answer": "é", "topic": "ser_estar"},

    {"question_text": "A sopa ___ quente agora. (temporary state)",
     "option_a": "é", "option_b": "somos", "option_c": "está", "option_d": "são",
     "correct_answer": "está", "topic": "ser_estar"},

    {"question_text": "Nós ___ portugueses. (nationality)",
     "option_a": "estamos", "option_b": "estou", "option_c": "somos", "option_d": "está",
     "correct_answer": "somos", "topic": "ser_estar"},

    {"question_text": "Tu ___ triste hoje? (emotional state)",
     "option_a": "és", "option_b": "estás", "option_c": "sou", "option_d": "estou",
     "correct_answer": "estás", "topic": "ser_estar"},

    {"question_text": "O museu ___ em Lisboa. (location of place)",
     "option_a": "é", "option_b": "sou", "option_c": "está", "option_d": "somos",
     "correct_answer": "é", "topic": "ser_estar"},

    {"question_text": "Ele ___ cansado depois do trabalho. (temporary state)",
     "option_a": "é", "option_b": "está", "option_c": "somos", "option_d": "são",
     "correct_answer": "está", "topic": "ser_estar"},

    {"question_text": "O João ___ médico. (profession)",
     "option_a": "está", "option_b": "é", "option_c": "estou", "option_d": "somos",
     "correct_answer": "é", "topic": "ser_estar"},

    {"question_text": "As janelas ___ abertas. (temporary state)",
     "option_a": "são", "option_b": "estou", "option_c": "é", "option_d": "estão",
     "correct_answer": "estão", "topic": "ser_estar"},

    {"question_text": "O livro ___ interessante. (quality/opinion)",
     "option_a": "está", "option_b": "estou", "option_c": "é", "option_d": "estamos",
     "correct_answer": "é", "topic": "ser_estar"},

    {"question_text": "Onde ___ a farmácia? (location—asking direction)",
     "option_a": "é", "option_b": "sou", "option_c": "estamos", "option_d": "está",
     "correct_answer": "está", "topic": "ser_estar"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: ter (to have)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Eu ___ um cão.",
     "option_a": "tens", "option_b": "tenho", "option_c": "tem", "option_d": "temos",
     "correct_answer": "tenho", "topic": "ter"},

    {"question_text": "Tu ___ irmãos?",
     "option_a": "tenho", "option_b": "tem", "option_c": "tens", "option_d": "têm",
     "correct_answer": "tens", "topic": "ter"},

    {"question_text": "Ela ___ vinte anos.",
     "option_a": "tenho", "option_b": "tens", "option_c": "tem", "option_d": "temos",
     "correct_answer": "tem", "topic": "ter"},

    {"question_text": "Nós ___ uma casa grande.",
     "option_a": "têm", "option_b": "tenho", "option_c": "tem", "option_d": "temos",
     "correct_answer": "temos", "topic": "ter"},

    {"question_text": "Eles ___ muito trabalho.",
     "option_a": "temos", "option_b": "tenho", "option_c": "têm", "option_d": "tem",
     "correct_answer": "têm", "topic": "ter"},

    {"question_text": "O hotel ___ piscina.",
     "option_a": "tenho", "option_b": "tens", "option_c": "tem", "option_d": "temos",
     "correct_answer": "tem", "topic": "ter"},

    {"question_text": "Eu não ___ fome.",
     "option_a": "tens", "option_b": "tenho", "option_c": "tem", "option_d": "têm",
     "correct_answer": "tenho", "topic": "ter"},

    {"question_text": "Quantos anos ___ tu?",
     "option_a": "tenho", "option_b": "tens", "option_c": "tem", "option_d": "temos",
     "correct_answer": "tens", "topic": "ter"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: ir (to go)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Eu ___ ao supermercado.",
     "option_a": "vais", "option_b": "vou", "option_c": "vai", "option_d": "vamos",
     "correct_answer": "vou", "topic": "ir"},

    {"question_text": "Tu ___ à escola hoje?",
     "option_a": "vou", "option_b": "vai", "option_c": "vais", "option_d": "vão",
     "correct_answer": "vais", "topic": "ir"},

    {"question_text": "Ele ___ ao trabalho de carro.",
     "option_a": "vou", "option_b": "vais", "option_c": "vai", "option_d": "vamos",
     "correct_answer": "vai", "topic": "ir"},

    {"question_text": "Nós ___ à praia no fim de semana.",
     "option_a": "vão", "option_b": "vou", "option_c": "vai", "option_d": "vamos",
     "correct_answer": "vamos", "topic": "ir"},

    {"question_text": "Elas ___ ao teatro amanhã.",
     "option_a": "vamos", "option_b": "vou", "option_c": "vão", "option_d": "vai",
     "correct_answer": "vão", "topic": "ir"},

    {"question_text": "Para onde ___ tu?",
     "option_a": "vou", "option_b": "vai", "option_c": "vais", "option_d": "vamos",
     "correct_answer": "vais", "topic": "ir"},

    {"question_text": "Nós ___ jantar fora esta noite.",
     "option_a": "vão", "option_b": "vou", "option_c": "vamos", "option_d": "vai",
     "correct_answer": "vamos", "topic": "ir"},

    {"question_text": "Eu ___ a Lisboa de comboio.",
     "option_a": "vai", "option_b": "vou", "option_c": "vais", "option_d": "vamos",
     "correct_answer": "vou", "topic": "ir"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: fazer (to do / to make)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "O que ___ tu ao fim de semana?",
     "option_a": "faço", "option_b": "fazes", "option_c": "faz", "option_d": "fazemos",
     "correct_answer": "fazes", "topic": "fazer"},

    {"question_text": "Eu ___ o jantar todos os dias.",
     "option_a": "fazes", "option_b": "faz", "option_c": "faço", "option_d": "fazemos",
     "correct_answer": "faço", "topic": "fazer"},

    {"question_text": "Ela ___ os trabalhos de casa.",
     "option_a": "faço", "option_b": "faz", "option_c": "fazes", "option_d": "fazem",
     "correct_answer": "faz", "topic": "fazer"},

    {"question_text": "Nós ___ muito exercício.",
     "option_a": "fazem", "option_b": "faz", "option_c": "fazemos", "option_d": "faço",
     "correct_answer": "fazemos", "topic": "fazer"},

    {"question_text": "Eles ___ uma festa no sábado.",
     "option_a": "fazemos", "option_b": "fazem", "option_c": "faz", "option_d": "faço",
     "correct_answer": "fazem", "topic": "fazer"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: regular -ar verbs  (falar, trabalhar, gostar, morar, estudar)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Eu ___ português todos os dias.",
     "option_a": "fala", "option_b": "falas", "option_c": "falo", "option_d": "falamos",
     "correct_answer": "falo", "topic": "regular_ar"},

    {"question_text": "Tu ___ inglês muito bem.",
     "option_a": "falo", "option_b": "falas", "option_c": "fala", "option_d": "falam",
     "correct_answer": "falas", "topic": "regular_ar"},

    {"question_text": "Ela ___ muito rápido.",
     "option_a": "falo", "option_b": "falas", "option_c": "fala", "option_d": "falamos",
     "correct_answer": "fala", "topic": "regular_ar"},

    {"question_text": "Nós ___ em Lisboa.",
     "option_a": "moram", "option_b": "moro", "option_c": "mora", "option_d": "moramos",
     "correct_answer": "moramos", "topic": "regular_ar"},

    {"question_text": "Eles ___ numa empresa grande.",
     "option_a": "trabalhamos", "option_b": "trabalha", "option_c": "trabalham", "option_d": "trabalho",
     "correct_answer": "trabalham", "topic": "regular_ar"},

    {"question_text": "Eu ___ de música.",
     "option_a": "gostas", "option_b": "gosta", "option_c": "gosto", "option_d": "gostamos",
     "correct_answer": "gosto", "topic": "regular_ar"},

    {"question_text": "Tu ___ de desporto?",
     "option_a": "gosto", "option_b": "gostas", "option_c": "gosta", "option_d": "gostam",
     "correct_answer": "gostas", "topic": "regular_ar"},

    {"question_text": "Eles ___ medicina na universidade.",
     "option_a": "estudo", "option_b": "estudam", "option_c": "estuda", "option_d": "estudamos",
     "correct_answer": "estudam", "topic": "regular_ar"},

    {"question_text": "Eu ___ no Porto.",
     "option_a": "mora", "option_b": "moras", "option_c": "moro", "option_d": "moram",
     "correct_answer": "moro", "topic": "regular_ar"},

    {"question_text": "Ela ___ numa escola primária.",
     "option_a": "trabalho", "option_b": "trabalhas", "option_c": "trabalha", "option_d": "trabalham",
     "correct_answer": "trabalha", "topic": "regular_ar"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: regular -er verbs  (comer, beber, vender, perceber)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Eu ___ peixe ao almoço.",
     "option_a": "comes", "option_b": "come", "option_c": "como", "option_d": "comemos",
     "correct_answer": "como", "topic": "regular_er"},

    {"question_text": "Tu ___ muita água?",
     "option_a": "bebo", "option_b": "bebes", "option_c": "bebe", "option_d": "bebemos",
     "correct_answer": "bebes", "topic": "regular_er"},

    {"question_text": "Ela ___ pão ao pequeno-almoço.",
     "option_a": "como", "option_b": "comes", "option_c": "come", "option_d": "comem",
     "correct_answer": "come", "topic": "regular_er"},

    {"question_text": "Nós ___ café ao fim da tarde.",
     "option_a": "bebem", "option_b": "bebo", "option_c": "bebe", "option_d": "bebemos",
     "correct_answer": "bebemos", "topic": "regular_er"},

    {"question_text": "Eles ___ legumes todos os dias.",
     "option_a": "comemos", "option_b": "como", "option_c": "comem", "option_d": "come",
     "correct_answer": "comem", "topic": "regular_er"},

    {"question_text": "Eu não ___ álcool.",
     "option_a": "bebes", "option_b": "bebe", "option_c": "bebo", "option_d": "bebem",
     "correct_answer": "bebo", "topic": "regular_er"},

    {"question_text": "Tu ___ português?",
     "option_a": "percebo", "option_b": "percebes", "option_c": "percebe", "option_d": "percebem",
     "correct_answer": "percebes", "topic": "regular_er"},

    {"question_text": "O mercado ___ frutas e legumes.",
     "option_a": "vendo", "option_b": "vendes", "option_c": "vende", "option_d": "vendemos",
     "correct_answer": "vende", "topic": "regular_er"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: regular -ir verbs  (partir, abrir, dormir)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "O comboio ___ às oito horas.",
     "option_a": "parto", "option_b": "partes", "option_c": "parte", "option_d": "partimos",
     "correct_answer": "parte", "topic": "regular_ir"},

    {"question_text": "Eu ___ a janela porque está calor.",
     "option_a": "abres", "option_b": "abre", "option_c": "abro", "option_d": "abrimos",
     "correct_answer": "abro", "topic": "regular_ir"},

    {"question_text": "Tu ___ a que horas?",
     "option_a": "durmo", "option_b": "dormes", "option_c": "dorme", "option_d": "dormimos",
     "correct_answer": "dormes", "topic": "regular_ir"},

    {"question_text": "Nós ___ para o Porto amanhã.",
     "option_a": "partem", "option_b": "parto", "option_c": "parte", "option_d": "partimos",
     "correct_answer": "partimos", "topic": "regular_ir"},

    {"question_text": "Ela ___ bem à noite.",
     "option_a": "durmo", "option_b": "dormes", "option_c": "dorme", "option_d": "dormem",
     "correct_answer": "dorme", "topic": "regular_ir"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: definite articles  (o, a, os, as)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "___ livro está na mesa.",
     "option_a": "A", "option_b": "Os", "option_c": "O", "option_d": "As",
     "correct_answer": "O", "topic": "articles"},

    {"question_text": "___ casa é muito bonita.",
     "option_a": "O", "option_b": "A", "option_c": "Os", "option_d": "As",
     "correct_answer": "A", "topic": "articles"},

    {"question_text": "___ professores são simpáticos.",
     "option_a": "A", "option_b": "O", "option_c": "Os", "option_d": "As",
     "correct_answer": "Os", "topic": "articles"},

    {"question_text": "___ crianças brincam no jardim.",
     "option_a": "Os", "option_b": "O", "option_c": "As", "option_d": "A",
     "correct_answer": "As", "topic": "articles"},

    {"question_text": "Eu gosto de ___ música clássica.",
     "option_a": "o", "option_b": "a", "option_c": "os", "option_d": "as",
     "correct_answer": "a", "topic": "articles"},

    {"question_text": "___ cão da Maria é castanho.",
     "option_a": "A", "option_b": "Os", "option_c": "O", "option_d": "As",
     "correct_answer": "O", "topic": "articles"},

    {"question_text": "___ janelas estão abertas.",
     "option_a": "O", "option_b": "A", "option_c": "Os", "option_d": "As",
     "correct_answer": "As", "topic": "articles"},

    {"question_text": "Onde está ___ autocarro?",
     "option_a": "a", "option_b": "o", "option_c": "os", "option_d": "as",
     "correct_answer": "o", "topic": "articles"},

    {"question_text": "___ filhos do Pedro são pequenos.",
     "option_a": "As", "option_b": "A", "option_c": "O", "option_d": "Os",
     "correct_answer": "Os", "topic": "articles"},

    {"question_text": "Eu gosto de ___ praias de Portugal.",
     "option_a": "o", "option_b": "os", "option_c": "as", "option_d": "a",
     "correct_answer": "as", "topic": "articles"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: indefinite articles  (um, uma, uns, umas)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Quero ___ café, por favor.",
     "option_a": "uma", "option_b": "um", "option_c": "uns", "option_d": "umas",
     "correct_answer": "um", "topic": "articles"},

    {"question_text": "Ela tem ___ gata muito bonita.",
     "option_a": "um", "option_b": "uns", "option_c": "uma", "option_d": "umas",
     "correct_answer": "uma", "topic": "articles"},

    {"question_text": "Há ___ livros na mesa.",
     "option_a": "uma", "option_b": "um", "option_c": "uns", "option_d": "umas",
     "correct_answer": "uns", "topic": "articles"},

    {"question_text": "Comprei ___ maçãs no mercado.",
     "option_a": "uns", "option_b": "um", "option_c": "umas", "option_d": "uma",
     "correct_answer": "umas", "topic": "articles"},

    {"question_text": "Tenho ___ amigo em Lisboa.",
     "option_a": "uma", "option_b": "um", "option_c": "uns", "option_d": "umas",
     "correct_answer": "um", "topic": "articles"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: prepositions  (em, de, para, com, sem, por)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Eu moro ___ Lisboa.",
     "option_a": "de", "option_b": "para", "option_c": "em", "option_d": "com",
     "correct_answer": "em", "topic": "prepositions"},

    {"question_text": "Ela vem ___ Porto.",
     "option_a": "em", "option_b": "de", "option_c": "para", "option_d": "sem",
     "correct_answer": "de", "topic": "prepositions"},

    {"question_text": "Este presente é ___ a minha mãe.",
     "option_a": "de", "option_b": "em", "option_c": "para", "option_d": "por",
     "correct_answer": "para", "topic": "prepositions"},

    {"question_text": "Vou ao cinema ___ os meus amigos.",
     "option_a": "de", "option_b": "para", "option_c": "com", "option_d": "sem",
     "correct_answer": "com", "topic": "prepositions"},

    {"question_text": "Ele bebe café ___ açúcar.",
     "option_a": "com", "option_b": "para", "option_c": "sem", "option_d": "de",
     "correct_answer": "sem", "topic": "prepositions"},

    {"question_text": "O livro é ___ João.",
     "option_a": "para", "option_b": "com", "option_c": "do", "option_d": "sem",
     "correct_answer": "do", "topic": "prepositions"},

    {"question_text": "Estou ___ Portugal há dois anos.",
     "option_a": "de", "option_b": "para", "option_c": "em", "option_d": "por",
     "correct_answer": "em", "topic": "prepositions"},

    {"question_text": "Falo ___ ela todos os dias.",
     "option_a": "de", "option_b": "com", "option_c": "para", "option_d": "sem",
     "correct_answer": "com", "topic": "prepositions"},

    {"question_text": "Obrigado ___ tudo!",
     "option_a": "de", "option_b": "para", "option_c": "por", "option_d": "em",
     "correct_answer": "por", "topic": "prepositions"},

    {"question_text": "O comboio ___ Lisboa chega às dez.",
     "option_a": "para", "option_b": "de", "option_c": "em", "option_d": "com",
     "correct_answer": "de", "topic": "prepositions"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: contractions  (a + o = ao, de + o = do, em + o = no…)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Vou ___ supermercado comprar pão.",
     "option_a": "de o", "option_b": "em o", "option_c": "ao", "option_d": "para o",
     "correct_answer": "ao", "topic": "contractions"},

    {"question_text": "Ela vem ___ escola a pé.",
     "option_a": "ao", "option_b": "da", "option_c": "em a", "option_d": "para a",
     "correct_answer": "da", "topic": "contractions"},

    {"question_text": "Moro ___ Porto.",
     "option_a": "em o", "option_b": "de o", "option_c": "no", "option_d": "ao",
     "correct_answer": "no", "topic": "contractions"},

    {"question_text": "Gosto muito ___ praias portuguesas.",
     "option_a": "em as", "option_b": "das", "option_c": "a as", "option_d": "para as",
     "correct_answer": "das", "topic": "contractions"},

    {"question_text": "Vamos ___ praia amanhã.",
     "option_a": "de a", "option_b": "em a", "option_c": "à", "option_d": "do",
     "correct_answer": "à", "topic": "contractions"},

    {"question_text": "O carro ___ meu pai é vermelho.",
     "option_a": "de o", "option_b": "ao", "option_c": "do", "option_d": "no",
     "correct_answer": "do", "topic": "contractions"},

    {"question_text": "Estamos ___ casa.",
     "option_a": "de a", "option_b": "na", "option_c": "ao", "option_d": "da",
     "correct_answer": "na", "topic": "contractions"},

    {"question_text": "Vou ___ médico amanhã.",
     "option_a": "no", "option_b": "da", "option_c": "ao", "option_d": "na",
     "correct_answer": "ao", "topic": "contractions"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: gender agreement
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "A rapariga é muito ___.",
     "option_a": "bonito", "option_b": "bonita", "option_c": "bonitos", "option_d": "bonitas",
     "correct_answer": "bonita", "topic": "gender"},

    {"question_text": "O rapaz é muito ___.",
     "option_a": "bonita", "option_b": "bonitas", "option_c": "bonito", "option_d": "bonitos",
     "correct_answer": "bonito", "topic": "gender"},

    {"question_text": "A casa é muito ___.",
     "option_a": "grande", "option_b": "grandes", "option_c": "grando", "option_d": "granda",
     "correct_answer": "grande", "topic": "gender"},

    {"question_text": "Ela é muito ___.",
     "option_a": "simpático", "option_b": "simpática", "option_c": "simpáticos", "option_d": "simpáticas",
     "correct_answer": "simpática", "topic": "gender"},

    {"question_text": "O professor é muito ___.",
     "option_a": "cansada", "option_b": "cansados", "option_c": "cansado", "option_d": "cansadas",
     "correct_answer": "cansado", "topic": "gender"},

    {"question_text": "A sopa está ___.",
     "option_a": "quento", "option_b": "quente", "option_c": "quentes", "option_d": "quenta",
     "correct_answer": "quente", "topic": "gender"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: plural formation
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Um livro → ___",
     "option_a": "livros", "option_b": "livres", "option_c": "librões", "option_d": "livreis",
     "correct_answer": "livros", "topic": "plurals"},

    {"question_text": "Uma cidade → ___",
     "option_a": "cidads", "option_b": "cidades", "option_c": "cidades", "option_d": "cidadis",
     "correct_answer": "cidades", "topic": "plurals"},

    {"question_text": "Um pão → ___",
     "option_a": "pões", "option_b": "pãos", "option_c": "pães", "option_d": "pãos",
     "correct_answer": "pães", "topic": "plurals"},

    {"question_text": "Um animal → ___",
     "option_a": "animais", "option_b": "animales", "option_c": "animals", "option_d": "animaus",
     "correct_answer": "animais", "topic": "plurals"},

    {"question_text": "Um português → ___",
     "option_a": "portugueses", "option_b": "portuguêses", "option_c": "portugals", "option_d": "português",
     "correct_answer": "portugueses", "topic": "plurals"},

    {"question_text": "Uma flor → ___",
     "option_a": "flores", "option_b": "floris", "option_c": "flors", "option_d": "florais",
     "correct_answer": "flores", "topic": "plurals"},

    {"question_text": "Um irmão → ___",
     "option_a": "irmãos", "option_b": "irmões", "option_c": "irmão", "option_d": "irmãs",
     "correct_answer": "irmãos", "topic": "plurals"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: negation
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Eu ___ falo espanhol.",
     "option_a": "nunca", "option_b": "não", "option_c": "nem", "option_d": "nada",
     "correct_answer": "não", "topic": "negation"},

    {"question_text": "Ela ___ come carne.",
     "option_a": "nada", "option_b": "nem", "option_c": "não", "option_d": "nunca",
     "correct_answer": "não", "topic": "negation"},

    {"question_text": "Não tenho ___ dinheiro.",
     "option_a": "nunca", "option_b": "não", "option_c": "nenhum", "option_d": "nem",
     "correct_answer": "nenhum", "topic": "negation"},

    {"question_text": "Eu ___ vou a festas.",
     "option_a": "não", "option_b": "nunca", "option_c": "nada", "option_d": "nenhum",
     "correct_answer": "nunca", "topic": "negation"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: question formation
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "___ é o teu nome?",
     "option_a": "Onde", "option_b": "Quando", "option_c": "Qual", "option_d": "Como",
     "correct_answer": "Qual", "topic": "questions"},

    {"question_text": "___ moras?",
     "option_a": "Como", "option_b": "Onde", "option_c": "Quando", "option_d": "Quem",
     "correct_answer": "Onde", "topic": "questions"},

    {"question_text": "___ anos tens?",
     "option_a": "Qual", "option_b": "Onde", "option_c": "Quantos", "option_d": "Como",
     "correct_answer": "Quantos", "topic": "questions"},

    {"question_text": "___ chamas?",
     "option_a": "Quando", "option_b": "Como te", "option_c": "Onde te", "option_d": "Por que",
     "correct_answer": "Como te", "topic": "questions"},

    {"question_text": "___ está o banco?",
     "option_a": "Como", "option_b": "Quem", "option_c": "Onde", "option_d": "Quando",
     "correct_answer": "Onde", "topic": "questions"},

    {"question_text": "___ custa este casaco?",
     "option_a": "Onde", "option_b": "Quanto", "option_c": "Como", "option_d": "Qual",
     "correct_answer": "Quanto", "topic": "questions"},

    {"question_text": "___ chega o comboio?",
     "option_a": "Quem", "option_b": "Onde", "option_c": "Quando", "option_d": "Como",
     "correct_answer": "Quando", "topic": "questions"},

    {"question_text": "___ vai à festa?",
     "option_a": "Onde", "option_b": "Quem", "option_c": "Como", "option_d": "Quando",
     "correct_answer": "Quem", "topic": "questions"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: possessives  (meu, teu, seu, nosso…)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Este é o ___ livro (de eu).",
     "option_a": "teu", "option_b": "seu", "option_c": "meu", "option_d": "nosso",
     "correct_answer": "meu", "topic": "possessives"},

    {"question_text": "Onde está a ___ mochila (de tu)?",
     "option_a": "minha", "option_b": "sua", "option_c": "nossa", "option_d": "tua",
     "correct_answer": "tua", "topic": "possessives"},

    {"question_text": "A Ana foi visitar o ___ avô (dela).",
     "option_a": "meu", "option_b": "seu", "option_c": "teu", "option_d": "nosso",
     "correct_answer": "seu", "topic": "possessives"},

    {"question_text": "___ casa é muito grande.",
     "option_a": "Minha nossa", "option_b": "Nossa", "option_c": "Nosso", "option_d": "Nossas",
     "correct_answer": "Nossa", "topic": "possessives"},

    {"question_text": "Eles trouxeram os ___ filhos.",
     "option_a": "seus", "option_b": "nossos", "option_c": "meus", "option_d": "teus",
     "correct_answer": "seus", "topic": "possessives"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: demonstratives  (este/essa/aquele)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "___ livro aqui é meu.",
     "option_a": "Esse", "option_b": "Aquele", "option_c": "Este", "option_d": "Aquela",
     "correct_answer": "Este", "topic": "demonstratives"},

    {"question_text": "___ casa ali é nova.",
     "option_a": "Esta", "option_b": "Esse", "option_c": "Essa", "option_d": "Aquela",
     "correct_answer": "Essa", "topic": "demonstratives"},

    {"question_text": "___ carro lá longe é de luxo.",
     "option_a": "Este", "option_b": "Esse", "option_c": "Aquele", "option_d": "Aquelas",
     "correct_answer": "Aquele", "topic": "demonstratives"},

    {"question_text": "___ são as minhas chaves.",
     "option_a": "Este", "option_b": "Estes", "option_c": "Estas", "option_d": "Esse",
     "correct_answer": "Estas", "topic": "demonstratives"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: numbers & time
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "São ___ horas. (it is 3 o'clock)",
     "option_a": "dois", "option_b": "três", "option_c": "uma", "option_d": "quatro",
     "correct_answer": "três", "topic": "time"},

    {"question_text": "É ___ hora. (it is 1 o'clock)",
     "option_a": "um", "option_b": "uma", "option_c": "dois", "option_d": "duas",
     "correct_answer": "uma", "topic": "time"},

    {"question_text": "O comboio parte às ___ e meia. (7:30)",
     "option_a": "oito", "option_b": "seis", "option_c": "sete", "option_d": "nove",
     "correct_answer": "sete", "topic": "time"},

    {"question_text": "Hoje é ___. (Monday)",
     "option_a": "terça-feira", "option_b": "quarta-feira", "option_c": "segunda-feira", "option_d": "domingo",
     "correct_answer": "segunda-feira", "topic": "time"},

    {"question_text": "O meu aniversário é em ___. (December)",
     "option_a": "novembro", "option_b": "setembro", "option_c": "dezembro", "option_d": "outubro",
     "correct_answer": "dezembro", "topic": "time"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: vocabulary in context  (practical A1 sentences)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Quero ___ um café, por favor. (order)",
     "option_a": "vender", "option_b": "pedir", "option_c": "beber", "option_d": "comprar",
     "correct_answer": "pedir", "topic": "vocabulary_context"},

    {"question_text": "Preciso de ___ o bilhete antes de entrar.",
     "option_a": "vender", "option_b": "perder", "option_c": "comprar", "option_d": "trazer",
     "correct_answer": "comprar", "topic": "vocabulary_context"},

    {"question_text": "Ela ___ inglês e francês.",
     "option_a": "bebe", "option_b": "come", "option_c": "fala", "option_d": "lê",
     "correct_answer": "fala", "topic": "vocabulary_context"},

    {"question_text": "Onde posso ___ o autocarro para o centro?",
     "option_a": "beber", "option_b": "apanhar", "option_c": "comer", "option_d": "escrever",
     "correct_answer": "apanhar", "topic": "vocabulary_context"},

    {"question_text": "Tenho de ___ ao médico amanhã.",
     "option_a": "beber", "option_b": "comer", "option_c": "ir", "option_d": "vender",
     "correct_answer": "ir", "topic": "vocabulary_context"},

    {"question_text": "Por favor, pode ___ mais devagar?",
     "option_a": "falar", "option_b": "comer", "option_c": "dormir", "option_d": "comprar",
     "correct_answer": "falar", "topic": "vocabulary_context"},

    {"question_text": "Vou ___ uma mesa para dois, por favor. (reserve)",
     "option_a": "comprar", "option_b": "reservar", "option_c": "vender", "option_d": "fechar",
     "correct_answer": "reservar", "topic": "vocabulary_context"},

    {"question_text": "Nós ___ peixe com batatas ao almoço.",
     "option_a": "bebemos", "option_b": "comemos", "option_c": "lemos", "option_d": "dormimos",
     "correct_answer": "comemos", "topic": "vocabulary_context"},

    {"question_text": "Ela ___ a carta e ficou feliz.",
     "option_a": "bebeu", "option_b": "leu", "option_c": "comeu", "option_d": "dormiu",
     "correct_answer": "leu", "topic": "vocabulary_context"},

    {"question_text": "O médico disse que preciso de ___ muito água.",
     "option_a": "comer", "option_b": "comprar", "option_c": "beber", "option_d": "vender",
     "correct_answer": "beber", "topic": "vocabulary_context"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: very common phrases & expressions
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Como se diz 'thank you' em português?",
     "option_a": "Desculpe", "option_b": "Por favor", "option_c": "Obrigado", "option_d": "De nada",
     "correct_answer": "Obrigado", "topic": "phrases"},

    {"question_text": "Como se diz 'you're welcome' em português?",
     "option_a": "Obrigado", "option_b": "Por favor", "option_c": "De nada", "option_d": "Desculpe",
     "correct_answer": "De nada", "topic": "phrases"},

    {"question_text": "O que significa 'com licença'?",
     "option_a": "I'm sick", "option_b": "Excuse me (to pass)", "option_c": "Thank you", "option_d": "Goodbye",
     "correct_answer": "Excuse me (to pass)", "topic": "phrases"},

    {"question_text": "Qual é a tradução de 'Bom dia'?",
     "option_a": "Good night", "option_b": "Good afternoon", "option_c": "Good morning", "option_d": "Good evening",
     "correct_answer": "Good morning", "topic": "phrases"},

    {"question_text": "O que quer dizer 'até logo'?",
     "option_a": "Good morning", "option_b": "See you soon", "option_c": "Thank you", "option_d": "Please",
     "correct_answer": "See you soon", "topic": "phrases"},

    {"question_text": "Qual é a tradução de 'Boa noite'?",
     "option_a": "Good morning", "option_b": "Good afternoon", "option_c": "Good evening / night", "option_d": "See you later",
     "correct_answer": "Good evening / night", "topic": "phrases"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: querer (to want) / poder (can)
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "Eu ___ uma água, por favor.",
     "option_a": "queres", "option_b": "quer", "option_c": "quero", "option_d": "queremos",
     "correct_answer": "quero", "topic": "modal_verbs"},

    {"question_text": "___ abrir a janela?",
     "option_a": "Posso", "option_b": "Podes", "option_c": "Pode", "option_d": "Podemos",
     "correct_answer": "Pode", "topic": "modal_verbs"},

    {"question_text": "Tu ___ vir amanhã?",
     "option_a": "posso", "option_b": "pode", "option_c": "podes", "option_d": "podemos",
     "correct_answer": "podes", "topic": "modal_verbs"},

    {"question_text": "Nós ___ ajudar?",
     "option_a": "posso", "option_b": "podemos", "option_c": "podem", "option_d": "pode",
     "correct_answer": "podemos", "topic": "modal_verbs"},

    {"question_text": "Eles ___ sair mais cedo.",
     "option_a": "quero", "option_b": "queremos", "option_c": "quer", "option_d": "querem",
     "correct_answer": "querem", "topic": "modal_verbs"},

    # ══════════════════════════════════════════════════════════════════════
    # TOPIC: fill-in practical contexts
    # ══════════════════════════════════════════════════════════════════════
    {"question_text": "O ___ está fechado ao domingo. (shop)",
     "option_a": "hospital", "option_b": "autocarro", "option_c": "supermercado", "option_d": "avião",
     "correct_answer": "supermercado", "topic": "vocabulary_context"},

    {"question_text": "Preciso de um ___ para pagar. (card)",
     "option_a": "bilhete", "option_b": "cartão", "option_c": "recibo", "option_d": "preço",
     "correct_answer": "cartão", "topic": "vocabulary_context"},

    {"question_text": "Vou de ___ porque é mais rápido. (metro)",
     "option_a": "autocarro", "option_b": "bicicleta", "option_c": "barco", "option_d": "metro",
     "correct_answer": "metro", "topic": "vocabulary_context"},

    {"question_text": "Hoje está muito ___. (sunny / hot)",
     "option_a": "frio", "option_b": "chuva", "option_c": "calor", "option_d": "neve",
     "correct_answer": "calor", "topic": "vocabulary_context"},

    {"question_text": "A ___ fica ao lado do banco. (pharmacy)",
     "option_a": "escola", "option_b": "farmácia", "option_c": "praia", "option_d": "estação",
     "correct_answer": "farmácia", "topic": "vocabulary_context"},

    {"question_text": "Quero reservar um ___ para dois adultos. (room)",
     "option_a": "bilhete", "option_b": "quarto", "option_c": "café", "option_d": "carro",
     "correct_answer": "quarto", "topic": "vocabulary_context"},

    {"question_text": "Ela tem dores de ___. (head → headache)",
     "option_a": "mão", "option_b": "pé", "option_c": "cabeça", "option_d": "costas",
     "correct_answer": "cabeça", "topic": "vocabulary_context"},

    {"question_text": "O ___ parte da estação às nove horas. (train)",
     "option_a": "autocarro", "option_b": "avião", "option_c": "comboio", "option_d": "barco",
     "correct_answer": "comboio", "topic": "vocabulary_context"},

    {"question_text": "Fui de férias à ___ em agosto. (beach)",
     "option_a": "montanha", "option_b": "floresta", "option_c": "cidade", "option_d": "praia",
     "correct_answer": "praia", "topic": "vocabulary_context"},

    {"question_text": "Vou ao ___ comprar pão e leite. (supermarket)",
     "option_a": "hospital", "option_b": "teatro", "option_c": "supermercado", "option_d": "banco",
     "correct_answer": "supermercado", "topic": "vocabulary_context"},

    {"question_text": "O Pedro ___ medicina na universidade.",
     "option_a": "bebe", "option_b": "estuda", "option_c": "come", "option_d": "vende",
     "correct_answer": "estuda", "topic": "vocabulary_context"},

    {"question_text": "Tens ___ de levar um casaco — está frio.",
     "option_a": "de", "option_b": "que", "option_c": "para", "option_d": "com",
     "correct_answer": "de", "topic": "vocabulary_context"},

    {"question_text": "A minha mãe ___ às seis da manhã todos os dias.",
     "option_a": "dorme", "option_b": "acorda", "option_c": "senta", "option_d": "corre",
     "correct_answer": "acorda", "topic": "vocabulary_context"},

    {"question_text": "Quanto ___ este vestido?",
     "option_a": "custa", "option_b": "tem", "option_c": "vai", "option_d": "está",
     "correct_answer": "custa", "topic": "vocabulary_context"},

    {"question_text": "Podem trazer a ___, por favor? (bill / check)",
     "option_a": "receita", "option_b": "carta", "option_c": "conta", "option_d": "senha",
     "correct_answer": "conta", "topic": "vocabulary_context"},

]
