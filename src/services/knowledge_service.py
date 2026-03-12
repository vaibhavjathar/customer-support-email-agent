"""Knowledge base service with FAISS RAG pipeline (with graceful fallback)."""
import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Flag to track if FAISS is available
HAS_FAISS = False
FAISS_ERROR = None

try:
    import faiss
    from langchain_huggingface import HuggingFaceEmbeddings
    HAS_FAISS = True
except ImportError as e:
    FAISS_ERROR = str(e)
    logger.warning(f"FAISS unavailable, using keyword search: {e}")


class KnowledgeService:
    """Service for managing and retrieving knowledge base using FAISS vector store (with fallback)."""

    def __init__(self):
        """Initialize knowledge service by loading pre-built FAISS index from disk or falling back to JSON."""
        self.documents = []
        self.index = None
        self.doc_ids = []
        self.embeddings = None
        self.use_faiss = False

        # Try to load pre-built FAISS index from disk
        if HAS_FAISS:
            try:
                self._load_faiss_from_disk()
                self.use_faiss = True
                logger.info("✓ FAISS index loaded from disk")
            except Exception as e:
                logger.warning(f"FAISS index not found or load failed, falling back to keyword search: {e}")
                self.use_faiss = False
                self._load_documents_from_json()
        else:
            logger.info("Using keyword search (FAISS not available)")
            self._load_documents_from_json()

    def _load_documents_from_json(self) -> None:
        """Load documents from JSON files in data/knowledge/ directory."""
        try:
            project_root = Path(__file__).parent.parent.parent
            knowledge_dir = project_root / "data" / "knowledge"

            if not knowledge_dir.exists():
                logger.warning(f"Knowledge directory not found: {knowledge_dir}")
                return

            category_files = ["billing.json", "technical.json", "account.json", "general.json"]

            for category_file in category_files:
                file_path = knowledge_dir / category_file
                if not file_path.exists():
                    logger.warning(f"File not found: {file_path}")
                    continue

                with open(file_path, 'r') as f:
                    documents = json.load(f)
                    self.documents.extend(documents)
                    logger.info(f"Loaded {len(documents)} documents from {category_file}")

            logger.info(f"✓ Loaded {len(self.documents)} documents from JSON files")
        except Exception as e:
            logger.error(f"Error loading documents from JSON: {str(e)}")
            raise

    def _load_faiss_from_disk(self) -> None:
        """Load pre-built FAISS index from disk."""
        try:
            import faiss

            project_root = Path(__file__).parent.parent.parent
            faiss_dir = project_root / "data" / "faiss_index"

            index_path = faiss_dir / "index.faiss"
            metadata_path = faiss_dir / "metadata.json"

            if not index_path.exists() or not metadata_path.exists():
                raise FileNotFoundError(f"FAISS index not found at {faiss_dir}")

            # Load FAISS index
            self.index = faiss.read_index(str(index_path))
            logger.info(f"Loaded FAISS index from {index_path}")

            # Load metadata
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                self.documents = metadata.get("documents", [])
                self.doc_ids = metadata.get("doc_ids", [])

            logger.info(f"✓ Loaded {len(self.documents)} documents from metadata")
        except Exception as e:
            logger.error(f"Error loading FAISS index from disk: {str(e)}")
            raise

    def _keyword_search(self, query: str, category: Optional[str] = None, top_k: int = 3) -> list[dict]:
        """Fallback keyword-based search when FAISS is unavailable."""
        results = []
        query_lower = query.lower()

        for doc in self.documents:
            # Filter by category if specified
            if category and doc["category"] != category:
                continue

            # Simple keyword matching
            score = 0
            if query_lower in doc["title"].lower():
                score += 2
            if query_lower in doc["content"].lower():
                score += 1
            if any(query_lower in tag.lower() for tag in doc.get("tags", [])):
                score += 1

            if score > 0:
                results.append((score, doc))

        # Sort by score and return top_k
        results.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in results[:top_k]]

    def search_knowledge_base(
        self, query: str, category: Optional[str] = None, top_k: int = 3
    ) -> list[dict]:
        """Search knowledge base using FAISS vector similarity or keyword fallback.

        Args:
            query: Search query
            category: Optional category filter
            top_k: Number of results to return

        Returns:
            List of relevant document snippets
        """
        try:
            if self.use_faiss and self.index:
                # Use FAISS vector search
                query_embedding = self.embeddings.embed_query(query)

                import numpy as np
                query_array = np.array([query_embedding]).astype('float32')
                distances, indices = self.index.search(query_array, top_k * 2)

                results = []
                for idx in indices[0]:
                    if idx < len(self.documents):
                        doc = self.documents[idx]

                        if category and doc["category"] != category:
                            continue

                        results.append({
                            "id": doc["id"],
                            "title": doc["title"],
                            "content": doc["content"],
                            "category": doc["category"],
                        })

                        if len(results) >= top_k:
                            break

                logger.info(f"FAISS search for '{query}' returned {len(results)} results")
                return results
            else:
                # Fall back to keyword search
                docs = self._keyword_search(query, category, top_k)
                results = [
                    {
                        "id": doc["id"],
                        "title": doc["title"],
                        "content": doc["content"],
                        "category": doc["category"],
                    }
                    for doc in docs
                ]
                logger.info(f"Keyword search for '{query}' returned {len(results)} results")
                return results

        except Exception as e:
            logger.error(f"Error searching knowledge base: {str(e)}")
            return []

    def get_category_articles(self, category: str) -> list[dict]:
        """Get all articles for a specific category."""
        return [
            {
                "id": doc["id"],
                "title": doc["title"],
                "content": doc["content"],
                "category": doc["category"],
            }
            for doc in self.documents
            if doc["category"] == category
        ]

    def format_knowledge_context(self, articles: list[dict]) -> str:
        """Format articles for use in prompts."""
        if not articles:
            return ""

        formatted = "Relevant Knowledge Base Articles:\n"
        for article in articles:
            formatted += f"\n- {article['title']}\n  {article['content'][:250]}...\n"

        return formatted
