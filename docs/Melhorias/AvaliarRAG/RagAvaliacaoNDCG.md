# Instruções para Construção de Sistemas RAG em Python com Avaliação por NDCG

A seguir, apresento instruções detalhadas para implementar um sistema RAG (Retrieval-Augmented Generation) em Python, similar aos planos de vetorização mostrados, com foco na avaliação usando NDCG como critério principal para selecionar o melhor modelo.

## 1. Configuração Inicial

```python
# Importações básicas
import os
import numpy as np
from typing import List, Dict, Tuple
from sklearn.metrics import ndcg_score

# Configuração de ambiente
os.environ["OPENAI_API_KEY"] = "sua-chave-openai"
os.environ["VOYAGE_API_KEY"] = "sua-chave-voyage"  # Se for usar Voyage AI
```

## 2. Implementação dos Planos de Vetorização

```python
class RAGSystem:
    def __init__(self, model_name: str, chunk_size: int = 500, chunk_overlap: int = 50):
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.dimensions = self._get_model_dimensions()
        
    def _get_model_dimensions(self) -> int:
        """Retorna as dimensões do embedding baseado no modelo selecionado"""
        model_dimensions = {
            "OpenAI Ada v2": 1536,
            "Voyage AI 2": 1024,
            "OpenAI v3 Large": 3072,
            "OpenAI v3 Small": 1536
        }
        return model_dimensions.get(self.model_name, 1536)
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Obtém embeddings para uma lista de textos"""
        if "OpenAI" in self.model_name:
            from openai import OpenAI
            client = OpenAI()
            model = self.model_name.lower().replace(" ", "-")
            response = client.embeddings.create(input=texts, model=model)
            return np.array([e.embedding for e in response.data])
        
        elif "Voyage" in self.model_name:
            import voyageai
            vo = voyageai.Client()
            return np.array(vo.embed(texts, model="voyage-2").embeddings)
        
        raise ValueError(f"Modelo não suportado: {self.model_name}")
    
    def chunk_text(self, text: str) -> List[str]:
        """Divide o texto em chunks com sobreposição"""
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        return splitter.split_text(text)
    
    def evaluate_with_ndcg(self, queries: List[str], relevant_docs: List[List[str]], top_k: int = 5) -> float:
        """
        Avalia o sistema RAG usando NDCG
        
        Args:
            queries: Lista de perguntas de teste
            relevant_docs: Lista de listas contendo documentos relevantes para cada pergunta
            top_k: Número de documentos a serem recuperados
            
        Returns:
            Score NDCG médio
        """
        all_scores = []
        
        for query, rel_docs in zip(queries, relevant_docs):
            # Obter embedding da query
            query_embedding = self.get_embeddings([query])[0]
            
            # Obter embeddings dos documentos (simulando o índice)
            doc_embeddings = self.get_embeddings(rel_docs)
            
            # Calcular similaridade cosseno
            similarities = np.dot(doc_embeddings, query_embedding) / (
                np.linalg.norm(doc_embeddings, axis=1) * np.linalg.norm(query_embedding)
            )
            
            # Ordenar documentos por similaridade
            ranked_indices = np.argsort(similarities)[::-1]
            ranked_docs = [rel_docs[i] for i in ranked_indices]
            
            # Criar ground truth de relevância (assumindo que todos os docs fornecidos são relevantes)
            true_relevance = np.ones(len(rel_docs))
            
            # Calcular NDCG
            ndcg = ndcg_score([true_relevance], [similarities])
            all_scores.append(ndcg)
        
        return np.mean(all_scores)
```

## 3. Implementação do Processo de Avaliação Comparativa

