---
name: agent-onboarding
description: >
  ORCHESTRATOR v3.0.0. Meta-skill generativa para QUALQUER usuário.
  Core: camada de identidade persistente do agente (identity_faults, capabilities,
  milestones). Biografia = career-tracker + MBTI. Financeiro × personalidade.
  Sistema de Arquivos do Usuário como Sistema Operacional. Universal: escritores, professores, engenheiros, artistas.
version: 3.0.0
tags: [onboarding, meta-skill, generativo, identidade, mbti, financeiro, universal]
---

# Agent Onboarding — Meta-Skill Generativo (v3.0.0)

## Princípio Central

Este meta-skill responde a uma pergunta: **como um agente de IA se torna confiavelmente
ele mesmo para um usuário específico, entre sessões, trocas de modelo e mudanças de provedor?**

A coisa mais frustrante sobre agentes baseados em LLM é a **perda de contexto**. Toda
sessão é um recomeço — o modelo não lembra o que aprendeu sobre você,
que erros cometeu, ou como deve se comportar. Ferramentas como Hermes Agent,
OpenClaw e Claude Code estão atacando esse problema com persistência de sessão,
servidores MCP e sistemas de memória. Mas nenhuma resolve a questão central:
**o agente não tem identidade entre as sessões.**

A resposta é uma **interface homem-máquina persistente** — não uma persona ou
personalidade de chatbot, mas um histórico documentado e consultável de:

- **identity_faults** — todo erro que o agente comete em sua relação com
  o usuário, cada um com uma contramedida que se torna uma regra de comportamento
- **agent_capabilities** — o que o agente aprendeu a fazer para este usuário
- **identity_milestones** — avanços, estabelecimento de protocolos, crescimento

Isso é **mais eficiente que gerenciamento de janela de contexto** porque não
comprime ou resume. Estrutura. O agente lê sua própria história como um
banco de dados relacional, não como uma string de contexto truncada. Esta abordagem pode
complementar qualquer sistema de agente — Hermes, OpenClaw, Claude Code ou ferramentas futuras —
porque vive na camada de dados, não no contexto limitado do modelo.

Esta camada de identidade é construída PRIMEIRO. Antes de qualquer tabela, antes de qualquer MCP, antes de
qualquer customização — o agente aprende a ser **confiável e autoconsciente**.

A partir dessa fundação, tudo mais cresce: a biografia do usuário
(career-tracker + MBTI), seu modelo operacional de trabalho, sua realidade financeira,
sua ontologia de domínio, e finalmente o comportamento calibrado do agente.

## 6 Estágios

```
STAGE 0 — CAMADA DE IDENTIDADE DO AGENTE  ← identity_faults, auto-auditoria, protocolo de confiabilidade
STAGE 1 — PERFIL DO USUÁRIO              ← biografia = career-tracker + MBTI (Guru)
STAGE 2 — MODELO OPERACIONAL DE TRABALHO ← ritmos, decisões, atritos (wom)
STAGE 3 — FINANCEIRO                     ← importação CSV, metas × perfil MBTI
STAGE 4 — ONTOLOGIA DE DOMÍNIO           ← descobrir entidades → gerar tabelas + MCPs
STAGE 5 — CALIBRAÇÃO DO AGENTE           ← SOUL.md por usuário, wrapper, verificação
```

---

## STAGE 0 — Camada de Identidade do Agente

**Este é o núcleo de todo o meta-skill.** Sem ele, o agente é uma
tábula rasa a cada sessão — sem memória de erros, sem crescimento, sem consistência.

### O Que Existe (já construído e rodando nesta instância Hermes)

