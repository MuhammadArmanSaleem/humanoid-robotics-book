import logging
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.http import models

from ..models import ContentChunk, ChatMessage, ChatSession, Source
from ..config import settings


logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=True
        )
        self.collection_name = settings.qdrant_collection_name

    def search_content(self, query: str, top_k: int = 5, min_relevance: float = 0.3) -> List[ContentChunk]:
        """
        Search for relevant content chunks based on the query
        """
        try:
            # Search in Qdrant for similar content
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_text=query,  # Using text-based search
                limit=top_k,
                with_payload=True,
                with_vectors=False
            )

            # Filter results by relevance score and convert to ContentChunk
            relevant_chunks = []
            for result in search_results:
                if result.score >= min_relevance:
                    payload = result.payload
                    chunk = ContentChunk(
                        id=result.id,
                        content=payload.get("content", ""),
                        chapter=payload.get("chapter", ""),
                        lesson=payload.get("lesson", ""),
                        section=payload.get("section"),
                        url=payload.get("url", ""),
                        embedding=None  # We don't need the embedding in the response
                    )
                    relevant_chunks.append(chunk)

            logger.info(f"Found {len(relevant_chunks)} relevant chunks for query")
            return relevant_chunks

        except Exception as e:
            logger.error(f"Error searching content: {str(e)}")
            return []

    def search_content_by_metadata(self, chapter: Optional[str] = None, lesson: Optional[str] = None,
                                   top_k: int = 10) -> List[ContentChunk]:
        """
        Search content by metadata filters (chapter, lesson, etc.)
        """
        try:
            # Build filter conditions
            must_conditions = []
            if chapter:
                must_conditions.append(
                    models.FieldCondition(
                        key="chapter",
                        match=models.MatchValue(value=chapter)
                    )
                )
            if lesson:
                must_conditions.append(
                    models.FieldCondition(
                        key="lesson",
                        match=models.MatchValue(value=lesson)
                    )
                )

            if must_conditions:
                filter_conditions = models.Filter(must=must_conditions)
            else:
                filter_conditions = None

            # Search with filters
            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_filter=filter_conditions,
                limit=top_k,
                with_payload=True,
                with_vectors=False
            )

            # Convert results to ContentChunk
            chunks = []
            for result in search_results:
                payload = result.payload
                chunk = ContentChunk(
                    id=result.id,
                    content=payload.get("content", ""),
                    chapter=payload.get("chapter", ""),
                    lesson=payload.get("lesson", ""),
                    section=payload.get("section"),
                    url=payload.get("url", ""),
                    embedding=None
                )
                chunks.append(chunk)

            logger.info(f"Found {len(chunks)} chunks by metadata")
            return chunks

        except Exception as e:
            logger.error(f"Error searching content by metadata: {str(e)}")
            return []

    def get_content_by_url(self, url: str, top_k: int = 10) -> List[ContentChunk]:
        """
        Retrieve content chunks by URL
        """
        try:
            filter_conditions = models.Filter(
                must=[
                    models.FieldCondition(
                        key="url",
                        match=models.MatchValue(value=url)
                    )
                ]
            )

            search_results = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_filter=filter_conditions,
                limit=top_k,
                with_payload=True,
                with_vectors=False
            )

            chunks = []
            for result in search_results:
                payload = result.payload
                chunk = ContentChunk(
                    id=result.id,
                    content=payload.get("content", ""),
                    chapter=payload.get("chapter", ""),
                    lesson=payload.get("lesson", ""),
                    section=payload.get("section"),
                    url=payload.get("url", ""),
                    embedding=None
                )
                chunks.append(chunk)

            logger.info(f"Retrieved {len(chunks)} chunks for URL: {url}")
            return chunks

        except Exception as e:
            logger.error(f"Error retrieving content by URL: {str(e)}")
            return []

    def get_all_content_urls(self) -> List[str]:
        """
        Get all unique URLs in the collection
        """
        try:
            # Get all points and extract unique URLs
            all_points = self.qdrant_client.scroll(
                collection_name=self.collection_name,
                limit=10000,  # Adjust based on expected content size
                with_payload=True,
                with_vectors=False
            )

            urls = set()
            for point, _ in all_points:
                if point.payload and "url" in point.payload:
                    urls.add(point.payload["url"])

            logger.info(f"Retrieved {len(urls)} unique URLs")
            return list(urls)

        except Exception as e:
            logger.error(f"Error retrieving all content URLs: {str(e)}")
            return []