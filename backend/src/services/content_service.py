import logging
from typing import List, Optional
from uuid import uuid4
from datetime import datetime, timedelta

# Try to import fastembed, use fallback if not available
try:
    from fastembed import TextEmbedding
    FASTEMBED_AVAILABLE = True
except ImportError:
    FASTEMBED_AVAILABLE = False
    TextEmbedding = None

from qdrant_client import QdrantClient
from qdrant_client.http import models

from ..models import ContentChunk
from ..config import settings


logger = logging.getLogger(__name__)


class ContentIndexingService:
    def __init__(self):
        if FASTEMBED_AVAILABLE:
            self.embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        else:
            logger.warning("fastembed not available, using mock embeddings")
            self.embedding_model = None

        self.qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=True
        )
        self.collection_name = settings.qdrant_collection_name
        self._init_collection()

    def _init_collection(self):
        """Initialize the Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            self.qdrant_client.get_collection(self.collection_name)
            logger.info(f"Collection '{self.collection_name}' already exists")
        except:
            # Create collection with 384-dimensional vectors
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )
            logger.info(f"Created collection '{self.collection_name}' with 384-dim vectors")

    def chunk_text(self, text: str, chunk_size: int = 500, overlap_size: int = 50) -> List[str]:
        """
        Split text into chunks of specified size with overlap
        """
        # Simple word-based chunking
        words = text.split()
        chunks = []

        start_idx = 0
        while start_idx < len(words):
            end_idx = start_idx + chunk_size
            chunk_words = words[start_idx:end_idx]
            chunk = " ".join(chunk_words)
            chunks.append(chunk)

            # Move start index by chunk_size - overlap_size to create overlap
            start_idx = end_idx - overlap_size
            if start_idx >= len(words):
                # If we've reached the end, make sure we include the last part
                break

        # If the last chunk is too small, merge it with the previous one if possible
        if len(chunks) > 1 and len(chunks[-1].split()) < chunk_size // 2:
            chunks[-2] += " " + chunks[-1]
            chunks = chunks[:-1]

        return chunks

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts using FastEmbed
        """
        if not FASTEMBED_AVAILABLE or self.embedding_model is None:
            # Return mock embeddings for testing purposes
            logger.warning("Using mock embeddings instead of real embeddings")
            embeddings = []
            for _ in texts:
                # Generate a 384-dimensional random vector as mock embedding
                # Using a simple approach without numpy to avoid additional dependencies
                import random
                mock_embedding = [random.random() for _ in range(384)]
                embeddings.append(mock_embedding)
            return embeddings

        embeddings = []
        for embedding in self.embedding_model.embed(texts):
            embeddings.append(embedding.tolist())
        return embeddings

    def index_content(self, content_chunks: List[ContentChunk]) -> dict:
        """
        Index content chunks in Qdrant with embeddings
        """
        successful_count = 0
        error_count = 0
        errors = []

        # Prepare points for batch insertion
        points = []
        for chunk in content_chunks:
            try:
                # Generate embedding for the content
                embeddings = self.generate_embeddings([chunk.content])
                if embeddings and len(embeddings) > 0:
                    embedding = embeddings[0]
                else:
                    raise Exception(f"Failed to generate embedding for chunk: {chunk.id}")

                # Create Qdrant point
                point = models.PointStruct(
                    id=chunk.id,
                    vector=embedding,
                    payload={
                        "content": chunk.content,
                        "chapter": chunk.chapter,
                        "lesson": chunk.lesson,
                        "section": chunk.section,
                        "url": chunk.url,
                        "created_at": datetime.now().isoformat()
                    }
                )
                points.append(point)
                successful_count += 1
            except Exception as e:
                error_count += 1
                errors.append(f"Error indexing chunk {chunk.id}: {str(e)}")
                logger.error(f"Error indexing chunk {chunk.id}: {str(e)}")

        # Batch insert points into Qdrant
        if points:
            try:
                self.qdrant_client.upsert(
                    collection_name=self.collection_name,
                    points=points
                )
                logger.info(f"Successfully indexed {successful_count} content chunks")
            except Exception as e:
                error_count += len(points)
                errors.append(f"Error during batch insert: {str(e)}")
                logger.error(f"Error during batch insert: {str(e)}")

        return {
            "success": error_count == 0,
            "indexed_count": successful_count,
            "error_count": error_count,
            "errors": errors
        }

    def index_single_content(self, content: str, chapter: str, lesson: str, url: str, section: Optional[str] = None) -> str:
        """
        Index a single piece of content by chunking it and storing in Qdrant
        """
        # Generate a unique ID for this content
        content_id = str(uuid4())

        # Chunk the content
        chunks = self.chunk_text(content)

        # Create ContentChunk objects
        content_chunks = []
        for i, chunk_text in enumerate(chunks):
            chunk_id = f"{content_id}_chunk_{i}"
            chunk = ContentChunk(
                id=chunk_id,
                content=chunk_text,
                chapter=chapter,
                lesson=lesson,
                section=section,
                url=url
            )
            content_chunks.append(chunk)

        # Index all chunks
        result = self.index_content(content_chunks)

        if result["success"]:
            logger.info(f"Successfully indexed content {content_id} with {len(chunks)} chunks")
            return content_id
        else:
            logger.error(f"Failed to index content {content_id}: {result['errors']}")
            raise Exception(f"Failed to index content: {result['errors']}")