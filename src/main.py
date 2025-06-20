import sys
import logging
from A.ingestao_de_arquivos.ingestao import IngestaoDeArquivos
from B.segmentacao_segmentacao_de_texto import SegmentadorUnificado
from C.limpeza_normalizacao import LimpezaNormalizacao
from D.chunking_inteligente import ChunkingInteligente
from E.classificacao_tagging import ClassificacaoTagging
from F.grafo_conhecimento import GrafoConhecimento
from G.geracao_qa import GeracaoQA
from H.embeddings_especializados import EmbeddingsEspecializados
from I.indexacao_vetorial import IndexacaoVetorial
from J.metadados_enriquecidos import MetadadosEnriquecidos
from K.hybrid_retriever import HybridRetriever
from L.reranking_cross_encoder import RerankingCrossEncoder
from M.llm_com_rag import LLMcomRAG
from N.avaliacao_continua import AvaliacaoContinua
from O.retriever_adaptativo import RetrieverAdaptativo
from P.atualizacao_incremental import AtualizacaoIncremental
from Q.otimizacao_prompts import OtimizacaoPrompts
from R.dashboard_monitoramento import DashboardMonitoramento
from S.sistema_alertas import SistemaAlertas
from numpy import array, load
import json
import os
from supabase import create_client
from supabase_config import SUPABASE_URL, SUPABASE_KEY
from Orquestrador import PipelineOrquestrador


def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)
def salvar_no_supabase(tabela: str, dados: dict):
    supabase = get_supabase_client()
    resp = supabase.table(tabela).insert(dados).execute()
    return resp

def etapa_ingestao(caminho_pasta):
    ingestao = IngestaoDeArquivos(
        tesseract_path=None,
        output_path="./saida_markdown",
        log_level=logging.INFO,
        language="por",
        max_workers=4
    )
    return ingestao.process_directory(
        caminho_pasta,
        save_markdown=True,
        filter_ext=None,
        min_size=0,
        return_format="markdown"
    )

def etapa_segmentacao(resultados):
    segmentador = SegmentadorUnificado()
    resultados_segmentados = []
    for doc in resultados:
        segmentos = segmentador.segment(doc["conteudo"], method="auto")
        resultados_segmentados.append({
            "nome_arquivo": doc["nome_arquivo"],
            "segmentos": segmentos
        })
    return resultados_segmentados

def etapa_limpeza(resultados_segmentados):
    limpeza = LimpezaNormalizacao()
    return limpeza.run(resultados_segmentados)

def etapa_chunking(resultados_limpos):
    chunker = ChunkingInteligente()
    return chunker.run(resultados_limpos)

def etapa_classificacao(resultados_chunking):
    classificador = ClassificacaoTagging()
    return classificador.run(resultados_chunking)

def etapa_grafo_conhecimento(resultados_classificados):
    grafo = GrafoConhecimento()
    grafo_obj = grafo.run(resultados_classificados)
    grafo.exportar_rdf("grafo.rdf")
    # Salva cada tripla no Supabase
    for s, p, o in grafo_obj:
        registro = {
            "sujeito": str(s),
            "predicado": str(p),
            "objeto": str(o),
        }
        salvar_no_supabase("triplas_grafo", registro)
    return grafo_obj

def etapa_geracao_qa(resultados_grafo):
    qa = GeracaoQA()
    resultados = qa.run(resultados_grafo)
    # Salva cada QA no Supabase
    for item in resultados:
        registro = {
            "pergunta": item.get("pergunta_gerada"),
            "resposta": item.get("resposta_gerada"),
            "tripla_relacionada": item.get("tripla"),
        }
        salvar_no_supabase("qa_gerado", registro)
    return resultados

def etapa_embeddings(resultados_qa):
    embeddings = EmbeddingsEspecializados()
    resultados = embeddings.run(resultados_qa)
    # Salva cada embedding no Supabase
    for item in resultados:
        registro = {
            "embedding": list(item.get("embedding")),  # Converta np.ndarray para list
            "referencia": item.get("pergunta_gerada") or item.get("resposta_gerada"),
        }
        salvar_no_supabase("embeddings", registro)
    return resultados