```python
def compare_rag_models(pdf_text: str, test_queries: List[str], relevant_docs: List[List[str]]) -> Dict[str, float]:
    """
    Compara diferentes modelos RAG usando NDCG como métrica principal
    
    Args:
        pdf_text: Texto extraído do PDF
        test_queries: Lista de perguntas de teste
        relevant_docs: Lista de listas com documentos relevantes para cada pergunta
        
    Returns:
        Dicionário com scores NDCG para cada modelo
    """
    # Definir os planos de vetorização a serem testados
    vectorization_plans = [
        ("OpenAI Ada v2", 500, 50),
        ("Voyage AI 2", 500, 50),
        ("OpenAI v3 Large", 500, 50),
        ("OpenAI v3 Small", 500, 50)
    ]
    
    results = {}
    
    for model_name, chunk_size, chunk_overlap in vectorization_plans:
        print(f"\nAvaliando modelo: {model_name}")
        
        # Inicializar sistema RAG
        rag = RAGSystem(model_name, chunk_size, chunk_overlap)
        
        # Processar o texto do PDF (chunking)
        chunks = rag.chunk_text(pdf_text)
        
        # Avaliar com NDCG
        ndcg_score = rag.evaluate_with_ndcg(test_queries, relevant_docs)
        results[model_name] = ndcg_score
        
        print(f"NDCG score para {model_name}: {ndcg_score:.4f}")
    
    return results

def select_best_model(ndcg_scores: Dict[str, float]) -> Tuple[str, float]:
    """Seleciona o melhor modelo baseado no score NDCG"""
    best_model = max(ndcg_scores.items(), key=lambda x: x[1])
    print(f"\nMelhor modelo: {best_model[0]} com NDCG = {best_model[1]:.4f}")
    return best_model
```

## 4. Exemplo de Uso com os Dados Fornecidos

```python
# Exemplo de texto do PDF (substituir pelo conteúdo real)
pdf_text = """
[Conteúdo completo do PDF sobre melhorias no campo de futebol, 
renovação do espaço comunitário, detalhes da assembleia, etc.]
"""

# Perguntas de teste (adaptadas da imagem)
test_questions = [
    "What was the outcome of the votes regarding the proposed projects?",
    "What advantages does synthetic grass provide for the football field?",
    "What is the approximate cost for the renovation of the community event space?",
    "What specific projects were proposed for funding during the assembly?",
    # Adicionar outras perguntas relevantes
]

# Documentos relevantes para cada pergunta (simulado - deve ser adaptado)
relevant_documents = [
    ["Documento 1 contendo informação sobre votação", "Documento 2 com detalhes de votação"],
    ["Documento sobre vantagens da grama sintética", "Relatório técnico de campos"],
    ["Orçamento da renovação do espaço", "Minutas da assembleia com custos"],
    ["Lista de projetos propostos", "Ata da assembleia com projetos"],
    # Adicionar documentos relevantes para cada pergunta
]

# Executar comparação
ndcg_results = compare_rag_models(pdf_text, test_questions, relevant_documents)

# Selecionar melhor modelo
best_model, best_score = select_best_model(ndcg_results)
```

## 5. Instruções para Implementação Completa

1. **Pré-processamento do PDF**:
   - Use uma biblioteca como `PyPDF2` ou `pdfplumber` para extrair texto do PDF
   - Limpe o texto removendo cabeçalhos, rodapés e elementos não relevantes

2. **Configuração dos Modelos**:
   - Crie contas e obtenha chaves API para OpenAI e Voyage AI
   - Instale os pacotes necessários: `openai`, `voyageai`, `langchain`, `numpy`, `scikit-learn`

3. **Preparação dos Dados de Avaliação**:
   - Para cada pergunta no conjunto de teste, identifique os trechos do PDF que são relevantes
   - Crie uma lista de listas onde cada elemento interno contém os documentos relevantes para uma pergunta

4. **Execução da Avaliação**:
   - Execute o script de comparação para obter os scores NDCG
   - O modelo com maior NDCG deve ser selecionado como o melhor

5. **Otimização**:
   - Experimente com diferentes tamanhos de chunk e sobreposições
   - Considere adicionar outros modelos de embedding para comparação
   - Ajuste o parâmetro `top_k` conforme necessário para seu caso de uso

## 6. Interpretação dos Resultados

- O NDCG (Normalized Discounted Cumulative Gain) varia de 0 a 1, onde 1 representa a ordenação perfeita dos resultados
- Como mostrado na sua imagem, valores acima de 0.8 são considerados bons
- O modelo "OpenAI v3 Large" foi escolhido como melhor na sua avaliação, provavelmente por oferecer um bom equilíbrio entre recall (0.89) e relevância

Esta implementação permite reproduzir o processo de avaliação mostrado na imagem, com foco no NDCG como métrica principal para seleção do melhor modelo RAG.