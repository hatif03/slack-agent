"""Open source tool manager to replace ArcadeToolManager."""

import logging
from typing import Any, Dict, List, Optional
from langchain_core.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun

from .github_tool import GitHubTool
from .google_tool import GoogleTool
from .search_tool import SearchTool
from .web_tool import WebTool

logger = logging.getLogger(__name__)


class OpenSourceToolManager:
    """Open source tool manager that provides tools without vendor lock-in."""
    
    def __init__(self):
        """Initialize the tool manager."""
        self.tools_registry = {
            "github": GitHubTool(),
            "google": GoogleTool(),
            "search": SearchTool(),
            "web": WebTool(),
        }
        
        # Tools that require OAuth authentication
        self.auth_required_tools = {"github", "google"}
        
    def get_tools(
        self, 
        tools: Optional[List[str]] = None, 
        toolkits: Optional[List[str]] = None,
        langgraph: bool = False
    ) -> List[BaseTool]:
        """
        Get tools based on the specified tool names and toolkits.
        
        Args:
            tools: List of specific tool names to include
            toolkits: List of toolkit names to include
            langgraph: Whether to format for LangGraph (unused for compatibility)
            
        Returns:
            List of LangChain tools
        """
        selected_tools = []
        
        # If no tools specified, use all available toolkits
        if not tools and toolkits:
            tools = toolkits
            
        # If still no tools, use all available
        if not tools:
            tools = list(self.tools_registry.keys())
            
        for tool_name in tools:
            if tool_name in self.tools_registry:
                tool = self.tools_registry[tool_name]
                if hasattr(tool, 'get_langchain_tools'):
                    selected_tools.extend(tool.get_langchain_tools())
                else:
                    selected_tools.append(tool)
            else:
                logger.warning(f"Tool '{tool_name}' not found in registry")
                
        return selected_tools
    
    def requires_auth(self, tool_name: str) -> bool:
        """
        Check if a tool requires authentication.
        
        Args:
            tool_name: Name of the tool to check
            
        Returns:
            True if the tool requires authentication
        """
        return tool_name in self.auth_required_tools
    
    def authorize(self, tool_name: str, user_id: str) -> Dict[str, Any]:
        """
        Authorize a tool for a user.
        
        Args:
            tool_name: Name of the tool to authorize
            user_id: ID of the user requesting authorization
            
        Returns:
            Authorization response with status and URL if needed
        """
        if tool_name not in self.auth_required_tools:
            return {"status": "completed", "url": None}
            
        if tool_name in self.tools_registry:
            tool = self.tools_registry[tool_name]
            if hasattr(tool, 'get_auth_url'):
                auth_url = tool.get_auth_url(user_id)
                return {"status": "pending", "url": auth_url}
                
        return {"status": "completed", "url": None}
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return list(self.tools_registry.keys())
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific tool.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool information dictionary or None if not found
        """
        if tool_name not in self.tools_registry:
            return None
            
        tool = self.tools_registry[tool_name]
        return {
            "name": tool_name,
            "requires_auth": tool_name in self.auth_required_tools,
            "description": getattr(tool, 'description', 'No description available')
        }
