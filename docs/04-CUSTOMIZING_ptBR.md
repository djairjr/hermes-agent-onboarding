# Personalizando para Seu Domínio

O meta-skill foi projetado para funcionar para QUALQUER trabalhador do conhecimento: escritores, engenheiros, professores, artistas, pesquisadores, terapeutas, designers.

Após o onboarding, você pode querer personalizar ainda mais.

## Adicionando Skills Específicas do Domínio

Cada estágio gera artefatos que podem ser empacotados como skills reutilizáveis:

```bash
# Exemplo: salvar um skill específico para escritor após o Estágio 4
hermes skill create writer-workflow
```

O skill pode incluir:
- Prompts personalizados para suas tarefas comuns
- Consultas pré-construídas contra suas tabelas de domínio
- Modelos para padrões de trabalho recorrentes

## Editando Suas Preferências

Suas preferências são armazenadas em `user_preferences`. Para atualizar:

```bash
# Via API REST do Supabase
source ~/.hermes/secrets.env
curl -s -X PATCH "$SUPABASE_URL/rest/v1/user_preferences" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPAB...KEY" \
  -H "Content-Type: application/json" \
  -d '{"preferred_tone": "casual", "autonomy_level": 5}'
```

Ou apenas diga ao seu agente: "Seja mais casual" — ele atualiza a preferência.

## Adicionando Novas Tabelas de Domínio

Após o onboarding, você pode continuar adicionando tabelas:

```bash
# O agente pode gerar novas tabelas sob demanda
hermes --skills agent-onboarding
# → "Adicione uma tabela 'publishing_contracts' com nome, editora, data_inicio, percentual_royalty"
```

## Compartilhando Sua Configuração

As tabelas `user_profiles`, `user_preferences` e `user_mbti` podem ser exportadas como um perfil JSON:

```bash
source ~/.hermes/secrets.env
curl -s "$SUPABASE_URL/rest/v1/user_profiles" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
  -H "Authorization: Bearer $SUPAB...KEY" > meu-perfil.json
```

Isso permite que o agente seja configurado em uma nova máquina com suas preferências existentes.

## Exemplos de Domínios

### Escritor (ficção, não-ficção, poesia)

Tabelas de domínio geradas pelo Estágio 4:
- **personagens** — nome, idade, personalidade, arco, relacionamentos
- **obras** — título, tipo, sinopse, contagem_palavras, status
- **submissões** — obra_id, editora, status, data_envio, resposta
- **editoras** — nome, contato, gêneros, tempo_resposta
- **capítulos** — obra_id, número, título, contagem_palavras, status

### Professor (K-12, universidade, workshops)

Tabelas de domínio geradas pelo Estágio 4:
- **turmas** — nome, nível, horário, quantidade_alunos
- **alunos** — nome, email, desempenho, observações
- **aulas** — turma_id, data, tópico, materiais
- **avaliações** — turma_id, tipo, peso, data
- **curriculo** — disciplina, série, tópicos, padrões

### Engenheiro (firmware, hardware, software)

Tabelas de domínio geradas pelo Estágio 4:
- **projetos** — nome, plataforma, status, repositório
- **componentes** — sku, nome, especificações, url_datasheet
- **boms** — projeto_id, componente_id, quantidade, fornecedor
- **clientes** — nome, empresa, projeto, contato
- **versões** — projeto_id, versão, changelog, data_lancamento

## Configuração Multi-Usuário

O meta-skill de onboarding atualmente suporta um usuário por projeto Supabase.
Para múltiplos usuários (ex: família, pequena equipe):

1. Cada tabela `user_*` tem uma chave estrangeira `profile_id`
2. Múltiplos perfis podem coexistir
3. O agente verifica `onboarding_completed = true` antes de pular o onboarding

Para trocar de usuário: crie uma nova linha em `user_profiles` e reinicie o estágio a partir dali.