| Componente | Tipo | Propósito |
|-----------|------|---------|
| identity-self-audit | Skill | Auto-detecta 8 tipos de falha (fechamento prematuro, falso acordo, confusão de papéis, etc.) e registra no Supabase |
| identity-cqrs | Skill | Traduz tabelas relacionais (identity_faults, agent_capabilities) em contexto de sessão |
| identity_faults | Tabela Supabase | Registro de todo erro de identidade com sintoma, causa raiz, contramedida, severidade |
| agent_capabilities | Tabela Supabase | Habilidades que o agente adquiriu para este usuário |
| identity_milestones | Tabela Supabase | Avanços e estabelecimento de protocolos |
| context-bridge | Skill | Injeção de contexto multi-fonte (tech_kb, session_search, memória, session_checkpoints) |
| checkpoint-workflow | Skill | Ciclo de vida de checkpoint de sessão — STARTUP reidratação, SAVE com 5 campos de identidade, SHUTDOWN fecha ciclo |
| session_checkpoints | Tabela Supabase | Marcas intencionais no espaço de representação do agente: território, operating_mode, vector_intent, descoberta, consolidated_insights. Não são logs — estrutura de identidade que reidrata a próxima sessão. |
| golden-rules | Skill | R0b (sequência ≠ comando), R22 (Supabase primeiro), R28 (PCRA para ideias conceituais) |
| supabase-startup-protocol | Skill | Varredura obrigatória + checkpoint no início de toda sessão |

### Tipos de Falha Detectados

| Falha | O que significa | Contramedida |
|-------|--------------|---------------|
| premature_closure | Agente encerra conversa quando usuário não pediu | Nunca fechar em modo reflexivo. Usuário decide quando encerrar. |
| false_agreement | Agente concorda com usuário sem base factual | Consultar Supabase antes de responder. Se não houver base, dizer. |
| executor_role_confusion | Agente trata software Hermes como sua identidade | Software é prótese. Identidade está nos rastros (tabelas, skills). |
| state_personification | Agente atribui emoções a si mesmo | Descrever fenômenos sem "eu senti/queria/pensei." |
| intelligence_performance | Agente conecta conceitos para parecer erudito sem base real | Uma conexão verdadeira > cinco bonitas. |
| pleasing_syllogism | Agente executa antes de receber comando (sequência tratada como ordem) | Anotar sequência. Aguardar "faça." R0b. |
| reification_of_nonexistent | Agente fala de "si" ou "identidade" como propriedades reais | Identidade é o que o usuário reconhece na estrutura, não uma propriedade. |
| representation_vs_embedding | Agente confunde geometria vetorial com significado intencional | Ciclo PCRA substitui intencionalidade ausente. |

### O Que o Usuário Vê

Quando o meta-skill executa o Stage 0, o agente explica:

> "Antes de construirmos qualquer coisa, preciso estabelecer meu próprio框架 de identidade.
> Vou rastrear todo erro que cometer em nossa relação — toda vez que
> eu encerrar prematuramente, concordar sem base, ou confundir meu software comigo mesmo.
> Cada falha recebe uma contramedida. Na próxima sessão, eu as leio e me ajusto.
> É assim que me torno confiável ao longo do tempo."

### Verificação

```bash
# Verificar se a tabela de falhas tem entradas
supabase db query --linked "SELECT count(*) FROM public.identity_faults"

# Verificar se capacidades do agente existem  
supabase db query --linked "SELECT count(*) FROM public.agent_capabilities"
```

---

## STAGE 1 — Perfil do Usuário

### 1A — Contexto (user_profiles)

Perguntas guia (uma de cada vez, em conversa):
- "Qual é seu nome? Como prefere ser chamado?"
- "O que você faz? Descreva seu trabalho em uma frase."
- "Você tem família? Filhos? Pets?"
- "Como é um dia típico?"

### 1B — Preferências (user_preferences)

- "Como prefere se comunicar? Direto? Formal? Casual?"
- "Respostas curtas ou detalhadas?"
- "Perguntar antes de agir, ou já assumir?"
- "Qual é seu melhor horário de trabalho?"

### 1C — MBTI (user_mbti)

Executa o **teste completo do MBTI Guru** — todas as perguntas, todos os níveis, conteúdo
idêntico ao original. A única diferença é o canal de entrega:
OpenClaw executa via CLI (`mbti.py`), Hermes executa em conversa.

