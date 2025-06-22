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

    resultados = etapa_ingestao(caminho_pasta)
    resultados_segmentados = etapa_segmentacao(resultados)
    resultados_limpos = etapa_limpeza(resultados_segmentados)
    resultados_chunking = etapa_chunking(resultados_limpos)
    resultados_classificados = etapa_classificacao(resultados_chunking)
    resultados_grafo = etapa_grafo_conhecimento(resultados_classificados)
    resultados_qa = etapa_geracao_qa(resultados_grafo)
    resultados_embeddings = etapa_embeddings(resultados_qa)
    
    print("\nPipeline finalizado com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_da_pasta>")
        sys.exit(1)
    caminho_pasta = sys.argv[1]
    print(f"Iniciando pipeline de ingestão na pasta: {caminho_pasta}\n")
    pipeline = PipelineOrquestrador(caminho_pasta)
    pipeline.rodar()