def etapa_indexacao(resultados_embeddings):
    indexador = IndexacaoVetorial()
    indexador.run(resultados_embeddings, versao="001")
    return resultados_embeddings  # Mantém compatibilidade sequencial

def etapa_metadados(resultados_indexados, grafo=None):
    metadados = MetadadosEnriquecidos()
    return metadados.run(resultados_indexados, grafo=grafo)

def etapa_hybrid_retriever(resultados_metadados, perguntas_qa):
    documentos = [doc.get("conteudo") or doc.get("pergunta_gerada") or "" for doc in resultados_metadados]
    retriever = HybridRetriever()
    resultados = []
    for pergunta in perguntas_qa:
        query = pergunta.get("pergunta_gerada", "")
        if not query:
            continue
        resultado = retriever.retrieve(query, documentos, k=5)
        print(f"Query: {query}\nResultados HybridRetriever: {resultado}\n")
        resultados.append({"query": query, "resultados": resultado})
    return resultados

def etapa_reranking(resultados_retriever):
    reranker = RerankingCrossEncoder()
    return reranker.run(resultados_retriever)

def etapa_llm_rag(resultados_reranking):
    llmrag = LLMcomRAG()
    return llmrag.run(resultados_reranking)

def etapa_avaliacao(resultados_llmrag, referencias=None):
    avaliador = AvaliacaoContinua()
    resultados = avaliador.run(resultados_llmrag, referencias=referencias)
    # Salva cada avaliação no Supabase
    for item in resultados:
        registro = {
            "pergunta": item.get("query"),
            "resposta": item.get("resposta"),
            "score": item.get("avaliacao_automatica", {}).get("rougeL"),
            "feedback": item.get("avaliacao_llm_judge"),
            "avaliacao_automatica": item.get("avaliacao_automatica"),
            "avaliacao_llm_judge": item.get("avaliacao_llm_judge"),
            "avaliacao_humana": item.get("avaliacao_humana"),
        }
        salvar_no_supabase("avaliacoes", registro)
    return resultados

def etapa_retriever_adaptativo(resultados_avaliacao):
    retriever_adapt = RetrieverAdaptativo()
    return retriever_adapt.run(resultados_avaliacao)

def etapa_atualizacao_incremental(resultados_retriever_adaptativo, resultados_embeddings, resultados_qa):
    # Carrega embeddings antigos de arquivo versionado
    atualizador = AtualizacaoIncremental()
    embeddings_antigos = atualizador.carregar_embeddings("001")  # ou caminho/versão anterior

    # Novos embeddings da execução atual
    novos_dados = array([d["embedding"] for d in resultados_embeddings if "embedding" in d])

    # Consultas: perguntas geradas na etapa de QA
    consultas = array([qa.get("pergunta_gerada") for qa in resultados_qa if "pergunta_gerada" in qa])

    # Ground truth: índices ou ids dos documentos corretos (ajuste conforme seu dataset)
    ground_truth = ...  # Exemplo: array de índices ou ids

    versao_atual = "001"
    versao_nova = "002"
    return atualizador.run(
        embeddings_antigos,
        novos_dados,
        consultas=consultas,
        ground_truth=ground_truth,
        versao_atual=versao_atual,
        versao_nova=versao_nova
    )

def etapa_otimizacao_prompts(resultados_avaliacao, metodo="ab_test"):
    otimizador = OtimizacaoPrompts()
    return otimizador.run(resultados_avaliacao, metodo=metodo)

def etapa_dashboard(resultados_avaliacao, recall=None, historico_metricas=None):
    dashboard = DashboardMonitoramento()
    dashboard.run(resultados_avaliacao, recall=recall, historico_metricas=historico_metricas)