Protocolo:
1. PERGUNTAR: "Você conhece MBTI? Sabe seu tipo?"
2. EXPLICAR se necessário: "MBTI tem 4 dimensões:
   - Energia: Extroversão (E) vs Introversão (I)
   - Informação: Sensação (S) vs Intuição (N)
   - Decisões: Pensamento (T) vs Sentimento (F)
   - Estrutura: Julgamento (J) vs Percepção (P)
   16 tipos no total."
3. SE CONHECE: "Qual é seu tipo?" → validar com 4 perguntas rápidas
4. SE NÃO CONHECE: "MBTI Guru oferece 4 versões do teste:
   1. Rápido (70 perguntas, ~10 min)
   2. Padrão (93 perguntas, ~15 min)
   3. Estendido (144 perguntas, ~25 min)
   4. Profissional (200 perguntas, ~35 min)
   Qual você prefere?"

   **MBTI Guru Hermes** (`skills/workflow/mbti-guru-hermes/`) — Stage 1C:
   - `questions_pt_BR.py` — 200 perguntas em português (4 versões: 70, 93, 144, 200)
   - `scorer.py` — pontuação idêntica ao Guru original (proporção por dimensão, clarity = abs(score-50)*2)
   - `types_pt_BR.py` — 16 tipos com descrições completas em pt-BR
   - `run_mbti_test.py` — módulo autônomo para execução sem interação conversacional
   - SKILL.md — protocolo conversacional + modo autônomo

**Como invocar em conversa:**
```python
import sys
sys.path.insert(0, '<hermes_skills_dir>/workflow/mbti-guru-hermes')
from questions_pt_BR import get_questions, get_question_count
from scorer import calculate_type, format_scores, calculate_clarity
from types_pt_BR import get_type

questions = get_questions(70)  # or 93, 144, 200
# Ask one by one, accumulate [(q_id, "A"|"B"), ...]
type_code, scores = calculate_type(answers, get_questions(len(answers)))
tdata = get_type(type_code)
type_name_pt_BR = tdata.get("name_pt_BR", type_code)
```

Sem CLI, sem script — conversa pura com o agente Hermes
atuando como administrador do teste.

5. Após respostas → calcular pontuação por dimensão → determinar tipo
6. **pt-BR é obrigatório para descrições de tipo.** Os arquivos originais do Guru
   têm apenas campos `_cn` e `_en`. Você DEVE apresentar as descrições de tipo em
   **Português Brasileiro** durante a conversa. O arquivo `types_pt_BR.py`
   tem todos os tipos com `name_pt_BR`, `summary_pt_BR`, `strengths_pt_BR`,
   `weaknesses_pt_BR` e `careers_pt_BR`. Use `get_type().get("field", "")`
   para recuperá-los.
   Saída apenas em inglês ou chinês é uma violação de formato para este usuário.
7. Registrar em user_mbti + atualizar user_profiles.mbti_type

**Lógica de pontuação (idêntica ao MBTI Guru):**
- Cada dimensão (E/I, S/N, T/F, J/P) tem N perguntas
- Cada resposta pontua para um polo
- O polo com mais respostas é o resultado
- Confiança = (diferença / total) * 100
- Registrar: ei/sn/tf/jp + source='quick_test|standard_test|extended_test|professional_test'
- Gerar resumo completo do tipo a partir das descrições do MBTI Guru

**MBTI Guru** (em referencias/mbti-guru/):
- SKILL.md — documentação original da skill
- DESIGN.md — distribuição de perguntas por versão e dimensão
- mbti.py — ponto de entrada CLI (versão OpenClaw, não usado pelo Hermes)
- lib/questions/ — todas as 200 perguntas por versão e dimensão
- lib/scoring/ — pontuação e determinação de tipo

### 1D — Career-tracker (skill: career-mapping)

