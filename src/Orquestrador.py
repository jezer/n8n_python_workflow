from persistencia_supabase import PersistenciaSupabase

class PipelineOrquestrador:
    def __init__(self, caminho_pasta):
        self.caminho_pasta = caminho_pasta
        self.db = PersistenciaSupabase()
        self._criar_tabelas()
        self.resultados = {}

    def _criar_tabelas(self):
        tabelas_sql = [
            """
            create table if not exists triplas_grafo (
                id serial primary key,
                sujeito text,
                predicado text,
                objeto text,
                data timestamp with time zone default now()
            );
            """,
            """
            create table if not exists metadados_enriquecidos (
                id serial primary key,
                entidade text,
                tipo text,
                documento_id text,
                data timestamp with time zone default now()
            );
            """,
            """
            create table if not exists qa_gerado (
                id serial primary key,
                pergunta text,
                resposta text,
                tripla_relacionada jsonb,
                data timestamp with time zone default now()
            );
            """,
            """
            create table if not exists embeddings (
                id serial primary key,
                embedding float8[],
                referencia text,
                data timestamp with time zone default now()
            );
            """,
            """
            create table if not exists avaliacoes (
                id serial primary key,
                pergunta text,
                resposta text,
                score float8,
                feedback text,
                avaliacao_automatica jsonb,
                avaliacao_llm_judge text,
                avaliacao_humana text,
                data timestamp with time zone default now()
            );
            """
        ]
        for sql in tabelas_sql:
            self.db.criar_tabela(sql)

    def rodar(self):
        # Exemplo de uso do pipeline, adaptando as etapas conforme seu main.py
        self.resultados['ingestao'] = etapa_ingestao(self.caminho_pasta)
        self.resultados['segmentacao'] = etapa_segmentacao(self.resultados['ingestao'])
        self.resultados['limpeza'] = etapa_limpeza(self.resultados['segmentacao'])
        self.resultados['chunking'] = etapa_chunking(self.resultados['limpeza'])
        self.resultados['classificacao'] = etapa_classificacao(self.resultados['chunking'])
        self.resultados['grafo'] = etapa_grafo_conhecimento(self.resultados['classificacao'])
        # Persistência de triplas
        for s, p, o in self.resultados['grafo']:
            self.db.inserir("triplas_grafo", {"sujeito": str(s), "predicado": str(p), "objeto": str(o)})

        self.resultados['qa'] = etapa_geracao_qa(self.resultados['grafo'])
        for item in self.resultados['qa']:
            self.db.inserir("qa_gerado", {
                "pergunta": item.get("pergunta_gerada"),
                "resposta": item.get("resposta_gerada"),
                "tripla_relacionada": item.get("tripla"),
            })

        self.resultados['embeddings'] = etapa_embeddings(self.resultados['qa'])
        for item in self.resultados['embeddings']:
            self.db.inserir("embeddings", {
                "embedding": list(item.get("embedding")),
                "referencia": item.get("pergunta_gerada") or item.get("resposta_gerada"),
            })

        self.resultados['indexados'] = etapa_indexacao(self.resultados['embeddings'])
        self.resultados['metadados'] = etapa_metadados(self.resultados['indexados'], grafo=self.resultados['grafo'])
        for doc in self.resultados['metadados']:
            for m in doc.get("metadados", []):
                self.db.inserir("metadados_enriquecidos", {
                    "entidade": m["texto"],
                    "tipo": m["label"],
                    "documento_id": doc.get("id") or doc.get("nome_arquivo") or None
                })

        self.resultados['retriever'] = etapa_hybrid_retriever(self.resultados['metadados'], self.resultados['qa'])
        self.resultados['reranking'] = etapa_reranking(self.resultados['retriever'])
        self.resultados['llmrag'] = etapa_llm_rag(self.resultados['reranking'])
        referencias = [qa.get("referencia") for qa in self.resultados['qa']] if self.resultados['qa'] and "referencia" in self.resultados['qa'][0] else None
        self.resultados['avaliacao'] = etapa_avaliacao(self.resultados['llmrag'], referencias=referencias)
        for item in self.resultados['avaliacao']:
            self.db.inserir("avaliacoes", {
                "pergunta": item.get("query"),
                "resposta": item.get("resposta"),
                "score": item.get("avaliacao_automatica", {}).get("rougeL"),
                "feedback": item.get("avaliacao_llm_judge"),
                "avaliacao_automatica": item.get("avaliacao_automatica"),
                "avaliacao_llm_judge": item.get("avaliacao_llm_judge"),
                "avaliacao_humana": item.get("avaliacao_humana"),
            })

        # Continue com as demais etapas normalmente...
        self.resultados['retriever_adaptativo'] = etapa_retriever_adaptativo(self.resultados['avaliacao'])
        self.resultados['atualizacao'] = etapa_atualizacao_incremental(self.resultados['retriever_adaptativo'], self.resultados['embeddings'], self.resultados['qa'])
        self.resultados['otimizacao'] = etapa_otimizacao_prompts(self.resultados['avaliacao'], metodo="ab_test")
        etapa_dashboard(self.resultados['avaliacao'])
        etapa_alertas()
        print("\nPipeline finalizado com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_da_pasta>")
        sys.exit(1)
    caminho_pasta = sys.argv[1]
    print(f"Iniciando pipeline de ingestão na pasta: {caminho_pasta}\n")
    pipeline = PipelineOrquestrador(caminho_pasta)
    pipeline.rodar()