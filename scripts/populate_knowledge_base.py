"""ETL script to build and persist FAISS knowledge base index."""
import json
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Add parent directory to path to import src modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def load_documents_from_json(knowledge_dir: Path) -> list[dict]:
    """Load all documents from JSON files in knowledge directory.

    Args:
        knowledge_dir: Path to directory containing category JSON files

    Returns:
        List of all documents across categories
    """
    all_documents = []
    category_files = ["billing.json", "technical.json", "account.json", "general.json"]

    for category_file in category_files:
        file_path = knowledge_dir / category_file
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            continue

        try:
            with open(file_path, 'r') as f:
                documents = json.load(f)
                all_documents.extend(documents)
                logger.info(f"Loaded {len(documents)} documents from {category_file}")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {category_file}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading {category_file}: {e}")
            raise

    logger.info(f"✓ Loaded {len(all_documents)} total documents")
    return all_documents


def build_faiss_index(documents: list[dict], output_dir: Path) -> None:
    """Build FAISS index from documents and save to disk.

    Args:
        documents: List of document dictionaries
        output_dir: Path to save FAISS index and metadata
    """
    try:
        import faiss
        from langchain_huggingface import HuggingFaceEmbeddings
    except ImportError as e:
        logger.error(f"Required packages not installed: {e}")
        logger.error("Install with: pip install faiss-cpu sentence-transformers langchain-huggingface")
        sys.exit(1)

    logger.info("Initializing HuggingFace embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    )

    # Extract document texts for embedding
    texts = [doc["content"] for doc in documents]

    logger.info(f"Embedding {len(texts)} documents (this may take a moment)...")
    embeddings_array = embeddings.embed_documents(texts)

    # Convert to numpy array
    embeddings_array = np.array(embeddings_array).astype('float32')

    # Create FAISS index
    logger.info(f"Building FAISS index with dimension {embeddings_array.shape[1]}...")
    index = faiss.IndexFlatL2(embeddings_array.shape[1])
    index.add(embeddings_array)

    # Save index to disk
    output_dir.mkdir(parents=True, exist_ok=True)
    index_path = output_dir / "index.faiss"
    faiss.write_index(index, str(index_path))
    logger.info(f"✓ Saved FAISS index to {index_path}")

    # Save metadata to disk
    metadata = {
        "documents": documents,
        "doc_ids": [doc["id"] for doc in documents],
        "total_documents": len(documents),
        "embedding_model": "all-MiniLM-L6-v2",
    }

    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"✓ Saved metadata to {metadata_path}")

    logger.info(f"✓ Knowledge base ETL complete: {len(documents)} documents indexed")


def main():
    """Main ETL pipeline."""
    logger.info("=" * 60)
    logger.info("Knowledge Base ETL Pipeline")
    logger.info("=" * 60)

    # Define paths
    project_root = Path(__file__).parent.parent
    knowledge_dir = project_root / "data" / "knowledge"
    faiss_dir = project_root / "data" / "faiss_index"

    # Validate knowledge directory exists
    if not knowledge_dir.exists():
        logger.error(f"Knowledge directory not found: {knowledge_dir}")
        logger.error("Run: mkdir -p data/knowledge")
        sys.exit(1)

    # Load documents
    logger.info(f"Loading documents from {knowledge_dir}")
    documents = load_documents_from_json(knowledge_dir)

    if not documents:
        logger.error("No documents loaded. Check that JSON files exist in data/knowledge/")
        sys.exit(1)

    # Build and save FAISS index
    logger.info(f"Building FAISS index and saving to {faiss_dir}")
    build_faiss_index(documents, faiss_dir)

    logger.info("=" * 60)
    logger.info("✓ ETL pipeline completed successfully")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
