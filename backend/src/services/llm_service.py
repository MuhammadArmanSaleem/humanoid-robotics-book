import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

# Try to import agents, use fallback if not available
try:
    from agents import AsyncOpenAI, OpenAIChatCompletionsModel
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    AsyncOpenAI = None
    OpenAIChatCompletionsModel = None

from ..models import ContentChunk, ChatMessage, ChatSession, Source, ChatResponse
from ..config import settings


logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        if AGENTS_AVAILABLE:
            # Initialize the OpenAI client with custom provider for Gemini
            self.client = AsyncOpenAI(
                api_key=settings.gemini_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai"
            )

            # Initialize the model
            self.model = OpenAIChatCompletionsModel(
                openai_client=self.client,
                model=settings.gemini_model
            )
            logger.info("LLM service initialized with agents")
        else:
            logger.warning("agents not available, LLM service will return mock responses")
            self.client = None
            self.model = None

    async def generate_response(self,
                               query: str,
                               context_chunks: List[ContentChunk],
                               chat_history: List[ChatMessage] = None,
                               selected_text: Optional[str] = None) -> ChatResponse:
        """
        Generate a response using the LLM with provided context
        """
        if not AGENTS_AVAILABLE or self.model is None:
            # Return a mock response when agents is not available
            logger.warning(f"Agents not available, returning mock response for query: {query[:50]}...")
            mock_response = f"I'm the textbook assistant. I would normally help you with: {query[:100]}..."

            # Extract sources from context chunks
            sources = self._extract_sources(context_chunks)

            # Generate navigation links if applicable
            navigation_links = self._generate_navigation_links(query, context_chunks)

            # Create and return the response
            chat_response = ChatResponse(
                type="text",
                content=mock_response,
                sources=sources,
                navigation=navigation_links
            )
            return chat_response

        try:
            # Prepare the system message with instructions
            system_message = self._build_system_message()

            # Prepare the user message with context
            user_message = self._build_user_message(query, context_chunks, selected_text)

            # Prepare messages for the API call
            messages = [{"role": "system", "content": system_message}]

            # Add chat history if available
            if chat_history:
                for msg in chat_history:
                    role = "assistant" if msg.role == "assistant" else "user"
                    messages.append({"role": role, "content": msg.content})

            # Add the current user query
            messages.append({"role": "user", "content": user_message})

            # Call the LLM
            response = await self.model.chat_async(messages=messages)

            # Extract the response text
            response_text = response.choices[0].message.content

            # Extract sources from context chunks
            sources = self._extract_sources(context_chunks)

            # Generate navigation links if applicable
            navigation_links = self._generate_navigation_links(query, context_chunks)

            # Create and return the response
            chat_response = ChatResponse(
                type="text",
                content=response_text,
                sources=sources,
                navigation=navigation_links
            )

            logger.info(f"Successfully generated response for query: {query[:50]}...")
            return chat_response

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            # Return a safe error response
            return ChatResponse(
                type="text",
                content="I encountered an error while processing your request. Please try again.",
                sources=[],
                navigation=[]
            )

    def _build_system_message(self) -> str:
        """
        Build the system message with instructions for the LLM
        """
        return """
        You are an intelligent learning assistant for a Physical AI & Humanoid Robotics textbook.
        Your purpose is to answer questions based ONLY on the provided textbook content.
        Do not use external knowledge or make up information.

        When responding:
        1. Ground all answers in the provided context
        2. Provide specific citations to the textbook content
        3. If asked about something not in the context, politely decline and explain the scope
        4. Generate navigation links to relevant textbook sections when helpful
        5. For questions about selected text, provide detailed explanations of that specific content
        6. For guidance questions, recommend next steps based on the curriculum structure

        Always maintain a helpful, educational tone appropriate for students learning Physical AI & Humanoid Robotics.
        """

    def _build_user_message(self, query: str, context_chunks: List[ContentChunk], selected_text: Optional[str] = None) -> str:
        """
        Build the user message with context
        """
        message_parts = []

        # Add selected text context if provided
        if selected_text:
            message_parts.append(f"Selected text: {selected_text}\n")
            message_parts.append("Please provide detailed information about this selected text.\n")

        # Add the original query
        message_parts.append(f"Question: {query}\n")

        # Add context from relevant chunks
        if context_chunks:
            message_parts.append("Relevant textbook content:\n")
            for i, chunk in enumerate(context_chunks):
                message_parts.append(f"Source {i+1} (Chapter: {chunk.chapter}, Lesson: {chunk.lesson}, URL: {chunk.url}):\n")
                message_parts.append(f"{chunk.content}\n\n")

        # Add instructions for citations and navigation
        message_parts.append("\nProvide your answer with specific citations to the textbook content. If relevant, suggest navigation links to other textbook sections that might be helpful.")

        return "\n".join(message_parts)

    def _extract_sources(self, context_chunks: List[ContentChunk]) -> List[Source]:
        """
        Extract sources from context chunks
        """
        sources = []
        for chunk in context_chunks:
            source = Source(
                url=chunk.url,
                title=f"{chunk.chapter} - {chunk.lesson}",
                chapter=chunk.chapter,
                lesson=chunk.lesson,
                relevance=0.8  # Default relevance, could be computed based on similarity score
            )
            sources.append(source)
        return sources

    def _generate_navigation_links(self, query: str, context_chunks: List[ContentChunk]) -> List[Dict[str, str]]:
        """
        Generate navigation links based on the query and context
        """
        navigation_links = []

        # Look for navigation-related keywords in the query
        nav_keywords = ["next", "continue", "where", "learn", "study", "after", "before", "prerequisite", "advanced"]
        is_navigation_query = any(keyword in query.lower() for keyword in nav_keywords)

        if is_navigation_query and context_chunks:
            # Generate navigation suggestions based on curriculum structure
            for chunk in context_chunks[:3]:  # Limit to top 3 suggestions
                # Create a link to the same chapter/lesson as a starting point
                navigation_links.append({
                    "url": chunk.url,
                    "title": f"Continue with {chunk.lesson}"
                })

        return navigation_links

    async def generate_guidance_response(self, query: str, curriculum_structure: Dict[str, Any]) -> ChatResponse:
        """
        Generate a guidance response for learning path recommendations
        """
        if not AGENTS_AVAILABLE or self.model is None:
            # Return a mock response when agents is not available
            logger.warning(f"Agents not available, returning mock guidance response for query: {query[:50]}...")
            mock_response = f"I'm the learning guide. I would normally provide guidance for: {query[:100]} based on curriculum structure."

            return ChatResponse(
                type="text",
                content=mock_response,
                sources=[],
                navigation=[]
            )

        try:
            system_message = """
            You are an intelligent learning guide for a Physical AI & Humanoid Robotics textbook.
            Your purpose is to help students navigate the curriculum and recommend learning paths.
            Use the curriculum structure to provide personalized guidance.
            """

            user_message = f"""
            Curriculum structure: {curriculum_structure}

            Student query: {query}

            Provide guidance based on the curriculum structure. Recommend next steps, prerequisites,
            or learning paths as appropriate.
            """

            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]

            response = await self.model.chat_async(messages=messages)
            response_text = response.choices[0].message.content

            return ChatResponse(
                type="text",
                content=response_text,
                sources=[],
                navigation=[]
            )

        except Exception as e:
            logger.error(f"Error generating guidance response: {str(e)}")
            return ChatResponse(
                type="text",
                content="I encountered an error while generating guidance. Please try again.",
                sources=[],
                navigation=[]
            )