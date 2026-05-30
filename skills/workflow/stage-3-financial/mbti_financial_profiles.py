#!/usr/bin/env python3
"""
MBTI × Financial Profiles — 16 tipos de personalidade e seu comportamento financeiro
Baseado em psicologia financeira e padrões observados por tipo MBTI.
Referência: MBTI Financeiro (https://www.myersbriggs.org/)
"""

FINANCIAL_PROFILES = {
    "INTJ": {
        "name_pt_BR": "O Arquiteto",
        "summary": "Planejador estratégico que vê dinheiro como ferramenta para realizar visões de longo prazo.",
        "detailed_profile": "INTJs abordam finanças como um sistema a ser otimizado. Criam planos financeiros detalhados e raramente se desviam. Preferem investir em conhecimento, ferramentas e projetos que expandam sua visão de futuro. A disciplina é seu maior ativo financeiro, mas podem ignorar o custo emocional de decisões puramente lógicas.",
        "strengths": [
            "Planejamento financeiro estratégico de longo prazo",
            "Disciplina para seguir orçamentos e metas",
            "Capacidade de adiar gratificação por objetivos maiores",
            "Investimentos bem pesquisados e calculados",
            "Automatização eficiente de finanças pessoais"
        ],
        "weaknesses": [
            "Pode ignorar necessidades emocionais em nome da eficiência",
            "Gasto impulsivo em projetos de alto impacto (tudo ou nada)",
            "Dificuldade em orçar para prazeres simples e descanso",
            "Tendência a subestimar custos de manutenção",
            "Impaciência com conselhos financeiros que considera 'óbvios'"
        ],
        "saving_style": "Sistemático e automatizado. Prefere contas separadas por objetivo. Poupa para independência, não para segurança.",
        "spending_style": "Gasta em educação, ferramentas de alta qualidade, livros, cursos e tecnologia. Economiza em experiências sociais e itens de status.",
        "risk_profile": "Assume riscos calculados. Pesquisa exaustivamente antes de investir. Prefere entender o mecanismo antes de alocar capital.",
        "money_belief": "Dinheiro é recurso, não objetivo. Um meio para realizar visões e construir legado.",
        "recommended_strategies": [
            "Automatizar 30%%+ da renda para investimentos antes de qualquer gasto",
            "Criar fundo de emergência de 12 meses (valoriza independência)",
            "Alocar 10%% em 'projetos estratégicos' — cursos, ferramentas, experimentos",
            "Usar planilha de patrimônio líquido mensal (satisfaz necessidade de ver progresso)",
            "Reservar 5%% para 'gasto livre' — para não sufocar o perfeccionismo financeiro"
        ],
        "common_pitfalls": [
            "Subestimar custos emocionais de decisões financeiras",
            "Gastar demais em 'otimização' que nunca se paga",
            "Ignorar seguros e proteções por excesso de confiança na própria capacidade"
        ],
        "mbti_financial_insight": "INTJs: seu cérebro projeta cenários futuros com alta precisão. Use isso a seu favor — modele financeiramente seus próximos 10 anos. Mas lembre: modelos são mapas, não o território. Reserve margem para o inesperado."
    },
    "INTP": {
        "name_pt_BR": "O Lógico",
        "summary": "Analisador curioso que busca entender todos os instrumentos financeiros antes de agir — e às vezes nunca age.",
        "detailed_profile": "INTPs adoram estudar finanças: leem sobre investimentos, criptomoedas, impostos, estratégias. Mas a análise pode paralisar a ação. Precisam de sistemas simples que tirem a decisão da equação. Tendem a subestimar a renda e superdimensionar riscos — mas quando investem, é com conhecimento profundo.",
        "strengths": [
            "Compreensão profunda de instrumentos financeiros",
            "Detecção de falhas lógicas em planos financeiros",
            "Criatividade para encontrar soluções financeiras não óbvias",
            "Baixo consumo por status ou aparência",
            "Adaptabilidade a mudanças econômicas"
        ],
        "weaknesses": [
            "Análise excessiva leva à paralisia (analysis paralysis)",
            "Dificuldade em automatizar — prefere entender a executar",
            "Tendência a negligenciar burocracia financeira",
            "Pode subestimar a importância de renda estável",
            "Impaciência com planejamento financeiro de curto prazo"
        ],
        "saving_style": "Irregular. Poupa quando sobra. Precisa de sistemas que separem antes que ele veja o dinheiro.",
        "spending_style": "Gasta em conhecimento: cursos, livros, assinaturas acadêmicas, experimentos. O que parece 'supérfluo' para outros é investimento em curiosidade.",
        "risk_profile": "Cauteloso — precisa entender 100%% do instrumento antes de investir. Mas uma vez que entende, pode fazer apostas ousadas.",
        "money_belief": "Dinheiro é um sistema fascinante. Entender como funciona é tão interessante quanto tê-lo.",
        "recommended_strategies": [
            "Automatização total — débito automático para investimento no dia seguinte ao recebimento",
            "Portfólio simples: 1-2 ETFs globais + renda fixa. Chega de otimizar.",
            "Criar 'conta de experimentos' com 5%% para testar teses financeiras",
            "Usar app que resuma patrimônio uma vez por mês (sem detalhes para não hiperfocar)",
            "Estabelecer gatilho: 'se pesquisar mais de 2 semanas sobre um investimento, executo ou descarto'"
        ],
        "common_pitfalls": [
            "Nunca começar por querer o plano perfeito",
            "Gastar demais em cursos que não geram retorno",
            "Esquecer contas e impostos por falta de sistema"
        ],
        "mbti_financial_insight": "INTPs: seu superpoder é ver padrões que ninguém vê. Use-o para identificar oportunidades, não para adiar decisões. O melhor investimento é aquele que você realmente faz — não aquele que você analisou perfeitamente."
    },
    "ENTJ": {
        "name_pt_BR": "O Comandante",
        "summary": "Estrategista financeiro nato que constrói impérios com visão, disciplina e execução implacável.",
        "detailed_profile": "ENTJs veem finanças como um jogo de conquista. Estabelecem metas ambiciosas e mobilizam todos os recursos para alcançá-las. São excelentes em negociar, empreender e construir múltiplas fontes de renda. O desafio: podem queimar pontes e pessoas no processo, e o impulso de 'ganhar mais' pode nunca ser saciado.",
        "strengths": [
            "Liderança financeira — toma decisões com rapidez e convicção",
            "Capacidade de gerar múltiplas fontes de renda",
            "Excelente em negociação e networking financeiro",
            "Visão de longo prazo com execução disciplinada",
            "Resiliência a perdas — vê como aprendizado"
        ],
        "weaknesses": [
            "Impaciência com retornos lentos — pode buscar atalhos arriscados",
            "Tendência a superestimar capacidade de gerar renda",
            "Pode negligenciar poupança em favor de investimento agressivo",
            "Dificuldade em desacelerar e aproveitar o que construiu",
            "Estilo de vida pode escalar junto com a renda (lifestyle creep)"
        ],
        "saving_style": "Minimalista — poupa o necessário para liberar capital para investimentos. Prefere ativos a dinheiro parado.",
        "spending_style": "Gasta em imagem, networking, ferramentas de produtividade e experiências de alto impacto. Investe em parecer bem-sucedido (e isso gera mais sucesso).",
        "risk_profile": "Assume riscos altos de forma calculada. Não tem medo de perder — tem medo de não tentar.",
        "money_belief": "Dinheiro é uma medida de sucesso e um instrumento de poder. Ter mais = poder fazer mais.",
        "recommended_strategies": [
            "Regra 50/30/20 com metas agressivas de investimento (30%%+)",
            "Diversificação obrigatória — freio natural para o excesso de confiança",
            "Mentor financeiro que questione suas decisões (não apenas quem concorde)",
            "Reserva de emergência de 6 meses em renda fixa (âncora para dias de 'vou arriscar tudo')",
            "Revisão trimestral com indicadores de bem-estar (não só patrimônio)"
        ],
        "common_pitfalls": [
            "Apostar demais em um único negócio/investimento",
            "Queimar pontes profissionais por atalhos financeiros",
            "Confundir patrimônio com valor pessoal"
        ],
        "mbti_financial_insight": "ENTJs: seu maior risco não é perder dinheiro — é nunca ter o suficiente. Defina 'o bastante' agora, antes que o jogo financeiro consuma sua vida. O império que vale a pena construir é o que inclui tempo para vivê-lo."
    },
    "ENTP": {
        "name_pt_BR": "O Debatedor",
        "summary": "Inovador financeiro que enxerga oportunidades onde outros veem problemas — mas pode pular de ideia em ideia sem concretizar nenhuma.",
        "detailed_profile": "ENTPs são empreendedores em série no mundo financeiro. Spotam tendências, criam estratégias não convencionais e adoram o jogo de negociar. O problema: o tédio chega rápido. Projetos de longo prazo (como aposentadoria) são abstratos demais para engajar. Precisam de sistemas que transformem consistência em desafio.",
        "strengths": [
            "Identificação rápida de oportunidades financeiras",
            "Criatividade para gerar renda de fontes não óbvias",
            "Excelente em negociação e vendas",
            "Adaptabilidade a mudanças econômicas",
            "Networking amplo e diversificado"
        ],
        "weaknesses": [
            "Dificuldade em manter consistência — pula de estratégia em estratégia",
            "Tédio com planejamento financeiro de rotina",
            "Impulso de 'apostar' em ideias novas antes de pesquisar",
            "Subestima a importância de fundo de emergência",
            "Pode negligenciar obrigações fiscais e burocráticas"
        ],
        "saving_style": "Errático. Precisa de gamificação — desafios de poupança, metas curtas, recompensas.",
        "spending_style": "Gasta em experiências novas, gadgets, viagens, cursos, Startups. O novo é irresistível.",
        "risk_profile": "Assume riscos com entusiasmo. Precisa de um 'freio' externo — parceiro ou sistema que o impeça de alocar demais em ideias não testadas.",
        "money_belief": "Dinheiro é combustível para explorar possibilidades. Quanto mais, mais se pode experimentar.",
        "recommended_strategies": [
            "Automatizar poupança antes de ver o dinheiro (remove a tentação de 'experimentar')",
            "Criar 'regra dos 7 dias': esperar uma semana antes de qualquer investimento não-planejado",
            "Alocar 70%% em investimentos sólidos (chatos, mas seguros) e 30%% em 'apostas inteligentes'",
            "Usar planilha gamificada com metas de curto prazo (30 dias)",
            "Ter um parceiro financeiro (cônjuge, amigo, mentor) que valide grandes decisões"
        ],
        "common_pitfalls": [
            "Diversificação excessiva — tantos investimentos que nenhum cresce",
            "Entrar em esquemas complexos por pura curiosidade intelectual",
            "Gastar mais do que ganha em períodos de otimismo"
        ],
        "mbti_financial_insight": "ENTPs: sua mente gera ideias financeiras brilhantes. Mas ideias não pagam contas — execução sim. Escolha UMA estratégia por semestre e leve até o fim. A próxima ideia vai esperar."
    },
    "INFJ": {
        "name_pt_BR": "O Advogado",
        "summary": "Guardião financeiro que busca segurança para si e para quem ama — com uma visão de abundância que vai além do material.",
        "detailed_profile": "INFJs veem dinheiro como ferramenta de cuidado e proteção. Poupar para eles não é sobre números — é sobre criar segurança para realizar seu propósito. São poupadores naturais, mas podem sacrificar demais o presente pelo futuro. Também tendem a gastar em causas e pessoas com generosidade que pode desbalancear o orçamento.",
        "strengths": [
            "Poupança disciplinada e consistente",
            "Visão de longo prazo alinhada com valores pessoais",
            "Capacidade de sacrificar conforto presente por segurança futura",
            "Generosidade financeira equilibrada com planejamento",
            "Baixo consumo por status"
        ],
        "weaknesses": [
            "Pode sacrificar demais o presente ('já já vou aproveitar')",
            "Dificuldade em dizer 'não' financeiramente para quem ama",
            "Tendência a acumular por medo, não por estratégia",
            "Pode evitar riscos mesmo quando valem a pena",
            "Estresse financeiro silencioso — não pede ajuda até estar sobrecarregado"
        ],
        "saving_style": "Conservador e emocional. Poupa para segurança, não para acumular. Poupar é cuidar.",
        "spending_style": "Gasta em causas, presentes, bem-estar de quem ama, experiências significativas. Subinveste em si mesmo.",
        "risk_profile": "Averso a riscos. Prefere renda fixa e o conhecido. Precisa de motivação baseada em propósito para investir de forma mais ousada.",
        "money_belief": "Dinheiro é segurança. Ter o suficiente é libertador — permite focar no que realmente importa.",
        "recommended_strategies": [
            "Fundo de emergência de 12 meses (traz paz de espírito)",
            "Alocar 10%% para 'propósito' — doações, ajudar família, causas",
            "Investimento em renda variável com propósito: 'este ETF financia minha liberdade'",
            "Orçamento com categoria 'autocuidado' obrigatória (não negociável)",
            "Revisão trimestral com foco em 'estou mais segura que há 3 meses?'"
        ],
        "common_pitfalls": [
            "Acumular demais sem nunca usufruir",
            "Assumir dívidas de familiares por culpa",
            "Confundir segurança financeira com controle excessivo"
        ],
        "mbti_financial_insight": "INFJs: seu dom não é acumular, é distribuir. Construa segurança primeiro — depois, use os recursos com generosidade estratégica. O mundo precisa da sua visão, e ela precisa de combustível financeiro para existir."
    },
    "INFP": {
        "name_pt_BR": "O Mediador",
        "summary": "Idealista financeiro que quer que o dinheiro sirva a um propósito maior — e luta para equilibrar ideais com realidade.",
        "detailed_profile": "INFPs veem dinheiro como um mal necessário — prefeririam um mundo onde não precisasse existir. Isso pode levar a dois extremos: negligência total (finanças como 'depois eu vejo') ou hiper-responsabilidade por medo de não estar à altura. Quando conectam finanças a um propósito, tornam-se incrivelmente disciplinados.",
        "strengths": [
            "Disciplina quando conectada a um propósito significativo",
            "Criatividade para gerar renda de formas autênticas",
            "Resistência ao consumismo e pressões sociais",
            "Generosidade genuína e desprendimento material",
            "Capacidade de viver com menos quando necessário"
        ],
        "weaknesses": [
            "Evitação de planejamento financeiro ('depois eu vejo')",
            "Tendência a gastar por impulso emocional",
            "Dificuldade em negociar ou pedir aumento",
            "Pode romantizar a pobreza ('artista sofredor')",
            "Ansiedade financeira que paralisa em vez de motivar"
        ],
        "saving_style": "Esporádico. Poupa em ondas de motivação. Precisa de propósito claro para manter consistência.",
        "spending_style": "Gasta em arte, livros, música, experiências significativas, causas sociais. O que parece 'fútil' para outros é expressão de quem é.",
        "risk_profile": "Prefere não pensar em riscos. Pode ser tanto excessivamente cauteloso quanto impulsivo — depende do momento emocional.",
        "money_belief": "Dinheiro não deveria ser tão importante... mas é. Quero que ele sirva ao que importa, não ao contrário.",
        "recommended_strategies": [
            "Conectar CADA meta financeira a um VALOR PESSOAL (ex: 'poupar para viajar = alimentar minha criatividade')",
            "Automatizar poupança como ato de autocuidado (não de privação)",
            "Conta separada para 'causas' (doações, presentes, apoio) — 5%% da renda",
            "Orçamento visual e colorido — planilha que pareça um diário criativo",
            "Mentor financeiro que fale de propósito, não só de números"
        ],
        "common_pitfalls": [
            "Evitar olhar para as contas por ansiedade",
            "Subestimar o próprio valor profissional",
            "Gastar para aliviar emoções negativas (retail therapy)"
        ],
        "mbti_financial_insight": "INFP: seu dinheiro é uma extensão dos seus valores. Não lute contra ele — alinhe-o. Um orçamento não é uma prisão; é a estrutura que liberta seus recursos para o que realmente importa. Você merece abundância tanto quanto qualquer um."
    },
    "ENFJ": {
        "name_pt_BR": "O Protagonista",
        "summary": "Líder inspirador que usa recursos financeiros para elevar os outros — mas precisa lembrar de se incluir no orçamento.",
        "detailed_profile": "ENFJs são naturalmente generosos e orientados a pessoas. Gastam em experiências coletivas, presentes, desenvolvimento dos outros. São excelentes em networking e em construir comunidades que geram oportunidades. O risco: dar tanto que esquecem das próprias necessidades financeiras.",
        "strengths": [
            "Networking financeiro — conexões viram oportunidades",
            "Capacidade de motivar equipes a alcançar metas financeiras coletivas",
            "Generosidade que fortalece relações",
            "Comunicação clara sobre dinheiro com parceiros",
            "Visão de abundância e prosperidade"
        ],
        "weaknesses": [
            "Dificuldade em priorizar necessidades financeiras próprias",
            "Gasto excessivo com presentes e experiências para outros",
            "Pode assumir compromissos financeiros por não querer decepcionar",
            "Ansiedade quando não consegue ajudar quem ama",
            "Tendência a evitar conversas financeiras difíceis"
        ],
        "saving_style": "Poupa para objetivos coletivos — viagens em grupo, presentes grandes, projetos comunitários. Poupança individual pode ser negligenciada.",
        "spending_style": "Gasta em experiências compartilhadas, desenvolvimento de pessoas, presentes significativos. O dinheiro deles é para conectar.",
        "risk_profile": "Moderado. Prefere investimentos que tragam benefício coletivo ou que possa compartilhar com outros.",
        "money_belief": "Dinheiro é para compartilhar. Prosperidade verdadeira é aquela que beneficia todos ao redor.",
        "recommended_strategies": [
            "Regra dos 3 potes: (1) necessidades, (2) compartilhar (presentes, causas), (3) seu futuro",
            "Automatizar poupança pessoal ANTES de qualquer gasto social",
            "Orçamento com categoria 'presentes' realista (não tentar gastar zero — gastará mesmo)",
            "Conta conjunta com parceiro para gastos compartilhados (transparência)",
            "Lembrete mensal: 'estou cuidando de mim para poder cuidar dos outros'"
        ],
        "common_pitfalls": [
            "Endividar-se para manter generosidade",
            "Negligenciar aposentadoria por focar no presente dos outros",
            "Não separar emergência pessoal de emergência alheia"
        ],
        "mbti_financial_insight": "ENFJ: sua generosidade é um superpoder — mas só se for sustentável. Você não pode ajudar ninguém de um barco furado. Construa sua base financeira primeiro; a generosidade que virá dela será mais estratégica e duradoura."
    },
    "ENFP": {
        "name_pt_BR": "O Ativista",
        "summary": "Explorador financeiro entusiasmado que abraça possibilidades — mas precisa de âncoras para não se perder no mar de oportunidades.",
        "detailed_profile": "ENFPs são otimistas financeiros. Veem potencial em todo lugar e têm dificuldade em dizer 'não' a experiências. A renda pode variar tanto quanto o humor, e o orçamento é mais uma sugestão que uma regra. Mas quando engajados com um propósito, são capazes de feitos financeiros impressionantes.",
        "strengths": [
            "Otimismo que atrai oportunidades",
            "Criatividade para gerar renda de múltiplas fontes",
            "Conexão emocional com metas financeiras (quando engajam)",
            "Adaptabilidade a mudanças de renda",
            "Habilidade de vender e inspirar"
        ],
        "weaknesses": [
            "Dificuldade em manter orçamento por impulso",
            "Gasto emocional — compra para celebrar, confortar, comemorar",
            "Tendência a subestimar despesas futuras",
            "Início de muitos projetos financeiros sem terminar nenhum",
            "Ansiedade financeira por falta de estrutura"
        ],
        "saving_style": "Criativo mas inconsistente. Funciona bem com 'desafios' de poupança e sistemas visuais.",
        "spending_style": "Gasta em experiências, viagens, cursos, arte, moda, restaurantes. O presente é irresistível — o amanhã parece distante.",
        "risk_profile": "Otimista em relação a riscos. Precisa de um 'amortecedor' externo que pergunte 'e se não der certo?'",
        "money_belief": "Dinheiro é para viver! Eu ganho mais amanhã. O importante é aproveitar agora.",
        "recommended_strategies": [
            "Sistema de 'contas de propósito' — contas separadas com nomes inspiradores",
            "Automatizar poupança no dia do recebimento (antes de gastar)",
            "Regra do 'sono': dormir antes de qualquer compra > R$ 200",
            "Orçamento flexível com 30%% para 'espontâneo' (não tentar se controlar demais)",
            "Parceiro de prestação de contas semanal (15 min)"
        ],
        "common_pitfalls": [
            "Subestimar despesas recorrentes",
            "Depender de 'dinheiro inesperado' para fechar contas",
            "Confundir entusiasmo com segurança financeira"
        ],
        "mbti_financial_insight": "ENFP: sua energia é contagiante — e pode encher ou esvaziar seus bolsos. Crie sistemas que aproveitem seu entusiasmo sem depender dele. Automatize o chato, libere sua criatividade para o que realmente importa."
    },
    "ISTJ": {
        "name_pt_BR": "O Fiscal",
        "summary": "Administrador financeiro exemplar — consistente, responsável e confiável. O tipo que paga as contas antes do vencimento.",
        "detailed_profile": "ISTJs são a espinha dorsal da estabilidade financeira. Seguem orçamentos com precisão, pagam contas em dia, mantêm registros impecáveis. Sua abordagem conservadora constrói riqueza lenta mas consistentemente. O risco: podem ser tão rígidos que perdem oportunidades por medo de sair do plano.",
        "strengths": [
            "Disciplina orçamentária exemplar",
            "Pagamento de contas em dia — zero juros",
            "Registros financeiros organizados e precisos",
            "Consistência em poupança e investimentos",
            "Avesso a dívidas desnecessárias"
        ],
        "weaknesses": [
            "Rigidez excessiva — dificuldade de se adaptar a mudanças",
            "Pode perder oportunidades por aversão a risco",
            "Tendência a subinvestir em experiências e prazeres",
            "Estresse quando o orçamento foge do planejado",
            "Dificuldade em delegar decisões financeiras"
        ],
        "saving_style": "Automático e inflexível. Poupa a mesma porcentagem todo mês, faça chuva ou sol.",
        "spending_style": "Gasta no necessário, com qualidade. Pesquisa antes de comprar. O supérfluo é raro e bem pensado.",
        "risk_profile": "Altamente avesso a riscos financeiros. Prefere renda fixa, CDB, tesouro direto. Ações são 'jogo'.",
        "money_belief": "Dinheiro é segurança. Deve ser administrado com responsabilidade, não com paixão.",
        "recommended_strategies": [
            "Sistema de orçamento que funciona para ISTJ: planilha detalhada + envelopes digitais",
            "Alocar 10%% para 'investimentos um pouco mais ousados' com pesquisa obrigatória",
            "Reserva de emergência de 6 meses (traz a paz que valoriza)",
            "Orçamento com verba de 'prazer' obrigatória (para não viver só de dever)",
            "Revisão financeira trimestral com indicadores de progresso"
        ],
        "common_pitfalls": [
            "Perder oportunidades de investimento por excesso de cautela",
            "Viver abaixo do que pode por medo de gastar",
            "Estresse desnecessário com flutuações normais de orçamento"
        ],
        "mbti_financial_insight": "ISTJ: sua consistência é seu maior ativo financeiro — mais que qualquer investimento. Mas lembre: a segurança que você construiu existe para ser VIVIDA, não apenas admirada. Permita-se gastar um pouco do que poupou."
    },
    "ISFJ": {
        "name_pt_BR": "O Defensor",
        "summary": "Cuidador financeiro dedicado que prioriza a segurança da família acima de tudo — às vezes esquecendo de si mesmo.",
        "detailed_profile": "ISFJs são os guardiões silenciosos das finanças domésticas. Lembram de cada conta, cada aniversário que precisa de presente, cada renovação de seguro. Sua abordagem é prática e orientada ao cuidado dos outros. O maior risco: negligenciar as próprias necessidades financeiras enquanto garantem que todos ao redor estão seguros.",
        "strengths": [
            "Gerenciamento impecável de finanças domésticas",
            "Lembrança de prazos e obrigações financeiras",
            "Priorização consistente de segurança familiar",
            "Consumo consciente e sem desperdício",
            "Lealdade a instituições financeiras de confiança"
        ],
        "weaknesses": [
            "Autossacrifício financeiro — prioriza todos menos si mesmo",
            "Dificuldade em pedir aumento ou negociar salário",
            "Resistência a mudanças em instituições financeiras",
            "Ansiedade com dívidas mesmo quando gerenciáveis",
            "Pode acumular poupança sem nunca usufruir"
        ],
        "saving_style": "Dedicado e consistente. Poupa para emergências e necessidades futuras da família.",
        "spending_style": "Gasta em conforto do lar, presentes para quem ama, qualidade de vida da família. Mesquinho consigo, generoso com os outros.",
        "risk_profile": "Muito conservador. Prefere o conhecido. Inovações financeiras são recebidas com ceticismo.",
        "money_belief": "Dinheiro é para proteger quem se ama. Segurança primeiro, sempre.",
        "recommended_strategies": [
            "Automatizar poupança pessoal ('para mim') como conta prioritária",
            "Orçamento com 'verba de autocuidado' obrigatória",
            "Previdência privada ou plano de aposentadoria (segurança a longo prazo)",
            "Diversificação gradual — 5%% em renda variável para começar",
            "Revisão financeira com foco em 'estou cuidando de mim também?'"
        ],
        "common_pitfalls": [
            "Acumular poupança sem nunca usar para prazer próprio",
            "Aceitar condições financeiras desfavoráveis por lealdade",
            "Não investir em si mesmo (cursos, saúde, desenvolvimento)"
        ],
        "mbti_financial_insight": "ISFJ: você é o alicerce financeiro de quem ama. Mas um alicerce também precisa de manutenção. Cuidar de você financeiramente não é egoísmo — é garantir que poderá cuidar dos outros por muito mais tempo."
    },
    "ESTJ": {
        "name_pt_BR": "O Executor",
        "summary": "Gestor financeiro nato — prático, direto e eficiente. Faz acontecer com disciplina e visão clara.",
        "detailed_profile": "ESTJs lideram as finanças como lideram tudo na vida: com estrutura, disciplina e senso de dever. Orçamentos são seguidos à risca, contas pagas no prazo, e o futuro é planejado com antecedência. Sua abordagem prática constrói estabilidade sólida. O risco: a rigidez pode custar relacionamentos e oportunidades.",
        "strengths": [
            "Liderança financeira clara e decisiva",
            "Disciplina orçamentária inabalável",
            "Capacidade de estabelecer e cumprir metas financeiras",
            "Organização impecável de documentos e registros",
            "Comunicação direta sobre dinheiro"
        ],
        "weaknesses": [
            "Rigidez excessiva — 'é assim porque sempre foi assim'",
            "Dificuldade em entender gastos que considera 'supérfluos'",
            "Pode ser autoritário em decisões financeiras conjuntas",
            "Impaciência com educação financeira de outros",
            "Estresse quando o plano não segue o previsto"
        ],
        "saving_style": "Disciplinado e sistemático. Poupa como dever. Não negocia.",
        "spending_style": "Gasta no funcional e de qualidade. Marca confiável, não tendência. Resistente a marketing e modismos.",
        "risk_profile": "Baixo. Prefere o testado e aprovado. Investe em imóveis, renda fixa, o que 'todo mundo sabe que funciona'.",
        "money_belief": "Dinheiro é responsabilidade. Deve ser trabalhado, não sorteado. Cada real tem seu lugar.",
        "recommended_strategies": [
            "Sistema de orçamento 50/30/20 com regras claras e inflexíveis",
            "Alocar 10%% para 'investimentos de crescimento' (fora da zona de conforto)",
            "Criar 'fundo de liberdade' para decisões financeiras conjuntas com parceiros",
            "Revisão mensal com indicadores objetivos",
            "Estabelecer 'verba de leveza' — dinheiro para gastar sem culpa"
        ],
        "common_pitfalls": [
            "Perder oportunidades por não sair do conhecido",
            "Desgastar relacionamentos por rigidez financeira",
            "Estresse excessivo com flutuações normais"
        ],
        "mbti_financial_insight": "ESTJ: você construiu sua estabilidade com suor e disciplina — e isso é admirável. Mas o melhor uso da segurança que você criou é a liberdade que ela traz. Nem tudo precisa ser 'útil'. Algumas coisas só precisam ser boas."
    },
    "ESFJ": {
        "name_pt_BR": "O Cônsul",
        "summary": "Anfitrião financeiro que adora compartilhar prosperidade — mas precisa equilibrar generosidade com sustentabilidade.",
        "detailed_profile": "ESFJs são o coração da comunidade financeira. Lembram de aniversários com presentes, organizam confraternizações, ajudam quem precisa. Sua abordagem é calorosa e inclusiva. O risco: querer agradar tanto que compromete a própria saúde financeira. Precisam de permissão para dizer 'não' sem culpa.",
        "strengths": [
            "Generosidade que fortalece laços comunitários",
            "Capacidade de organizar finanças coletivas (rifas, vaquinhas, festas)",
            "Lealdade a instituições e relacionamentos financeiros",
            "Organização de documentos e contas domésticas",
            "Comunicação acolhedora sobre dinheiro"
        ],
        "weaknesses": [
            "Dificuldade em dizer 'não' a pedidos financeiros",
            "Gasto excessivo em celebrações e presentes",
            "Tendência a manter padrão de vida além do orçamento para 'parecer bem'",
            "Ansiedade quando não pode ajudar alguém",
            "Pode evitar conversas financeiras por medo de conflito"
        ],
        "saving_style": "Poupa para objetivos sociais — viagens em grupo, festas, presentes grandes. Poupança individual é secundária.",
        "spending_style": "Gasta em alimentação, presentes, decoração, celebrações. O lar e as relações são onde o dinheiro flui.",
        "risk_profile": "Conservador e tradicional. Prefere o banco que a família sempre usou. Inovações financeiras assustam.",
        "money_belief": "Dinheiro é para compartilhar com quem se ama. Prosperidade sem comunidade não é prosperidade.",
        "recommended_strategies": [
            "Orçamento com categoria 'generosidade' realista (não tentar gastar zero)",
            "Automatizar poupança pessoal como 'presente para meu futuro'",
            "Regra: 'se não cabe no orçamento deste mês, cabe no próximo'",
            "Conta separada para 'imprevistos sociais'",
            "Parceiro financeiro que ajude a manter o equilíbrio"
        ],
        "common_pitfalls": [
            "Endividar-se para manter aparências sociais",
            "Comprometer aposentadoria por gastos presentes com outros",
            "Não negociar preços ou condições por constrangimento"
        ],
        "mbti_financial_insight": "ESFJ: sua generosidade aquece o mundo. Mas você não pode encher o copo dos outros com um jarro vazio. Encha o seu primeiro — a abundância que transbordar será ainda mais genuína."
    },
    "ISTP": {
        "name_pt_BR": "O Virtuoso",
        "summary": "Artesão financeiro prático que prefere entender o mecanismo antes de investir — e valoriza a liberdade acima de tudo.",
        "detailed_profile": "ISTPs são solucionadores práticos. Aplicam sua mente mecânica às finanças: querem saber como cada instrumento funciona, qual a alavanca certa para puxar. São excelentes em consertar situações financeiras complicadas. O risco: a busca por liberdade pode levá-los a subestimar a importância de segurança de longo prazo.",
        "strengths": [
            "Raciocínio prático para resolver problemas financeiros",
            "Habilidade manual e técnica que gera renda extra",
            "Adaptabilidade a mudanças econômicas",
            "Baixo consumo material — não liga para status",
            "Capacidade de viver com pouco quando necessário"
        ],
        "weaknesses": [
            "Dificuldade com planejamento financeiro de longo prazo",
            "Impulso por gratificação imediata em hobbies/interesses",
            "Pode negligenciar burocracia financeira",
            "Tendência a 'consertar' problemas financeiros de outros em vez dos próprios",
            "Resistência a sistemas financeiros tradicionais"
        ],
        "saving_style": "Poupa para liberdade, não para segurança. Poupar para 'poder fazer o que quiser' é motivador; poupar 'para o futuro' é abstrato demais.",
        "spending_style": "Gasta em ferramentas, equipamentos, hobbies práticos, experiências ao ar livre. O dinheiro volta em forma de habilidade.",
        "risk_profile": "Assume riscos calculados quando entende o mecanismo. Pode ser surpreendentemente ousado em investimentos que domina.",
        "money_belief": "Dinheiro é liberdade. Ter o suficiente significa poder fazer o que quiser, quando quiser.",
        "recommended_strategies": [
            "Automatizar poupança como 'compra de liberdade futura'",
            "Investir em habilidades que geram renda (cursos técnicos, certificações)",
            "Reserva de emergência em conta separada (não misturar com 'dinheiro livre')",
            "Portfólio simples que não exige monitoramento constante",
            "Regra: 'antes de comprar uma ferramenta nova, usar a atual por mais 3 meses'"
        ],
        "common_pitfalls": [
            "Gastar demais em hobbies que não geram retorno",
            "Subestimar aposentadoria ('depois eu vejo')",
            "Ignorar seguros e proteções"
        ],
        "mbti_financial_insight": "ISTP: sua habilidade de 'consertar' se aplica a dinheiro também. Mas finanças não são só conserto — são construção. Invista em sistemas que funcionem sem você. A verdadeira liberdade é não precisar gerenciar cada centavo."
    },
    "ISFP": {
        "name_pt_BR": "O Aventureiro",
        "summary": "Artista financeiro sensível que busca beleza e significado — e para quem dinheiro é só um meio para a expressão criativa.",
        "detailed_profile": "ISFPs vivem o presente com intensidade. Gastam em arte, música, natureza, beleza. O dinheiro flui para o que toca o coração no momento. Planejamento financeiro parece abstrato e distante. Mas quando conectam finanças a um valor estético ou emocional, tornam-se incrivelmente disciplinados.",
        "strengths": [
            "Alta tolerância a viver com pouco por períodos",
            "Gasto alinhado com valores estéticos e autênticos",
            "Capacidade de encontrar beleza e valor no simples",
            "Resistência ao consumismo de massa",
            "Criatividade que gera renda de formas não convencionais"
        ],
        "weaknesses": [
            "Dificuldade com planejamento financeiro de qualquer tipo",
            "Gasto impulsivo por prazer estético ou emocional",
            "Ansiedade financeira que prefere ignorar",
            "Tendência a subestimar despesas futuras",
            "Pode evitar carreiras estáveis em nome da liberdade criativa"
        ],
        "saving_style": "Irregular e emocional. Poupa quando sobra. Funciona bem com poupança visual (ver o dinheiro crescer como uma obra de arte).",
        "spending_style": "Gasta em arte, música, viagens, beleza, experiências sensoriais. O supérfluo para outros é essencial para a alma.",
        "risk_profile": "Prefere não pensar em riscos. Pode tanto ignorar completamente quanto ter medo paralisante.",
        "money_belief": "Dinheiro vem e vai. O importante é a experiência, a beleza, o momento.",
        "recommended_strategies": [
            "Contas separadas com NOMES BONITOS (não 'emergência' — 'liberdade criativa')",
            "Automatizar poupança como ato de amor-próprio",
            "Orçamento visual (colagem, cores, imagens)",
            "Fundo 'experiência' obrigatório: 10%% da renda para viver agora",
            "Lembrete: 'segurança financeira é a base para sua arte florescer'"
        ],
        "common_pitfalls": [
            "Viver de 'bico' em vez de construir estabilidade",
            "Evitar completamente pensar em aposentadoria",
            "Gastar mais do que ganha por impulso criativo"
        ],
        "mbti_financial_insight": "ISFP: seu coração é seu guia — inclusive financeiro. Não lute contra isso. Crie um sistema financeiro que seja TÃO bonito quanto sua arte. Uma planilha pode ser uma tela em branco para seu futuro."
    },
    "ESTP": {
        "name_pt_BR": "O Empreendedor",
        "summary": "Jogador financeiro nato que prospera na ação rápida e no risco calculado — mas precisa de freios para não queimar toda a energia.",
        "detailed_profile": "ESTPs são empreendedores no sangue. Enxergam oportunidades onde outros veem problemas e agem com velocidade impressionante. São excelentes em vendas, negociação e negócios. O risco: o vício em ação pode levar a decisões precipitadas e o foco no presente pode sabotar a construção de riqueza duradoura.",
        "strengths": [
            "Ação rápida — aproveita oportunidades antes dos outros",
            "Excelente em vendas, negociação e persuasão",
            "Adaptabilidade a mercados em mudança",
            "Resiliência a perdas — não paralisa, aprende e segue",
            "Capacidade de gerar renda de múltiplas fontes"
        ],
        "weaknesses": [
            "Impaciência — quer resultados agora, não amanhã",
            "Tendência a superestimar oportunidades e subestimar riscos",
            "Dificuldade com planejamento financeiro de rotina",
            "Pode gastar impulsivamente em 'grandes ideias'",
            "Lifestyle inflation — a renda sobe e os gastos também"
        ],
        "saving_style": "Poupa quando sobra ou quando uma meta de curto prazo motiva. Poupança de longo prazo é desafiadora.",
        "spending_style": "Gasta em experiências, carros, viagens, jantares, roupas. Vive o agora com intensidade.",
        "risk_profile": "Assume riscos altos com confiança. Precisa de contraponto que traga perspectiva de longo prazo.",
        "money_belief": "Dinheiro é o placar do jogo. Quem não arrisca, não petisca.",
        "recommended_strategies": [
            "Automatizar 20%% da renda para investimento (antes de ver o dinheiro)",
            "Regra do 'conselheiro': consultar alguém de confiança antes de qualquer investimento > R$ 5.000",
            "Diversificação OBRIGATÓRIA — não mais que 20%% em qualquer ativo",
            "Orçamento com 'verba de risco' controlada",
            "Estabelecer métricas: 'este negócio tem 6 meses para mostrar resultado ou encerro'"
        ],
        "common_pitfalls": [
            "Superexposição em um único negócio/investimento",
            "Gastos que sobem junto com a renda",
            "Ignorar seguro e proteção por excesso de confiança"
        ],
        "mbti_financial_insight": "ESTP: seu instinto é seu maior ativo — mas também seu maior risco. O jogo financeiro não é sprint, é maratona. Os maiores jogadores são os que sobrevivem mais tempo. Construa defesas para poder continuar atacando."
    },
    "ESFP": {
        "name_pt_BR": "O Animador",
        "summary": "Celebrador da vida que faz o dinheiro trabalhar para viver momentos inesquecíveis — e precisa de estrutura para que a festa nunca acabe.",
        "detailed_profile": "ESFPs são a alma da festa financeira. Gastam com generosidade e entusiasmo, criando experiências memoráveis para si e para os outros. São excelentes em entretenimento, hospitalidade e qualquer carreira que envolva pessoas e alegria. O risco: a busca pelo prazer imediato pode comprometer a segurança de longo prazo.",
        "strengths": [
            "Generosidade que cria laços fortes",
            "Habilidade de ganhar dinheiro com entretenimento e serviços",
            "Otimismo contagiante que atrai oportunidades",
            "Adaptabilidade a mudanças de renda",
            "Rede social extensa e diversificada"
        ],
        "weaknesses": [
            "Dificuldade em dizer 'não' a gastos sociais",
            "Impulso por gratificação imediata",
            "Tendência a evitar olhar para o orçamento",
            "Pode gastar mais do que ganha em períodos de otimismo",
            "Subestima a importância de poupança de longo prazo"
        ],
        "saving_style": "Desafiador. ESFP poupa melhor quando a poupança é gamificada ou conectada a um objetivo emocionante.",
        "spending_style": "Gasta em viagens, festas, restaurantes, presentes, entretenimento. Viver é gastar.",
        "risk_profile": "Otimista. Tende a subestimar riscos. Precisa de alguém que traga os pés ao chão.",
        "money_belief": "Dinheiro é para viver, não para acumular. 'A felicidade não está no fim da jornada, está no caminho.'",
        "recommended_strategies": [
            "Sistema de 'contas divertidas' — contas separadas para cada sonho",
            "Automatizar poupança como 'futuro mais divertido ainda'",
            "Regra do 'amigo financeiro': parceiro que ajuda a manter o foco",
            "Orçamento visual com metas de curto prazo (30 dias)",
            "Reserva de emergência em conta separada com nome 'PAZ'"
        ],
        "common_pitfalls": [
            "Gastar o que não tem em momentos de celebração",
            "Depender de renda variável sem planejar os meses baixos",
            "Negligenciar completamente aposentadoria"
        ],
        "mbti_financial_insight": "ESFP: sua alegria é seu presente para o mundo. Mas a melhor festa é a que pode continuar. Crie uma base financeira que garanta que você possa celebrar por muitos e muitos anos. Segurança não é o fim da diversão — é o que permite que ela dure."
    }
}

