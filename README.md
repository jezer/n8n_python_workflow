# n8n_python_workflow README.md

# n8n Python Workflow

This project implements a comprehensive workflow for processing text data using various AI techniques. The workflow is structured into multiple modules, each responsible for a specific aspect of the data processing pipeline.

## Project Structure

The project is organized into the following folders:

- **A.Ingestao**: Implementation for the ingestion of files, including necessary scripts or modules.
- **B.Segmentacao**: Handles the text segmentation logic, including relevant functions or classes.
- **C.Limpeza**: Focuses on data cleaning and normalization processes.
- **D.Chunking**: Implements the intelligent chunking of text.
- **E.Classificacao**: Contains the classification and tagging logic.
- **F.GrafoConhecimento**: Manages the construction of the knowledge graph.
- **G.GeracaoQA**: Handles the generation of question-answer pairs.
- **H.Embeddings**: Focuses on creating specialized embeddings.
- **I.Indexacao**: Implements vector indexing.
- **J.Metadados**: Manages enriched metadata generation.
- **K.HybridRetriever**: Implements the hybrid retrieval system.
- **L.Reranking**: Handles the reranking of results.
- **M.LLM_RAG**: Implements the RAG (Retrieval-Augmented Generation) logic.
- **N.Avaliacao**: Focuses on continuous evaluation processes.
- **O.RetrieverAdaptativo**: Manages the adaptive retriever logic.
- **P.AtualizacaoIncremental**: Handles incremental updates.
- **Q.OtimizacaoPrompts**: Focuses on prompt optimization.
- **R.Dashboard**: Implements the dashboard for monitoring.
- **S.SistemaAlertas**: Manages the alert system.

## Setup Instructions

1. **Clone the Repository**: 
   ```bash
   git clone <repository-url>
   cd n8n_python_workflow
   ```

2. **Install Dependencies**: 
   Ensure you have Python 3.7 or higher installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Compile the Library**: 
   Use the provided PowerShell script to compile the library and generate the wheel file:
   ```powershell
   .\compile_library.ps1
   ```

4. **Usage**: 
   After compiling, you can use the generated wheel file in your N8N workflows.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.