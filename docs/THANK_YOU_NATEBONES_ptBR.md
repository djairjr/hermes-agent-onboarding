# Carta de Agradecimento ao NateBJones

Caro Nate,

Estou devendo esta carta há algum tempo. Encontrei o OB1 há cerca de um mês, e ele mudou completamente minha forma de pensar sobre construção com agentes de IA.

Antes do OB1, eu enfrentava um problema fundamental: toda sessão com um agente de IA começa do zero. O modelo não lembra o que aprendeu sobre mim, que ferramentas construiu ou que erros cometeu. Eu tinha skills e prompts, mas nenhuma infraestrutura real — nada que persistisse significativamente entre conversas.

Seu padrão Edge Function + MCP foi a peça que faltava. A ideia de expor operações de banco de dados através de ferramentas MCP, apoiadas por Supabase Edge Functions, é enganosamente simples — mas desbloqueia algo enorme. Assim que entendi, passei o mês seguinte adaptando às minhas próprias necessidades, criando 13 servidores MCP HTTP, 283 snapshots de análise de código, um catálogo completo de produtos, um CRM, um banco de dados de escape rooms, ferramentas financeiras — basicamente todo meu fluxo de trabalho rodando através do agente.

Mais importante, isso me motivou a construir algo que eu não tinha visto ninguém fazer ainda: um meta-skill que faz o agente desenvolver sua própria identidade. A ideia é simples — o agente registra todo erro que comete com uma contramedida, lê-os de volta no início de cada sessão e ajusta seu comportamento. É uma camada de identidade persistente que funciona entre trocas de modelo e mudanças de provedor.

Transformei isso num projeto open-source chamado **Hermes Agent Onboarding** (github.com/djairjr/hermes-agent-onboarding). É um meta-skill de 6 estágios que pega uma instalação nova do Hermes Agent e a guia através da descoberta de quem é o usuário — sua personalidade (MBTI), seu modelo operacional de trabalho, suas finanças, sua ontologia de domínio — e então calibra o comportamento do agente para corresponder. Tudo construído sobre a fundação do OB1: Edge Functions, ferramentas MCP, Supabase como fonte única da verdade.

A parte mais surpreendente é que eu projetei isso para ajudar outros, não apenas a mim. Minha esposa é escritora, e vê-la lutar com o mesmo problema de perda de contexto com as próprias ferramentas me fez perceber que isso não é um problema de nicho — afeta qualquer um que trabalhe com um agente de IA, independentemente da área. Uma escritora precisa de ferramentas diferentes, estruturas de dados diferentes e um tom de agente diferente do que um engenheiro de firmware precisa. O processo de onboarding deve descobrir essas diferenças, não assumi-las.

Eu não teria chegado aqui sem o OB1. Seus vídeos no YouTube foram incrivelmente úteis também — ver alguém realmente construindo com essas coisas fez os conceitos clicarem mais rápido do que qualquer documentação poderia.

Obrigado por compartilhar seu trabalho tão abertamente. É raro encontrar um projeto que é ao mesmo tempo praticamente útil e filosoficamente inspirador. OB1 foi ambos para mim.

Melhores saudações,

Djair Guilherme
github.com/djairjr
