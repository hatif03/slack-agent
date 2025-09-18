"""Web search tool using DuckDuckGo."""

import logging
from typing import Any, Dict, List, Optional
from langchain_core.tools import BaseTool, tool
from langchain_community.tools import DuckDuckGoSearchRun

logger = logging.getLogger(__name__)


class SearchTool:
    """Web search tool using DuckDuckGo for privacy-focused search."""
    
    def __init__(self):
        """Initialize search tool."""
        self.search = DuckDuckGoSearchRun()
    
    def get_langchain_tools(self) -> List[BaseTool]:
        """Get LangChain tools for web search."""
        return [
            self.web_search,
            self.search_news,
            self.search_images,
        ]
    
    @tool
    def web_search(query: str, max_results: int = 5) -> str:
        """Search the web using DuckDuckGo."""
        try:
            results = self.search.run(f"{query} site:duckduckgo.com")
            
            if not results:
                return f"No results found for query: {query}"
            
            # Format results for better readability
            response = f"Web search results for '{query}':\n\n"
            response += results
            
            return response
            
        except Exception as e:
            logger.error(f"Error performing web search: {e}")
            return f"Error performing web search: {str(e)}"
    
    @tool
    def search_news(query: str, max_results: int = 5) -> str:
        """Search for news articles."""
        try:
            # Use DuckDuckGo with news-specific query
            news_query = f"{query} news"
            results = self.search.run(news_query)
            
            if not results:
                return f"No news found for query: {query}"
            
            response = f"News search results for '{query}':\n\n"
            response += results
            
            return response
            
        except Exception as e:
            logger.error(f"Error searching news: {e}")
            return f"Error searching news: {str(e)}"
    
    @tool
    def search_images(query: str, max_results: int = 5) -> str:
        """Search for images."""
        try:
            # Use DuckDuckGo with image-specific query
            image_query = f"{query} images"
            results = self.search.run(image_query)
            
            if not results:
                return f"No images found for query: {query}"
            
            response = f"Image search results for '{query}':\n\n"
            response += results
            
            return response
            
        except Exception as e:
            logger.error(f"Error searching images: {e}")
            return f"Error searching images: {str(e)}"
