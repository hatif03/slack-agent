"""Open source tool manager for Slack Agent."""

from typing import List, Dict, Any
from langchain.tools import BaseTool


class OpenSourceToolManager:
    """Manages open source tools for the Slack Agent."""
    
    def __init__(self):
        """Initialize the tool manager."""
        self.tools: List[BaseTool] = []
        self._initialize_tools()
    
    def _initialize_tools(self):
        """Initialize all available tools."""
        # This will be populated by individual tool modules
        pass
    
    def get_tools(self) -> List[BaseTool]:
        """Get all available tools."""
        return self.tools
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return [tool.name for tool in self.tools]
    
    def add_tool(self, tool: BaseTool):
        """Add a tool to the manager."""
        self.tools.append(tool)
