#!/usr/bin/env python3
"""
Test script to verify Coral protocol integration.
This script tests the basic functionality without requiring a full Coral server.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def test_imports():
    """Test that all required imports work."""
    print("Testing imports...")
    
    try:
        from langchain.chat_models import init_chat_model
        print("✓ langchain.chat_models imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import langchain.chat_models: {e}")
        return False
    
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient
        print("✓ langchain_mcp_adapters.client imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import langchain_mcp_adapters: {e}")
        return False
    
    try:
        from slack_agent.agent.agent import ReactAgent
        print("✓ slack_agent.agent.agent imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import slack_agent: {e}")
        return False
    
    return True

async def test_config_loading():
    """Test configuration loading."""
    print("\nTesting configuration loading...")
    
    # Load environment variables
    load_dotenv()
    
    required_vars = [
        "MODEL_API_KEY",
        "SLACK_BOT_TOKEN", 
        "SLACK_SIGNING_SECRET"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"✗ Missing required environment variables: {missing_vars}")
        print("Please set these variables in your .env file")
        return False
    else:
        print("✓ All required environment variables are set")
        return True

async def test_agent_creation():
    """Test agent creation without Coral server."""
    print("\nTesting agent creation...")
    
    try:
        from slack_agent.agent.agent import ReactAgent
        from slack_agent.defaults import get_available_toolkits
        
        # Test agent creation
        agent = ReactAgent(
            model="gpt-4o",
            tools=get_available_toolkits()
        )
        print("✓ ReactAgent created successfully")
        
        # Test tool manager
        from slack_agent.tools.manager import OpenSourceToolManager
        manager = OpenSourceToolManager()
        print("✓ OpenSourceToolManager created successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to create agent: {e}")
        return False

async def test_coral_tools_description():
    """Test Coral tools description generation."""
    print("\nTesting Coral tools description...")
    
    try:
        # Mock coral tools for testing
        class MockTool:
            def __init__(self, name, args):
                self.name = name
                self.args = args
        
        mock_tools = [
            MockTool("test_tool_1", {"param1": "string", "param2": "number"}),
            MockTool("test_tool_2", {"param3": "boolean"})
        ]
        
        # Import the function from main.py
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", "main.py")
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        
        description = main_module.get_tools_description(mock_tools)
        print("✓ Tools description generated successfully")
        print(f"Description length: {len(description)} characters")
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to generate tools description: {e}")
        return False

async def main():
    """Run all tests."""
    print("=" * 50)
    print("Coral Protocol Integration Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config_loading,
        test_agent_creation,
        test_coral_tools_description
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            result = await test()
            if result:
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Coral integration is ready.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