def etapa_alertas():
    # Carrega o relatório do dashboard gerado na etapa R
    relatorio_path = "./dashboard/relatorio_dashboard.json"
    if not os.path.exists(relatorio_path):
        print("Relatório do dashboard não encontrado. Nenhum alerta gerado.")
        return
    with open(relatorio_path, "r", encoding="utf-8") as f:
        relatorio_dashboard = json.load(f)
    alertas = SistemaAlertas(email_alerta=None).run(relatorio_dashboard)
    if alertas:
        print("Alertas gerados:")
        for alerta in alertas:
            print(alerta)
    else:
        print("Nenhum alerta gerado.")



def criar_tabela_triplas():
    supabase = get_supabase_client()
    sql = """
    create table if not exists triplas_grafo (
        id serial primary key,
        sujeito text,
        predicado text,
        objeto text,
        data timestamp with time zone default now()
    );
    """
    supabase.rpc("execute_sql", {"sql": sql}).execute()

def criar_tabela_metadados():
    supabase = get_supabase_client()
    sql = """
    create table if not exists metadados_enriquecidos (
        id serial primary key,
        entidade text,
        tipo text,
        documento_id text,
        data timestamp with time zone default now()
    );
    """
    supabase.rpc("execute_sql", {"sql": sql}).execute()

def criar_tabela_qa_gerado():
    supabase = get_supabase_client()
    sql = """
    create table if not exists qa_gerado (
        id serial primary key,
        pergunta text,
        resposta text,
        tripla_relacionada jsonb,
        data timestamp with time zone default now()
    );
    """
    supabase.rpc("execute_sql", {"sql": sql}).execute()    

def criar_tabela_embeddings():
    supabase = get_supabase_client()
    sql = """
    create table if not exists embeddings (
        id serial primary key,
        embedding float8[],
        referencia text,
        data timestamp with time zone default now()
    );
    """
    supabase.rpc("execute_sql", {"sql": sql}).execute()

def criar_tabela_avaliacoes():
    supabase = get_supabase_client()
    sql = """
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
    supabase.rpc("execute_sql", {"sql": sql}).execute()



def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_da_pasta>")
        sys.exit(1)
    caminho_pasta = sys.argv[1]
    print(f"Iniciando pipeline de ingestão na pasta: {caminho_pasta}\n")
    
    criar_tabela_triplas()
    criar_tabela_metadados()
    criar_tabela_qa_gerado()
    criar_tabela_embeddings()
    criar_tabela_avaliacoes()

    resultados = etapa_ingestao(caminho_pasta)
    print(f"\nArquivos processados: {len(resultados)}")

    resultados_segmentados = etapa_segmentacao(resultados)
    print(f"\nArquivos segmentados: {len(resultados_segmentados)}")

    resultados_limpos = etapa_limpeza(resultados_segmentados)
    resultados_chunking = etapa_chunking(resultados_limpos)
    resultados_classificados = etapa_classificacao(resultados_chunking)
    resultados_grafo = etapa_grafo_conhecimento(resultados_classificados)
    resultados_qa = etapa_geracao_qa(resultados_grafo)
    resultados_embeddings = etapa_embeddings(resultados_qa)
    resultados_indexados = etapa_indexacao(resultados_embeddings)
    resultados_metadados = etapa_metadados(resultados_indexados, grafo=resultados_grafo)
    resultados_retriever = etapa_hybrid_retriever(resultados_metadados, resultados_qa)
    resultados_reranking = etapa_reranking(resultados_retriever)
    resultados_llmrag = etapa_llm_rag(resultados_reranking)
    # Extraia as referências das perguntas/respostas de QA, se existirem
    referencias = [qa.get("referencia") for qa in resultados_qa] if resultados_qa and "referencia" in resultados_qa[0] else None
    resultados_avaliacao = etapa_avaliacao(resultados_llmrag, referencias=referencias)
    resultados_retriever_adaptativo = etapa_retriever_adaptativo(resultados_avaliacao)
    resultados_atualizacao = etapa_atualizacao_incremental(resultados_retriever_adaptativo, resultados_embeddings, resultados_qa)
    resultados_otimizacao = etapa_otimizacao_prompts(resultados_avaliacao, metodo="ab_test")
    etapa_dashboard(resultados_avaliacao)
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