def get_profile(type_code: str) -> dict:
    """
    Retorna perfil financeiro de um tipo MBTI.

    Args:
        type_code: str com código de 4 letras (ex: 'INTJ', 'enfp')

    Returns:
        dict com perfil financeiro ou dict vazio se tipo inválido
    """
    return FINANCIAL_PROFILES.get(type_code.upper(), {})


def get_all_profiles() -> dict:
    """
    Retorna todos os 16 perfis financeiros MBTI.
    """
    return FINANCIAL_PROFILES


def assess_financial_personality(answers: dict, type_code: str = None) -> dict:
    """
    Correlaciona respostas financeiras com o perfil MBTI.

    Args:
        answers: dict com respostas sobre comportamento financeiro
            Ex: {"saving_habit": "automatic", "risk_tolerance": "high",
                 "spending_trigger": "tools", "money_belief": "freedom"}
        type_code: str com código MBTI (ex: 'INTJ'). Se None, usa as respostas
                   para sugerir um perfil financeiro independente do MBTI.

    Returns:
        dict com perfil + recomendações
    """
    result = {
        "type_code": type_code,
        "profile": get_profile(type_code) if type_code else None,
        "answers_analysis": {},
        "observations": [],
        "recommendations": []
    }

    if not answers:
        result["observations"].append("Nenhuma resposta financeira fornecida.")
        return result

    # Analisar hábito de poupança
    saving = answers.get("saving_habit", "").lower()
    if saving == "automatic":
        result["answers_analysis"]["saving"] = "Poupança automatizada — excelente fundação"
        result["observations"].append("Você já automatiza sua poupança. Isso remove a tentação e a fadiga de decisão.")
    elif saving == "manual":
        result["answers_analysis"]["saving"] = "Poupança manual — vulnerável à consistência"
        result["observations"].append("Poupar manualmente depende de força de vontade, que é um recurso limitado. Automatizar libera sua energia para decisões mais importantes.")
    elif saving == "sporadic":
        result["answers_analysis"]["saving"] = "Poupança esporádica — alto risco de não poupar"
        result["observations"].append("Poupar 'quando sobra' raramente funciona. O dinheiro que 'sobra' no final do mês geralmente é zero. Separe antes de gastar.")

    # Analisar tolerância a risco
    risk = answers.get("risk_tolerance", "").lower()
    if risk == "high":
        result["answers_analysis"]["risk"] = "Alta tolerância a risco — oportunidade e perigo"
        if type_code:
            profile = get_profile(type_code)
            if profile:
                result["observations"].append(f"Como {profile['name_pt_BR']}, sua alta tolerância a risco {profile['risk_profile'].lower()}")
        result["recommendations"].append("Diversifique seus investimentos. Nunca aloque mais de 20%% em um único ativo.")
    elif risk == "medium":
        result["answers_analysis"]["risk"] = "Tolerância moderada — equilíbrio saudável"
        result["recommendations"].append("Mantenha 60/30/10 entre renda fixa, renda variável e alternativos.")
    elif risk == "low":
        result["answers_analysis"]["risk"] = "Baixa tolerância — segurança primeiro"
        result["recommendations"].append("Invista em renda fixa com liquidez. Considere alocar 10-20%% em ETFs amplos para não perder poder de compra.")

    # Analisar gatilho de gasto
    trigger = answers.get("spending_trigger", "").lower()
    if trigger:
        trigger_map = {
            "tools": "Gasta em ferramentas e equipamentos — investe em capacidade",
            "social": "Gasta em experiências sociais — investe em relacionamentos",
            "comfort": "Gasta em conforto e bem-estar — investe em qualidade de vida",
            "status": "Gasta em status e aparência — investe em imagem",
            "knowledge": "Gasta em conhecimento — investe em si mesmo"
        }
        result["answers_analysis"]["spending_trigger"] = trigger_map.get(trigger, f"Gatilho: {trigger}")
        if type_code:
            profile = get_profile(type_code)
            if profile:
                result["observations"].append(f"Seu principal gatilho de gasto ({trigger}) {profile['spending_style'].lower()}")

    # Analisar crença sobre dinheiro
    belief = answers.get("money_belief", "").lower()
    if belief:
        belief_map = {
            "freedom": "Dinheiro como liberdade — busca independência financeira",
            "security": "Dinheiro como segurança — prioriza estabilidade",
            "tool": "Dinheiro como ferramenta — meio para fins maiores",
            "status": "Dinheiro como status — medida de sucesso",
            "enjoyment": "Dinheiro para viver — foco no presente"
        }
        result["answers_analysis"]["money_belief"] = belief_map.get(belief, f"Crença: {belief}")
        if type_code:
            profile = get_profile(type_code)
            if profile and "money_belief" in profile:
                result["observations"].append(profile["money_belief"])

    # Se tem tipo, adicionar insight MBTI
    if type_code:
        profile = get_profile(type_code)
        if profile and "mbti_financial_insight" in profile:
            result["recommendations"].append(profile["mbti_financial_insight"])
            if "recommended_strategies" in profile:
                for s in profile["recommended_strategies"]:
                    result["recommendations"].append(s)

    return result


if __name__ == "__main__":
    import json

    print("=== PERFIS FINANCEIROS MBTI ===")
    print(f"Total: {len(FINANCIAL_PROFILES)} tipos\n")

    for code, data in FINANCIAL_PROFILES.items():
        print(f"{code} — {data['name_pt_BR']}")
        print(f"  {data['summary'][:80]}...")
    print()

    # Teste rápido
    result = assess_financial_personality(
        {"saving_habit": "automatic", "risk_tolerance": "high", "spending_trigger": "tools"},
        "INTJ"
    )
    print("=== TESTE: INTJ ===")
    print(f"  Observações: {len(result['observations'])}")
    print(f"  Recomendações: {len(result['recommendations'])}")
    print("  Perfil carregado:", result['profile']['name_pt_BR'] if result['profile'] else "NÃO")
