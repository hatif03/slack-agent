#!/usr/bin/env python3
"""Test script to verify imports and basic functionality."""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work correctly."""
    try:
        print("Testing imports...")
        
        # Test tool manager import
        from slack_agent.tools import OpenSourceToolManager
        print("✓ OpenSourceToolManager import successful")
        
        # Test individual tool imports
        from slack_agent.tools.github_tool import GitHubTool
        print("✓ GitHubTool import successful")
        
        from slack_agent.tools.google_tool import GoogleTool
        print("✓ GoogleTool import successful")
        
        from slack_agent.tools.search_tool import SearchTool
        print("✓ SearchTool import successful")
        
        from slack_agent.tools.web_tool import WebTool
        print("✓ WebTool import successful")
        
        # Test tool manager initialization
        manager = OpenSourceToolManager()
        print("✓ OpenSourceToolManager initialization successful")
        
        # Test getting tools
        tools = manager.get_tools()
        print(f"✓ Got {len(tools)} tools from manager")
        
        # Test available tools
        available_tools = manager.get_available_tools()
        print(f"✓ Available tools: {available_tools}")
        
        print("\n🎉 All tests passed! The open-source tool system is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