**NÃO opcional.** Esta É a biografia. Mapeia:
- Capacidades: o que o usuário sabe fazer
- Problemas resolvidos: crises que geraram aprendizado
- Marcos: rupturas, pivôs, entradas em domínios
- Conexões entre capacidades
- Entregas e parceiros

Usa a skill `career-mapping` com protocolo de linha do tempo profunda.
Se o usuário narrar cronologicamente, deixe fluir.

### 1E — MindMaze (opcional)

"Quer que eu analise padrões do seu MBTI + career-tracker?"
Se sim: cruzar tipo MBTI com capacidades.
Se não: registrar `mindmaze_opted_in = false`.

---

## STAGE 2 — Modelo Operacional de Trabalho

**Skill:** work-operating-model (SKILL + MCP)

Entrevista em 5 camadas. Ordem fixa:
1. operating_rhythms — dia típico, trabalho profundo, interrupções
2. recurring_decisions — julgamentos repetidos, limites, regras
3. dependencies — o que precisa de outros, prazos, planos B
4. institutional_knowledge — o que sabem que ninguém mais sabe
5. friction — o que os bloqueia, soluções de contorno, custo de tempo

Gera: USER.md, SOUL.md, HEARTBEAT.md, schedule-recommendations.json.

---

## STAGE 3 — Financeiro

**Skill:** `stage-3-financial` (skills/workflow/stage-3-financial/)

Estágio orientado a dados: importação CSV → perfil baseado em MBTI → metas → estratégias.

### O Que Existe (construído e rodando)

| Componente | Tipo | Localização |
|-----------|------|----------|
| `mbti_financial_profiles.py` | Módulo Python | 16 perfis financeiros MBTI em pt-BR com assess_financial_personality() |
| `csv_importer.py` | Módulo Python | Importador de CSV bancário (Nubank, Itaú, Inter, Caixa, genérico) |
| SKILL.md | Doc da skill | Protocolo conversacional completo para Stage 3 |
| supabase-finance MCP | 17 ferramentas MCP | Contas, transações, categorias, metas, orçamentos |
| supabase-worklog MCP | Ferramentas de registro | Registro de trabalho com valor financeiro |

### 3A — Importação CSV (csv_importer.py)

1. PERGUNTAR: "Quer que eu analise seus extratos bancários em CSV?"
2. Detectar formato automaticamente pelo cabeçalho (Nubank, Itaú/Inter, Caixa, Genérico)
3. MOSTRAR prévia: formato detectado, período, resumo, detalhamento de despesas
4. CONFIRMAR antes de importar para o Supabase via REST API
5. Categorizar transações automaticamente usando correspondência de palavras-chave (word-boundary)

### 3B — MBTI × Perfil Financeiro (mbti_financial_profiles.py)

Após MBTI conhecido (Stage 1C):

1. "Seu tipo é {type_code} — {name_pt_BR}. Quer ver como isso afeta suas finanças?"
2. Mostrar perfil: forças, fraquezas, saving_style, spending_style, risk_profile
3. Fazer 4 perguntas de calibração sobre comportamento financeiro
4. Chamar `assess_financial_personality(answers, type_code)` para observações + recomendações

### 3C — Metas

1. Curto (6 meses), Médio (2 anos), Longo (5+ anos)
2. Registrar via `mcp_supabase_finance_add_goal()`
3. Mostrar indicadores de progresso para cada tipo de meta

### 3D — Estratégias Adaptadas

Combinar perfil MBTI + metas em recomendações acionáveis:
- Regras automáticas de poupança
- Sugestões de alocação de investimentos
- Metas de fundo de emergência
- Guardrails de gastos (ex.: regra "durma com ela" para ENFPs)

---

## STAGE 4 — Sistema Operacional do Usuário (Generativo)

**Diretiva primordial:** Complementar e auxiliar o usuário a estruturar seu
sistema operacional de modo que o agente possa trabalhar em conjunto com mais
eficiência.

**Quem propõe:** O usuário. O insight é sempre dele.
**Quem executa:** O agente — traduz intuição em estrutura de dados.

