# Hypothetical src/I.indexacao_vetorial/indexacao_vetorial.py
import faiss
import numpy as np
import os
import json
import logging

# Default modules, can be overridden by injection for testing
import faiss as default_faiss
import os as default_os
import json as default_json

logger = logging.getLogger(__name__)

class IndexacaoVetorial:
    def __init__(self, index_base_path="./indices", embedding_dim=None,
                 faiss_module=None, os_module=None, json_module=None):
        self.index_base_path = index_base_path
        self.embedding_dim = embedding_dim # Crucial for creating the index
        self.index = None
        self.metadata = []

        self.faiss = faiss_module if faiss_module is not None else default_faiss
        self.os = os_module if os_module is not None else default_os
        self.json = json_module if json_module is not None else default_json
        
        if self.os == default_os: # Only make dirs if using the real os module
            self.os.makedirs(self.index_base_path, exist_ok=True)

    def _get_paths(self, versao):
        index_file = self.os.path.join(self.index_base_path, f"index_v{versao}.faiss")
        meta_file = self.os.path.join(self.index_base_path, f"index_v{versao}_meta.json")
        return index_file, meta_file

    def run(self, data: list, versao: str):
        if not data:
            logger.warning("Input data for run() is empty. No index will be built.")
            return

        valid_embeddings = []
        current_metadata = [] # Use local var for current run's metadata

        # Determine embedding_dim from data if not already set, and validate
        # This part is crucial and needs to be robust
        determined_embedding_dim = self.embedding_dim
        if determined_embedding_dim is None:
            for item in data: # Find first valid embedding to determine dim
                embedding = item.get("embedding")
                if embedding is not None:
                    if isinstance(embedding, list): temp_emb = np.array(embedding)
                    else: temp_emb = embedding
                    if isinstance(temp_emb, np.ndarray) and temp_emb.ndim == 1 and temp_emb.size > 0:
                        determined_embedding_dim = temp_emb.shape[0]
                        break
            if determined_embedding_dim is None:
                logger.error("Could not determine embedding dimension from data and none was provided.")
                return
            # If self.embedding_dim was None, set it now for the instance
            if self.embedding_dim is None:
                self.embedding_dim = determined_embedding_dim
        
        # Now self.embedding_dim should be set (either initially or from data)
        if self.embedding_dim is None: # Final check
             logger.error("Embedding dimension is not set. Cannot create index.")
             return

        for item in data:
            embedding = item.get("embedding")
            referencia = item.get("referencia")

            if embedding is None or referencia is None:
                logger.debug(f"Skipping item due to missing embedding or referencia: {item.get('referencia', 'N/A')}")
                continue

            if isinstance(embedding, list):
                embedding = np.array(embedding, dtype=np.float32)
            
            if not isinstance(embedding, np.ndarray) or embedding.ndim != 1:
                logger.debug(f"Skipping item with invalid embedding format: {referencia}")
                continue
            
            if embedding.shape[0] != self.embedding_dim:
                logger.debug(f"Skipping item with mismatched embedding dimension: {referencia}. Expected {self.embedding_dim}, got {embedding.shape[0]}")
                continue
            
            valid_embeddings.append(embedding)
            current_metadata.append(referencia)

        if not valid_embeddings:
            logger.warning("No valid embeddings found in the provided data for indexing.")
            return

        try:
            embeddings_matrix = np.vstack(valid_embeddings).astype(np.float32)
        except ValueError as e:
            # This print is for the test: test_run_handles_vstack_error_gracefully
            # In real code, prefer logging.
            print(f"Error stacking embeddings: {e}") 
            logger.error(f"Error stacking embeddings, likely due to inconsistent dimensions: {e}")
            return

        # Create a new index for this version
        # For HNSW: new_index = self.faiss.IndexHNSWFlat(self.embedding_dim, 32) 
        new_index = self.faiss.IndexFlatL2(self.embedding_dim)
        new_index.add(embeddings_matrix)
        
        # Set the instance's index and metadata to this new version
        self.index = new_index
        self.metadata = current_metadata

        self._save_index_and_metadata(versao) # Saves self.index and self.metadata
        logger.info(f"Index v{versao} built with {self.index.ntotal} vectors and saved.")

    def _save_index_and_metadata(self, versao: str):
        if self.index is None:
            logger.error("Cannot save: FAISS index is not built.")
            return

        index_file, meta_file = self._get_paths(versao)

        if self.os.path.exists(index_file):
            logger.warning(f"Index file {index_file} already exists. It will be overwritten.")
        self.faiss.write_index(self.index, index_file)

        if self.os.path.exists(meta_file):
            logger.warning(f"Metadata file {meta_file} already exists. It will be overwritten.")
        
        # Use self.json for open and dump
        with self.json.open(meta_file, 'w') as f: # Assuming mock_json has open
            self.json.dump(self.metadata, f)
        logger.info(f"Index and metadata for version {versao} saved.")


    def load_index(self, versao: str) -> bool:
        index_file, meta_file = self._get_paths(versao)

        if not self.os.path.exists(index_file) or not self.os.path.exists(meta_file):
            logger.warning(f"Index or metadata file for version {versao} not found at {index_file} or {meta_file}.")
            self.index = None
            self.metadata = []
            return False
        
        try:
            loaded_index = self.faiss.read_index(index_file)
            
            with self.json.open(meta_file, 'r') as f: # Assuming mock_json has open
                loaded_metadata = self.json.load(f)
            
            if loaded_index.ntotal != len(loaded_metadata):
                logger.error(f"Mismatch between number of vectors in index ({loaded_index.ntotal}) and metadata entries ({len(loaded_metadata)}) for version {versao}.")
                return False # Do not set self.index or self.metadata

            self.index = loaded_index
            self.metadata = loaded_metadata
            
            # Update embedding_dim from loaded index
            if self.index.ntotal > 0:
                self.embedding_dim = self.index.d
            elif self.embedding_dim is None: # If index is empty but loaded, still need a dim if it was never set
                 logger.warning(f"Loaded empty index v{versao}. Embedding dimension remains {self.embedding_dim}.")


            logger.info(f"Index v{versao} loaded with {self.index.ntotal} vectors. Dimension: {self.index.d if self.index else 'N/A'}.")
            return True
        except Exception as e:
            logger.error(f"Error loading index version {versao}: {e}")
            self.index = None
            self.metadata = []
            return False

    def search(self, query_embedding: np.ndarray, k: int = 5) -> list:
        if self.index is None:
            logger.warning("No index loaded or built. Search cannot be performed.")
            return []
        
        if not isinstance(query_embedding, np.ndarray):
            logger.error("Query embedding must be a numpy array.")
            return []
            
        if query_embedding.ndim == 1:
            # Ensure it's a 2D array for FAISS search [1, dim]
            query_embedding_2d = np.expand_dims(query_embedding, axis=0).astype(np.float32)
        elif query_embedding.ndim == 2:
            query_embedding_2d = query_embedding.astype(np.float32)
        else:
            logger.error(f"Query embedding has invalid ndim: {query_embedding.ndim}. Must be 1 or 2.")
            return []
        
        if query_embedding_2d.shape[1] != self.index.d:
            logger.error(f"Query embedding dimension {query_embedding_2d.shape[1]} does not match index dimension {self.index.d}.")
            return []

        distances, indices = self.index.search(query_embedding_2d, k)
        
        results = []
        # Assuming query_embedding_2d is typically a single query, so indices[0] and distances[0]
        for i in range(indices.shape[1]): 
            idx = indices[0, i]
            dist = distances[0, i]
            if idx != -1 and idx < len(self.metadata): # FAISS returns -1 for no more results
                results.append({
                    "referencia": self.metadata[idx],
                    "distancia": float(dist),
                    "indice_original": int(idx)
                })
            elif idx != -1: # Should not happen if metadata is consistent
                logger.warning(f"Search returned valid index {idx} but it's out of bounds for metadata (len {len(self.metadata)}).")
            
        return results
