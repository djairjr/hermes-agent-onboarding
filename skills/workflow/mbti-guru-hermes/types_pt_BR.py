#!/usr/bin/env python3
"""
MBTI Types Data - 16 Personality Types (English + Chinese + Brazilian Portuguese)
"""
from typing import Dict

# 16 Personality Types / 16种人格类型 / 16 Tipos de Personalidade
TYPES: Dict = {
    "INTJ": {
        "name_cn": "建筑师",
        "name_en": "The Architect",
        "name_pt_BR": "O Arquiteto",
        "summary": "An imaginative and strategic thinker with a plan for everything.",
        "summary_cn": "一个富有想象力且具有战略思维的思考者，对一切都制定计划。",
        "summary_pt_BR": "O Arquiteto é um pensador imaginativo e estratégico que planeja cada passo. Com uma mente analítica afiada, busca constantemente melhorar sistemas e estruturas, sempre pensando no futuro e antecipando cenários.",
        "strengths": [
            "Strategic and analytical / 战略与分析",
            "Independent and determined / 独立与坚定",
            "Rational and logical / 理性与逻辑",
            "High standards / 高标准",
            "Decisive / 果断"
        ],
        "strengths_pt_BR": [
            "Estratégico e analítico",
            "Independente e determinado",
            "Racional e lógico",
            "Padrões elevados de excelência",
            "Decisivo e confiante"
        ],
        "weaknesses": [
            "Arrogant and critical / 傲慢与批评",
            "Impatient with inefficiency / 对低效缺乏耐心",
            "Dismissive of emotions / 忽视情感",
            "Perfectionist / 完美主义者",
            "Socially awkward / 社交笨拙"
        ],
        "weaknesses_pt_BR": [
            "Arrogante e crítico demais",
            "Impaciente com ineficiência",
            "Desconsidera as emoções alheias",
            "Perfeccionista excessivo",
            "Desajeitado socialmente"
        ],
        "careers": [
            "Scientist / 科学家",
            "Engineer / 工程师",
            "Programmer / 程序员",
            "Financial Analyst / 金融分析师",
            "Strategist / 战略家"
        ],
        "careers_pt_BR": [
            "Cientista",
            "Engenheiro(a)",
            "Programador(a)",
            "Analista Financeiro(a)",
            "Estrategista"
        ],
        "relationships": {
            "best": ["INFJ", "ENFJ"],
            "challenging": ["ESFP", "ESTP"]
        }
    },
    "INTP": {
        "name_cn": "逻辑学家",
        "name_en": "The Logician",
        "name_pt_BR": "O Lógico",
        "summary": "An innovative inventor with an unquenchable thirst for knowledge.",
        "summary_cn": "一个具有永不满足求知欲的创新发明家。",
        "summary_pt_BR": "O Lógico é um inventor inovador com uma sede insaciável por conhecimento. Movido pela curiosidade intelectual, adora explorar teorias e encontrar padrões ocultos no mundo ao seu redor.",
        "strengths": [
            "Analytical and objective / 分析与客观",
            "Intelligent and knowledgeable / 聪明与博学",
            "Open-minded / 开放心态",
            "Creative and innovative / 创意与创新",
            "Independent / 独立"
        ],
        "strengths_pt_BR": [
            "Analítico e objetivo",
            "Inteligente e sedento por conhecimento",
            "Mente aberta para novas ideias",
            "Criativo e inovador",
            "Independente"
        ],
        "weaknesses": [
            "Detached and dismissive / 冷漠与轻视",
            "Critical of others / 批评他人",
            "Overthinker / 过度思考",
            "Struggles with practicality / 实践困难",
            "Emotionally guarded / 情感封闭"
        ],
        "weaknesses_pt_BR": [
            "Distante e desdenhoso",
            "Crítico com os outros",
            "Pensador excessivo (paralisia por análise)",
            "Dificuldade com o lado prático da vida",
            "Fechado emocionalmente"
        ],
        "careers": [
            "Research Scientist / 研究员",
            "Software Developer / 软件开发",
            "Professor / 教授",
            "Philosopher / 哲学家",
            "Data Scientist / 数据科学家"
        ],
        "careers_pt_BR": [
            "Cientista Pesquisador(a)",
            "Desenvolvedor(a) de Software",
            "Professor(a) Universitário(a)",
            "Filósofo(a)",
            "Cientista de Dados"
        ],
        "relationships": {
            "best": ["ENTJ", "ENFJ"],
            "challenging": ["ESFJ", "ESTJ"]
        }
    },
    "ENTJ": {
        "name_cn": "指挥官",
        "name_en": "The Commander",
        "name_pt_BR": "O Comandante",
        "summary": "A bold, forthright leader with a drive for organization.",
        "summary_cn": "一个有组织驱动的大胆、直率的领导者。",
        "summary_pt_BR": "O Comandante é um líder ousado e direto com uma forte motivação para organizar e estruturar. Visionário e determinado, não tem medo de assumir o controle e guiar equipes rumo a grandes objetivos.",
        "strengths": [
            "Bold and confident / 大胆与自信",
            "Natural leader / 天生领导者",
            "Efficient and organized / 高效与有条理",
            "Strategic thinker / 战略思考者",
            "Strong-willed / 意志坚定"
        ],
        "strengths_pt_BR": [
            "Audacioso e confiante",
            "Líder nato",
            "Eficiente e organizado",
            "Pensador estratégico",
            "Determinado e obstinado"
        ],
        "weaknesses": [
            "Intolerant and stubborn / 狭隘与固执",
            "Cold and ruthless / 冷漠与无情",
            "Dominating / 支配性",
            "Poor emotional expression / 情感表达差",
            "Impatient with others / 对他人不耐烦"
        ],
        "weaknesses_pt_BR": [
            "Intolerante e teimoso",
            "Frio e implacável",
            "Dominador",
            "Dificuldade em expressar emoções",
            "Impaciente com os outros"
        ],
        "careers": [
            "CEO / 首席执行官",
            "Entrepreneur / 企业家",
            "Management Consultant / 管理顾问",
            "Lawyer / 律师",
            "Executive / 高管"
        ],
        "careers_pt_BR": [
            "CEO / Diretor(a) Executivo(a)",
            "Empreendedor(a)",
            "Consultor(a) de Gestão",
            "Advogado(a)",
            "Executivo(a)"
        ],
        "relationships": {
            "best": ["INTP", "INFJ"],
            "challenging": ["ISFP", "ISTP"]
        }
    },
    "ENTP": {
        "name_cn": "辩论家",
        "name_en": "The Debater",
        "name_pt_BR": "O Debatedor",
        "summary": "A smart and curious thinker who can find any answer.",
        "summary_cn": "一个聪明好奇的思考者，能找到任何答案。",
        "summary_pt_BR": "O Debatedor é um pensador inteligente e curioso que adora explorar ideias e desafiar o status quo. Com uma mente ágil e criativa, encontra soluções inovadoras para problemas complexos.",
        "strengths": [
            "Quick-witted and clever / 机智与聪明",
            "Creative and innovative / 创意与创新",
            "Enthusiastic and energetic / 热情与活力",
            "Good at debate / 善于辩论",
            "Adaptable / 适应性强"
        ],
        "strengths_pt_BR": [
            "Rápido e perspicaz",
            "Criativo e inovador",
            "Entusiasmado e energético",
            "Habilidade em debate e argumentação",
            "Adaptável a novas situações"
        ],
        "weaknesses": [
            "Argumentative and critical / 争辩与批评",
            "Easily bored / 容易厌倦",
            "Insensitive to others / 对他人不敏感",
            "Struggles with follow-through / 难以坚持",
            "Disorganized / 无条理"
        ],
        "weaknesses_pt_BR": [
            "Argumentativo e crítico demais",
            "Entedia-se facilmente",
            "Insensível com os outros",
            "Dificuldade em finalizar projetos",
            "Desorganizado"
        ],
        "careers": [
            "Lawyer / 律师",
            "Marketing Manager / 市场经理",
            "Entrepreneur / 企业家",
            "Journalist / 记者",
            "Political Strategist / 政治战略家"
        ],
        "careers_pt_BR": [
            "Advogado(a)",
            "Gerente de Marketing",
            "Empreendedor(a)",
            "Jornalista",
            "Estrategista Político(a)"
        ],
        "relationships": {
            "best": ["INFJ", "INTJ"],
            "challenging": ["ISFJ", "ISTJ"]
        }
    },
    "INFJ": {
        "name_cn": "提倡者",
        "name_en": "The Advocate",
        "name_pt_BR": "O Advogado",
        "summary": "A quiet protector who believes in the potential of people.",
        "summary_cn": "一个相信人类潜能的安静守护者。",
        "summary_pt_BR": "O Advogado é um protetor silencioso que acredita profundamente no potencial das pessoas. Idealista e compassivo, busca um propósito maior e trabalha incansavelmente para tornar o mundo um lugar melhor.",
        "strengths": [
            "Principled and idealistic / 有原则与理想主义",
            "Creative and artistic / 创意与艺术",
            "Caring and compassionate / 关爱与同情",
            "Intuitive and insightful / 直觉与洞察",
            "Quiet but inspiring / 安静但鼓舞人心"
        ],
        "strengths_pt_BR": [
            "Íntegro e idealista",
            "Criativo e artístico",
            "Cuidadoso e compassivo",
            "Intuitivo e perspicaz",
            "Silencioso mas inspirador"
        ],
        "weaknesses": [
            "Perfectionist / 完美主义者",
            "Sensitive to criticism / 对批评敏感",
            "Reluctant to open up / 不愿敞开心扉",
            "Burnout prone / 容易倦怠",
            "Self-righteous / 自以为义"
        ],
        "weaknesses_pt_BR": [
            "Perfeccionista extremo",
            "Sensível a críticas",
            "Relutante em se abrir emocionalmente",
            "Propenso a esgotamento (burnout)",
            "Moralista ou arrogante em suas convicções"
        ],
        "careers": [
            "Counselor / 心理咨询师",
            "Writer / 作家",
            "Psychologist / 心理学家",
            "Teacher / 教师",
            "HR Specialist / 人力资源专员"
        ],
        "careers_pt_BR": [
            "Psicólogo(a) / Terapeuta",
            "Escritor(a)",
            "Psicólogo(a) Clínico(a)",
            "Professor(a)",
            "Especialista em RH"
        ],
        "relationships": {
            "best": ["INFP", "ENFP"],
            "challenging": ["ESTP", "ESFP"]
        }
    },
    "INFP": {
        "name_cn": "调停者",
        "name_en": "The Mediator",
        "name_pt_BR": "O Mediador",
        "summary": "A people-pleaser who believes in the goodness of human nature.",
        "summary_cn": "一个相信人性善良的人。",
        "summary_pt_BR": "O Mediador é uma alma sensível e idealista que acredita na bondade humana. Guiado por valores profundos, busca harmonia e autenticidade em tudo que faz, dedicando-se a causas nas quais acredita.",
        "strengths": [
            "Idealistic and principled / 理想主义与原则",
            "Creative and expressive / 创意与表达",
            "Compassionate and caring / 同情与关爱",
            "Flexible and adaptable / 灵活与适应",
            "Loyal and devoted / 忠诚与投入"
        ],
        "strengths_pt_BR": [
            "Idealista e cheio de princípios",
            "Criativo e expressivo",
            "Compassivo e acolhedor",
            "Flexível e adaptável",
            "Leal e dedicado"
        ],
        "weaknesses": [
            "Overly trusting / 过度信任",
            "Self-critical / 自我批评",
            "Disorganized and scattered / 无条理与分散",
            "Avoids conflict / 回避冲突",
            "Too idealistic / 过于理想化"
        ],
        "weaknesses_pt_BR": [
            "Confia demais nas pessoas",
            "Muito autocrítico",
            "Desorganizado e disperso",
            "Evita conflitos a todo custo",
            "Idealista demais para o mundo real"
        ],
        "careers": [
            "Writer / 作家",
            "Counselor / 心理咨询师",
            "Social Worker / 社会工作者",
            "Graphic Designer / 平面设计师",
            "HR Specialist / 人力资源专员"
        ],
        "careers_pt_BR": [
            "Escritor(a)",
            "Psicólogo(a) / Terapeuta",
            "Assistente Social",
            "Designer Gráfico(a)",
            "Especialista em RH"
        ],
        "relationships": {
            "best": ["ENFP", "INFJ"],
            "challenging": ["ESTJ", "ENTJ"]
        }
    },
    "ENFJ": {
        "name_cn": "主人公",
        "name_en": "The Protagonist",
        "name_pt_BR": "O Protagonista",
        "summary": "A charismatic leader who inspires others to be their best.",
        "summary_cn": "一个激励他人成为最好的魅力的领导者。",
        "summary_pt_BR": "O Protagonista é um líder carismático que inspira os outros a darem o melhor de si. Com uma habilidade natural para conectar pessoas e motivar equipes, é um verdadeiro catalisador de mudanças positivas.",
        "strengths": [
            "Natural leader / 天生领导者",
            "Charismatic and inspiring / 魅力与鼓舞",
            "Caring and supportive / 关爱与支持",
            "Diplomatic and tactful / 外交与得体",
            "Enthusiastic and persuasive / 热情与说服"
        ],
        "strengths_pt_BR": [
            "Líder nato",
            "Carismático e inspirador",
            "Cuidadoso e solidário",
            "Diplomático e com tato",
            "Entusiasmado e persuasivo"
        ],
        "weaknesses": [
            "Overly idealistic / 过于理想化",
            "Self-righteous / 自以为义",
            "People-pleaser / 讨好他人",
            "Inauthentic / 不真实",
            "Burnout prone / 容易倦怠"
        ],
        "weaknesses_pt_BR": [
            "Idealista em excesso",
            "Moralista / acha que sempre está certo",
            "Agrada os outros em vez de ser autêntico",
            "Pode parecer falso ao forçar harmonia",
            "Propenso a esgotamento (burnout)"
        ],
        "careers": [
            "Teacher / 教师",
            "HR Manager / 人力资源经理",
            "Marketing Manager / 市场经理",
            "Sales Manager / 销售经理",
            "Coach / 教练"
        ],
        "careers_pt_BR": [
            "Professor(a)",
            "Gerente de RH",
            "Gerente de Marketing",
            "Gerente de Vendas",
            "Coach / Mentor(a)"
        ],
        "relationships": {
            "best": ["INFP", "ISFP"],
            "challenging": ["ISTP", "ESTP"]
        }
    },
    "ENFP": {
        "name_cn": "竞选者",
        "name_en": "The Campaigner",
        "name_pt_BR": "O Ativista",
        "summary": "An enthusiastic creator with an infectious positive attitude.",
        "summary_cn": "一个具有感染性积极态度的热情创造者。",
        "summary_pt_BR": "O Ativista é um criador entusiasmado com uma atitude positiva contagiante. Cheio de energia e curiosidade, adora explorar novas possibilidades e inspirar as pessoas ao seu redor com seu otimismo inabalável.",
        "strengths": [
            "Enthusiastic and energetic / 热情与活力",
            "Creative and artistic / 创意与艺术",
            "Social and outgoing / 社交与外向",
            "Optimistic and fun / 乐观与有趣",
            "Great communicator / 优秀沟通者"
        ],
        "strengths_pt_BR": [
            "Entusiasmado e cheio de energia",
            "Criativo e artístico",
            "Sociável e extrovertido",
            "Otimista e divertido",
            "Excelente comunicador"
        ],
        "weaknesses": [
            "Scattered and disorganized / 分散与无条理",
            "Overly emotional / 过于情绪化",
            "Needs approval / 需要认可",
            "Fear of rejection / 害怕被拒绝",
            "Difficulty with follow-through / 难以坚持"
        ],
        "weaknesses_pt_BR": [
            "Disperso e desorganizado",
            "Excessivamente emocional",
            "Precisa de aprovação constante",
            "Medo de rejeição",
            "Dificuldade em manter o foco até o fim"
        ],
        "careers": [
            "Writer / 作家",
            "Journalist / 记者",
            "Actor / 演员",
            "Marketing Manager / 市场经理",
            "Consultant / 顾问"
        ],
        "careers_pt_BR": [
            "Escritor(a)",
            "Jornalista",
            "Ator / Atriz",
            "Gerente de Marketing",
            "Consultor(a)"
        ],
        "relationships": {
            "best": ["INFJ", "INTJ"],
            "challenging": ["ISTJ", "ESTJ"]
        }
    },
    "ISTJ": {
        "name_cn": "物流师",
        "name_en": "The Logistician",
        "name_pt_BR": "O Fiscal",
        "summary": "A practical fact-based thinker who keeps promises.",
        "summary_cn": "一个保持承诺的实用、基于事实的思考者。",
        "summary_pt_BR": "O Fiscal é um pensador prático e objetivo que honra seus compromissos. Confiável e dedicado, valoriza a tradição, a ordem e a responsabilidade, sendo um pilar de estabilidade em qualquer ambiente.",
        "strengths": [
            "Responsible and reliable / 负责与可靠",
            "Practical and traditional / 实用与传统",
            "Organized and efficient / 有条理与高效",
            "Honest and direct / 诚实与直接",
            "Patient and thorough / 耐心与细致"
        ],
        "strengths_pt_BR": [
            "Responsável e confiável",
            "Prático e tradicional",
            "Organizado e eficiente",
            "Honesto e direto",
            "Paciente e minucioso"
        ],
        "weaknesses": [
            "Stubborn and rigid / 固执与刻板",
            "Judgmental of others / 评判他人",
            "Insensitive to emotions / 对情感不敏感",
            "Not easily adaptable / 不易适应",
            "Overly focused on rules / 过于关注规则"
        ],
        "weaknesses_pt_BR": [
            "Teimoso e rígido",
            "Julgador com os outros",
            "Insensível a emoções",
            "Dificuldade de adaptação a mudanças",
            "Preso demais a regras e normas"
        ],
        "careers": [
            "Accountant / 会计",
            "Auditor / 审计师",
            "Judge / 法官",
            "Financial Manager / 财务经理",
            "Admin Manager / 行政经理"
        ],
        "careers_pt_BR": [
            "Contador(a)",
            "Auditor(a)",
            "Juiz(a)",
            "Gerente Financeiro(a)",
            "Gerente Administrativo(a)"
        ],
        "relationships": {
            "best": ["ESFJ", "ESTJ"],
            "challenging": ["ENFP", "ENTP"]
        }
    },
    "ISFJ": {
        "name_cn": "守卫者",
        "name_en": "The Defender",
        "name_pt_BR": "O Defensor",
        "summary": "A devoted protector who values tradition and loyalty.",
        "summary_cn": "一个重视传统和忠诚的忠诚守护者。",
        "summary_pt_BR": "O Defensor é um protetor dedicado que valoriza profundamente a tradição e a lealdade. Gentil e atencioso, está sempre pronto para cuidar dos outros e criar um ambiente seguro e acolhedor.",
        "strengths": [
            "Reliable and hard-working / 可靠与勤奋",
            "Patient and gentle / 耐心与温和",
            "Practical and helpful / 实用与助人",
            "Devoted and protective / 投入与保护",
            "Memory for details / 细节记忆"
        ],
        "strengths_pt_BR": [
            "Confiável e trabalhador",
            "Paciente e gentil",
            "Prático e prestativo",
            "Dedicado e protetor",
            "Excelente memória para detalhes"
        ],
        "weaknesses": [
            "Overly selfless / 过度忘我",
            "Neglects own needs / 忽视自己的需求",
            "Fear of change / 害怕变化",
            "Too critical of self / 过于自我批评",
            "Absorbs others' stress / 吸收他人压力"
        ],
        "weaknesses_pt_BR": [
            "Altruísmo excessivo",
            "Negligencia as próprias necessidades",
            "Medo de mudanças",
            "Autocrítica exagerada",
            "Absorve o estresse dos outros"
        ],
        "careers": [
            "Nurse / 护士",
            "Social Worker / 社会工作者",
            "Accountant / 会计",
            "Teacher / 教师",
            "HR Specialist / 人力资源专员"
        ],
        "careers_pt_BR": [
            "Enfermeiro(a)",
            "Assistente Social",
            "Contador(a)",
            "Professor(a)",
            "Especialista em RH"
        ],
        "relationships": {
            "best": ["ESFP", "ESTP"],
            "challenging": ["ENTP", "ENFP"]
        }
    },
    "ESTJ": {
        "name_cn": "经理",
        "name_en": "The Executive",
        "name_pt_BR": "O Executor",
        "summary": "An efficient organizer who gets things done.",
        "summary_cn": "一个高效完成事情的组织者。",
        "summary_pt_BR": "O Executor é um organizador eficiente que faz as coisas acontecerem. Prático, direto e orientado a resultados, lidera com firmeza e garante que prazos e metas sejam cumpridos com excelência.",
        "strengths": [
            "Practical and realistic / 实用与现实",
            "Natural leader / 天生领导者",
            "Organized and decisive / 有条理与果断",
            "Honest and direct / 诚实与直接",
            "Traditional and responsible / 传统与负责"
        ],
        "strengths_pt_BR": [
            "Prático e realista",
            "Líder nato",
            "Organizado e decisivo",
            "Honesto e direto",
            "Tradicional e responsável"
        ],
        "weaknesses": [
            "Inflexible and stubborn / 不灵活与固执",
            "Judgmental and critical / 评判与批评",
            "Domineering / 霸道",
            "Insensitive to emotions / 对情感不敏感",
            "Workaholic tendency / 工作狂倾向"
        ],
        "weaknesses_pt_BR": [
            "Inflexível e teimoso",
            "Crítico e julgador",
            "Dominador",
            "Insensível a questões emocionais",
            "Tendência ao vício em trabalho"
        ],
        "careers": [
            "Business Manager / 业务经理",
            "Police Officer / 警官",
            "Judge / 法官",
            "Financial Officer / 财务主管",
            "Teacher / 教师"
        ],
        "careers_pt_BR": [
            "Gerente de Negócios",
            "Oficial de Polícia",
            "Juiz(a)",
            "Diretor(a) Financeiro(a)",
            "Professor(a)"
        ],
        "relationships": {
            "best": ["ISTP", "ISFP"],
            "challenging": ["INFP", "ENFP"]
        }
    },
    "ESFJ": {
        "name_cn": "执政官",
        "name_en": "The Consul",
        "name_pt_BR": "O Cônsul",
        "summary": "A popular people-pleaser who values harmony.",
        "summary_cn": "一个重视和谐的受欢迎的讨好者。",
        "summary_pt_BR": "O Cônsul é uma pessoa popular e acolhedora que valoriza a harmonia acima de tudo. Atencioso e sociável, dedica-se a cuidar dos outros e a criar um ambiente de cooperação e bem-estar ao seu redor.",
        "strengths": [
            "Caring and warm / 关爱与温暖",
            "Popular and outgoing / 受欢迎与外向",
            "Conscientious and organized / 尽责与有条理",
            "Practical and helpful / 实用与助人",
            "Social responsibility / 社会责任"
        ],
        "strengths_pt_BR": [
            "Cuidadoso e caloroso",
            "Popular e extrovertido",
            "Consciencioso e organizado",
            "Prático e prestativo",
            "Fortemente comprometido socialmente"
        ],
        "weaknesses": [
            "Needing approval / 需要认可",
            "Overly generous / 过于慷慨",
            "Insecure without harmony / 没有和谐就不安",
            "Judgmental of differences / 评判差异",
            "Self-sacrificing / 自我牺牲"
        ],
        "weaknesses_pt_BR": [
            "Depende de aprovação externa",
            "Generosidade excessiva",
            "Inseguro sem harmonia",
            "Julgador de diferenças alheias",
            "Autossacrifício em prol dos outros"
        ],
        "careers": [
            "Nurse / 护士",
            "HR Manager / 人力资源经理",
            "Sales Representative / 销售代表",
            "Teacher / 教师",
            "Receptionist / 前台接待"
        ],
        "careers_pt_BR": [
            "Enfermeiro(a)",
            "Gerente de RH",
            "Representante de Vendas",
            "Professor(a)",
            "Recepcionista"
        ],
        "relationships": {
            "best": ["ISFP", "ISTP"],
            "challenging": ["INTP", "INTJ"]
        }
    },
    "ISTP": {
        "name_cn": "鉴赏家",
        "name_en": "The Virtuoso",
        "name_pt_BR": "O Virtuoso",
        "summary": "A bold and practical explorer of mechanical things.",
        "summary_cn": "一个大胆且实用的机械事物探索者。",
        "summary_pt_BR": "O Virtuoso é um explorador prático e ousado do mundo físico. Com uma habilidade inata para entender mecanismos e sistemas, é um solucionador de problemas nato que age com calma sob pressão.",
        "strengths": [
            "Practical and realistic / 实用与现实",
            "Adventurous and spontaneous / 冒险与自发",
            "Natural mechanic / 天生机械师",
            "Logical and analytical / 逻辑与分析",
            "Calm under pressure / 压力下冷静"
        ],
        "strengths_pt_BR": [
            "Prático e realista",
            "Aventureiro e espontâneo",
            "Habilidade nata com mecanismos",
            "Lógico e analítico",
            "Calmo sob pressão"
        ],
        "weaknesses": [
            "Risky behavior / 冒险行为",
            "Insensitive to emotions / 对情感不敏感",
            "Bored by routine / 对例行公事感到无聊",
            "Private and reserved / 私人与内敛",
            "Avoids commitment / 回避承诺"
        ],
        "weaknesses_pt_BR": [
            "Comportamento de risco",
            "Insensível a emoções alheias",
            "Entedia-se com rotina",
            "Muito reservado e fechado",
            "Evita compromissos de longo prazo"
        ],
        "careers": [
            "Engineer / 工程师",
            "Mechanic / 机械师",
            "Pilot / 飞行员",
            "Athlete / 运动员",
            "Forensic Scientist / 法医"
        ],
        "careers_pt_BR": [
            "Engenheiro(a)",
            "Mecânico(a)",
            "Piloto",
            "Atleta",
            "Perito(a) Forense"
        ],
        "relationships": {
            "best": ["ESTJ", "ESFJ"],
            "challenging": ["ENFJ", "INFJ"]
        }
    },
    "ISFP": {
        "name_cn": "探险家",
        "name_en": "The Adventurer",
        "name_pt_BR": "O Aventureiro",
        "summary": "A flexible artist who follows their heart.",
        "summary_cn": "一个跟随内心的灵活艺术家。",
        "summary_pt_BR": "O Aventureiro é um artista flexível que segue o coração. Sensível e criativo, aprecia a beleza do mundo e vive o momento presente com autenticidade, expressando-se através de sua arte e ações.",
        "strengths": [
            "Artistic and aesthetic / 艺术与美学",
            "Practical and realistic / 实用与现实",
            "Gentle and caring / 温和与关爱",
            "Flexible and adaptable / 灵活与适应",
            "Patient and present / 耐心与当下"
        ],
        "strengths_pt_BR": [
            "Artístico e apreciador da estética",
            "Prático e realista",
            "Gentil e cuidadoso",
            "Flexível e adaptável",
            "Paciente e presente no momento"
        ],
        "weaknesses": [
            "Overly private / 过于私密",
            "Fear of conflict / 害怕冲突",
            "Unpredictable / 不可预测",
            "Self-critical / 自我批评",
            "Disorganized / 无条理"
        ],
        "weaknesses_pt_BR": [
            "Excessivamente reservado",
            "Medo de conflitos",
            "Imprevisível",
            "Muito autocrítico",
            "Desorganizado"
        ],
        "careers": [
            "Artist / 艺术家",
            "Designer / 设计师",
            "Photographer / 摄影师",
            "Musician / 音乐家",
            "Chef / 厨师"
        ],
        "careers_pt_BR": [
            "Artista Plástico(a)",
            "Designer",
            "Fotógrafo(a)",
            "Músico(a)",
            "Chef de Cozinha"
        ],
        "relationships": {
            "best": ["ENFJ", "ESFJ"],
            "challenging": ["INTJ", "ENTJ"]
        }
    },
    "ESTP": {
        "name_cn": "企业家",
        "name_en": "The Entrepreneur",
        "name_pt_BR": "O Empreendedor",
        "summary": "A bold action-taker who lives in the moment.",
        "summary_cn": "一个活在当下的大胆行动者。",
        "summary_pt_BR": "O Empreendedor é um tomador de ações ousado que vive intensamente o momento presente. Energético e persuasivo, está sempre em busca de novas emoções e oportunidades, influenciando quem está ao seu redor.",
        "strengths": [
            "Energetic and enthusiastic / 活力与热情",
            "Practical and realistic / 实用与现实",
            "Direct and honest / 直接与诚实",
            "Social and outgoing / 社交与外向",
            "Adaptable and flexible / 适应与灵活"
        ],
        "strengths_pt_BR": [
            "Energético e entusiasmado",
            "Prático e realista",
            "Direto e honesto",
            "Sociável e extrovertido",
            "Adaptável e flexível"
        ],
        "weaknesses": [
            "Impatient and reckless / 急躁与鲁莽",
            "Insensitive to others / 对他人不敏感",
            "Bored by routine / 对例行公事感到无聊",
            "Risk-taker / 冒险者",
            "Poor long-term planning / 长期规划差"
        ],
        "weaknesses_pt_BR": [
            "Impaciente e imprudente",
            "Insensível com os outros",
            "Entedia-se com a rotina",
            "Assume riscos excessivos",
            "Planejamento de longo prazo deficiente"
        ],
        "careers": [
            "Sales Representative / 销售代表",
            "Real Estate Agent / 房地产经纪人",
            "Entertainer / 艺人",
            "Athlete / 运动员",
            "Business Owner / 企业主"
        ],
        "careers_pt_BR": [
            "Representante de Vendas",
            "Corretor(a) de Imóveis",
            "Artista / Animador(a)",
            "Atleta",
            "Empresário(a)"
        ],
        "relationships": {
            "best": ["ISFJ", "ISTJ"],
            "challenging": ["INFJ", "INFP"]
        }
    },
    "ESFP": {
        "name_cn": "表演者",
        "name_en": "The Entertainer",
        "name_pt_BR": "O Animador",
        "summary": "A fun-loving entertainer who lives in the moment.",
        "summary_cn": "一个活在当下的热爱娱乐的人。",
        "summary_pt_BR": "O Animador é um artista nato que adora viver o momento e espalhar alegria. Com seu carisma contagiante e energia vibrante, é a alma da festa e sabe como tornar qualquer ocasião especial.",
        "strengths": [
            "Spontaneous and fun / 自发与有趣",
            "Social and outgoing / 社交与外向",
            "Artistic and creative / 艺术与创意",
            "Optimistic and enthusiastic / 乐观与热情",
            "Charismatic and charming / 魅力与迷人"
        ],
        "strengths_pt_BR": [
            "Espontâneo e divertido",
            "Sociável e extrovertido",
            "Artístico e criativo",
            "Otimista e entusiasmado",
            "Carismático e encantador"
        ],
        "weaknesses": [
            "Easily bored / 容易厌倦",
            "Fear of criticism / 害怕批评",
            "Poor planning / 规划差",
            "Overly sensitive / 过于敏感",
            "Materialistic / 物质主义"
        ],
        "weaknesses_pt_BR": [
            "Entedia-se facilmente",
            "Medo de críticas",
            "Planejamento deficiente",
            "Excessivamente sensível",
            "Tendência ao materialismo"
        ],
        "careers": [
            "Actor / 演员",
            "Singer / 歌手",
            "Event Planner / 活动策划",
            "Marketing Manager / 市场经理",
            "Sales Representative / 销售代表"
        ],
        "careers_pt_BR": [
            "Ator / Atriz",
            "Cantor(a)",
            "Organizador(a) de Eventos",
            "Gerente de Marketing",
            "Representante de Vendas"
        ],
        "relationships": {
            "best": ["ISTJ", "ISFJ"],
            "challenging": ["INTJ", "INFJ"]
        }
    }
}


def get_type(type_code: str) -> Dict:
    """Get type data by code"""
    return TYPES.get(type_code.upper(), {})


def get_all_types() -> Dict:
    """Get all types"""
    return TYPES