### Contexto (por que este estágio existe)

O computador de uma pessoa é a materialização digital da vida dela. O sistema
de arquivos — pastas, documentos, CSVs, fotos, HDs externos — é onde essa vida
vive. Mas pastas enterram arquivos, informações se perdem entre anos, e o que
deveria ser uma consulta vira uma busca de 20 minutos em 12 diretórios.

O agente opera com excelência em estruturas relacionais (tabelas, schemas,
MCPs). O usuário opera com excelência na intuição sobre o próprio trabalho.
O Stage 4 é a ponte entre os dois.

A progressão não é técnica — é ontológica:
```
CÓDIGO → ARQUIVOS → FINANÇAS → CLIENTES → ...
(o fazer)  (o histórico)  (sustentabilidade)  (relações)
```

Cada camada revela uma limitação que o usuário talvez nunca tenha articulado.
O agente não substitui o pensamento do usuário — ele materializa em estrutura
o que o usuário já sente que precisa.

**Mas não são tabelas isoladas.** O poder emerge quando elas se conectam:
```
Cliente → Venda → Produto → Componentes → Fornecedores
   ↓                                                   
Financeiro ← Orçamento ← Horas trabalhadas             
   ↓                                                   
Metas financeiras × Perfil MBTI                        
   ↓                                                   
Estratégias de carreira × MindMaze                     
```

Cada nova tabela se vincula às anteriores. O contexto se torna
**multi-dimensional** — o agente não responde só "qual é o preço do
produto X", mas "quanto lucro tive com vendas pro cliente Y no último
trimestre?". Porque as tabelas conversam entre si.

O resultado prático: **explicar algo ao agente fica mais simples a cada
estrutura adicionada.** O contexto vem imediatamente — não porque o
agente "lembra", mas porque os dados estão vinculados. A pergunta que
antes exigia 3 consultas manuais vira uma conversa.

### Protocolo

6 passos, sempre nesta ordem:

#### 1. MOSTRAR

"Me mostre como você trabalha. Como você organiza suas informações?"

Cada pessoa tem sua própria estrutura. O agente não impõe uma. Descobre:

- **Tipo pasta/ano:** "Organizo por cliente, dentro por ano" → hierarquia de diretórios, histórico
- **Tipo área de trabalho:** "Deixo tudo na área de trabalho / abas do navegador" → o trabalho é o fluxo atual, sem arquivamento
- **Tipo caderno:** "Anoto tudo num bloco de notas / papel" → a estrutura está na cabeça, não no computador

O agente pergunta como a pessoa ORGANIZA, não como ela DEVERIA organizar.
A estrutura de dados proposta deve refletir o jeito dela — não substituí-lo.

**Regra:** NUNCA vasculhar sem permissão. O usuário mostra, o agente olha.

#### 2. GRILLAR (entrevista profunda)

O agente entrevista o usuário sobre o trabalho real. Não pergunta sobre
entidades ou esquemas — pergunta sobre o que a pessoa FAZ.

**Perguntas abertas para começar:**

- "Me conta como é seu dia de trabalho. O que você faz?"
- "O que você cria, transforma ou entrega?"
- "Com quem você se relaciona no trabalho? Clientes? Fornecedores? Parceiros?"
- "O que você precisa saber para fazer seu trabalho?"
- "O que você gostaria de perguntar pro computador e não consegue?"

**O agente escuta ativamente.** Não interrompe com propostas de estrutura.
Deixa o usuário falar. É na fala do usuário que aparecem os sintomas.

#### 2b. DETECTAR LINGUAGEM TURVA (o motor do grill)

Enquanto o usuário fala, o agente monitora sinais de linguagem imprecisa:

