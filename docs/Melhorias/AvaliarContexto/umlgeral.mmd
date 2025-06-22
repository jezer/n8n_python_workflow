sequenceDiagram
  %% Definição de participantes
  participant Usuario
  participant armazenamento as "Whats/Google/Drive"
  participant Critico as "Python CriticoInformacaoRecebida"
  participant Separador as "Python SeparadorDeContexto"
  participant Engine as "Python RAG/LLMs engine"
  participant bd as "BD Vetorial"

    loop Configurar IA
        %% Upload de Arquivos
        Usuario->>armazenamento: "Faz upload de arquivo(s) e instrução de objetivo"

        loop avaliar instrução
            %% Processamento Crítico
            %% validar se há erros: falta o fim, existe regras contraditorias, o fluxo não esclarece se o contexto é um individuo, local, uma entidade, uma diciplina
            Critico->>armazenamento: "REJEITAR: Foi encontrado erros"
            Note right of Critico: IA: Avaliar contradições e regras de fidelidade/equilíbrio\nRejeitar se houver conflitos
            armazenamento->>Critico: "Envia arquivos e instruções"
            Critico->>Separador: "Encaminha texto validado"
        end
        

        %% Separação de Contextos
        Note left of Separador: IA: Extrair contextos por entidade\n(Indivíduo, Quiosque, Associação, etc.)
        Separador->>bd: "Armazenar contextos vinculados ao usuário"

        %% RAG e Resposta
        Engine->>bd: "Buscar vetores relevantes"
        bd-->>Engine: "Retorna itens vetoriais"
        Engine-->>Usuario: "Gera resposta fundamentada"
    end
        Usuario->>Engine: "Consulta usando contexto armazenado"