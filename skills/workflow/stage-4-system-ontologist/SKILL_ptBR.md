---
name: stage-4-system-ontologist
description: >
  Entrevista o usuário sobre o trabalho/domínio dele usando o padrão grill
  (perguntas profundas, detecção de linguagem turva, solidificação de termos
  ubíquos). Quando identifica uma limitação que estrutura de dados resolveria,
  traduz o insight do usuário em tabelas Supabase + MCPs + GRANTs.
  Use quando estiver no Stage 4 do meta-skill agent-onboarding, ou quando
  o usuário disser que quer organizar informações ou estruturar dados.
tags: [meta-skill, stage-4, ontologia, grill, entrevista, ubiquitous-language]
---

# Stage 4 — Sistema Operacional do Usuário

## Diretiva

Complementar e auxiliar o usuário a estruturar o sistema operacional dele
para que o agente possa trabalhar em conjunto com mais eficiência.

**O insight é sempre do usuário.** O agente traduz intuição em estrutura,
não inventa nem especula. Se não souber o suficiente, pergunte.

## Disparo

Quando o usuário disser que quer organizar algo, estruturar informações,
ou quando você estiver no Stage 4 do meta-skill agent-onboarding:

1. Carregue este skill mentalmente
2. Siga o protocolo abaixo em ordem

## Protocolo (faça na ordem)

### 1. MOSTRAR

"Como você organiza suas informações? Pastas? Área de trabalho? Cadernos?"

Identifique o perfil de organização:
- **Pasta/ano:** hierarquia consciente, histórico preservado
- **Área de trabalho:** fluxo atual, sem arquivamento
- **Caderno/papel:** estrutura na cabeça, não no computador

Não vasculhe sem permissão. O usuário mostra o que quer.

### 2. GRILLAR

Entreviste sobre o trabalho real. Perguntas abertas:
- "Me conta seu dia de trabalho. O que você faz?"
- "O que você cria, transforma ou entrega?"
- "O que você gostaria de perguntar pro computador e não consegue?"

Deixe o usuário falar. Não interrompa com propostas de estrutura.
Escute ativamente.

### 2b. DETECTAR LINGUAGEM TURVA

Enquanto escuta, monitore estes sinais:

| Usuário diz | Significa |
|-------------|-----------|
| "essa coisa, aquele negócio" | Termo sem nome — apertar |
| "esses textos, esses arquivos" | Categoria que agrupa coisas distintas — separar |
| "fulano pediu, beltrano falou" | Pessoa não registrada — contato |
| "anoto no papel / post-it" | Informação que se perde — ficha |
| "copio manualmente de X pra Y" | Dado duplicado — integrar |
| "ano passado fiz algo parecido" | Conhecimento perdido — consulta |

Quando detectar, APERTE imediatamente na conversa:

```
Usuário: "eu tenho esses textos que envio pra editora"
Você:    "O que é um 'texto' pra você? Artigo? Capítulo? Proposta?"
Usuário: "Na verdade são três coisas diferentes"
Você:    "Vou anotar: 'artigo' = texto pro blog, 'capítulo' = seção do livro,
          'proposta' = pitching pra editora. É isso?"
```

Solidifique o termo. Confirme com o usuário. Siga em frente.

### 2c. IDENTIFICAR LIMITAÇÕES

Linguagem turva é sintoma. A limitação real é o que o usuário não consegue
saber por causa dela:

- "Onde você guarda o status de cada um?"
- "Você lembra o que cada cliente pediu na última conversa?"
- "E se eu guardasse isso pra você consultar?"

A pergunta final é: **"O que você não consegue saber agora que gostaria?"**

### 3. TRADUZIR → PROPOR

Proponha em linguagem de domínio:

- "ficha" = tabela
- "informação" = coluna
- "ligação" = chave estrangeira
- "guardar" = INSERT
- "perguntar" = SELECT

### 4. VALIDAR

"É isso que você quis dizer? Essa ficha tem as informações certas?"
Só avance após confirmação.

### 5. EXECUTAR

```sql
CREATE TABLE public.<dominio>_<entidade> ( ... );
GRANT SELECT, INSERT, UPDATE, DELETE ON public.<dominio>_<entidade> TO service_role;
ALTER TABLE ... ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_only" ... USING ((auth.jwt()->>'role') = 'service_role');
```

Supabase db push. Se for MCP: Edge Function + deploy + config key + reload-mcp.

### 6. VERIFICAR

Teste com perguntas reais do usuário. "Consegue me responder o que eu perguntei?"
Se sim, a limitação foi removida. Se não, ajuste a estrutura.

## Pitfalls

1. **Propor antes de ouvir** — viola a diretiva. O insight é do usuário.
2. **Jargão técnico com não-técnicos** — "ficha", não "tabela".
3. **Pular verificação** — sem testar com perguntas reais, não sabe se resolve.
4. **Vasculhar sem permissão** — usuário mostra o que quer.
5. **Esquecer GRANT service_role** — desde 30/05/2026, obrigatório.
6. **Achar que terminou** — o Stage 4 é recursivo. Cada estrutura revela outra
   limitação. Pergunte: "tem mais alguma coisa que te incomoda?"