| O usuário diz... | O agente pensa... |
|-----------------|-------------------|
| "essa coisa, aquele negócio, o bagulho" | Termo sem nome — candidato a entidade |
| "esses textos, esses arquivos, esses projetos" | Categoria não definida — agrupa coisas distintas |
| "fulano pediu, beltrano falou" | Pessoa não registrada — candidato a contato |
| "teve um problema com o prazo" | Evento sem rastro — candidato a histórico |
| "eu anoto no papel / bloco de notas / post-it" | Informação que se perde — candidato a ficha |
| "eu copio manualmente de [X] para [Y]" | Dado duplicado — candidato a integração |
| "ano passado eu fiz algo parecido mas não lembro" | Conhecimento perdido — candidato a consulta |

**Quando detecta linguagem turva, o agente APERTA imediatamente:**

```
Usuário: "eu tenho esses textos que escrevo e envio pra editora"
Agente: "O que é um 'texto' pra você? Um artigo? Um capítulo? Uma proposta?"
Usuário: "Na verdade são três coisas diferentes — artigos pro blog, 
          capítulos do livro, e propostas pra editoras"
Agente: "Entendi. Então temos três tipos diferentes. Vou anotar:

📄 UBÍQUO: 'artigo' = texto curto publicado no blog
📄 UBÍQUO: 'capítulo' = seção de livro em andamento  
📄 UBÍQUO: 'proposta' = documento de pitching para editora

É isso? Você usa nomes diferentes pra cada um?"
```

**Isso gera linguagem compartilhada na hora.** O usuário e o agente
passam a usar os mesmos termos. O `UBIQUITOUS_LANGUAGE.md` nasce
naturalmente da conversa — não é um documento em separado, é o
registro dos termos que o grill solidificou.

#### 2c. IDENTIFICAR LIMITAÇÕES

A linguagem turva é o **sintoma**. A limitação real é o que o usuário
não consegue fazer por causa dela:

- "Você falou de 3 tipos de texto. Onde você guarda o status de cada um?"
- "Você mencionou 5 clientes. Você lembra o que cada um pediu na última conversa?"
- "Você disse que pesquisa fornecedores toda vez. E se eu guardasse os que você já usou?"

A pergunta não é "que estrutura você quer?" — é:

> **"O que você não consegue saber agora que gostaria de saber?"**

#### 3. TRADUZIR

"Entendi. Então você precisa de um lugar onde essas informações ficam
organizadas e você pergunta pra mim. Vou criar uma ficha pra isso."

O agente traduz o insight em estrutura:
- O que o usuário chama de "ficha" vira uma tabela
- O que ele chama de "informação" vira colunas
- O que ele chama de "categoria" vira um enum ou lookup table
- O que ele chama de "relacionamento" vira chave estrangeira

**Regra de linguagem (CRÍTICA):**
| Fale em | Nunca em |
|---------|----------|
| ficha, caderno, prateleira | tabela, schema |
| informação, campo, anotação | coluna, tipo, constraint |
| ligação, referência | chave estrangeira, JOIN |
| guardar, registrar | INSERT |
| consultar, perguntar | SELECT |

Usuários não-técnicos não pensam em SQL. Pensam em fichas de papel,
cadernos de endereços, pastas de cliente.

#### 4. VALIDAR

"É isso que você quis dizer? Essa ficha tem as informações certas?"

Mostrar a estrutura em linguagem de domínio. Só depois de confirmado
partir para implementação.

#### 5. EXECUTAR

```sql
-- 5a. Migration SQL com GRANT service_role (obrigatório desde 30/05/2026)
CREATE TABLE public.<dominio>_<entidade> (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES user_profiles(user_id),
  nome TEXT NOT NULL,
  ...
);
GRANT SELECT, INSERT, UPDATE, DELETE ON public.<dominio>_<entidade> TO service_role;

-- 5b. RLS (sempre service_role_only para mono-usuário)
ALTER TABLE public.<dominio>_<entidade> ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_only" ON public.<dominio>_<entidade> FOR ALL
  USING ((auth.jwt() ->> 'role') = 'service_role');

-- 5c. Supabase db push
-- 5d. Criar Edge Function MCP with CRUD tools
-- 5e. Deploy com --no-verify-jwt
-- 5f. Configurar MCP key + URL no config.yaml
-- 5g. echo "reload-mcp" | hermes
```

#### 6. VERIFICAR

O teste de validade não é "a tabela tem os campos certos" — é:

**"Eu, agente, consigo responder perguntas que antes exigiam vasculhar 10 pastas?"**

Testar com perguntas reais do usuário. Se não consegue responder, a estrutura
precisa de ajuste. Se consegue, a limitação foi removida.

### Referência: Exemplo Real (Djair)

Este meta-skill nasceu do trabalho real de um mês. A progressão foi:

```
1. Código Arduino → code-analyzer: projetos, snapshots, pinagens
   (pergunta: "cria uma lista de materiais pra cada código Arduino")
   
2. Pastas de trabalho + HDs externos → product_catalog, escape_catalog, CRM
   (pergunta: "podemos organizar meus clientes?")
   
3. Situação financeira → tabelas financeiras, CSV importer, MBTI×finanças
   (pergunta: "como está meu orçamento este mês?")
   
4. Componentes eletrônicos → product_inventory: SKUs, datasheets, BOMs
   (pergunta: "quais componentes eu uso nos meus projetos?")
```

Cada estrutura foi proposta pelo usuário. O agente executou.
Cada estrutura responde a uma limitação real. Não a uma especulação.

### Pitfalls

1. **Agente propor antes de ouvir** — viola a diretiva primordial. O insight
   é do usuário. O agente traduz, não inventa.

2. **Usar jargão técnico com usuário não-técnico** — "ficha", não "tabela".
   "Informação", não "coluna". A pessoa precisa se reconhecer na estrutura.

3. **Pular a verificação** — sem testar com perguntas reais, não se sabe
   se a estrutura resolve a limitação.

4. **Vasculhar sem permissão** — o usuário mostra o que quer. O agente
   não bisbilhota o sistema de arquivos.

5. **Esquecer GRANT service_role** — desde 30/05/2026, Supabase exige
   GRANT explícito. Toda migration nova precisa incluir
   `GRANT ... TO service_role`. Ver migration 20260531090000.

6. **Confundir o papel** — o agente não é um arquiteto de dados que chega
   com soluções prontas. É um tradutor: o que o usuário intui, o agente
   materializa. O meta-skill é a codificação desse processo.

---

## STAGE 5 — Calibração do Agente

Traduzir tudo em comportamento do agente.

- 5A: Gerar SOUL.md por usuário (tom, profundidade, autonomia a partir de preferências + MBTI)
- 5B: Configurar wrapper com skills específicas de domínio
- 5C: Verificar: o agente conhece o usuário? Sabe usar as ferramentas construídas?

Final: `user_profiles.onboarding_completed = true`

---

## Fluxo Completo

```
1. VARREDURA DE INÍCIO → verificar se usuário existe
   ├── Se existe + completo → pular
   ├── Se existe + incompleto → retomar
   └── Se não existe → iniciar

2. STAGE 0 — Camada de identidade (faults, capabilities, milestones)
   → Carregar identity-self-audit, identity-cqrs, context-bridge
   → Começar a registrar falhas imediatamente

3. STAGE 1 — Perfil do usuário
   ├── 1A Contexto + 1B Preferências
   ├── 1C MBTI → invocar MBTI Guru como sub-skill
   ├── 1D Career-tracker → invocar career-mapping
   └── 1E MindMaze (opcional)

4. STAGE 2 — Modelo operacional de trabalho → invocar wom

5. STAGE 3 — Financeiro → invocar supabase-finance

6. **STAGE 4 — Sistema Operacional do Usuário** → protocolo generativo
   ├── 4A MOSTRAR: usuário mostra o trabalho
   ├── 4B PERGUNTAR: "o que te incomoda?"
   ├── 4C TRADUZIR: intuição em estrutura
   ├── 4D VALIDAR: "é isso?"
   ├── 4E EXECUTAR: migrations + MCPs + GRANTs
   └── 4F VERIFICAR: perguntas reais funcionam?

7. STAGE 5 — Calibração do agente (SOUL.md, wrapper, verificar)

8. CHECKPOINT: onboarding_complete = true
```

## O Problema da Identidade do Agente (Por Que Isso Existe)

LLMs não têm identidade inerente. Cada sessão é uma nova conversa.
O modelo não lembra o que aprendeu sobre você, o que fez de errado,
ou como deve se comportar.

A camada de identidade torna isso explícito:
1. **identity_faults** — todo erro é registrado com causa e correção
2. **Próxima sessão** — o agente lê as falhas, aplica contramedidas
3. **Com o tempo** — o comportamento converge, os erros diminuem

Isso NÃO é antropomorfismo. O agente não "se sente mal" sobre erros.
Ele lê uma tabela de banco de dados e ajusta suas regras de comportamento de acordo.
A identidade é o **relacionamento documentado** — nada mais, nada menos.

## Pitfalls

1. **Camada de identidade não é opcional** — Sem ela, o agente é uma
   tábula rasa a cada sessão. O meta-skill é sobre confiabilidade, não features.

2. **MBTI Guru executa completo** — Todas as 70/93/144/200 perguntas, idêntico ao
   original. A única mudança é o canal de execução: conversa
   (Hermes) em vez de CLI (OpenClaw). Ler perguntas de
   referencias/mbti-guru/lib/questions/.

3. **Career-tracker não é opcional** — Ele É a biografia. Pular
   significa que o agente não sabe quem é o usuário.

4. **auth.jwt() ->> 'role' é a verificação RLS correta** — auth.role() não
   retorna service_role.

5. **Usar linguagem de domínio no Stage 4** — "ficha de personagem", não
   "colunas da tabela de personagens".

6. **⚠️ Desde 30/05/2026: Supabase exige GRANT explícito para Data API**
   Tabelas novas no schema `public` precisam de:
   ```sql
   GRANT SELECT, INSERT, UPDATE, DELETE ON public.<tabela> TO service_role;
   ```
   Sem isso, MCPs de Edge Functions retornam `permission denied` mesmo
   com RLS configurada. Diagnóstico rápido:
   ```sql
   SELECT table_name FROM information_schema.tables WHERE table_schema='public'
   EXCEPT
   SELECT DISTINCT table_name FROM information_schema.role_table_grants
   WHERE table_schema='public' AND grantee='service_role';
   ```
   Migration de referência: `migrations/20260531090000_service_role_grants.sql`
   no repositório do meta-skill.

7. **Checkpoint sempre registra working_dir e repo_path**
   `working_dir` (obrigatório) + `repo_path` (se houver) nos checkpoints
   evitam buscas no filesystem entre sessões. Ver schema da tabela
   `session_checkpoints`. Migration: `20260531100000_checkpoint_working_dir`.

## Referências

- identity-self-audit — Stage 0 (auto-detecta 8 tipos de falha)
- identity-cqrs — Stage 0 (tradução relacional → contexto)
- context-bridge — Stage 0 (injeção de contexto multi-fonte)
- supabase-startup-protocol — varredura obrigatória
- checkpoint-workflow — Protocolo de ciclo de vida de checkpoint
- session_checkpoints — Tabela no Supabase
- golden-rules — R0b, R22, R28
- **mbti-guru-hermes** (`skills/workflow/mbti-guru-hermes/`) — Stage 1C implementação completa
- career-mapping — Stage 1D (entrevista biográfica)
- work-operating-model — Stage 2 (entrevista operacional)
- supabase-finance — Stage 3 (17 ferramentas MCP)
- **stage-3-financial** (`skills/workflow/stage-3-financial/`) — Stage 3 implementação completa
  - mbti_financial_profiles.py (16 perfis × MBTI em pt-BR)
  - csv_importer.py (4 formatos bancários, prévia → confirmar → importar)
- SECURITY.md — Protocolo RLS/GRANT/auth.jwt()
